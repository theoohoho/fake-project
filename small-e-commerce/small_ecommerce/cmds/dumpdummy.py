from sqlalchemy.orm import Session

from small_ecommerce.common.enums import UserRole
from small_ecommerce.common.secure import get_password_hash
from small_ecommerce.db import get_cmd_db_session
from small_ecommerce.model import Product, User

from .base import cmdjob


@cmdjob.command()
def dumpdummy(session: Session = get_cmd_db_session()):
    FAKE_USER_DB = {
        "johndoe": {
            "username": "johndoe@example.com",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "password": "fakeuser",
            "is_active": False,
            "role": UserRole.manager,
        },
        "alice": {
            "username": "alice@example.com",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "password": "fakeuser",
            "is_active": True,
            "role": UserRole.manager,
        },
        "bob": {
            "username": "bob@example.com",
            "full_name": "bob",
            "email": "bob@example.com",
            "password": "fakeuser",
            "is_active": True,
            "role": UserRole.customer,
        },
    }
    objs = []
    for key in FAKE_USER_DB:
        objs.append(
            User(
                **dict(
                    full_name=FAKE_USER_DB[key]["full_name"],
                    email=FAKE_USER_DB[key]["email"],
                    hashed_password=get_password_hash(FAKE_USER_DB[key]["password"]),
                    is_active=FAKE_USER_DB[key]["is_active"],
                    role=FAKE_USER_DB[key]["role"],
                )
            )
        )

    FAKE_PRODUCT_DB = {
        "juice": {
            "name": "juice",
            "price": 10.5,
            "stock": 5,
        },
        "milk": {
            "name": "milk",
            "price": 9.5,
            "stock": 3,
        },
    }
    for key in FAKE_PRODUCT_DB:
        objs.append(
            Product(
                name=FAKE_PRODUCT_DB[key]["name"],
                price=FAKE_PRODUCT_DB[key]["price"],
                stock=FAKE_PRODUCT_DB[key]["stock"],
            )
        )

    with session as s:
        s.bulk_save_objects(objs)
