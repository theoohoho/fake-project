import uuid
from typing import List

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.orm import Session

from small_ecommerce.api.query_params import OrderListQueryParams
from small_ecommerce.db import get_db_session
from small_ecommerce.model import User
from small_ecommerce.schemas import order as order_schema
from small_ecommerce.services import order as order_service

from .depends import get_current_active_user

router = APIRouter()


@router.get("/orders", response_model=List[order_schema.Order])
def list_orders(
    query_params: OrderListQueryParams = Depends(),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    return order_service.lists(session, current_user, query_params)


@router.post("/orders", response_model=order_schema.Order)
def create_order(
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
    order_create: order_schema.CreateOrder = Body(...),
):
    return order_service.create(session, current_user, order_create)


@router.get("/orders/{order_id}", response_model=order_schema.OrderDetail)
def get_order(
    order_id: uuid.UUID = Path(...),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    return order_service.retrieve(session, current_user, order_id)
