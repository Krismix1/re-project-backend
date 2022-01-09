import datetime
import time
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from backend import models
from backend.schemas.student import (
    Education,
    InternshipApplicationCreate,
    StudentProfile,
    StudentProfileCreate,
    Volunteering,
)
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


def get_student(db: Session, user_id: uuid.UUID) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == user_id).first()


def date_to_ts(date: datetime.date) -> float:
    return time.mktime(date.timetuple())


def student_from_db_model(student: models.Student):
    return StudentProfile(
        id=student.id,
        email=student.account.email,
        firstName=student.first_name,
        secondName=student.last_name,
        birthday=date_to_ts(student.birthdate),
        description=student.description,
        phone=student.phone,
        education=[
            Education(
                id=education.id,
                institutionName=education.institution_name,
                studiesProgramme=education.studies_programme,
                startingDate=date_to_ts(education.starting_date),
                endingDate=date_to_ts(education.ending_date),
            )
            for education in student.educations
        ],
        volunteering=[
            Volunteering(
                id=volunteering.id,
                name=volunteering.name,
                position=volunteering.position,
                startingDate=date_to_ts(volunteering.starting_date),
                endingDate=date_to_ts(volunteering.ending_date),
            )
            for volunteering in student.volunteerings
        ],
    )


def create_internship_application(
    db: Session,
    student: models.Student,
    internship_id: uuid.UUID,
    application: InternshipApplicationCreate,
) -> models.InternshipApplication:
    db_application = models.InternshipApplication(
        message=application.message, internship_id=internship_id, student_id=student.id
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def get_applications_for_student(
    db: Session,
    student: models.Student,
) -> list[models.InternshipApplication]:
    print(student.id)
    return (
        db.query(models.InternshipApplication)
        .join(models.InternshipApplication.student)
        .filter(models.Student.id == student.id)
        .all()
    )
