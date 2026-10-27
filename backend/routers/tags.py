from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
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

@router.get("/tags")
async def get_tags_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("name"),
    sortDesc: bool = Query(False),
    db: AsyncSession = Depends(get_db),
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