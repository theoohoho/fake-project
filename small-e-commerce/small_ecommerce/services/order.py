import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from small_ecommerce import crud
from small_ecommerce.api.query_params import OrderListQueryParams
from small_ecommerce.common.enums import UserRole
from small_ecommerce.model import Order, OrderProduct, Product, User
from small_ecommerce.schemas import order as order_schema


def list(session: Session, user: User, query_params: OrderListQueryParams):
    where_clauses = []
    if user.role != UserRole.manager:
        where_clauses = [Order.user_id == user.id]
    orders = crud.order.get_multi(
        session,
        where_clauses=where_clauses,
        order_by_clauses=[query_params.ordering],
        offset=query_params.offset,
        limit=query_params.limit,
    )

    return [order_schema.Order(**o.__dict__) for o in orders] or []


def retrieve(session: Session, user: User, order_id: uuid.UUID):
    order = crud.order.get(session, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Check if the user has access to this order
    if user.role == UserRole.customer and order.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this order",
        )
    details = [
        order_schema.OrderProductItem(
            **od.__dict__,
            id=od.product_id,
            sub_total=od.quantity * od.product.price,
        )
        for od in order.order_details
    ]
    return order_schema.OrderDetail(
        **order.__dict__,
        details=details,
        total=sum([d.sub_total for d in details]),
    )


def create(session: Session, user: User, order_create: order_schema.CreateOrder):
    if user.role != UserRole.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can create orders",
        )
    try:
        new_order = Order(user_id=user.id)
        session.add(new_order)
        session.flush()

        # Process each product in the order
        products = crud.product.get_multi(
            session,
            where_clauses=[Product.id.in_({p.id for p in order_create.products})],
        )
        exist_products = {p.id: p for p in products}

        for product in order_create.products:
            if product.id not in exist_products:
                raise HTTPException(
                    status_code=404, detail=f"Product with ID {product.id} not found"
                )
            # Check if the user's order product quantity does not exceed the product stock
            if product.quantity > exist_products[product.id].stock:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for product with ID {product.id}",
                )

            # Update the product stock
            exist_products[product.id].stock -= product.quantity

            # Create the order product relationship
            order_product = OrderProduct(
                order_id=new_order.id,
                product_id=product.id,
                quantity=product.quantity,
            )
            session.add(order_product)
            session.refresh(new_order)
    except Exception:
        session.rollback()
        raise
    finally:
        session.commit()

    return order_schema.Order(**new_order.__dict__)
