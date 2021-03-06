from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend import models
from backend.core.config import SETTINGS
from backend.dependencies import get_db
from backend.schemas.user import User
from backend.services.company import get_company
from backend.services.students import get_student
from backend.services.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SETTINGS.JWT_SECRET_KEY.get_secret_value(), algorithms=[SETTINGS.JWT_ALGORITHM]
        )

    except JWTError as exc:
        raise credentials_exception from exc

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_by_email(db, email=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_company_user(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> models.Company:
    company = get_company(db, current_user.id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Must be logged in with company account"
        )

    return company


def get_student_user(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> models.Student:
    student = get_student(db, current_user.id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Must be logged in with student account"
        )

    return student


def get_company_or_student_user(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> Union[models.Student, models.Company]:
    try:
        return get_student_user(current_user, db)
    except HTTPException:
        return get_company_user(current_user, db)
