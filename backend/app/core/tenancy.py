import contextvars
from contextlib import contextmanager
from typing import Generator, Optional, Union
from uuid import UUID

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

tenant_id_ctx: contextvars.ContextVar[Optional[UUID]] = contextvars.ContextVar(
    "tenant_id_ctx", default=None
)
bypass_isolation_ctx: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "bypass_isolation_ctx", default=False
)


class TenantContextError(Exception):
    """Raised when tenant context is required but missing or invalid."""

    pass


class TenantCrossIsolationError(Exception):
    """Raised when cross-tenant data access or mutation is attempted."""

    pass


def set_tenant_id(org_id: Optional[Union[UUID, str]]) -> contextvars.Token:
    """Set current tenant ID in context variable."""
    if org_id is None:
        return tenant_id_ctx.set(None)

    if isinstance(org_id, str):
        try:
            org_id = UUID(org_id)
        except ValueError as e:
            raise TenantContextError(
                f"Invalid UUID format for tenant_id: '{org_id}'"
            ) from e
    elif not isinstance(org_id, UUID):
        raise TenantContextError(f"tenant_id must be UUID or valid str UUID, got: {type(org_id)}")

    return tenant_id_ctx.set(org_id)


def get_current_tenant_id() -> Optional[UUID]:
    """Retrieve the current tenant ID from context."""
    return tenant_id_ctx.get()


def is_tenant_isolation_bypassed() -> bool:
    """Return whether tenant isolation filtering is bypassed."""
    return bypass_isolation_ctx.get()


@contextmanager
def tenant_context(org_id: Optional[Union[UUID, str]]) -> Generator[None, None, None]:
    """Context manager to scope execution to a specific tenant ID."""
    token = set_tenant_id(org_id)
    try:
        yield
    finally:
        tenant_id_ctx.reset(token)


@contextmanager
def bypass_tenant_isolation() -> Generator[None, None, None]:
    """Context manager to temporarily bypass tenant isolation filtering."""
    token = bypass_isolation_ctx.set(True)
    try:
        yield
    finally:
        bypass_isolation_ctx.reset(token)


class TenantContextMiddleware(BaseHTTPMiddleware):
    """FastAPI/Starlette middleware that sets tenant context from HTTP headers."""

    async def dispatch(self, request: Request, call_next) -> Response:
        org_header = request.headers.get("X-Org-Id") or request.headers.get("X-Tenant-Id")
        token = None
        if org_header:
            try:
                org_uuid = UUID(org_header)
                token = tenant_id_ctx.set(org_uuid)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": f"Invalid Tenant/Org ID format in header: '{org_header}'"},
                )
        try:
            response = await call_next(request)
            return response
        finally:
            if token is not None:
                tenant_id_ctx.reset(token)
