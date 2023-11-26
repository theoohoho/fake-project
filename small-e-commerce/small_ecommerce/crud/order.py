from small_ecommerce.model import Order
from small_ecommerce.schemas.order import OrderCreate, OrderUpdate

from .base import CRUDBase


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    pass


order = CRUDOrder(Order)
