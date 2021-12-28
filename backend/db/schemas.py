"""API schemas using Pydantic to later be passed to the database."""
from typing import Optional

from pydantic import BaseModel

# pylint:disable=missing-class-docstring


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item]

    class Config:
        orm_mode = True
