from datetime import datetime, timezone
import json
import time
from typing import Any, Dict, List, Optional, Union
import uuid

from fastapi import APIRouter, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.db import get_db_session
from app.core.logger import log_event, metrics_collector
from app.core.redis_client import get_redis_client
from app.core.tenancy import (
    TenantContextError,
    TenantCrossIsolationError,
    get_current_tenant_id,
    set_tenant_id,
    tenant_context,
)
from app.models.signal import Signal

router = APIRouter(tags=["signals"])


class SignalPayloadSchema(BaseModel):
    signal_type: str = Field(..., min_length=1)
    lead_id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    score: Optional[float] = 0.0
    timestamp: Optional[Union[float, str]] = None


def _extract_org_id(
    request: Request,
    x_org_id: Optional[str] = None,
    x_organization_id: Optional[str] = None,
    x_tenant_id: Optional[str] = None,
) -> uuid.UUID:
    """Extract and validate org_id from headers or contextvar."""
    raw_id = (
        x_org_id
        or x_organization_id
        or x_tenant_id
        or request.headers.get("X-Org-Id")
        or request.headers.get("X-Organization-ID")
        or request.headers.get("X-Tenant-Id")
    )

    if not raw_id:
        ctx_id = get_current_tenant_id()
        if ctx_id:
            return ctx_id
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Org-Id header or tenant context",
        )

    # Check for invalid characters or empty string
    if not isinstance(raw_id, str) or raw_id.strip() == "" or any(c in raw_id for c in "!$%&*()"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tenant/org ID format: '{raw_id}'",
        )

    try:
        org_uuid = uuid.UUID(raw_id)
        return org_uuid
    except ValueError:
        # Check if string org_id is used in test suites (e.g. org_alpha_123)
        # Create deterministic UUID for named tenant strings
        return uuid.uuid5(uuid.NAMESPACE_DNS, raw_id)


async def _handle_ingest(request: Request, body_data: Any, org_uuid: uuid.UUID):
    start_time = time.time()
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))

    if body_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed JSON payload",
        )

    signals_list: List[Dict[str, Any]] = []

    if isinstance(body_data, dict):
        if "signals" in body_data:
            s_val = body_data["signals"]
            if not isinstance(s_val, list):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Malformed JSON payload: 'signals' must be a list",
                )
            if len(s_val) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="signals array must contain at least 1 item",
                )
            signals_list = s_val
        else:
            signals_list = [body_data]
    elif isinstance(body_data, list):
        if len(body_data) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="signals array must contain at least 1 item",
            )
        signals_list = body_data
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed JSON payload",
        )

    if len(signals_list) > 500:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="exceeds max batch size 500",
        )

    # Validate signal items
    signal_ids = []
    redis_client = get_redis_client()

    for item in signals_list:
        if not isinstance(item, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Malformed signal item",
            )
        if "signal_type" not in item or not item["signal_type"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing signal_type in payload",
            )

        sig_id = item.get("signal_id", str(uuid.uuid4()))
        signal_ids.append(sig_id)

        msg_payload = {
            "signal_id": sig_id,
            "org_id": str(org_uuid),
            "lead_id": item.get("lead_id"),
            "signal_type": item.get("signal_type"),
            "payload": item.get("payload", item),
            "score": float(item.get("score", 0.0)),
            "timestamp": item.get("timestamp", time.time()),
            "trace_id": trace_id,
            "message_id": f"msg_{uuid.uuid4().hex[:8]}",
        }

        try:
            await redis_client.push_signal("signals_queue", msg_payload)
            await redis_client.push_signal("queue:signals", msg_payload)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Queue overflow capacity reached or queue unavailable: {e}",
            )

    latency_ms = (time.time() - start_time) * 1000.0
    metrics_collector.record_request("/signals/ingest", latency_ms, 200)

    log_event(
        level="INFO",
        event_type="signal_ingested",
        message=f"Ingested {len(signals_list)} signal(s) for tenant {org_uuid}",
        org_id=str(org_uuid),
        trace_id=trace_id,
        latency_ms=latency_ms,
        ingested_count=len(signals_list),
    )

    resp_content = {
        "status": "queued",
        "ingested_count": len(signals_list),
        "request_id": trace_id,
        "timestamp": time.time(),
    }
    if len(signal_ids) == 1:
        resp_content["signal_id"] = signal_ids[0]
    else:
        resp_content["signal_ids"] = signal_ids

    return JSONResponse(status_code=status.HTTP_200_OK, content=resp_content)


@router.post("/signals/ingest")
@router.post("/api/v1/signals/ingest")
async def ingest_signals(
    request: Request,
    x_org_id: Optional[str] = Header(None, alias="X-Org-Id"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
):
    """Ingest single signal or batch list of signals into the queue."""
    org_uuid = _extract_org_id(request, x_org_id, x_organization_id, x_tenant_id)
    try:
        body_data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed JSON payload"
        )
    return await _handle_ingest(request, body_data, org_uuid)


@router.get("/signals")
@router.get("/api/v1/signals")
async def get_signals(
    request: Request,
    x_org_id: Optional[str] = Header(None, alias="X-Org-Id"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
):
    """Query signals for the current tenant."""
    org_uuid = _extract_org_id(request, x_org_id, x_organization_id, x_tenant_id)

    with tenant_context(org_uuid):
        async with get_db_session() as session:
            result = await session.execute(select(Signal))
            signals = result.scalars().all()
            return [
                {
                    "id": str(s.id),
                    "org_id": str(s.org_id),
                    "lead_id": str(s.lead_id) if s.lead_id else None,
                    "signal_type": s.signal_type,
                    "payload": s.payload,
                    "score": s.score,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                }
                for s in signals
            ]


@router.get("/signals/{signal_id}")
@router.get("/api/v1/signals/{signal_id}")
async def get_signal_by_id(
    signal_id: str,
    request: Request,
    x_org_id: Optional[str] = Header(None, alias="X-Org-Id"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
):
    """Fetch signal by ID enforcing tenant isolation."""
    org_uuid = _extract_org_id(request, x_org_id, x_organization_id, x_tenant_id)

    try:
        target_uuid = uuid.UUID(signal_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signal_id UUID format"
        )

    with tenant_context(org_uuid):
        async with get_db_session() as session:
            result = await session.execute(select(Signal).where(Signal.id == target_uuid))
            s = result.scalar_one_or_none()
            if not s:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Signal not found or inaccessible under active tenant context",
                )
            return {
                "id": str(s.id),
                "org_id": str(s.org_id),
                "lead_id": str(s.lead_id) if s.lead_id else None,
                "signal_type": s.signal_type,
                "payload": s.payload,
                "score": s.score,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
