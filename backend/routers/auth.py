from datetime import datetime, timedelta
from typing import Any, Literal, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

UnicodeOrBytes = Union[str, bytes]

router = APIRouter(prefix="/auth", tags=["auth"])

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: dict[str, dict[str, Any]], username: str) -> Optional[UserInDB]:
    user_dict = db.get(username)
    return UserInDB(**user_dict) if user_dict else None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError as exc:
        raise credentials_exception from exc

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # token_data = TokenData(username=username)
    # user = get_user(fake_users_db, username=token_data.username)
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
