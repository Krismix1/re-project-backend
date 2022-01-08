import uuid
from typing import Optional

from sqlalchemy.orm import Session

from backend import models
from backend.schemas.company import (
    CompanyProfile,
    CompanyProfileCreate,
    InternshipCreate,
)
from backend.services.user import get_user


def create_company(
    db: Session, company: CompanyProfileCreate, account_id: uuid.UUID
) -> models.Company:
    db_account = get_user(db, account_id)
    if not db_account:
        raise ValueError(f"User with ID {account_id} not found")

    db_company = models.Company(
        id=account_id, phone=company.phone, description=company.description, name=company.name
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_companies(db: Session, *, skip: int = 0, limit: int = 100) -> list[models.Company]:
    return db.query(models.Company).offset(skip).limit(limit).all()


def get_company(db: Session, user_id: uuid.UUID) -> Optional[models.Company]:
    return db.query(models.Company).filter(models.Company.id == user_id).first()


def company_from_db_model(company: models.Company) -> CompanyProfile:
    return CompanyProfile(
        id=company.id,
        email=company.account.email,
        name=company.name,
        description=company.description,
        phone=company.phone,
    )


def create_internship(
    db: Session, company: models.Company, internship: InternshipCreate
) -> models.Internship:
    db_internship = models.Internship(
        company_id=company.id, description=internship.description, title=internship.title
    )
    db.add(db_internship)
    db.commit()
    db.refresh(db_internship)
    return db_internship


def get_internships_for_company(db: Session, company: models.Company) -> list[models.Internship]:
    return db.query(models.Internship).filter(models.Internship.company_id == company.id).all()


def get_internships(db: Session) -> list[models.Internship]:
    return db.query(models.Internship).all()
