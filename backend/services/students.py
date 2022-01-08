import uuid

from sqlalchemy.orm import Session

from backend import models
from backend.schemas.student import StudentProfileCreate
from backend.services.user import get_user


def create_student(
    db: Session, student: StudentProfileCreate, account_id: uuid.UUID
) -> models.Student:
    db_account = get_user(db, account_id)
    if not db_account:
        raise ValueError(f"User with ID {account_id} not found")

    educations_db: list[models.Education] = []
    for education in student.educations:
        education_db = models.Education(**education.dict())
        db.add(education_db)
        educations_db.append(education_db)

    volunteerings_db: list[models.Volunteering] = []
    for volunteering in student.volunteerings:
        volunteering_db = models.Volunteering(**volunteering.dict())
        db.add(volunteering_db)
        volunteerings_db.append(volunteering_db)

    db_student = models.Student(
        id=account_id,
        phone=student.phone,
        birthdate=student.birthdate,
        description=student.description,
        first_name=student.first_name,
        last_name=student.last_name,
        educations=educations_db,
        volunteerings=volunteerings_db,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, *, skip: int = 0, limit: int = 100) -> list[models.Student]:
    return db.query(models.Student).offset(skip).limit(limit).all()
