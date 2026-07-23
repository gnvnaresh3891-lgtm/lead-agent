"""
Tier 1 Feature Tests: DB Connection Pool Settings & Resilience
Asserts strictly against real database engine pool methods in app/core/db.py.
"""
import asyncio
import pytest
from sqlalchemy import text

from app.core.db import (
    check_db_health,
    close_db_connection_pool,
    get_db_session,
    init_db_pool,
)


@pytest.mark.asyncio
async def test_pool_init_and_session_creation():
    """Test engine initialization and session creation from pool."""
    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    assert engine is not None

    async with get_db_session() as session:
        res = await session.execute(text("SELECT 1"))
        assert res.scalar() == 1


@pytest.mark.asyncio
async def test_concurrent_session_acquisition():
    """Test acquiring multiple DB sessions concurrently."""
    init_db_pool("sqlite+aiosqlite:///:memory:")

    async def execute_query(i: int):
        async with get_db_session() as session:
            res = await session.execute(text(f"SELECT {i}"))
            return res.scalar()

    tasks = [execute_query(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    assert results == list(range(10))


@pytest.mark.asyncio
async def test_db_health_check_metrics():
    """Test check_db_health returns healthy status and pool stats."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    health = await check_db_health()

    assert health["status"] == "healthy"
    assert health["ping_ms"] is not None and health["ping_ms"] >= 0.0
    assert "pool" in health


@pytest.mark.asyncio
async def test_db_pool_close_and_reinit():
    """Test closing DB pool and re-initializing."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    await close_db_connection_pool()

    uninit_health = await check_db_health()
    assert uninit_health["status"] == "uninitialized"

    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    assert engine is not None
    healthy = await check_db_health()
    assert healthy["status"] == "healthy"


@pytest.mark.asyncio
async def test_db_session_commit_and_query():
    """Test creating table and querying via get_db_session."""
    init_db_pool("sqlite+aiosqlite:///:memory:")
    async with get_db_session() as session:
        await session.execute(text("CREATE TABLE pool_test (id INT PRIMARY KEY, val TEXT)"))
        await session.execute(text("INSERT INTO pool_test VALUES (1, 'pool_val')"))

    async with get_db_session() as session:
        res = await session.execute(text("SELECT val FROM pool_test WHERE id = 1"))
        assert res.scalar() == "pool_val"
