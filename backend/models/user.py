import uuid

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from backend.db.database import Base
from backend.schemas.user import UserType


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4
    )
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    user_type = Column(
        Enum(UserType, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
