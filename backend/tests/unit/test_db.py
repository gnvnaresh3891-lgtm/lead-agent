import pytest
from sqlalchemy import text
from app.core.db import (
    init_db_pool,
    close_db_connection_pool,
    get_db_session,
    check_db_health,
)


@pytest.mark.asyncio
async def test_init_db_pool_and_session():
    """Test initialization of DB engine pool and query execution using session."""
    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    assert engine is not None

    async with get_db_session() as session:
        res = await session.execute(text("SELECT 42"))
        val = res.scalar()
        assert val == 42


@pytest.mark.asyncio
async def test_check_db_health():
    """Test check_db_health functionality."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    health = await check_db_health()
    assert health["status"] == "healthy"
    assert isinstance(health["ping_ms"], float)
    assert health["ping_ms"] >= 0.0
    assert "pool" in health


@pytest.mark.asyncio
async def test_close_db_connection_pool():
    """Test graceful closing of DB engine pool."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    await close_db_connection_pool()

    health = await check_db_health()
    assert health["status"] == "uninitialized"
    assert health["ping_ms"] is None


@pytest.mark.asyncio
async def test_db_session_rollback_on_exception():
    """Test automatic rollback when exception is raised inside get_db_session."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    with pytest.raises(RuntimeError):
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))
            raise RuntimeError("Database transaction test failure")
