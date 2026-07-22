from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.campaign import Campaign
from app.models.message import Message

router = APIRouter()

@router.get("/")
def get_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).all()
    return {
        "campaigns": [
            {
                "id": c.id,
                "name": c.name,
                "status": c.status,
                "total_leads": c.total_leads,
                "total_sent": c.total_sent,
                "total_opened": c.total_opened,
                "total_replied": c.total_replied
            } for c in campaigns
        ]
    }

@router.post("/")
def create_campaign(campaign_data: dict, db: Session = Depends(get_db)):
    campaign = Campaign(**campaign_data)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return {"id": campaign.id, "status": "created"}

@router.get("/{id}")
def get_campaign(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {
        "id": campaign.id,
        "name": campaign.name,
        "status": campaign.status,
        "total_leads": campaign.total_leads,
        "total_sent": campaign.total_sent,
        "total_opened": campaign.total_opened,
        "total_replied": campaign.total_replied
    }

@router.put("/{id}")
def update_campaign(id: str, campaign_data: dict, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for k, v in campaign_data.items():
        if hasattr(campaign, k):
            setattr(campaign, k, v)
    db.commit()
    return {"id": campaign.id, "status": "updated"}

@router.post("/{id}/launch")
def launch_campaign(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.status = "active"
    db.commit()
    return {"status": "launched"}

@router.post("/{id}/pause")
def pause_campaign(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.status = "paused"
    db.commit()
    return {"status": "paused"}

@router.get("/{id}/messages")
def get_campaign_messages(id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.campaign_id == id).all()
    return {
        "messages": [
            {
                "id": m.id,
                "subject": m.subject,
                "status": m.status,
                "sent_at": m.sent_at
            } for m in messages
        ]
    }

@router.get("/{id}/analytics")
def get_campaign_analytics(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {
        "sent": campaign.total_sent,
        "delivered": campaign.total_delivered,
        "opened": campaign.total_opened,
        "replied": campaign.total_replied,
        "booked": campaign.total_booked
    }
