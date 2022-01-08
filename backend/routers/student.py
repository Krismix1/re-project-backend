from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from backend import models
from backend.core.security import get_student_user
from backend.dependencies import get_db
from backend.schemas.student import InternshipApplicationCreate, StudentProfile
from backend.services import students
from backend.services.company import get_internship

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentProfile])
def get_students(db: Session = Depends(get_db)):
    return [students.student_from_db_model(student) for student in students.get_students(db)]


@router.post(
    "/internships/{internship_id}/apply",
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
