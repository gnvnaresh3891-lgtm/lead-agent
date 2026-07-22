import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    lead_id = Column(String, ForeignKey("leads.id"))
    org_id = Column(String, ForeignKey("organizations.id"))
    channel = Column(String)
    subject = Column(String)
    body = Column(String)
    personalization_context = Column(JSON)
    quality_score = Column(Float)
    compliance_status = Column(String)
    status = Column(String, default="draft")
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    campaign = relationship("Campaign", back_populates="messages")
    lead = relationship("Lead", back_populates="messages")
