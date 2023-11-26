"""Types define."""
import uuid

from pydantic import UUID4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR, TypeDecorator
from sqlalchemy_utils import ChoiceType as SQLAlchemyChoiceType


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(36), storing as regular strings.
    """

    class UUIDChar(CHAR):
        """Define UUIDChar."""

        python_type = UUID4

    impl = UUIDChar
    cache_ok = False

    def load_dialect_impl(self, dialect):
        """Load dialect impl."""
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        """Process bind param."""
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        """Process result value."""
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class ChoiceType(SQLAlchemyChoiceType):
    """Temp fix for https://github.com/kvesteri/sqlalchemy-utils/pull/565."""

    cache_ok = True
