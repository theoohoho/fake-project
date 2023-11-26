import uuid

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.orm import Session

from small_ecommerce.api.query_params import ProductListQueryParams
from small_ecommerce.db import get_db_session
from small_ecommerce.model import User
from small_ecommerce.schemas.product import (
    DetailProduct,
    ListProduct,
    ProductCreate,
    UpdateProduct,
)
from small_ecommerce.services import product as product_service

from .depends import get_current_active_user

router = APIRouter()


@router.get("/products", response_model=ListProduct)
def list_products(
    query_params: ProductListQueryParams = Depends(),
    session: Session = Depends(get_db_session),
):
    return product_service.list(session, query_params)


@router.post("/products", response_model=DetailProduct)
def create_product(
    product_create: ProductCreate,
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    return product_service.create(session, current_user, product_create)


@router.patch("/products/{product_id}", response_model=DetailProduct)
def update_product(
    product_id: uuid.UUID = Path(...),
    body: UpdateProduct = Body(...),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    return product_service.update(session, current_user, product_id, body)


@router.delete("/products/{product_id}", response_model=None)
def delete_product(
    product_id: uuid.UUID = Path(...),
    session: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    product_service.delete(session, current_user, product_id)
