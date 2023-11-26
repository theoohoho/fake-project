import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: Optional[int] = None


class OrderCreate(OrderBase):
    user_id: int


class OrderUpdate(OrderBase):
    pass


class OrderInDBBase(OrderBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class Order(OrderInDBBase):
    created_at: Optional[datetime]


class OrderInDB(OrderInDBBase):
    user_id: int


class OrderProductBase(BaseModel):
    id: uuid.UUID
    quantity: int


class CreateOrderProduct(OrderProductBase):
    pass


class CreateOrder(BaseModel):
    products: list[CreateOrderProduct]


class OrderProductItem(BaseModel):
    product_id: uuid.UUID
    quantity: int
    sub_total: float


class OrderDetail(BaseModel):
    id: uuid.UUID
    details: list[OrderProductItem]
    total: float
    created_at: Optional[datetime]
