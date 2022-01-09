from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from backend import models
from backend.core.security import (
    get_company_or_student_user,
    get_company_user,
    get_student_user,
)
from backend.dependencies import get_db
from backend.schemas.company import Internship, InternshipCreate
from backend.schemas.student import InternshipApplication, InternshipApplicationCreate
from backend.services import company as company_service
from backend.services import students
from backend.services.company import get_internship

router = APIRouter(prefix="/internships", tags=["internships"])


@router.post("", response_class=Response, status_code=status.HTTP_201_CREATED)
def create_internship(
    internship: InternshipCreate,
    company: models.Company = Depends(get_company_user),
    db: Session = Depends(get_db),
):
    company_service.create_internship(db, company, internship)


# @router.get("/{company_id}/internships", response_model=list[Internship])
# def get_internship_for_company(
#     company_id: UUID4,
#     db: Session = Depends(get_db),
# ):
#     company = company_service.get_company(db, company_id)
#     if not company:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

#     return company_service.get_internships_for_company(db, company)


def convert_internship(i: models.Internship) -> Internship:
    return Internship(
        id=i.id,
        title=i.title,
        description=i.description,
        company=company_service.company_from_db_model(i.company),
        deadline=students.date_to_ts(i.deadline),
        startingDate=students.date_to_ts(i.starting_date),
        endingDate=students.date_to_ts(i.ending_date),
    )


def convert_internships(internships: list[models.Internship]) -> list[Internship]:
    return [convert_internship(i) for i in internships]


@router.get("", response_model=list[Internship])
def get_internships(
    user: Union[models.Student, models.Company] = Depends(get_company_or_student_user),
    db: Session = Depends(get_db),
) -> list[Internship]:
    """Get the internship available in the platform.

    If the user is a student, then it will return all internships.
    If the user is a company, then it will return only the internships of the company.
    """
    if isinstance(user, models.Company):
        return convert_internships(company_service.get_internships_for_company(db, user))
    return convert_internships(company_service.get_internships(db))


@router.post(
    "/{internship_id}/apply",
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
)
def apply_to_internship(
    internship_id: UUID4,
    application_data: InternshipApplicationCreate,
    db: Session = Depends(get_db),
    student: models.Student = Depends(get_student_user),
):
    db_internship = get_internship(db, internship_id)
    if not db_internship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internship not found")

    students.create_internship_application(db, student, internship_id, application_data)


def convert_internship_applications(
    applications: list[models.InternshipApplication],
) -> list[InternshipApplication]:
    return [
        InternshipApplication(
            id=ia.id,
            message=ia.message,
            internship=convert_internship(ia.internship),
            student=students.student_from_db_model(ia.student),
        )
        for ia in applications
    ]


@router.get("/applications", response_model=list[InternshipApplication])
def get_all_internship_applications(
    db: Session = Depends(get_db),
    user: Union[models.Student, models.Company] = Depends(get_company_or_student_user),
):
    if isinstance(user, models.Student):
        return convert_internship_applications(students.get_applications_for_student(db, user))
    return convert_internship_applications(company_service.get_applications_for_company(db, user))


@router.get("/{internship_id}/applications", response_model=list[InternshipApplication])
def get_internship_applications(
    internship_id: UUID4,
    db: Session = Depends(get_db),
    company: models.Company = Depends(get_company_user),
):
    db_internship = company_service.get_internship(db, internship_id)
    if not db_internship or db_internship.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Internship does not exist"
        )

    return convert_internship_applications(
        company_service.get_applications_for_internship(db, db_internship)
    )
