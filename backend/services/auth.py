from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend import models
from backend.core.config import SETTINGS
from backend.schemas import user as user_schemas
from backend.services.user import get_user_by_email

UnicodeOrBytes = Union[str, bytes]
# https://passlib.readthedocs.io/en/stable/narr/context-tutorial.html#deprecation-hash-migration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: UnicodeOrBytes, hashed_password: UnicodeOrBytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: UnicodeOrBytes) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: UnicodeOrBytes) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.JWT_SECRET_KEY.get_secret_value(), algorithm=SETTINGS.JWT_ALGORITHM
    )
    return encoded_jwt


def create_user(db: Session, user: user_schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
