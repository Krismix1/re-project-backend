from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    account = relationship("User")
