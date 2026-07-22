import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ConsentRecord(Base):
    __tablename__ = "consents"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    lead_id = Column(String, ForeignKey("leads.id"))
    org_id = Column(String, ForeignKey("organizations.id"))
    consent_type = Column(String)
    jurisdiction = Column(String)
    lia_documented = Column(Boolean, default=False)
    data_source_description = Column(String)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lead = relationship("Lead", back_populates="consents")
