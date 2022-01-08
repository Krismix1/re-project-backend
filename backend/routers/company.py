from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.schemas.company import CompanyProfile
from backend.services import company as company_service

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyProfile])
def get_companies(db: Session = Depends(get_db)):
    return [
        CompanyProfile(
            id=company.id,
            email=company.account.email,
            name=company.name,
            description=company.description,
            phone=company.phone,
        )
        for company in company_service.get_companies(db)
    ]
