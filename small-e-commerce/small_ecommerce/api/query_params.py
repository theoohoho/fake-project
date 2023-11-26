import re
from typing import Literal, Optional

from fastapi import Query
from pydantic import validator
from pydantic.dataclasses import dataclass

from small_ecommerce.model import Order, Product


@dataclass
class OrderListQueryParams:
    limit: Optional[int] = Query(100)
    offset: Optional[int] = Query(0)

    ordering: Optional[
        Literal[
            "created_at",
            "-created_at",
        ]
    ] = Query("created_at")

    @validator("ordering")
    def parse_ordering(cls, v):
        if re.search("^(.?)([a-z].*).*", v).group(1) == "-":
            field_name = re.search("^(.?)([a-z].*).*", v).group(2)
            return Order.__table__.c[field_name].desc()
        else:
            return Order.__table__.c[v].asc()


@dataclass
class ProductListQueryParams:
    min_price: Optional[float] = Query(0)
    max_price: Optional[float] = Query(99999)
    min_stock: Optional[int] = Query(0)
    max_stock: Optional[int] = Query(99999)

    limit: Optional[int] = Query(100)
    offset: Optional[int] = Query(0)

    ordering: Optional[Literal["price", "stock", "-price", "-stock"]] = Query("price")

    @validator("ordering")
    def parse_ordering(cls, v):
        print(v)
        if re.search("^(.?)([a-z].*).*", v).group(1) == "-":
            field_name = re.search("^(.?)([a-z].*).*", v).group(2)
            return Product.__table__.c[field_name].desc()
        else:
            return Product.__table__.c[v].asc()
