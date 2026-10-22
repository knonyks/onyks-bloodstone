from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from datetime import datetime
from typing import Any, List, Optional, Generic, TypeVar
from fastapi import Query
from typing import Annotated
from uuid import UUID
from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel

from pydantic import BaseModel, Field, BeforeValidator

def emptyToNone(v: str | None) -> str | None:
    if isinstance(v, str) and not v.strip():
        return None
    return v

NotEmptyString = Annotated[str | None, BeforeValidator(emptyToNone)]

# GENERAL
T = TypeVar('T')

class PageQuery(BaseModel):
    search: Optional[str] = None
    sortBy: str = "id"
    sortDesc: bool = True
    page: int = 1
    limit: int = 100

class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int

# SUPPLIERS
class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class SupplierFull(SupplierBase):
    id: int
    createdAt: datetime

# MANUFACTURERS
class ManufacturerBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class ManufacturerFull(ManufacturerBase):
    id: int
    createdAt: datetime

# TABLES
class TableBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class TableFull(TableBase):
    id: int
    createdAt: datetime

# ELEMENTS
class ElementBase(BaseModel):
    partName: NotEmptyString = Field(min_length=3, max_length=256)
    manufacturer: NotEmptyString = Field(default=None, max_length=256)
    table: NotEmptyString = Field(default=None, max_length=256)
    description: NotEmptyString = Field(default=None, max_length=1024)

    value: NotEmptyString = Field(default=None, max_length=256)
    availability: NotEmptyString = Field(default=None, max_length=256)
    
    libraryReference: NotEmptyString = Field(default=None, max_length=1024)
    libraryPath: NotEmptyString = Field(default=None, max_length=1024)

    footprintReferenceNo1: NotEmptyString = Field(default=None, max_length=1024)
    footprintPathNo1: NotEmptyString = Field(default=None, max_length=1024)

    footprintReferenceNo2: NotEmptyString = Field(default=None, max_length=1024)
    footprintPathNo2: NotEmptyString = Field(default=None, max_length=1024)

    footprintReferenceNo3: NotEmptyString = Field(default=None, max_length=1024)
    footprintPathNo3: NotEmptyString = Field(default=None, max_length=1024)

    tags: List[str] = []

    @field_validator("tags")
    @classmethod
    def clearTags(cls, v: List[str]) -> List[str]:
        clear = [tag.strip().lower() for tag in v if tag.strip()]
        return list(dict.fromkeys(clear))

class ElementInsert(ElementBase):
    suppliers: dict[str, Any] = Field(default_factory=dict)
    datasheets: list = Field(default_factory=list)

class ElementOutput(ElementBase):
    uuid: UUID
    createdAt: datetime
    suppliers: dict = Field(default_factory=dict)
    datasheets: list = Field(default_factory=list)

# USERS
class UserRank(str, Enum):
    EDITOR = 'editor'
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    login: str
    email: str
    rank: UserRank

class UserFull(UserBase):
    id: int
    expirationTime: datetime