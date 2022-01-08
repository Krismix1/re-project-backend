from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from backend.core.config import SETTINGS
from backend.dependencies import get_db
from backend.schemas.auth import TokenResponse
from backend.schemas.company import CompanyProfileCreate
from backend.schemas.student import StudentProfileCreate
from backend.schemas.user import UserCreate
from backend.services import auth
from backend.services import company as company_service
from backend.services import students
from backend.services.auth import authenticate_user, create_access_token
from backend.services.user import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestFormStrict = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/signup/students",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
def create_student(student: StudentProfileCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, student.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user_create = UserCreate(email=student.email, password=student.password.get_secret_value())
    db_user = auth.create_user(db, user_create)
    students.create_student(db, student, db_user.id)


@router.post(
    "/signup/companies",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
def create_company(company: CompanyProfileCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, company.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user_create = UserCreate(email=company.email, password=company.password.get_secret_value())
    db_user = auth.create_user(db, user_create)
    company_service.create_company(db, company, db_user.id)
