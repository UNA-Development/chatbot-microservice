"""
Admin API endpoints for managing companies
Add this to main.py or import as a router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from models import Company, get_db
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["admin"])


# Pydantic models for API
class CompanyCreate(BaseModel):
    site_id: str = Field(..., description="Unique identifier (e.g., 'mycompany')")
    name: str = Field(..., description="Company name")
    domain: Optional[str] = None
    description: Optional[str] = None
    primary_color: str = "#0066cc"
    greeting: str = "Hello! How can I help you today?"
    assistant_id: Optional[str] = None
    model: str = "gpt-4o-mini"
    temperature: str = "0.4"
    max_tokens: int = 500
    system_prompt: str = ""
    contact_info: Optional[dict] = None
    knowledge_base: str = ""
    faqs: Optional[List[dict]] = None
    sms_enabled: bool = False
    sms_phone_number: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = None
    greeting: Optional[str] = None
    assistant_id: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[str] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None
    contact_info: Optional[dict] = None
    knowledge_base: Optional[str] = None
    faqs: Optional[List[dict]] = None
    sms_enabled: Optional[bool] = None
    sms_phone_number: Optional[str] = None
    active: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: int
    site_id: str
    name: str
    domain: Optional[str]
    description: Optional[str]
    branding: dict
    ai: dict
    contact_info: Optional[dict]
    knowledge_base: str
    faqs: Optional[List[dict]]
    sms: dict
    active: bool
    created_at: Optional[str]
    updated_at: Optional[str]


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all companies
    Query params:
    - active_only: Filter for active companies only (default: true)
    """
    query = db.query(Company)
    if active_only:
        query = query.filter(Company.active == True)

    companies = query.all()
    return [company.to_dict() for company in companies]


@router.get("/companies/{site_id}", response_model=CompanyResponse)
async def get_company(site_id: str, db: Session = Depends(get_db)):
    """Get a specific company by site_id"""
    company = db.query(Company).filter(Company.site_id == site_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{site_id}' not found")
    return company.to_dict()


@router.post("/companies", response_model=CompanyResponse, status_code=201)
async def create_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company/chatbot
    No redeployment needed!
    """
    # Check if site_id already exists
    existing = db.query(Company).filter(Company.site_id == company_data.site_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Company with site_id '{company_data.site_id}' already exists"
        )

    # Create new company
    company = Company(
        site_id=company_data.site_id,
        name=company_data.name,
        domain=company_data.domain,
        description=company_data.description,
        primary_color=company_data.primary_color,
        greeting=company_data.greeting,
        assistant_id=company_data.assistant_id,
        model=company_data.model,
        temperature=company_data.temperature,
        max_tokens=company_data.max_tokens,
        system_prompt=company_data.system_prompt,
        contact_info=company_data.contact_info or {},
        knowledge_base=company_data.knowledge_base,
        faqs=company_data.faqs or [],
        sms_enabled=company_data.sms_enabled,
        sms_phone_number=company_data.sms_phone_number,
        active=True
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company.to_dict()


@router.patch("/companies/{site_id}", response_model=CompanyResponse)
async def update_company(
    site_id: str,
    updates: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update company configuration
    Only updates fields that are provided (partial update)
    """
    company = db.query(Company).filter(Company.site_id == site_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{site_id}' not found")

    # Update only provided fields
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    company.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(company)

    return company.to_dict()


@router.delete("/companies/{site_id}")
async def delete_company(site_id: str, permanent: bool = False, db: Session = Depends(get_db)):
    """
    Delete or deactivate a company
    Query params:
    - permanent: If true, permanently delete. If false (default), just deactivate
    """
    company = db.query(Company).filter(Company.site_id == site_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{site_id}' not found")

    if permanent:
        db.delete(company)
        db.commit()
        return {"message": f"Company '{site_id}' permanently deleted"}
    else:
        company.active = False
        company.updated_at = datetime.utcnow()
        db.commit()
        return {"message": f"Company '{site_id}' deactivated"}


@router.post("/companies/{site_id}/activate")
async def activate_company(site_id: str, db: Session = Depends(get_db)):
    """Reactivate a deactivated company"""
    company = db.query(Company).filter(Company.site_id == site_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{site_id}' not found")

    company.active = True
    company.updated_at = datetime.utcnow()
    db.commit()

    return {"message": f"Company '{site_id}' activated", "company": company.to_dict()}


class KnowledgeUpdate(BaseModel):
    knowledge_base: str = Field(..., description="Updated knowledge base content")


@router.patch("/companies/{site_id}/knowledge")
async def update_knowledge_base(
    site_id: str,
    data: KnowledgeUpdate,
    db: Session = Depends(get_db)
):
    """
    Quick endpoint to update just the knowledge base
    Use this for frequent content updates without touching other config
    """
    company = db.query(Company).filter(Company.site_id == site_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{site_id}' not found")

    company.knowledge_base = data.knowledge_base
    company.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Knowledge base updated", "updated_at": company.updated_at.isoformat()}
