from datetime import datetime, timedelta
from typing import Any, Literal, Union

from jose import jwt
from passlib.context import CryptContext

from backend.core.config import SETTINGS
from backend.schemas.user import UserInDB
from backend.services.user import get_user

UnicodeOrBytes = Union[str, bytes]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: UnicodeOrBytes, hashed_password: UnicodeOrBytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: UnicodeOrBytes) -> str:
    return pwd_context.hash(password)


def authenticate_user(
    fake_db, username: str, password: UnicodeOrBytes
) -> Union[Literal[False], UserInDB]:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.JWT_SECRET_KEY, algorithm=SETTINGS.JWT_ALGORITHM)
    return encoded_jwt
