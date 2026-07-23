import asyncio
import os
import pytest
from sqlalchemy import text
from sqlalchemy.exc import TimeoutError as SATimeoutError

from app.core.db import (
    check_db_health,
    close_db_connection_pool,
    get_db_session,
    init_db_pool,
)


@pytest.mark.asyncio
async def test_db_pool_init_and_session_creation():
    """Test DB pool initialization and session creation."""
    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    assert engine is not None

    async with get_db_session() as session:
        result = await session.execute(text("SELECT 1"))
        val = result.scalar()
        assert val == 1

    await close_db_connection_pool()


@pytest.mark.asyncio
async def test_concurrent_session_acquisition_and_pool_exhaustion():
    """Test concurrent session acquisition and pool exhaustion timeout behavior."""
    test_db_file = "test_pool_exhaustion.db"

    # Remove stale DB file if present
    if os.path.exists(test_db_file):
        os.remove(test_db_file)

    try:
        # Initialize pool with max capacity = 1 connection and 0.2s timeout
        engine = init_db_pool(
            database_url=f"sqlite+aiosqlite:///{test_db_file}",
            pool_size=1,
            max_overflow=0,
            pool_timeout=0.2,
        )

        conn1 = await engine.connect()

        async def acquire_second():
            conn2 = await engine.connect()
            await conn2.close()

        # Attempt to acquire 2nd connection while max pool size = 1 is fully checked out
        with pytest.raises((SATimeoutError, asyncio.TimeoutError, Exception)) as exc_info:
            await asyncio.wait_for(acquire_second(), timeout=1.0)

        assert "QueuePool limit" in str(exc_info.value) or "timed out" in str(exc_info.value).lower() or isinstance(exc_info.value, SATimeoutError)

        await conn1.close()
    finally:
        await close_db_connection_pool()
        if os.path.exists(test_db_file):
            os.remove(test_db_file)


@pytest.mark.asyncio
async def test_check_db_health_metrics():
    """Test check_db_health() returns status, ping latency, and pool stats."""
    init_db_pool("sqlite+aiosqlite:///:memory:")

    health = await check_db_health()
    assert health["status"] == "healthy"
    assert isinstance(health["ping_ms"], float)
    assert health["ping_ms"] >= 0.0
    assert "pool" in health
    assert isinstance(health["pool"], dict)

    await close_db_connection_pool()


@pytest.mark.asyncio
async def test_close_db_connection_pool_graceful_disposal():
    """Test close_db_connection_pool() gracefully disposes pool."""
    init_db_pool("sqlite+aiosqlite:///:memory:")

    health_before = await check_db_health()
    assert health_before["status"] == "healthy"

    await close_db_connection_pool()

    health_after = await check_db_health()
    assert health_after["status"] == "uninitialized"
    assert health_after["ping_ms"] is None
    assert health_after["pool"] is None
