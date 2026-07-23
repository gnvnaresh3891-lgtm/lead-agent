from contextlib import asynccontextmanager
import time
from typing import AsyncGenerator, Optional

from sqlalchemy import event, inspect, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, with_loader_criteria
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.tenancy import (
    TenantContextError,
    TenantCrossIsolationError,
    get_current_tenant_id,
    is_tenant_isolation_bypassed,
)
from app.models.base import TenantMixin

async_engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


@event.listens_for(Session, "do_orm_execute")
def _do_orm_execute(execute_state):
    """SQLAlchemy ORM event listener enforcing tenant criteria on SELECT statements."""
    if execute_state.is_select and not is_tenant_isolation_bypassed():
        current_tenant = get_current_tenant_id()
        if current_tenant is not None:
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    TenantMixin,
                    lambda cls: cls.org_id == current_tenant,
                    include_aliases=True,
                )
            )
        else:
            all_models = execute_state.all_models
            if all_models and any(
                isinstance(m, type) and issubclass(m, TenantMixin) for m in all_models
            ):
                raise TenantContextError(
                    "Tenant context is required to query multi-tenant models when tenant isolation is active."
                )


@event.listens_for(Session, "before_flush")
def _before_flush(session: Session, flush_context, instances):
    """SQLAlchemy ORM event listener enforcing tenant validation on flush."""
    if is_tenant_isolation_bypassed():
        return

    current_tenant = get_current_tenant_id()

    # Check newly created objects
    for obj in session.new:
        if isinstance(obj, TenantMixin):
            if current_tenant is not None:
                if obj.org_id is None:
                    obj.org_id = current_tenant
                elif obj.org_id != current_tenant:
                    raise TenantCrossIsolationError(
                        f"Cannot insert instance with org_id '{obj.org_id}' under active tenant context '{current_tenant}'."
                    )
            else:
                if obj.org_id is None:
                    raise TenantContextError(
                        "Tenant context is required to insert multi-tenant models."
                    )

    # Check dirty (modified) objects
    for obj in session.dirty:
        if isinstance(obj, TenantMixin):
            state = inspect(obj)
            history = state.get_history("org_id", True)
            if history.has_changes():
                raise TenantCrossIsolationError(
                    "Changing org_id of an existing multi-tenant object is strictly forbidden."
                )
            if current_tenant is not None and obj.org_id != current_tenant:
                raise TenantCrossIsolationError(
                    f"Cannot update instance belonging to tenant '{obj.org_id}' under active tenant context '{current_tenant}'."
                )
            if current_tenant is None:
                raise TenantContextError(
                    "Tenant context is required to update multi-tenant models."
                )

    # Check deleted objects
    for obj in session.deleted:
        if isinstance(obj, TenantMixin):
            if current_tenant is not None and obj.org_id != current_tenant:
                raise TenantCrossIsolationError(
                    f"Cannot delete instance belonging to tenant '{obj.org_id}' under active tenant context '{current_tenant}'."
                )
            if current_tenant is None:
                raise TenantContextError(
                    "Tenant context is required to delete multi-tenant models."
                )


def init_db_pool(
    database_url: Optional[str] = None,
    pool_size: Optional[int] = None,
    max_overflow: Optional[int] = None,
    pool_timeout: Optional[float] = None,
) -> AsyncEngine:
    """Initialize database connection engine pool and sessionmaker."""
    global async_engine, AsyncSessionLocal

    url = database_url or settings.DATABASE_URL
    p_size = pool_size if pool_size is not None else settings.DB_POOL_SIZE
    p_overflow = max_overflow if max_overflow is not None else settings.DB_MAX_OVERFLOW
    p_timeout = pool_timeout if pool_timeout is not None else settings.DB_POOL_TIMEOUT

    engine_kwargs = {}
    if "sqlite" in url:
        if ":memory:" in url:
            engine_kwargs.update(
                {
                    "poolclass": StaticPool,
                    "connect_args": {"check_same_thread": False},
                }
            )
    else:
        engine_kwargs.update(
            {
                "pool_size": p_size,
                "max_overflow": p_overflow,
                "pool_timeout": p_timeout,
                "pool_recycle": settings.DB_POOL_RECYCLE,
                "pool_pre_ping": settings.DB_POOL_PRE_PING,
            }
        )

    async_engine = create_async_engine(url, **engine_kwargs)
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=True,
    )
    return async_engine


async def close_db_connection_pool() -> None:
    """Gracefully close and dispose the database engine connection pool."""
    global async_engine, AsyncSessionLocal
    if async_engine is not None:
        await async_engine.dispose()
        async_engine = None
        AsyncSessionLocal = None


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Async context manager / dependency for yielding DB sessions."""
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        init_db_pool()
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def check_db_health() -> dict:
    """Check database health, ping latency, and connection pool statistics."""
    if async_engine is None:
        return {"status": "uninitialized", "ping_ms": None, "pool": None}

    start_time = time.perf_counter()
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        ping_ms = (time.perf_counter() - start_time) * 1000.0
        status = "healthy"
    except Exception as e:
        ping_ms = None
        status = f"unhealthy: {str(e)}"

    pool = async_engine.pool
    pool_stats = {
        "size": getattr(pool, "size", lambda: None)(),
        "checkedin": getattr(pool, "checkedin", lambda: None)(),
        "checkedout": getattr(pool, "checkedout", lambda: None)(),
        "overflow": getattr(pool, "overflow", lambda: None)(),
    }
    return {
        "status": status,
        "ping_ms": round(ping_ms, 2) if ping_ms is not None else None,
        "pool": pool_stats,
    }
