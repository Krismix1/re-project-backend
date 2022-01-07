from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: SecretStr = Field(..., min_length=8, max_length=64)
