from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import models
import schemas
from database import AsyncSessionLocal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import models
from database import AsyncSessionLocal
from routers.common import get_db
import schemas
from pydantic import ValidationError

router = APIRouter()

@router.get('/suppliers/count')
async def get_suppliers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Supplier)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@router.get("/suppliers", response_model = schemas.PageResponse[schemas.SupplierFull])
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

@router.delete('/suppliers/{id}')
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
    return id

@router.post('/suppliers')
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

@router.get('/suppliers/{id}')
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

@router.patch('/suppliers/{id}')
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
        validated_supplier = schemas.SupplierBase.model_validate(supplier)
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc

    update_data = validated_supplier.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
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