from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from database import Base
from datetime import datetime, timezone
import uuid as uuid_module
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import DDL, event
from typing import List
from typing import Optional

event.listen(
    Base.metadata,
    "before_create",
    DDL("CREATE EXTENSION IF NOT EXISTS pgcrypto"),
)

class UserRank(PyEnum):
    viewer = "viewer"
    admin = "admin"
    editor = "editor"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'private'}

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expirationTime: Mapped[datetime] = mapped_column(
        'expiration_time',
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
    rank: Mapped[UserRank] = mapped_column(
        Enum(UserRank, name='user_rank', native_enum=True),
        nullable=False,
        default=UserRank.viewer,
    )

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = {'schema': 'private'}

    id:  Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column('name', String(256), unique=True, index=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    elements: Mapped[List["Element"]] = relationship(back_populates="manufacturerRel")

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {'schema': 'private'}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column('name', String(256), unique=True, index=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    elementSuppliers: Mapped[List["ElementSupplier"]] = relationship(
        back_populates="suppliers",
        passive_deletes=True,
    )

class Table(Base):
    __tablename__ = "tables"
    __table_args__ = {'schema': 'private'}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column('name', String(256), unique=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    elements = relationship(
        "Element",
        back_populates="tableCategory",
        foreign_keys="Element.table",
    )


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = {'schema': 'private'}

    uuid: Mapped[uuid_module.UUID] = mapped_column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid_module.uuid4)
    partName: Mapped[str] = mapped_column("part_name", String(256), nullable=False)

    manufacturer: Mapped[Optional[str]] = mapped_column(
        String(256), 
        ForeignKey("private.manufacturers.name", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True
    )

    table: Mapped[str] = mapped_column('table',
        String(1024), 
        ForeignKey("private.tables.name", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column('description', String(1024), nullable=True, default='')





    value: Mapped[Optional[str]] = mapped_column('value', String(256), nullable=True, default='')
    availability: Mapped[Optional[str]] = mapped_column('availability', String(256), nullable=True, default='')

    
    libraryReference: Mapped[Optional[str]] = mapped_column('library_ref', String(1024), nullable=True, default='')
    libraryPath: Mapped[Optional[str]] = mapped_column('library_path', String(1024), nullable=True, default='')
    
    footprintReferenceNo1: Mapped[Optional[str]] = mapped_column('footprint_reference_1', String(1024), nullable=True, default='')
    footprintPathNo1: Mapped[Optional[str]] = mapped_column('footprint_path_1', String(1024), nullable=True, default='')
    
    footprintReferenceNo2: Mapped[Optional[str]] = mapped_column('footprint_reference_2', String(1024), nullable=True, default='')
    footprintPathNo2: Mapped[Optional[str]] = mapped_column('footprint_path_2', String(1024), nullable=True, default='')
    
    footprintReferenceNo3: Mapped[Optional[str]] = mapped_column('footprint_reference_3', String(1024), nullable=True, default='')
    footprintPathNo3: Mapped[Optional[str]] = mapped_column('footprint_path_3', String(1024), nullable=True, default='')
    
    suppliers: Mapped[List["ElementSupplier"]] = relationship(
        back_populates="elements",
        cascade="all, delete-orphan",
        lazy="selectin", 
    )

    
    
    
    
    datasheets: Mapped[dict] = mapped_column('datasheets', JSONB, default=dict)

    createdAt: Mapped[datetime] = mapped_column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    tableCategory = relationship(
        "Table",
        back_populates="elements"
    )
    manufacturerRel = relationship("Manufacturer", back_populates="elements")

class ElementSupplier(Base):
    __tablename__ = "element_supplier"
    __table_args__ = {'schema': 'private'}

    elementId: Mapped[uuid_module.UUID] = mapped_column(
        ForeignKey("private.elements.uuid", ondelete="CASCADE"), primary_key=True
    )
    
    supplierId: Mapped[int] = mapped_column(
        ForeignKey("private.suppliers.id", ondelete="CASCADE"), primary_key=True
    )
    value: Mapped[str] = mapped_column(String(255))


    elements: Mapped["Element"] = relationship(back_populates="suppliers")
    suppliers: Mapped["Supplier"] = relationship(back_populates="elementSuppliers", lazy="joined")

    @property
    def id(self) -> int:
        return self.supplierId

    @property
    def name(self) -> str:
        return self.suppliers.name