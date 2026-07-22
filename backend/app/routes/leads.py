from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.lead import Lead
from app.models.signal import Signal
from typing import Optional

router = APIRouter()

@router.get("/")
def get_leads(
    status: Optional[str] = None,
    search: Optional[str] = None,
    min_score: Optional[float] = None,
    sort_by: str = "composite_score",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    if search:
        query = query.filter(
            (Lead.first_name.ilike(f"%{search}%")) |
            (Lead.last_name.ilike(f"%{search}%")) |
            (Lead.company_name.ilike(f"%{search}%"))
        )
    if min_score:
        query = query.filter(Lead.composite_score >= min_score)
    
    total = query.count()
    
    if sort_order == "desc":
        query = query.order_by(getattr(Lead, sort_by, Lead.composite_score).desc())
    else:
        query = query.order_by(getattr(Lead, sort_by, Lead.composite_score).asc())
    
    leads = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "leads": [
            {
                "id": l.id,
                "email": l.email,
                "first_name": l.first_name,
                "last_name": l.last_name,
                "title": l.title,
                "company_name": l.company_name,
                "company_domain": l.company_domain,
                "linkedin_url": l.linkedin_url,
                "industry": l.industry,
                "employee_count": l.employee_count,
                "country": l.country,
                "icp_fit_score": l.icp_fit_score,
                "intent_score": l.intent_score,
                "composite_score": l.composite_score,
                "status": l.status,
                "source": l.source,
                "created_at": l.created_at.isoformat() if l.created_at else None,
                "updated_at": l.updated_at.isoformat() if l.updated_at else None,
                "signal_count": db.query(Signal).filter(Signal.lead_id == l.id).count()
            }
            for l in leads
        ]
    }

@router.get("/pipeline")
def get_pipeline(db: Session = Depends(get_db)):
    statuses = ["new", "enriched", "sequenced", "replied", "qualified", "booked", "lost"]
    pipeline = {}
    for status in statuses:
        leads = db.query(Lead).filter(Lead.status == status).all()
        pipeline[status] = {
            "count": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "first_name": l.first_name,
                    "last_name": l.last_name,
                    "company_name": l.company_name,
                    "title": l.title,
                    "composite_score": l.composite_score,
                    "status": l.status
                }
                for l in leads[:10]
            ]
        }
    return pipeline

@router.get("/{lead_id}")
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    signals = db.query(Signal).filter(Signal.lead_id == lead_id).all()
    return {
        "id": lead.id,
        "email": lead.email,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "title": lead.title,
        "company_name": lead.company_name,
        "company_domain": lead.company_domain,
        "industry": lead.industry,
        "employee_count": lead.employee_count,
        "country": lead.country,
        "icp_fit_score": lead.icp_fit_score,
        "intent_score": lead.intent_score,
        "composite_score": lead.composite_score,
        "status": lead.status,
        "signals": [
            {
                "id": s.id,
                "signal_type": s.signal_type,
                "signal_data": s.signal_data,
                "decayed_score": s.decayed_score,
                "detected_at": s.detected_at.isoformat() if s.detected_at else None
            }
            for s in signals
        ]
    }

@router.post("/")
def create_lead(lead_data: dict, db: Session = Depends(get_db)):
    lead = Lead(**lead_data)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"id": lead.id, "status": "created"}

@router.put("/{lead_id}")
def update_lead(lead_id: str, lead_data: dict, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for key, value in lead_data.items():
        if hasattr(lead, key):
            setattr(lead, key, value)
    db.commit()
    return {"id": lead.id, "status": "updated"}

@router.delete("/{lead_id}")
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"status": "deleted"}
