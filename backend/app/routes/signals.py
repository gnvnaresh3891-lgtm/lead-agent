from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models.signal import Signal
from app.models.lead import Lead
from app.services.signals.ingestion import SignalIngestionService, WebhookSignalPayload
from typing import Optional
import datetime
import random

router = APIRouter()

@router.get("/")
def get_signals(
    signal_type: Optional[str] = None,
    min_score: Optional[float] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Signal)
    if signal_type:
        query = query.filter(Signal.signal_type == signal_type)
    if min_score:
        query = query.filter(Signal.decayed_score >= min_score)
    
    total = query.count()
    signals = query.order_by(Signal.detected_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "signals": [
            {
                "id": s.id,
                "lead_id": s.lead_id,
                "signal_type": s.signal_type,
                "signal_data": s.signal_data,
                "detected_at": s.detected_at.isoformat() if s.detected_at else None
            } for s in signals
        ]
    }

@router.get("/stats")
def get_signal_stats(db: Session = Depends(get_db)):
    types_count = db.query(Signal.signal_type, func.count(Signal.id)).group_by(Signal.signal_type).all()
    types_dict = {t[0]: t[1] for t in types_count}
    
    thirty_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    recent_signals = db.query(Signal).filter(Signal.detected_at >= thirty_days_ago).all()
    
    return {
        "total_count": db.query(Signal).count(),
        "by_type": types_dict,
        "recent_count": len(recent_signals)
    }

@router.post("/webhook")
def receive_webhook_signal(payload: WebhookSignalPayload, db: Session = Depends(get_db)):
    """Production endpoint for receiving real-time webhook signals from RB2B, Zapier, Crunchbase, etc."""
    ingester = SignalIngestionService(db)
    result = ingester.process_webhook_signal(payload, org_id="demo-org-1")
    return {"status": "success", "data": result}

@router.post("/")
def create_signal(signal_data: dict, db: Session = Depends(get_db)):
    signal = Signal(**signal_data)
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return {"id": signal.id, "status": "created"}

@router.post("/generate-demo")
def generate_demo_signals(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    if not leads:
        raise HTTPException(status_code=400, detail="No leads to attach signals to")
    
    signal_types = ["job_change", "funding", "hiring_surge", "website_visit"]
    created = []
    for _ in range(10):
        lead = random.choice(leads)
        sig = Signal(
            lead_id=lead.id,
            signal_type=random.choice(signal_types),
            signal_data={"source": "Demo Generator", "details": "Auto generated signal"},
            detected_at=datetime.datetime.utcnow()
        )
        db.add(sig)
        created.append(sig)
    
    db.commit()
    return {"status": "ok", "generated": len(created)}
