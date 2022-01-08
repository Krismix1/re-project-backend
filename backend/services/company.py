import uuid

from sqlalchemy.orm import Session

from backend import models
from backend.schemas.company import CompanyProfileCreate
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
