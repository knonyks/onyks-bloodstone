from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import models
import schemas
from database import AsyncSessionLocal
from routers.common import get_db

router = APIRouter()

@router.get('/manufacturers/count')
async def get_manufacturers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Manufacturer)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@router.get('/manufacturers/counts')
async def get_manufacturers_counts(db = Depends(get_db)):
    query = select(models.Manufacturer.name, func.count(models.Element.uuid)).select_from(models.Manufacturer).outerjoin(models.Element, models.Manufacturer.name == models.Element.manufacturer).group_by(models.Manufacturer.name)
    result = await db.execute(query)
    rows = result.all()
    data = {}
    for name, count in rows:
        data[name] = count
    return data

@router.get("/manufacturers", response_model = schemas.PageResponse[schemas.ManufacturerFull])
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

@router.delete('/manufacturers/{id}')
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
    return id

@router.post('/manufacturers')
async def post_manufacturers(manufacturer: dict, db = Depends(get_db)):
    name = manufacturer.get("name")
    if isinstance(name, str) and not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "EMPTY_MANUFACTURER_NAME",
                "message": "Manufacturer name cannot be empty."
            }
        )

    try:
        validated_manufacturer = schemas.ManufacturerBase.model_validate(manufacturer)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "INVALID_MANUFACTURER_DATA",
                "message": "Invalid manufacturer data."
            }
        )

    item = models.Manufacturer(**validated_manufacturer.model_dump())
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
                "error_code": "INVALID_DATA_OR_MANUFACTURER_ALREADY_EXISTS",
                "message": "Invalid data or a manufacturer with this name already exists."
            }
        )

@router.get('/manufacturers/{id}')
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

@router.patch('/manufacturers/{id}')
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
        validated_manufacturer = schemas.ManufacturerBase.model_validate(manufacturer)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "INVALID_MANUFACTURER_DATA",
                "message": "Invalid manufacturer data."
            }
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
    
    update_data = validated_manufacturer.model_dump(exclude_unset=True)

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
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "error_code": "INVALID_DATA_OR_MANUFACTURER_ALREADY_EXISTS",
            "message": "Invalid data or a manufacturer with this name already exists."
        })
