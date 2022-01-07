import uuid

from sqlalchemy.orm import Session

from backend import models
from backend.schemas.student import StudentProfileCreate
from backend.services.user import get_user


def create_student(
    db: Session, student: StudentProfileCreate, account_id: uuid.UUID
) -> models.Student:
    db_account = get_user(db, account_id)
    print(student.birthday.isoformat())
    if not db_account:
        raise ValueError(f"User with ID {account_id} not found")

    db_student = models.Student(id=account_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
