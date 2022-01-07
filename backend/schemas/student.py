import datetime

from pydantic import BaseModel, EmailStr, Field, SecretStr


class Education(BaseModel):
    institution_name: str = Field(..., alias="institutionName")
    studies_programme: str = Field(..., alias="studiesProgramme")
    starting_date: datetime.date = Field(..., alias="startingDate")
    ending_date: datetime.date = Field(..., alias="endingDate")


class Volunteering(BaseModel):
    name: str
    position: str
    starting_date: datetime.date = Field(..., alias="startingDate")
    ending_date: datetime.date = Field(..., alias="endingDate")


class Skill(BaseModel):
    pass


class StudentProfileCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=64)
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="secondName")
    birthday: datetime.date
    description: str
    phone: str

    education: list[Education]
    volunteering: list[Volunteering]
    # skills: list[Skill]

    # class Config:
    #     orm_mode = True
