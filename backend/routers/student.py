from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.schemas.student import StudentProfile
from backend.services import students

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentProfile])
def get_students(db: Session = Depends(get_db)):
    return [students.student_from_db_model(student) for student in students.get_students(db)]
