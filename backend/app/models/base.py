import uuid
from typing import Optional
from sqlalchemy import CHAR, ForeignKey, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.tenancy import (
    TenantCrossIsolationError,
    get_current_tenant_id,
    is_tenant_isolation_bypassed,
)


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36).
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(str(value)))
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(str(value))
        return value


class Base(DeclarativeBase):
    pass


class TenantMixin:
    """Mixin for multi-tenant models requiring mandatory org_id."""

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    def __init__(self, **kw):
        current_tenant = get_current_tenant_id()
        if "org_id" in kw and kw["org_id"] is not None:
            provided_org = kw["org_id"]
            if isinstance(provided_org, str):
                provided_org = uuid.UUID(provided_org)
            if (
                current_tenant is not None
                and not is_tenant_isolation_bypassed()
                and provided_org != current_tenant
            ):
                raise TenantCrossIsolationError(
                    f"Cannot instantiate model with org_id '{provided_org}' when active tenant context is '{current_tenant}'"
                )
        elif current_tenant is not None:
            kw["org_id"] = current_tenant

        super().__init__(**kw)
