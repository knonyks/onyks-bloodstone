from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from routers import tables, manufacturers, suppliers, tags, elements, users, repository
from sqlalchemy.orm import Session, selectinload
import models
import schemas
import utils
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
from routers import repository, manufacturers, suppliers, tables, users
from redis_client import r

app = FastAPI()

app.include_router(repository.router)
app.include_router(tables.router)
app.include_router(manufacturers.router)
app.include_router(suppliers.router)
app.include_router(tags.router)
app.include_router(elements.router)
app.include_router(users.router)


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
    except Exception as e:
        print(f"{e}")
        raise e































































































































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