from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session, selectinload
import models
import schemas
import utils
import crud
from database import engine, AsyncSessionLocal
from typing import List
import json
import os
import shutil
import database
import math
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path
from sqlalchemy import select
import uuid
import uuid as uuid_module
from sqlalchemy import inspect as sa_inspect
from sqlalchemy import select, func, Uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import Json, ValidationError
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from utils import MyRepository, MyDatabase
import redis

app = FastAPI()
r = redis.Redis(host='redis', port=6379, db=0)

UPLOAD_DIR = "/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="datasheet")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS private;"))
            await conn.run_sync(models.Base.metadata.create_all)
            # await MyDatabase.updateElementsViews(conn)
    except Exception as e:
        print(f"❌❌❌ DB Startup Failed: {e}")
        raise e

########################################

# REPOSITORY
@app.get('/repository/info')
async def get_repository_info():
    repo_name = os.getenv("SVN_REPO_NAME")
    if not repo_name:
        raise HTTPException(status_code=500, detail="Error! Can't get the name of the repository!")
    return {'name': repo_name}

@app.get("/repository/content")
async def get_repository_content(path: str):
    enterData = ["file:///local_svn", path]
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return MyRepository.getPcbContent(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return MyRepository.getFolderList(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/repository/statistics")
async def get_repository_statistics():
    try:
        schlib_count = int(r.get('schlib_count') or 0)
        pcblib_count = int(r.get('pcblib_count') or 0)
        footprints_count = int(r.get('footprints_count') or 0)
        symbols_count = int(r.get('symbols_count') or 0)
        return {"schlib_count": schlib_count, "pcblib_count": pcblib_count, 'footprints_count': footprints_count, 'symbols_count':symbols_count}
    except redis.exceptions.ConnectionError as e:
        return {"error": "Failed to connect to Redis: " + str(e)}

########################################

# TABLES

# xxx
@app.get('/tables/count')
async def get_tables_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Table)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

# xxx
@app.get('/tables/counts')
async def get_tables_counts(db = Depends(get_db)):
    query = select(models.Table.name, func.count(models.Element.uuid)).select_from(models.Table).outerjoin(models.Element, models.Table.name == models.Element.table).group_by(models.Table.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

# xxx
@app.get("/tables", response_model = schemas.PageResponse[schemas.TableFull])
async def get_tables_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Table)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Table.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Table, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "UNSUPPORTED_SORT_BY",
                "message": f"Unsupported sortBy value: {sortBy}"
            }
        )

    queryEntries = select(models.Table)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Table.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

@app.delete('/tables/{id}')
async def delete_tables(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "TABLE_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )

    elements_query = select(func.count()).select_from(models.Element).where(
        models.Element.table == item.name
    )
    elements_result = await db.execute(elements_query)
    if elements_result.scalar() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "TABLE_NOT_EMPTY",
                "message": "Table cannot be deleted because it is not empty."
            }
        )
    
    await db.delete(item)
    await db.commit()
    # await MyDatabase.updateElementsViews(db)
    
    return id

# xxx
@app.post('/tables')
async def post_tables(table_data: dict, db = Depends(get_db)):
    name = table_data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "TABLE_EMPTY_NAME",
                "message": "Name cannot be empty."
            }
        )

    try:
        table = schemas.TableBase.model_validate(table_data)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc

    item = models.Table(**table.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_TABLE_ALREADY_EXISTS",
                "message": "Invalid data or a table with this name already exists."
            }
        )

@app.get('/tables/{id}')
async def get_tables(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "TABLE_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )
    
    return item

@app.patch('/tables/{id}')
async def patch_tables(id: int, table: dict, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "TABLE_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )
    
    name = table.get("name")
    if "name" in table and (not isinstance(name, str) or not name.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "TABLE_EMPTY_NAME",
                "message": "Name cannot be empty."
            }
        )

    try:
        validated_table = schemas.TableBase.model_validate(table)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors()
        )

    update_data = validated_table.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_TABLE_ALREADY_EXISTS",
                "message": "Invalid data or a table with this name already exists."
            }
        )

########################################

# MANUFACTURERS

# count manufacturers
@app.get('/manufacturers/count')
async def get_manufacturers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Manufacturer)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

# count manufacturers
@app.get('/manufacturers/counts')
async def get_manufacturers_counts(db = Depends(get_db)):
    query = select(models.Manufacturer.name, func.count(models.Element.uuid)).select_from(models.Manufacturer).outerjoin(models.Element, models.Manufacturer.name == models.Element.manufacturer).group_by(models.Manufacturer.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

# list manufacturers
@app.get("/manufacturers", response_model = schemas.PageResponse[schemas.ManufacturerFull])
async def get_manufacturers_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Manufacturer)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Manufacturer.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Manufacturer, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "UNSUPPORTED_SORT_BY",
                "message": f"Unsupported sortBy value: {sortBy}"
            }
        )

    queryEntries = select(models.Manufacturer)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Manufacturer.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

# delete manufacturers
@app.delete('/manufacturers/{id}')
async def delete_manufacturers(id: int, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "MANUFACTURER_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )
    
    await db.delete(item)
    await db.commit()
    # await MyDatabase.updateElementsViews(db)
    return id

# create manufacturers
@app.post('/manufacturers')
async def post_manufacturers(manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
    if manufacturer.name == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_MANUFACTURER_NAME",
                "message": "Manufacturer name cannot be 0."
            }
        )

    item = models.Manufacturer(**manufacturer.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_MANUFACTURER_ALREADY_EXISTS",
                "message": "Invalid data or a manufacturer with this name already exists."
            }
        )

@app.get('/manufacturers/{id}')
async def get_manufacturers(id: int, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "MANUFACTURER_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )
    
    return item

# edit manufacturers
@app.patch('/manufacturers/{id}')
async def patch_manufacturers(id: int, manufacturer: dict, db = Depends(get_db)):
    if "name" in manufacturer and (
        not isinstance(manufacturer["name"], str) or not manufacturer["name"].strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_MANUFACTURER_NAME",
                "message": "Manufacturer name cannot be empty."
            }
        )

    try:
        manufacturer = schemas.ManufacturerBase.model_validate(manufacturer)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors()
        )

    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "MANUFACTURER_NOT_FOUND",
                "message": "ID doesn't exist!"
            }
        )
    
    update_data = manufacturer.model_dump(exclude_unset=True)

    if "name" in update_data and (
        not isinstance(update_data["name"], str) or not update_data["name"].strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_MANUFACTURER_NAME",
                "message": "Manufacturer name cannot be empty."
            }
        )

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "error_code": "INVALID_DATA_OR_MANUFACTURER_ALREADY_EXISTS",
            "message": "Invalid data or a manufacturer with this name already exists."
        })

########################################

# SUPPLIERS

# get the total count of suppliers
@app.get('/suppliers/count')
async def get_suppliers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Supplier)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

# get a list of suppliers with pagination, search, and sorting
@app.get("/suppliers", response_model = schemas.PageResponse[schemas.SupplierFull])
async def get_suppliers_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Supplier)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Supplier.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Supplier, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sortBy value: {sortBy}"
        )

    queryEntries = select(models.Supplier)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Supplier.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

# delete a supplier by id
@app.delete('/suppliers/{id}')
async def delete_suppliers(id: int, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "SUPPLIER_NOT_FOUND",
                "message": "Supplier not found."
            }
        )
    
    await db.delete(item)
    await db.commit()
    # await MyDatabase.updateElementsViews(db)
    
    return id

# creating a new supplier
@app.post('/suppliers')
async def post_suppliers(supplier_data: dict, db = Depends(get_db)):
    name = supplier_data.get('name')
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_SUPPLIER_NAME",
                "message": "Supplier name cannot be empty."
            }
        )
    supplier = schemas.SupplierBase.model_validate(supplier_data)
    item = models.Supplier(**supplier.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_SUPPLIER_ALREADY_EXISTS",
                "message": "Invalid data or a supplier with this name already exists."
            }
        )

# getting a single supplier by id
@app.get('/suppliers/{id}')
async def get_suppliers(id: int, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "SUPPLIER_NOT_FOUND",
                "message": "Supplier not found."
            }
        )
    
    return item

# updating a supplier by id
@app.patch('/suppliers/{id}')
async def patch_suppliers(id: int, supplier: dict, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "SUPPLIER_NOT_FOUND",
                "message": "Supplier not found."
            }
        )
    
    if "name" in supplier and (
        not isinstance(supplier["name"], str) or not supplier["name"].strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_SUPPLIER_NAME",
                "message": "Supplier name cannot be empty."
            }
        )

    try:
        supplier = schemas.SupplierBase.model_validate(supplier)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc

    update_data = supplier.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        # await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INVALID_DATA_OR_SUPPLIER_ALREADY_EXISTS",
                "message": "Invalid data or a supplier with this name already exists."
            }
        )

########################################

# SERVER
@app.get('/server/info')
async def get_server_info():
    return {'name': 'ONYKS Bloodstone', 'version': 'v0.2.0-alpha'}

########################################

# ELEMENTS
def _serialize_element(item):
    out = {a.key: getattr(item, a.key) for a in sa_inspect(models.Element).column_attrs}
    out["suppliers"] = {
        str(es.supplierId): {"value": es.value, "name": es.suppliers.name}
        for es in item.suppliers
    }
    return out

@app.get('/elements/count')
async def get_elements_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@app.get('/elements/last-added')
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

@app.post("/elements")
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

    if data.get("datasheets") is not None and data.get("datasheets") != []:

        if len(data.get("datasheets")) == len(files):
            print(files)
            for i, file in enumerate(files):
                if file.content_type != "application/pdf":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={"error_code": "INVALID_FILE_TYPE", "message": f"File {file.filename} is not a PDF."}
                    )
            for i in data.get("datasheets"):
                i["uuid"] = str(uuid_module.uuid4())
            print(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "MISMATCHED_FILE_COUNT", "message": "Number of datasheets does not match number of uploaded files."}
            )

        for i, file in enumerate(files or []):
            with open(os.path.join(UPLOAD_DIR, f"{data['datasheets'][i]['uuid']}.pdf"), "wb") as f:
                f.write(await file.read())

    
    # if data.get("datasheets") is None or data.get("datasheets") == []:
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
    # else:
    #     for i in range(len(data['datasheets'])):
    #         data['datasheets'][i]["uuid"] = str(uuid_module.uuid4())

@app.patch('/elements/{uuid}')
async def path_elements(uuid: str, element: str = Form(...), files: List[UploadFile] | None = File(default=None), db = Depends(get_db)):
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



@app.get("/elements")
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


@app.get('/elements/{uuid}')
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

@app.post('/elements/{uuid}/duplicate')
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

########################################

@app.get("/tags")
async def get_tags_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("name"),
    sortDesc: bool = Query(False),
    db: Session = Depends(get_db),
):
    tag_col = func.unnest(models.Element.tags).label("tag_name")
    
    subq = select(tag_col).subquery()

    column_name = subq.c.tag_name
    column_count = func.count().label("count")
    
    stmt = select(column_name, column_count).group_by(column_name)

    if search:
        stmt = stmt.where(column_name.ilike(f"%{search.strip()}%"))

    total_stmt = select(func.count()).select_from(stmt.subquery())
    total: int = (await db.scalar(total_stmt)) or 0

    sort_column = column_count if sortBy == "count" else column_name
    sort_direction = sort_column.desc() if sortDesc else sort_column.asc()
    stmt = stmt.order_by(sort_direction)

    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)

    result = await db.execute(stmt)
    rows = result.all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {"name": row.tag_name, "count": row.count}
            for row in rows
        ],
    }


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
##################################################################################################################################































































































































# USERS
# @app.get("/users", response_model = schemas.PageResponse[schemas.UserFull])
# async def get_users_list(
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1, le=100),
#     search: str | None = Query(None),
#     sortBy: str = Query("id"),
#     sortDesc: bool = Query(False),
#     db = Depends(get_db)
# ):
#     user_model = models.User
#     limit = max(1, min(limit, 100))
#     skip = (page - 1) * limit

#     sort_column = getattr(user_model, sortBy, None)
#     if sort_column is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Unsupported sortBy value: {sortBy}"
#         )

#     count_query = select(func.count()).select_from(user_model)
#     query_entries = select(user_model)
#     if search:
#         search_term = f"%{search.strip()}%"
#         search_filters = [
#             column.ilike(search_term)
#             for column in user_model.__table__.columns
#             if getattr(column.type, "python_type", None) is str
#         ]
#         if search_filters:
#             from sqlalchemy import or_
#             search_filter = or_(*search_filters)
#             count_query = count_query.where(search_filter)
#             query_entries = query_entries.where(search_filter)

#     count_result = await db.execute(count_query)
#     total_count = count_result.scalar() or 0

#     query_entries = (
#         query_entries
#         .order_by(sort_column.desc() if sortDesc else sort_column.asc())
#         .offset(skip)
#         .limit(limit)
#     )
#     entries_result = await db.execute(query_entries)
#     entries = entries_result.scalars().all()

#     return schemas.PageResponse(
#         items=entries,
#         total=total_count,
#         page=page,
#         limit=limit
#     )

# @app.delete('/users/{id}')
# async def delete_users(id: int, db = Depends(get_db)):
#     query = select(models.User).where(models.User.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()

#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )

#     await db.delete(item)
#     await db.commit()
#     await MyDatabase.updateElementsViews(db)

#     return id

# @app.post('/users')
# async def post_users(user: schemas.UserBase, db = Depends(get_db)):
#     item = models.User(**user.model_dump())
#     db.add(item)
#     try:
#         await db.commit()
#         await db.refresh(item)
#         await MyDatabase.updateElementsViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid data or a user with these details already exists."
#         )

# @app.get('/users/{id}')
# async def get_users(id: int, db = Depends(get_db)):
#     query = select(models.User).where(models.User.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()

#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )

#     return item

# @app.patch('/users/{id}')
# async def patch_users(id: int, user: schemas.UserBase, db = Depends(get_db)):
#     query = select(models.User).where(models.User.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()

#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )

#     update_data = user.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(item, field, value)

#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         await MyDatabase.updateElementsViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid data or a user with these details already exists."
#         )




# ELEMENT
# do poprawy
# @app.post("/element/create")
# async def elementCreate(
#     element: str = Form(...),
#     datasheet: UploadFile | None = File(default=None), 
#     db = Depends(get_db)):
#     if datasheet is not None and datasheet.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Datasheet must be a PDF file."
#         )

#     item_data = schemas.ElementBase.model_validate_json(element).model_dump(
#         exclude={"isDatasheetSupposedToChange"}
#     )
#     item = models.Element(**item_data)
#     item.datasheet = False
#     db.add(item)
#     pdf_path = None
#     try:
#         await db.flush()

#         if datasheet is not None:
#             pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
#             with open(pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True

#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         if pdf_path is not None:
#             try:
#                 os.remove(pdf_path)
#             except FileNotFoundError:
#                 pass
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid input data."
#         )
#     except Exception:
#         await db.rollback()
#         if pdf_path is not None:
#             try:
#                 os.remove(pdf_path)
#             except FileNotFoundError:
#                 pass
#         raise

# # do poprawy
# @app.post("/element/duplicate/{id}")
# async def elementDuplicate(
#     id: uuid.UUID,
#     element: str = Form(...),
#     datasheet: UploadFile | None = File(default=None),
#     db = Depends(get_db)
# ):
#     element_data = schemas.ElementBase.model_validate_json(element)
#     change_mode = element_data.isDatasheetSupposedToChange

#     if change_mode not in (0, 1, 2):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="isDatasheetSupposedToChange must be 0, 1 or 2."
#         )
#     if change_mode == 2 and datasheet is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="A new datasheet is required."
#         )
#     if datasheet is not None and datasheet.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Datasheet must be a PDF file."
#         )

#     result = await db.execute(
#         select(models.Element).where(models.Element.uuid == id)
#     )
#     source = result.scalar_one_or_none()
#     if source is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="UUID doesn't exist!")

#     data = element_data.model_dump()
#     data.pop("isDatasheetSupposedToChange", None)
#     data["uuid"] = uuid.uuid4()
#     data["datasheet"] = False
#     item = models.Element(**data)
#     db.add(item)

#     new_pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
#     old_pdf_path = os.path.join(UPLOAD_DIR, f"{source.uuid}.pdf")
#     try:
#         await db.flush()
#         if change_mode == 0:
#             if not source.datasheet or not os.path.isfile(old_pdf_path):
#                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                     detail="The source element has no datasheet.")
#             shutil.copyfile(old_pdf_path, new_pdf_path)
#             item.datasheet = True
#         elif change_mode == 2:
#             with open(new_pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True

#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         if os.path.isfile(new_pdf_path):
#             os.remove(new_pdf_path)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#     except Exception:
#         await db.rollback()
#         if os.path.isfile(new_pdf_path):
#             os.remove(new_pdf_path)
#         raise






# do poprawy
# @app.get("/elements", response_model = schemas.PageResponse[schemas.ElementFull])
# async def elementList(
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1, le=100),
#     search: str | None = Query(None),
#     sortBy: str = Query("createdAt"),
#     sortDesc: bool = Query(False),
#     db=Depends(get_db),
# ):
#     limit = max(1, min(limit, 100))
#     skip = (page - 1) * limit

#     sort_column = getattr(models.Element, sortBy, None)
#     if sort_column is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Unsupported sortBy value: {sortBy}",
#         )

#     count_query = select(func.count()).select_from(models.Element)
#     query_entries = select(models.Element)
#     if search:
#         from sqlalchemy import JSON, String, cast, or_

#         search_term = f"%{search.strip()}%"
#         search_filters = []
#         for column in models.Element.__table__.columns:
#             try:
#                 python_type = column.type.python_type
#             except (NotImplementedError, AttributeError):
#                 python_type = None
#             if python_type is str:
#                 search_filters.append(column.ilike(search_term))
#             elif python_type is uuid.UUID:
#                 search_filters.append(cast(column, String).ilike(search_term))
#             elif isinstance(column.type, JSON):
#                 search_filters.append(cast(column, String).ilike(search_term))
#         if search_filters:
#             search_filter = or_(*search_filters)
#             count_query = count_query.where(search_filter)
#             query_entries = query_entries.where(search_filter)

#     count_result = await db.execute(count_query)
#     total_count = count_result.scalar() or 0
#     query_entries = (
#         query_entries
#         .order_by(sort_column.desc() if sortDesc else sort_column.asc())
#         .offset(skip)
#         .limit(limit)
#     )
#     entries_result = await db.execute(query_entries)
#     entries = entries_result.scalars().all()

#     return schemas.PageResponse(items=entries, total=total_count, page=page, limit=limit)

# # do poprawy
# @app.delete('/element/delete/{id}')
# async def elementDelete(id: uuid.UUID, db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )

#     pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
#     if os.path.isfile(pdf_path):
#         os.remove(pdf_path)
    
#     await db.delete(item)
#     await db.commit()
    
#     return id

# # do poprawy
# @app.put('/element/edit/{id}')
# async def elementEdit(id: uuid.UUID, element: str = Form(...), datasheet: UploadFile | None = File(default=None), db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )
    
#     update_data = schemas.ElementBase.model_validate_json(element).model_dump(exclude_unset=True)
#     datasheet_change = update_data.pop('isDatasheetSupposedToChange', 0)
#     if datasheet_change not in (0, 1, 2):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="isDatasheetSupposedToChange must be 0, 1, or 2."
#         )
#     if datasheet_change == 2:
#         if datasheet is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Datasheet is required when replacing the datasheet."
#             )
#         if datasheet.content_type != "application/pdf":
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Datasheet must be a PDF file."
#             )

#     update_data['uuid'] = id
#     update_data['createdAt'] = item.createdAt

#     pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
#     for field, value in update_data.items():
#         setattr(item, field, value)

#     if datasheet_change == 2:
#         try:
#             with open(pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True
#         except Exception:
#             await db.rollback()
#             raise
#     elif datasheet_change == 1:
#         if os.path.isfile(pdf_path):
#             os.remove(pdf_path)
#         item.datasheet = False
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

# # do poprawy
# @app.get('/element/{id}')
# async def elementID(id: uuid.UUID = Path(...), db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
    
#     result = await db.execute(query)
    
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )
        
#     return item

# # MANUFACTURER


# # do poprawy
# @app.post('/manufacturer/create')
# async def manufacturerCreate(manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.name == manufacturer.name)
#     existing = await db.execute(query)
    
#     if existing.scalar_one_or_none() is not None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Manufacturer with this name already exists."
#         )
    
#     item = models.Manufacturer(**manufacturer.model_dump())
#     db.add(item)
#     try:
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid manufacturer data.")

# # do poprawy
# @app.delete('/manufacturer/delete/{id}')
# async def manufacturerDelete(id: int, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     await db.delete(item)
#     await db.commit()
    
#     return id

# # do poprawy
# @app.get("/manufacturer/list", response_model = schemas.ManufacturerList)
# async def manufacturerList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
#     query = select(func.count()).select_from(models.Manufacturer)
#     result = await db.execute(query)
#     totalCount = result.scalar()
    
#     queryEntries = select(models.Manufacturer).order_by(models.Manufacturer.id).offset(skip).limit(limit)
#     entriesResult = await db.execute(queryEntries)
#     entries = entriesResult.scalars().all()
    
#     return {"total": totalCount, "items": entries}

# @app.put('/manufacturer/edit/{id}')
# async def manufacturerEdit(id: int, manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     update_data = manufacturer.model_dump(exclude_unset=True)

#     for field, value in update_data.items():
#         setattr(item, field, value)
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a manufacturer with this name already exists.")



# # SUPPLIER



# # TABLE




# @app.put('/table/edit/{id}')
# async def tableEdit(id: int, table: schemas.TableBase, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     update_data = table.model_dump(exclude_unset=True)
    
#     for field, value in update_data.items():
#         setattr(item, field, value)
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         await utils.dbCreateOrUpdateElementViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

# @app.post('/table/create')
# async def tableCreate(table: schemas.TableBase, db = Depends(get_db)):
#     item = models.Table(**table.model_dump())
#     db.add(item)
#     try:
#         await db.commit()
#         await db.refresh(item)
#         await utils.dbCreateOrUpdateElementViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

# @app.delete('/table/delete/{id}')
# async def tableDelete(id: int, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )

#     elements_query = select(func.count()).select_from(models.Element).where(
#         models.Element.table == item.name
#     )
#     elements_result = await db.execute(elements_query)
#     if elements_result.scalar() > 0:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="The table cannot be deleted while it contains elements."
#         )
    
#     await db.delete(item)
#     await db.commit()
#     await utils.dbCreateOrUpdateElementViews(db)
#     return id

# @app.get("/table/list", response_model = schemas.TableList)
# async def tableList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
#     query = select(func.count()).select_from(models.Table)
#     result = await db.execute(query)
#     totalCount = result.scalar()
    
#     queryEntries = select(models.Table).order_by(models.Table.id).offset(skip).limit(limit)
#     entriesResult = await db.execute(queryEntries)
#     entries = entriesResult.scalars().all()
    
#     return {"total": totalCount, "items": entries}

# @app.get('/table/{id}')
# async def tableID(id: int, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     count_query = select(func.count()).select_from(models.Element).where(models.Element.table == item.name)
#     count_result = await db.execute(count_query)
#     elements_count = count_result.scalar()
    
#     return {
#         "table": item,
#         "numberOfItems": elements_count
#     }