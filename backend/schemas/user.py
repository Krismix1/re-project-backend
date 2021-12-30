from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class User(UserBase):
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
