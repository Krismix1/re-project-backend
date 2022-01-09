import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field, SecretStr


class CompanyProfileCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=64)
    name: str
    domain: str = Field(default="", example="IT")
    description: str
    phone: str


class CompanyProfile(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    domain: str
    description: str
    phone: str


class InternshipBase(BaseModel):
    title: str
    description: str
    deadline: datetime.date
    starting_date: datetime.date = Field(..., alias="startingDate")
    ending_date: datetime.date = Field(..., alias="endingDate")


class InternshipCreate(InternshipBase):
    pass


class Internship(InternshipBase):
    id: UUID4
    company: CompanyProfile
    deadline: int
    starting_date: int = Field(..., alias="startingDate")
    ending_date: int = Field(..., alias="endingDate")

    class Config:
        orm_mode = True
