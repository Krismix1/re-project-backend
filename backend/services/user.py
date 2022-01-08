"""Database access layer."""
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from backend.models import user as user_models


def get_user(db: Session, user_id: uuid.UUID) -> Optional[user_models.User]:
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[user_models.User]:
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_users(db: Session, *, skip: int = 0, limit: int = 100) -> list[user_models.User]:
    return db.query(user_models.User).offset(skip).limit(limit).all()
