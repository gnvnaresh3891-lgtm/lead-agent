import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SuppressionEntry(Base):
    __tablename__ = "suppressions"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    org_id = Column(String, ForeignKey("organizations.id"))
    email = Column(String, nullable=False, index=True)
    reason = Column(String)
    source = Column(String)
    suppressed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
