from small_ecommerce.model import Product
from small_ecommerce.schemas.product import ProductCreate, ProductUpdate

from .base import CRUDBase


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product = CRUDProduct(Product)
