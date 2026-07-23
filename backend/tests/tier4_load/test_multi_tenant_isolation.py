"""
Tier 4 Load Harness: Multi-Tenant Data Isolation Verification (1,000 Orgs, 0 Leaks)
Asserts strictly against real tenancy isolation logic in app/core/tenancy.py and app/core/db.py.
"""
import asyncio
import uuid
import pytest
from sqlalchemy import select

from app.core.db import get_db_session
from app.core.tenancy import tenant_context
from app.models.organization import Organization
from app.models.signal import Signal


async def run_isolation_verification(org_count: int = 1000) -> dict:
    org_uuids = [uuid.uuid4() for _ in range(org_count)]

    # 1. Populate database with Organization records and Signals (2 per tenant = 2,000 records)
    async with get_db_session() as session:
        for org_uuid in org_uuids:
            org = Organization(id=org_uuid, name=f"Org {str(org_uuid)[:8]}")
            session.add(org)

    # Insert signals for each org under tenant_context
    async with get_db_session() as session:
        for org_uuid in org_uuids:
            with tenant_context(org_uuid):
                sig1 = Signal(lead_id=uuid.uuid4(), signal_type="isolation_test_1", score=1.0)
                sig2 = Signal(lead_id=uuid.uuid4(), signal_type="isolation_test_2", score=2.0)
                session.add_all([sig1, sig2])

    cross_tenant_leaks = 0
    total_tenant_queries = 0

    # 2. Query each org under its tenant_context and verify zero leaks
    async with get_db_session() as session:
        for org_uuid in org_uuids:
            total_tenant_queries += 1
            with tenant_context(org_uuid):
                res = await session.execute(select(Signal))
                records = res.scalars().all()

                leaked = [r for r in records if r.org_id != org_uuid]
                if leaked:
                    cross_tenant_leaks += len(leaked)

    isolation_percentage = (
        100.0
        if cross_tenant_leaks == 0
        else max(0.0, 100.0 - (cross_tenant_leaks / total_tenant_queries * 100.0))
    )

    return {
        "total_orgs_tested": org_count,
        "total_tenant_queries": total_tenant_queries,
        "isolated_queries": total_tenant_queries - cross_tenant_leaks,
        "cross_tenant_leaks": cross_tenant_leaks,
        "isolation_percentage": isolation_percentage,
    }


@pytest.mark.asyncio
async def test_multi_tenant_isolation_verification(test_db):
    """Test multi-tenant isolation across 1,000 orgs with 0 cross-tenant leaks."""
    metrics = await run_isolation_verification(org_count=1000)

    assert metrics["cross_tenant_leaks"] == 0, f"Expected 0 cross-tenant leaks, found {metrics['cross_tenant_leaks']}"
    assert metrics["isolation_percentage"] == 100.0, f"Isolation percentage {metrics['isolation_percentage']}% below 100.0%"
    assert metrics["total_tenant_queries"] == 1000
