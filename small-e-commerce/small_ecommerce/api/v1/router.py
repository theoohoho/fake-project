from fastapi import APIRouter

from .endpoints import auth, order, product, user

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(order.router, tags=["order"])
api_router.include_router(product.router, tags=["product"])
