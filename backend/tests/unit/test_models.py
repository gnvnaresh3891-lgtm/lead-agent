import uuid
import pytest
from app.models.base import GUID
from app.models.organization import Organization
from app.models.signal import Signal
from app.models.lead import Lead
from app.models.task_log import TaskLog
from app.core.tenancy import tenant_context


def test_organization_instantiation():
    """Test Organization ORM model instantiation and attributes."""
    org_id = uuid.uuid4()
    org = Organization(id=org_id, name="Acme Corp")
    assert org.id == org_id
    assert org.name == "Acme Corp"
    assert "<Organization" in repr(org)


def test_signal_instantiation(org1_id):
    """Test Signal ORM model instantiation under tenant context."""
    with tenant_context(org1_id):
        lead_id = uuid.uuid4()
        sig = Signal(lead_id=lead_id, signal_type="click", score=2.5)
        assert sig.org_id == org1_id
        assert sig.lead_id == lead_id
        assert sig.signal_type == "click"
        assert sig.score == 2.5
        assert "<Signal" in repr(sig)


def test_lead_instantiation(org1_id):
    """Test Lead ORM model instantiation under tenant context."""
    with tenant_context(org1_id):
        lead = Lead(name="John Doe", email="john@example.com")
        assert lead.org_id == org1_id
        assert lead.name == "John Doe"
        assert lead.email == "john@example.com"
        assert "<Lead" in repr(lead)


def test_task_log_instantiation(org1_id):
    """Test TaskLog ORM model instantiation under tenant context."""
    with tenant_context(org1_id):
        tlog = TaskLog(task_name="process_signal", status="PROCESSED", execution_time=15.2)
        assert tlog.org_id == org1_id
        assert tlog.task_name == "process_signal"
        assert tlog.status == "PROCESSED"
        assert tlog.execution_time == 15.2
        assert "<TaskLog" in repr(tlog)


def test_guid_type_decorator():
    """Test GUID TypeDecorator conversions."""
    guid_decorator = GUID()

    # None handling
    assert guid_decorator.process_bind_param(None, None) is None
    assert guid_decorator.process_result_value(None, None) is None

    # UUID handling
    u = uuid.uuid4()
    # Mock dialect for non-postgresql
    class DummyDialect:
        name = "sqlite"
        def type_descriptor(self, impl):
            return impl

    bind_val = guid_decorator.process_bind_param(u, DummyDialect())
    assert bind_val == str(u)

    res_val = guid_decorator.process_result_value(str(u), DummyDialect())
    assert res_val == u
