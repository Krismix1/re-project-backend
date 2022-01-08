import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    account = relationship("User")
    internships = relationship("Internship", back_populates="company")


class Internship(Base):
    __tablename__ = "internships"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    company = relationship("Company", back_populates="internships")
