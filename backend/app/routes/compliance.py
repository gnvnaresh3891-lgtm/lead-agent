from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.suppression import SuppressionEntry
from app.models.lead import Lead

router = APIRouter()

@router.get("/check/{lead_id}")
def check_compliance(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    suppression = db.query(SuppressionEntry).filter(SuppressionEntry.email == lead.email).first()
    if suppression:
        return {"status": "suppressed", "reason": suppression.reason}
        
    return {"status": "compliant"}

@router.get("/suppression")
def get_suppression_list(db: Session = Depends(get_db)):
    entries = db.query(SuppressionEntry).all()
    return {
        "suppressions": [
            {
                "id": e.id,
                "email": e.email,
                "reason": e.reason,
                "source": e.source,
                "suppressed_at": e.suppressed_at.isoformat() if e.suppressed_at else None
            } for e in entries
        ]
    }

@router.post("/suppression")
def add_to_suppression(data: dict, db: Session = Depends(get_db)):
    entry = SuppressionEntry(**data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"status": "added", "id": entry.id}

@router.delete("/suppression/{id}")
def remove_suppression(id: str, db: Session = Depends(get_db)):
    entry = db.query(SuppressionEntry).filter(SuppressionEntry.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Suppression entry not found")
    db.delete(entry)
    db.commit()
    return {"status": "removed"}

@router.get("/stats")
def get_compliance_stats(db: Session = Depends(get_db)):
    count = db.query(SuppressionEntry).count()
    return {
        "suppression_count": count,
        "spam_rate": 0.02,
        "bounce_rate": 0.05,
        "unsubscribe_rate": 0.03
    }
