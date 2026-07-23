"""
Tier 2 Boundary Tests: Multi-Tenant DB Scoping & Header Resilience
Asserts strictly against real tenancy enforcement in app/core/tenancy.py and SQLAlchemy models.
"""
import uuid
import pytest
from sqlalchemy import select

from app.core.tenancy import (
    TenantContextError,
    TenantCrossIsolationError,
    set_tenant_id,
    tenant_context,
)
from app.models.lead import Lead
from app.models.signal import Signal
from app.workers.signal_worker import SignalWorker


@pytest.mark.asyncio
async def test_missing_tenant_context_query(db_session, setup_orgs):
    """Querying multi-tenant model without tenant context raises TenantContextError."""
    with pytest.raises(TenantContextError) as exc_info:
        await db_session.execute(select(Lead))
    assert "Tenant context is required" in str(exc_info.value)


@pytest.mark.asyncio
async def test_empty_string_org_id_header(async_client):
    """Empty string X-Org-Id header returns 400 Bad Request."""
    headers = {"X-Org-Id": ""}
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=headers, json={"signal_type": "click"}
    )
    assert response.status_code == 400
    assert "Invalid tenant/org ID format" in response.json()["detail"]


@pytest.mark.asyncio
async def test_invalid_uuid_set_tenant_id():
    """Passing invalid UUID string to set_tenant_id raises TenantContextError."""
    with pytest.raises(TenantContextError) as exc_info:
        set_tenant_id("invalid-uuid-string")
    assert "Invalid UUID format" in str(exc_info.value)


@pytest.mark.asyncio
async def test_non_existent_org_id_get_signals(async_client):
    """GET /api/v1/signals with non-existent org UUID returns empty list."""
    random_org = str(uuid.uuid4())
    response = await async_client.get("/api/v1/signals", headers={"X-Org-Id": random_org})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_cross_tenant_get_signal_by_id(async_client, redis_client, setup_orgs, org1_id, org2_id):
    """Attempting to fetch Org 1 signal using Org 2 header returns 404 Not Found."""
    sig_uuid = uuid.uuid4()
    # Ingest signal for Org 1
    with tenant_context(org1_id):
        await redis_client.push_signal("signals_queue", {
            "signal_id": str(sig_uuid),
            "org_id": str(org1_id),
            "signal_type": "secret_event",
            "score": 10.0,
        })
        worker = SignalWorker(redis_client=redis_client)
        res = await worker.process_next_signal()
        assert res["status"] == "PROCESSED"

    # Query signal using Org 2 header
    headers_org2 = {"X-Org-Id": str(org2_id)}
    response = await async_client.get(f"/api/v1/signals/{sig_uuid}", headers=headers_org2)
    assert response.status_code == 404
    assert "Signal not found or inaccessible" in response.json()["detail"]
