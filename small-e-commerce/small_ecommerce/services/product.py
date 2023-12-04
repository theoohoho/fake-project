import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from small_ecommerce import crud
from small_ecommerce.api.v1.endpoints.product import ProductListQueryParams
from small_ecommerce.common.enums import UserRole
from small_ecommerce.model import Product, User
from small_ecommerce.schemas.product import (
    DetailProduct,
    ListProduct,
    ProductCreate,
    ProductItem,
    ProductUpdate,
    UpdateProduct,
)


def lists(session: Session, query_params: ProductListQueryParams):
    products = crud.product.get_multi(
        session,
        where_clauses=[
            Product.price >= query_params.min_price,
            Product.price <= query_params.max_price,
            Product.stock >= query_params.min_stock,
            Product.stock <= query_params.max_stock,
        ],
        order_by_clauses=[query_params.ordering],
    )
    return ListProduct(
        data=[ProductItem(**p.__dict__) for p in products],
        total=len(products),
        current=len(products),
    )


def create(session: Session, user: User, product_create: ProductCreate):
    if user.role != UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can create products",
        )
    new_product = crud.product.create(session, obj_in=product_create)
    return new_product


def retrieve(session: Session, product_id: uuid.UUID):
    product = crud.product.get(session, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return DetailProduct(**product.__dict__)


def update(session: Session, user: User, product_id: uuid.UUID, body: UpdateProduct):
    if user.role != UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can update products",
        )
    product = crud.product.get(session, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    updated_product = crud.product.update(
        session, db_obj=product, obj_in=ProductUpdate(**body.dict())
    )

    return DetailProduct(**updated_product.__dict__)


def delete(session: Session, user: User, product_id: uuid.UUID):
    if user.role != UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can delete products",
        )

    product = crud.product.get(session, id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Check if there are no associated orders
    if product.product_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete product with associated orders",
        )

    deleted_product = crud.product.remove(session, id=product_id)
    return DetailProduct(**deleted_product.__dict__)
