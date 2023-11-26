from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from small_ecommerce.common.enums import UserRole
from small_ecommerce.db import Base

from .mixins import CreateUpdateAtMixin
from .types import ChoiceType


class User(CreateUpdateAtMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    role = Column(ChoiceType(UserRole, impl=String()))

    orders = relationship("Order", back_populates="user")
