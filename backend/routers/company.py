from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from backend import models
from backend.core.security import get_company_user
from backend.dependencies import get_db
from backend.schemas.company import CompanyProfile, Internship, InternshipCreate
from backend.services import company as company_service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyProfile])
def get_companies(db: Session = Depends(get_db)):
    return [
        company_service.company_from_db_model(company)
        for company in company_service.get_companies(db)
    ]


@router.post("/internships", response_class=Response, status_code=status.HTTP_201_CREATED)
def create_internship(
    internship: InternshipCreate,
    company: models.Company = Depends(get_company_user),
    db: Session = Depends(get_db),
):
    company_service.create_internship(db, company, internship)


@router.get("/{company_id}/internships", response_model=list[Internship])
def get_internship_for_company(
    company_id: UUID4,
    db: Session = Depends(get_db),
):
    company = company_service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    return company_service.get_internships_for_company(db, company)


@router.get("/internships", response_model=list[Internship])
def get_internships(db: Session = Depends(get_db)):
    return company_service.get_internships(db)
