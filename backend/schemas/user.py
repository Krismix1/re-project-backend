from enum import Enum
from typing import Union

from pydantic import BaseModel, EmailStr, Field, SecretStr
from pydantic.types import UUID4

from backend.schemas.company import CompanyProfile
from backend.schemas.student import StudentProfile


class UserBase(BaseModel):
    email: EmailStr


class User(UserBase):
    id: UUID4
    is_active: bool = Field(..., alias="isActive")

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: SecretStr = Field(..., min_length=8, max_length=64)


class UserType(str, Enum):
    STUDENT = "STUDENT"
    COMPANY = "COMPANY"


class UserProfileResponse(User):
    user_type: UserType = Field(..., alias="userType")
    profile: Union[StudentProfile, CompanyProfile]
