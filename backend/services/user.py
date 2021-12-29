from typing import Any, Optional

from backend.schemas.user import UserInDB

FAKE_USERS_DB = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(db: dict[str, dict[str, Any]], username: str) -> Optional[UserInDB]:
    user_dict = db.get(username)
    return UserInDB(**user_dict) if user_dict else None
