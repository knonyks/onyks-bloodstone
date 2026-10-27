from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import models
import schemas
from database import AsyncSessionLocal
from routers.common import get_db

router = APIRouter()

@router.get('/tables/count')
async def get_tables_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Table)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@router.get('/tables/counts')
async def get_tables_counts(db = Depends(get_db)):
    query = select(models.Table.name, func.count(models.Element.uuid)).select_from(models.Table).outerjoin(models.Element, models.Table.name == models.Element.table).group_by(models.Table.name)
    result = await db.execute(query)
    rows = result.all()
    data = {}
    for name, count in rows:
        data[name] = count
    return data

@router.get("/tables", response_model = schemas.PageResponse[schemas.TableFull])
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

@router.delete('/tables/{id}')
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
    return id

@router.post('/tables')
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

@router.get('/tables/{id}')
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

@router.patch('/tables/{id}')
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
            detail={
                "error_code": "INVALID_TABLE_DATA",
                "message": "Invalid table data."
            }
        )

    update_data = validated_table.model_dump(exclude_unset=True)

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
                "error_code": "INVALID_DATA_OR_TABLE_ALREADY_EXISTS",
                "message": "Invalid data or a table with this name already exists."
            }
        )