from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from routers import tables, manufacturers, suppliers, tags, elements, users, repository, auth
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
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repository.router)
app.include_router(tables.router)
app.include_router(manufacturers.router)
app.include_router(suppliers.router)
app.include_router(tags.router)
app.include_router(elements.router)
app.include_router(users.router)
app.include_router(auth.router)

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