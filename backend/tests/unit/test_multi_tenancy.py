import uuid
import pytest
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import Response

from app.core.tenancy import (
    TenantContextError,
    TenantContextMiddleware,
    TenantCrossIsolationError,
    bypass_tenant_isolation,
    get_current_tenant_id,
    tenant_context,
)
from app.models.lead import Lead
from app.models.signal import Signal
from app.models.task_log import TaskLog


@pytest.mark.asyncio
async def test_explicit_org_id_isolation(db_session, setup_orgs, org1_id, org2_id):
    """Test explicit org_id isolation: Org 1 sees only Org 1 data, Org 2 sees only Org 2 data."""
    # Insert data for Org 1
    with tenant_context(org1_id):
        lead1 = Lead(name="Org 1 Lead", email="org1@example.com")
        db_session.add(lead1)
        await db_session.commit()
        lead1_id = lead1.id

    # Insert data for Org 2
    with tenant_context(org2_id):
        lead2 = Lead(name="Org 2 Lead", email="org2@example.com")
        db_session.add(lead2)
        await db_session.commit()
        lead2_id = lead2.id

    # Verify query under Org 1 context
    with tenant_context(org1_id):
        result = await db_session.execute(select(Lead))
        leads = result.scalars().all()
        assert len(leads) == 1
        assert leads[0].id == lead1_id
        assert leads[0].org_id == org1_id

    # Verify query under Org 2 context
    with tenant_context(org2_id):
        result = await db_session.execute(select(Lead))
        leads = result.scalars().all()
        assert len(leads) == 1
        assert leads[0].id == lead2_id
        assert leads[0].org_id == org2_id

    # Verify query under bypass mode sees all
    with bypass_tenant_isolation():
        result = await db_session.execute(select(Lead))
        leads = result.scalars().all()
        assert len(leads) == 2


@pytest.mark.asyncio
async def test_missing_tenant_context_behavior(db_session, setup_orgs):
    """Test missing tenant context behavior (raises TenantContextError)."""
    assert get_current_tenant_id() is None

    # Querying multi-tenant model without tenant context raises error
    with pytest.raises(TenantContextError) as exc_info:
        await db_session.execute(select(Lead))
    assert "Tenant context is required" in str(exc_info.value)

    # Creating model without tenant context and without explicit org_id raises error on flush
    l = Lead(name="No Context Lead", email="nocontext@example.com")
    db_session.add(l)
    with pytest.raises(TenantContextError) as exc_info:
        await db_session.flush()
    assert "Tenant context is required" in str(exc_info.value)
    await db_session.rollback()


@pytest.mark.asyncio
async def test_automatic_org_id_assignment(db_session, setup_orgs, org1_id):
    """Test automatic org_id assignment on model instantiation when context is active."""
    with tenant_context(org1_id):
        lead = Lead(name="Auto Org Lead", email="auto@example.com")
        assert lead.org_id == org1_id

        signal = Signal(lead_id=uuid.uuid4(), signal_type="page_view", score=10.0)
        assert signal.org_id == org1_id

        task_log = TaskLog(task_name="enrichment", status="completed", execution_time=1.2)
        assert task_log.org_id == org1_id

        db_session.add_all([lead, task_log])
        await db_session.commit()

        # Query back to ensure org_id persisted correctly
        result = await db_session.execute(select(Lead).where(Lead.id == lead.id))
        fetched_lead = result.scalar_one()
        assert fetched_lead.org_id == org1_id


@pytest.mark.asyncio
async def test_cross_tenant_instantiation_prevention(org1_id, org2_id):
    """Test prevention of cross-tenant org_id instantiation when tenant context is active."""
    with tenant_context(org1_id):
        with pytest.raises(TenantCrossIsolationError) as exc_info:
            Lead(org_id=org2_id, name="Cross Lead", email="cross@example.com")
        assert "Cannot instantiate model" in str(exc_info.value)


@pytest.mark.asyncio
async def test_cross_tenant_mutation_prevention(db_session, setup_orgs, org1_id, org2_id):
    """Test cross-tenant model insertion/update/deletion prevention."""
    # Create Lead 1 under Org 1
    with tenant_context(org1_id):
        lead1 = Lead(name="Org 1 Lead", email="org1@example.com")
        db_session.add(lead1)
        await db_session.commit()
        lead1_id = lead1.id

    # Attempt cross-tenant update under Org 2 context
    with tenant_context(org2_id):
        with bypass_tenant_isolation():
            res = await db_session.execute(select(Lead).where(Lead.id == lead1_id))
            target_lead = res.scalar_one()

        # Now active context is Org 2, modifying target_lead (belongs to Org 1)
        target_lead.name = "Hacked Name"
        with pytest.raises(TenantCrossIsolationError) as exc_info:
            await db_session.flush()
        assert "Cannot update instance belonging to tenant" in str(exc_info.value)
        await db_session.rollback()

    # Attempt org_id modification
    with tenant_context(org1_id):
        res = await db_session.execute(select(Lead).where(Lead.id == lead1_id))
        target_lead = res.scalar_one()
        target_lead.org_id = org2_id
        with pytest.raises(TenantCrossIsolationError) as exc_info:
            await db_session.flush()
        assert "Changing org_id" in str(exc_info.value)
        await db_session.rollback()

    # Attempt cross-tenant deletion under Org 2 context
    with tenant_context(org2_id):
        with bypass_tenant_isolation():
            res = await db_session.execute(select(Lead).where(Lead.id == lead1_id))
            target_lead = res.scalar_one()

        await db_session.delete(target_lead)
        with pytest.raises(TenantCrossIsolationError) as exc_info:
            await db_session.flush()
        assert "Cannot delete instance belonging to tenant" in str(exc_info.value)
        await db_session.rollback()


@pytest.mark.asyncio
async def test_tenant_context_middleware(org1_id):
    """Test TenantContextMiddleware sets and resets context variable from headers."""
    middleware = TenantContextMiddleware(app=None)
    header_val = str(org1_id)

    async def dummy_call_next(request: Request) -> Response:
        assert get_current_tenant_id() == org1_id
        return Response("OK")

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"x-org-id", header_val.encode())],
    }
    request = Request(scope)
    response = await middleware.dispatch(request, dummy_call_next)
    assert response.status_code == 200
    # After dispatch completes, context should be reset
    assert get_current_tenant_id() is None
