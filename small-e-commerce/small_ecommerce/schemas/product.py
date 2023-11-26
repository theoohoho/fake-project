import uuid
from typing import Any, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class ProductBase(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    price: float
    stock: int


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass


class UpdateProduct(BaseModel):
    name: str


class ProductInDBBase(ProductBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductItem(ProductInDBBase):
    pass


# Additional properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class PaginationBase(BaseModel):
    data: Any
    total: int
    current: int


class ListProduct(PaginationBase):
    data: list[ProductItem]


class DetailProduct(ProductInDBBase):
    pass
