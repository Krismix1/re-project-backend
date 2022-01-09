import uuid

from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.database import Base


class Education(Base):
    __tablename__ = "educations"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4
    )
    institution_name = Column(String, nullable=False)
    studies_programme = Column(String, nullable=False)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    student = relationship("Student", back_populates="educations")


class Volunteering(Base):
    __tablename__ = "volunteerings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    student = relationship("Student", back_populates="volunteerings")


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
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    account = relationship("User")
    educations = relationship("Education", back_populates="student")
    volunteerings = relationship("Volunteering", back_populates="student")

    internship_applications = relationship("InternshipApplication", back_populates="student")


class InternshipApplication(Base):
    __tablename__ = "internship_applications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
    message = Column(String, nullable=True)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    student = relationship("Student", back_populates="internship_applications")

    internship_id = Column(UUID(as_uuid=True), ForeignKey("internships.id"))
    internship = relationship("Internship", back_populates="applications")
