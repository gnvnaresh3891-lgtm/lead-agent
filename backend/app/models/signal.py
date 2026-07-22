import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Signal(Base):
    __tablename__ = "signals"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    lead_id = Column(String, ForeignKey("leads.id"))
    org_id = Column(String, ForeignKey("organizations.id"))
    signal_type = Column(String, nullable=False)
    signal_source = Column(String)
    signal_data = Column(JSON)
    raw_weight = Column(Float)
    decayed_score = Column(Float)
    detected_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lead = relationship("Lead", back_populates="signals")
