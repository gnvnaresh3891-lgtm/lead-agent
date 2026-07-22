import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    org_id = Column(String, ForeignKey("organizations.id"))
    email = Column(String, nullable=False, index=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    company_name = Column(String)
    company_domain = Column(String)
    linkedin_url = Column(String)
    industry = Column(String)
    employee_count = Column(Integer)
    annual_revenue = Column(Float)
    technologies = Column(JSON)
    country = Column(String)
    icp_fit_score = Column(Float)
    intent_score = Column(Float)
    composite_score = Column(Float)
    status = Column(String, default="new")
    source = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", back_populates="leads")
    signals = relationship("Signal", back_populates="lead")
    messages = relationship("Message", back_populates="lead")
    consents = relationship("ConsentRecord", back_populates="lead")
