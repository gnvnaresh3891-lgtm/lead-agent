"""
Tier 2 Boundary Tests: Connection Pool Boundary Cases & Failovers
Asserts strictly against real database pool management in app/core/db.py.
"""
import pytest
from sqlalchemy import text

from app.core.db import (
    check_db_health,
    close_db_connection_pool,
    get_db_session,
    init_db_pool,
)


@pytest.mark.asyncio
async def test_uninitialized_db_health():
    """check_db_health returns status 'uninitialized' when engine is closed."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    await close_db_connection_pool()

    health = await check_db_health()
    assert health["status"] == "uninitialized"
    assert health["ping_ms"] is None
    assert health["pool"] is None


@pytest.mark.asyncio
async def test_close_db_connection_pool_idempotent():
    """close_db_connection_pool is idempotent and can be called multiple times."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    await close_db_connection_pool()
    await close_db_connection_pool()

    health = await check_db_health()
    assert health["status"] == "uninitialized"


@pytest.mark.asyncio
async def test_db_session_exception_handling():
    """Exception inside get_db_session block rolls back and re-raises exception."""
    init_db_pool("sqlite+aiosqlite:///:memory:")

    with pytest.raises(ValueError) as exc_info:
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))
            raise ValueError("Session boundary exception")

    assert "Session boundary exception" in str(exc_info.value)


@pytest.mark.asyncio
async def test_db_pool_reinit_after_disposal():
    """Disposing pool and re-initializing restores healthy status."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    await close_db_connection_pool()

    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    assert engine is not None

    health = await check_db_health()
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_db_endpoint(async_client):
    """GET /api/v1/health/db returns 200 OK and healthy pool metrics."""
    response = await async_client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert isinstance(data["ping_ms"], float)
