from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from backend.core.config import SETTINGS
from backend.schemas.user import User
from backend.services.user import FAKE_USERS_DB, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SETTINGS.JWT_SECRET_KEY, algorithms=[SETTINGS.JWT_ALGORITHM])

    except JWTError as exc:
        raise credentials_exception from exc

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user(FAKE_USERS_DB, username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
