from pydantic import UUID4, BaseModel, EmailStr, Field, SecretStr


class CompanyProfileCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=64)
    name: str
    description: str
    phone: str


class CompanyProfile(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    description: str
    phone: str
