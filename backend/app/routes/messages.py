from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.message import Message
from app.models.lead import Lead
from typing import Optional

router = APIRouter()

@router.get("/")
def get_messages(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Message)
    if status:
        query = query.filter(Message.status == status)
    
    messages = query.offset(skip).limit(limit).all()
    return {
        "messages": [
            {
                "id": m.id,
                "lead_id": m.lead_id,
                "campaign_id": m.campaign_id,
                "subject": m.subject,
                "body": m.body,
                "status": m.status,
                "sent_at": m.sent_at.isoformat() if m.sent_at else None
            } for m in messages
        ]
    }

@router.post("/generate")
def generate_message(request: dict, db: Session = Depends(get_db)):
    lead_id = request.get("lead_id")
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Mock generation
    content = f"Hi {lead.first_name},\n\nI noticed {lead.company_name} is growing. We can help with that."
    return {"content": content}

@router.post("/{id}/approve")
def approve_message(id: str, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.status = "approved"
    db.commit()
    return {"status": "approved"}
