from typing import Generic, Optional, TypeVar
import secrets
import bcrypt
from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String, cast, func, or_, select
import models
import schemas
from database import AsyncSessionLocal
from routers.common import get_db




router = APIRouter()

@router.get("/users", response_model=schemas.PageResponse[schemas.UserFull])
async def get_users(query: schemas.PageQuery = Depends(), db=Depends(get_db)):
	columns = {
		column.name: getattr(models.User, column.name)
		for column in models.User.__table__.columns
	}
	if query.sort_by not in columns:
		raise HTTPException(status_code=400, detail={
            "error_code": "INVALID_SORT_BY",
            "message": f"Invalid sort_by field: {query.sort_by}"
        })

	statement = select(models.User)
	if query.search:
		search_filters = [
			cast(column, String).ilike(f"%{query.search}%")
			for column in columns.values()
			if isinstance(column.type, String)
		]
		if search_filters:
			statement = statement.where(or_(*search_filters))

	total = await db.scalar(select(func.count()).select_from(statement.subquery()))
	order_column = columns[query.sort_by]
	statement = statement.order_by(
		order_column.desc() if query.sort_desc else order_column.asc()
	)
	statement = statement.offset((query.page - 1) * query.limit).limit(query.limit)
	result = await db.execute(statement)
	return {
		"items": result.scalars().all(),
		"total": total,
		"page": query.page,
		"limit": query.limit,
	}

@router.delete("/users/{id}")
async def delete_user(id: int, db=Depends(get_db)):
    statement = select(models.User).where(models.User.id == id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={
            "error_code": "USER_NOT_FOUND",
            "message": f"User with id {id} not found"
        })
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)

@router.patch("/users/{id}", response_model=schemas.UserFull)
async def update_user(id: int, user: schemas.UserBase, db: AsyncSession = Depends(get_db)):
    statement = select(models.User).where(models.User.id == id)
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail={
            "error_code": "USER_NOT_FOUND",
            "message": f"User with id {id} not found"
        })
    for key, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, key, value)
    await db.commit()
    await db.refresh(existing_user)
    return existing_user

@router.post("/users", response_model=schemas.UserFull)
async def create_user(user: schemas.UserBase, db: AsyncSession = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    plain_password = secrets.token_urlsafe(16)
    user_data["password"] = bcrypt.hashpw(
        plain_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    new_user = models.User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    response_data = {
        column.name: getattr(new_user, column.name)
        for column in models.User.__table__.columns
    }
    response_data["password"] = plain_password
    return response_data