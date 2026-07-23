from datetime import datetime, timezone
import uuid
from typing import Any, Dict, Optional
from sqlalchemy import JSON, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, GUID, TenantMixin


class Signal(TenantMixin, Base):
    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False
    )
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Signal id={self.id} org_id={self.org_id} type='{self.signal_type}'>"
