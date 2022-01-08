import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, SecretStr


class EducationBase(BaseModel):
    institution_name: str = Field(..., alias="institutionName")
    studies_programme: str = Field(..., alias="studiesProgramme")
    starting_date: datetime.date = Field(..., alias="startingDate")
    ending_date: datetime.date = Field(..., alias="endingDate")


class VolunteeringBase(BaseModel):
    name: str
    position: str
    starting_date: datetime.date = Field(..., alias="startingDate")
    ending_date: datetime.date = Field(..., alias="endingDate")


class SkillBase(BaseModel):
    pass


class EducationCreate(EducationBase):
    pass


class VolunteeringCreate(VolunteeringBase):
    pass


class SkillCreate(SkillBase):
    pass


class StudentProfileCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=64)
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="secondName")
    birthdate: datetime.date = Field(..., alias="birthday")
    description: str
    phone: str

    educations: list[EducationCreate] = Field(..., alias="education")
    volunteerings: list[VolunteeringCreate] = Field(..., alias="volunteering")
    # skills: list[SkillCreate]

    # class Config:
    #     orm_mode = True


class Education(EducationBase):
    id: UUID4
    starting_date: int = Field(..., alias="startingDate")
    ending_date: int = Field(..., alias="endingDate")


class Volunteering(VolunteeringBase):
    id: UUID4
    starting_date: int = Field(..., alias="startingDate")
    ending_date: int = Field(..., alias="endingDate")


class StudentProfile(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="secondName")
    birthdate: int = Field(..., alias="birthday")
    description: str
    phone: str

    educations: list[Education] = Field(..., alias="education")
    volunteerings: list[Volunteering] = Field(..., alias="volunteering")


class InternshipApplicationBase(BaseModel):
    message: Optional[str] = Field(None)


class InternshipApplicationCreate(InternshipApplicationBase):
    pass


class InternshipApplication(InternshipApplicationBase):
    id: UUID4
