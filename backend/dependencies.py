"""FastAPI dependencies."""
from typing import Generator

from sqlalchemy.orm import Session

from backend.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Create a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
