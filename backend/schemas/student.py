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
    birthdate: datetime.date = Field(..., alias="birthday")
    description: str
    phone: str

    educations: list[Education] = Field(..., alias="education")
    volunteerings: list[Volunteering] = Field(..., alias="volunteering")
    # skills: list[Skill]

    # class Config:
    #     orm_mode = True
