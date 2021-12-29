"""Main module for API routes."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from backend.core.config import SETTINGS
from backend.db import crud, schemas
from backend.dependencies import get_db
from backend.schemas.operational import BuildInfo

router = APIRouter()
ops_router = APIRouter()

# pylint:disable=missing-function-docstring


@ops_router.get("/healthcheck", response_class=PlainTextResponse, tags=["operational"])
async def healthcheck() -> str:
    """Heroku healthcheck endpoint."""
    return "OK"


@ops_router.get("/build-info", response_model=BuildInfo, tags=["operational"])
async def build_info():
    return {"build_id": SETTINGS.BUILD_ID}


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)
