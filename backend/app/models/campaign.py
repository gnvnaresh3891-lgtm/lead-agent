import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    org_id = Column(String, ForeignKey("organizations.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="draft")
    icp_filters = Column(JSON)
    signal_filters = Column(JSON)
    sequence_config = Column(JSON)
    total_leads = Column(Integer, default=0)
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_replied = Column(Integer, default=0)
    total_booked = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", back_populates="campaigns")
    messages = relationship("Message", back_populates="campaign")
