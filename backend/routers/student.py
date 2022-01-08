import datetime
import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.schemas.student import Education, StudentProfile, Volunteering
from backend.services import students

router = APIRouter(prefix="/students", tags=["students"])


def _date_to_ts(date: datetime.date) -> float:
    return time.mktime(date.timetuple())


@router.post("", response_model=list[StudentProfile])
def get_students(db: Session = Depends(get_db)):
    return [
        StudentProfile(
            id=student.id,
            email=student.account.email,
            firstName=student.first_name,
            secondName=student.last_name,
            birthday=_date_to_ts(student.birthdate),
            description=student.description,
            phone=student.phone,
            education=[
                Education(
                    id=education.id,
                    institutionName=education.institution_name,
                    studiesProgramme=education.studies_programme,
                    startingDate=_date_to_ts(education.starting_date),
                    endingDate=_date_to_ts(education.ending_date),
                )
                for education in student.educations
            ],
            volunteering=[
                Volunteering(
                    id=volunteering.id,
                    name=volunteering.name,
                    position=volunteering.position,
                    startingDate=_date_to_ts(volunteering.starting_date),
                    endingDate=_date_to_ts(volunteering.ending_date),
                )
                for volunteering in student.volunteerings
            ],
        )
        for student in students.get_students(db)
    ]
