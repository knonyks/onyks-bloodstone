from pydantic import BaseModel, Field, field_validator, BeforeValidator
from datetime import datetime
from typing import Any, List, Optional, Generic, TypeVar, Annotated
from uuid import UUID
from enum import Enum

def emptyToNone(v: str | None) -> str | None:
    if isinstance(v, str) and not v.strip():
        return None
    return v

NotEmptyString = Annotated[str | None, BeforeValidator(emptyToNone)]

class ElementBase(BaseModel):
    part_name: NotEmptyString = Field(min_length=3, max_length=256)
    manufacturer: NotEmptyString = Field(default=None, max_length=256)
    table: NotEmptyString = Field(default=None, max_length=256)
    description: NotEmptyString = Field(default=None, max_length=1024)

    value: NotEmptyString = Field(default=None, max_length=256)
    availability: NotEmptyString = Field(default=None, max_length=256)
    
    library_reference: NotEmptyString = Field(default=None, max_length=1024)
    library_path: NotEmptyString = Field(default=None, max_length=1024)

    footprint_reference_1: NotEmptyString = Field(default=None, max_length=1024)
    footprint_path_1: NotEmptyString = Field(default=None, max_length=1024)

    footprint_reference_2: NotEmptyString = Field(default=None, max_length=1024)
    footprint_path_2: NotEmptyString = Field(default=None, max_length=1024)

    footprint_reference_3: NotEmptyString = Field(default=None, max_length=1024)
    footprint_path_3: NotEmptyString = Field(default=None, max_length=1024)

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
    created_at: datetime
    suppliers: dict = Field(default_factory=dict)
    datasheets: list = Field(default_factory=list)

class UserRank(str, Enum):
    EDITOR = 'editor'
    ADMIN = "admin"

class UserBase(BaseModel):
    username: Optional[str] = None
    rank: Optional[UserRank] = None
    expiration_time: Optional[datetime] = None
    created_at: Optional[datetime] = None

class UserFull(UserBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None

T = TypeVar('T')

class PageQuery(BaseModel):
    search: Optional[str] = None
    sort_by: str = "id"
    sort_desc: bool = True
    page: int = 1
    limit: int = 100

class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    
class TableBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class TableFull(TableBase):
    id: int
    created_at: datetime

class ManufacturerBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class ManufacturerFull(ManufacturerBase):
    id: int
    created_at: datetime

class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)

class SupplierFull(SupplierBase):
    id: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"