"""
Tier 1 Feature Tests: Multi-Tenant DB Queries
Asserts strictly against real SQLAlchemy models and tenant filtering logic in app/core/db.py.
"""
import uuid
import pytest
from sqlalchemy import select

from app.core.tenancy import bypass_tenant_isolation, tenant_context
from app.models.lead import Lead
from app.models.signal import Signal


@pytest.mark.asyncio
async def test_tenant_scoped_select(db_session, setup_orgs, org1_id, org2_id):
    """Test tenant scoped SELECT returns only records matching active tenant_context."""
    lead_id1 = uuid.uuid4()
    lead_id2 = uuid.uuid4()

    with tenant_context(org1_id):
        sig1 = Signal(lead_id=lead_id1, signal_type="alpha_sig", score=1.0)
        db_session.add(sig1)
        await db_session.commit()

    with tenant_context(org2_id):
        sig2 = Signal(lead_id=lead_id2, signal_type="beta_sig", score=2.0)
        db_session.add(sig2)
        await db_session.commit()

    # Query under Org 1 context
    with tenant_context(org1_id):
        res = await db_session.execute(select(Signal))
        records = res.scalars().all()
        assert len(records) == 1
        assert records[0].org_id == org1_id
        assert records[0].signal_type == "alpha_sig"

    # Query under Org 2 context
    with tenant_context(org2_id):
        res = await db_session.execute(select(Signal))
        records = res.scalars().all()
        assert len(records) == 1
        assert records[0].org_id == org2_id
        assert records[0].signal_type == "beta_sig"


@pytest.mark.asyncio
async def test_tenant_scoped_insert(db_session, setup_orgs, org1_id):
    """Test automatic org_id population on model insertion."""
    with tenant_context(org1_id):
        lead = Lead(name="Test Lead", email="test@lead.local")
        db_session.add(lead)
        await db_session.commit()

        assert lead.id is not None
        assert lead.org_id == org1_id


@pytest.mark.asyncio
async def test_tenant_scoped_update(db_session, setup_orgs, org1_id):
    """Test updating model under matching active tenant_context."""
    with tenant_context(org1_id):
        lead = Lead(name="Original Name", email="orig@lead.local")
        db_session.add(lead)
        await db_session.commit()
        lead_id = lead.id

    with tenant_context(org1_id):
        res = await db_session.execute(select(Lead).where(Lead.id == lead_id))
        fetched = res.scalar_one()
        fetched.name = "Updated Name"
        await db_session.commit()

    with tenant_context(org1_id):
        res = await db_session.execute(select(Lead).where(Lead.id == lead_id))
        fetched = res.scalar_one()
        assert fetched.name == "Updated Name"


@pytest.mark.asyncio
async def test_tenant_scoped_delete(db_session, setup_orgs, org1_id, org2_id):
    """Test deleting model under matching active tenant_context."""
    with tenant_context(org1_id):
        lead1 = Lead(name="Lead 1", email="l1@lead.local")
        db_session.add(lead1)
        await db_session.commit()
        lead1_id = lead1.id

    with tenant_context(org2_id):
        lead2 = Lead(name="Lead 2", email="l2@lead.local")
        db_session.add(lead2)
        await db_session.commit()

    # Delete lead1 under Org 1 context
    with tenant_context(org1_id):
        res = await db_session.execute(select(Lead).where(Lead.id == lead1_id))
        l1 = res.scalar_one()
        await db_session.delete(l1)
        await db_session.commit()

        res_after = await db_session.execute(select(Lead))
        assert len(res_after.scalars().all()) == 0

    # Org 2 lead remains intact
    with tenant_context(org2_id):
        res_beta = await db_session.execute(select(Lead))
        assert len(res_beta.scalars().all()) == 1


@pytest.mark.asyncio
async def test_bypass_tenant_isolation(db_session, setup_orgs, org1_id, org2_id):
    """Test bypass_tenant_isolation context manager returns all tenant records."""
    with tenant_context(org1_id):
        l1 = Lead(name="Alpha Lead", email="a@lead.local")
        db_session.add(l1)
        await db_session.commit()

    with tenant_context(org2_id):
        l2 = Lead(name="Beta Lead", email="b@lead.local")
        db_session.add(l2)
        await db_session.commit()

    with bypass_tenant_isolation():
        res = await db_session.execute(select(Lead))
        all_leads = res.scalars().all()
        assert len(all_leads) == 2
