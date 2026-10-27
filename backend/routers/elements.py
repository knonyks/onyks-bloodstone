from fastapi import Depends, APIRouter, HTTPException, status, Query
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import shutil
import models
import schemas
from database import AsyncSessionLocal
from routers.common import get_db
from fastapi import Form, UploadFile, File
from typing import List
import os
import json
import uuid as uuid_module
from sqlalchemy import inspect as sa_inspect
from pydantic import ValidationError

UPLOAD_DIR = "/uploads"

router = APIRouter()

def _serialize_element(item):
    out = {a.key: getattr(item, a.key) for a in sa_inspect(models.Element).column_attrs}
    out["suppliers"] = {
        str(es.supplierId): {"value": es.value, "name": es.suppliers.name}
        for es in item.suppliers
    }
    return out

@router.get('/elements/count')
async def get_elements_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@router.get('/elements/last-added')
async def get_elements_last_added(db = Depends(get_db)):
    query = (select(models.Element).order_by(models.Element.createdAt.desc()).limit(1))
    result = await db.execute(query)
    
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "ELEMENT_NOT_FOUND",
                "message": "No elements found in the database."
            }
        )
        
    return item

@router.post("/elements")
async def post_elements(element: str = Form(...), files: List[UploadFile] | None = File(default=None), db = Depends(get_db)):
    try:
        data = json.loads(element)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_JSON", "message": "Invalid element JSON."}
        )

    try:
        data = schemas.ElementInsert.model_validate(data).model_dump()
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "INVALID_ELEMENT", "message": exc.errors()}
        )

    if data.get("datasheets"):
        if len(data.get("datasheets") or []) == len(files or []):
            for i, file in enumerate(files or []):
                if file.content_type != "application/pdf":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={"error_code": "INVALID_FILE_TYPE", "message": f"File {file.filename} is not a PDF."}
                    )
            for i in data.get("datasheets") or []:
                i["uuid"] = str(uuid_module.uuid4())
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "MISMATCHED_FILE_COUNT", "message": "Number of datasheets does not match number of uploaded files."}
            )

        for i, file in enumerate(files or []):
            with open(os.path.join(UPLOAD_DIR, f"{data['datasheets'][i]['uuid']}.pdf"), "wb") as f:
                f.write(await file.read())


    suppliers = data.pop("suppliers", {})
    item = models.Element(**data)
    item.suppliers = [
        models.ElementSupplier(supplierId=int(sid), value=(sdata or {}).get("value", ""))
        for sid, sdata in suppliers.items()
    ]
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        return _serialize_element(item)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_OBJECT_ALREADY_EXISTS",
                "message": "Invalid data or an element with this name already exists."
            }
        )

@router.patch('/elements/{uuid}')
async def path_elements(uuid: str, element: str = Form(...), files: List[UploadFile] | None = File(default=None), db: AsyncSession = Depends(get_db)):
    try:
        element_uuid = uuid_module.UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_UUID", "message": "Invalid UUID."}
        )

    result = await db.execute(
        select(models.Element).where(models.Element.uuid == element_uuid)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "ELEMENT_NOT_FOUND", "message": "Element not found."}
        )

    try:
        data = json.loads(element)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_JSON", "message": "Invalid element JSON."}
        )

    try:
        data = schemas.ElementInsert.model_validate(data).model_dump()
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "INVALID_ELEMENT", "message": exc.errors()}
        )

    datasheets = data.get("datasheets") or []

    old_uuids = [datasheet["uuid"] for datasheet in item.datasheets]
    new_uuid = [datasheet["uuid"] for datasheet in datasheets if datasheet.get("uuid")]
    to_remove = list(set(old_uuids) - set(new_uuid))
    to_add = [datasheet for datasheet in datasheets if not datasheet.get("uuid")]

    files = files or []
    if len(to_add) != len(files):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "MISMATCHED_FILE_COUNT",
                "message": "Number of new datasheets does not match number of uploaded files."
            }
        )
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "INVALID_FILE_TYPE", "message": f"File {file.filename} is not a PDF."}
            )

    for datasheet_uuid in to_remove:
        pdf_path = os.path.join(UPLOAD_DIR, f"{datasheet_uuid}.pdf")
        if os.path.isfile(pdf_path):
            os.remove(pdf_path)

    for datasheet, file in zip(to_add, files):
        datasheet["uuid"] = str(uuid_module.uuid4())
        pdf_path = os.path.join(UPLOAD_DIR, f"{datasheet['uuid']}.pdf")
        with open(pdf_path, "wb") as pdf:
            pdf.write(await file.read())

    for field, value in data.items():
        if field not in {"uuid", "datasheets", "suppliers"}:
            setattr(item, field, value)
    item.datasheets = datasheets

    if "suppliers" in data:
        item.suppliers = [
            models.ElementSupplier(
                supplierId=int(supplier_id),
                value=(supplier_data or {}).get("value", "")
            )
            for supplier_id, supplier_data in (data["suppliers"] or {}).items()
        ]

    try:
        await db.commit()
        await db.refresh(item)
        return _serialize_element(item)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_OBJECT_ALREADY_EXISTS",
                "message": "Invalid data or an element with this name already exists."
            }
        )



@router.get("/elements")
async def get_elements_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("createdAt"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    skip = (page - 1) * limit
    keys = {a.key for a in sa_inspect(models.Element).column_attrs}
    sort_key = sortBy if sortBy in keys else "createdAt"
    sort_column = getattr(models.Element, sort_key)

    query = select(models.Element)
    countQuery = select(func.count()).select_from(models.Element)
    if search:
        cond = models.Element.partName.ilike(f"%{search.strip()}%")
        query = query.where(cond)
        countQuery = countQuery.where(cond)

    totalCount = (await db.execute(countQuery)).scalar() or 0
    query = (
        query
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entries = (await db.execute(query)).scalars().all()

    return {
        "items": [_serialize_element(e) for e in entries],
        "total": totalCount,
        "page": page,
        "limit": limit,
    }


@router.get('/elements/{uuid}')
async def get_element(uuid: str, db = Depends(get_db)):
    try:
        element_uuid = uuid_module.UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_UUID", "message": "Invalid UUID."}
        )
    result = await db.execute(
        select(models.Element).where(models.Element.uuid == element_uuid)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "ELEMENT_NOT_FOUND", "message": "Element not found."}
        )
    return _serialize_element(item)

@router.post('/elements/{uuid}/duplicate')
async def duplicate_element(
    uuid: str,
    element: str | None = Form(default=None),
    files: List[UploadFile] | None = File(default=None),
    db = Depends(get_db)
):
    try:
        element_uuid = uuid_module.UUID(uuid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_UUID", "message": "Invalid UUID."}
        )

    result = await db.execute(
        select(models.Element)
        .options(selectinload(models.Element.suppliers))
        .where(models.Element.uuid == element_uuid)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "ELEMENT_NOT_FOUND", "message": "Element not found."}
        )

    excluded_fields = {"uuid", "createdAt", "updatedAt"}
    values = {
        column.key: getattr(item, column.key)
        for column in sa_inspect(models.Element).column_attrs
        if column.key not in excluded_fields and column.key != "datasheets"
    }
    if "partName" in values:
        values["partName"] = f"{values['partName']} (copy)"

    data = None
    if element is not None:
        try:
            data = json.loads(element)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "INVALID_JSON", "message": "Invalid element JSON."}
            )
        try:
            data = schemas.ElementInsert.model_validate(data).model_dump()
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error_code": "INVALID_ELEMENT", "message": exc.errors()}
            )
        for field, value in data.items():
            if field not in {"uuid", "datasheets", "suppliers"}:
                values[field] = value
        source_datasheets = data.get("datasheets") or []
    else:
        source_datasheets = list(item.datasheets or [])

    files = files or []
    to_add = [d for d in source_datasheets if not d.get("uuid")]
    if len(to_add) != len(files):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "MISMATCHED_FILE_COUNT",
                "message": "Number of new datasheets does not match number of uploaded files."
            }
        )
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "INVALID_FILE_TYPE", "message": f"File {file.filename} is not a PDF."}
            )

    copied_datasheets = []
    new_files = iter(files)
    for datasheet in source_datasheets:
        copied = dict(datasheet)
        old_uuid = copied.get("uuid")
        new_uuid = str(uuid_module.uuid4())
        destination = os.path.join(UPLOAD_DIR, f"{new_uuid}.pdf")
        if old_uuid:
            source = os.path.join(UPLOAD_DIR, f"{old_uuid}.pdf")
            if os.path.isfile(source):
                shutil.copyfile(source, destination)
        else:
            with open(destination, "wb") as pdf:
                pdf.write(await next(new_files).read())
        copied["uuid"] = new_uuid
        copied_datasheets.append(copied)
    values["datasheets"] = copied_datasheets

    duplicate = models.Element(**values)
    if data is not None and "suppliers" in data:
        duplicate.suppliers = [
            models.ElementSupplier(
                supplierId=int(supplier_id),
                value=(supplier_data or {}).get("value", "")
            )
            for supplier_id, supplier_data in (data["suppliers"] or {}).items()
        ]
    else:
        duplicate.suppliers = [
            models.ElementSupplier(supplierId=supplier.supplierId, value=supplier.value)
            for supplier in item.suppliers
        ]
    db.add(duplicate)
    try:
        await db.commit()
        await db.refresh(duplicate)
        return _serialize_element(duplicate)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_OBJECT_ALREADY_EXISTS",
                "message": "Invalid data or an element with this name already exists."
            }
        )

@router.delete('/elements/{uuid}')
async def delete_element(uuid: str, db: AsyncSession = Depends(get_db)):
    element = await db.get(models.Element, uuid)
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "ELEMENT_NOT_FOUND", "message": "Element not found."}
        )
    await db.delete(element)
    try:
        await db.commit()
        return {"message": "Element deleted successfully."}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "DELETE_FAILED",
                "message": "Failed to delete element due to integrity constraints."
            }
        )


