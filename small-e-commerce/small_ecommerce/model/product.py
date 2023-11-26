import uuid
from typing import Any

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from small_ecommerce.db import Base

from .mixins import CreateUpdateAtMixin
from .types import GUID


class Product(CreateUpdateAtMixin, Base):
    __tablename__ = "products"

    id: Any = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    product_orders = relationship("OrderProduct", back_populates="product")


class Order(CreateUpdateAtMixin, Base):
    __tablename__ = "orders"

    id: Any = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    __tablename__ = "order_products"

    order_id = Column(GUID(), ForeignKey("orders.id"), primary_key=True)
    product_id = Column(GUID(), ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="product_orders")
