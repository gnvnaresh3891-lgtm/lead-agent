import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.models.signal import Signal
from app.services.signals.scoring import calculate_signal_score, calculate_icp_fit, calculate_composite_score

logger = logging.getLogger("lead_agent.ingestion")

class WebhookSignalPayload(BaseModel):
    source: str  # e.g., "rb2b", "koala", "crunchbase_rss", "linkedin_webhook"
    signal_type: str  # e.g., "website_visit", "funding", "job_change", "hiring_surge"
    company_name: str
    company_domain: str
    first_name: Optional[str] = "Prospect"
    last_name: Optional[str] = "Lead"
    email: Optional[str] = None
    title: Optional[str] = "Decision Maker"
    industry: Optional[str] = "Technology"
    employee_count: Optional[int] = 100
    country: Optional[str] = "US"
    signal_details: Dict[str, Any] = {}

class SignalIngestionService:
    """Production Real-Time Webhook & Feed Signal Ingestion Engine."""

    def __init__(self, db: Session):
        self.db = db

    def process_webhook_signal(self, payload: WebhookSignalPayload, org_id: str) -> Dict[str, Any]:
        """Parse incoming webhook signal, auto-discover or enrich lead, and recalculate scores."""
        logger.info(f"Processing incoming {payload.source} signal ({payload.signal_type}) for {payload.company_domain}")

        # 1. Deduplicate or create Lead record
        email = payload.email or f"contact@{payload.company_domain}"
        lead = self.db.query(Lead).filter(
            (Lead.org_id == org_id) & 
            ((Lead.email == email) | (Lead.company_domain == payload.company_domain))
        ).first()

        if not lead:
            lead = Lead(
                org_id=org_id,
                email=email,
                first_name=payload.first_name,
                last_name=payload.last_name,
                title=payload.title,
                company_name=payload.company_name,
                company_domain=payload.company_domain,
                industry=payload.industry,
                employee_count=payload.employee_count,
                country=payload.country,
                status="new",
                source=payload.source
            )
            self.db.add(lead)
            self.db.commit()
            self.db.refresh(lead)

        # 2. Calculate time-decayed signal weight
        now = datetime.now(timezone.utc)
        decayed_score = calculate_signal_score(payload.signal_type, now)

        # 3. Save Signal record
        signal_entry = Signal(
            lead_id=lead.id,
            org_id=org_id,
            signal_type=payload.signal_type,
            signal_source=payload.source,
            signal_data=payload.signal_details,
            raw_weight=decayed_score,
            decayed_score=decayed_score,
            detected_at=now
        )
        self.db.add(signal_entry)

        # 4. Recalculate Composite Score
        icp_config = {
            "target_industries": ["Technology", "Software", "Fintech", "B2B SaaS"],
            "company_size_min": 20,
            "company_size_max": 1000,
            "target_roles": ["VP", "Director", "CRO", "Head"]
        }
        lead_dict = {
            "industry": lead.industry,
            "company_size": lead.employee_count or 100,
            "role": lead.title or ""
        }
        icp_score = calculate_icp_fit(lead_dict, icp_config)
        composite = calculate_composite_score(decayed_score, icp_score)

        lead.intent_score = decayed_score
        lead.icp_fit_score = icp_score
        lead.composite_score = composite

        if composite >= 75:
            lead.status = "enriched"

        self.db.commit()

        return {
            "lead_id": lead.id,
            "signal_id": signal_entry.id,
            "composite_score": composite,
            "status": lead.status,
            "signal_type": payload.signal_type
        }
