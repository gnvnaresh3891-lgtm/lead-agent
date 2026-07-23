"""
Shared Pytest Fixtures for backend_rebuild E2E Test Suite.
Uses ZERO synthetic mocks and connects directly to real application code in app/.
"""
import uuid
from typing import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import (
    AsyncSessionLocal,
    async_engine,
    close_db_connection_pool,
    get_db_session,
    init_db_pool,
)
from app.core.redis_client import RedisClient, redis_client as global_redis_client
from app.main import app
from app.models.base import Base
from app.models.organization import Organization


@pytest_asyncio.fixture(autouse=True)
async def test_db():
    """Real async SQLAlchemy database engine fixture initializing sqlite+aiosqlite:///:memory: and creating ORM metadata."""
    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await close_db_connection_pool()


@pytest_asyncio.fixture
async def db_session(test_db) -> AsyncGenerator[AsyncSession, None]:
    """Yield a real async SQLAlchemy session from the test database pool."""
    async with get_db_session() as session:
        yield session


@pytest.fixture
def test_org_id() -> uuid.UUID:
    """Default test organization UUID."""
    return uuid.UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def test_headers(test_org_id: uuid.UUID) -> dict:
    """Default HTTP headers containing X-Org-Id."""
    return {"X-Org-Id": str(test_org_id)}


@pytest.fixture
def org1_id() -> uuid.UUID:
    """Primary test organization UUID for multi-tenant isolation tests."""
    return uuid.UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def org2_id() -> uuid.UUID:
    """Secondary test organization UUID for multi-tenant isolation tests."""
    return uuid.UUID("22222222-2222-2222-2222-222222222222")


@pytest_asyncio.fixture
async def setup_orgs(test_db, org1_id, org2_id):
    """Seed Organization records into DB for FK constraint compliance."""
    async with get_db_session() as session:
        org1 = Organization(id=org1_id, name="Organization Alpha")
        org2 = Organization(id=org2_id, name="Organization Beta")
        session.add_all([org1, org2])
        await session.commit()


@pytest_asyncio.fixture
async def redis_client() -> AsyncGenerator[RedisClient, None]:
    """Real RedisClient instance (using in-memory fallback queue if Redis server daemon is absent)."""
    client = global_redis_client
    await client.connect()
    await client.clear()
    yield client
    await client.clear()


@pytest_asyncio.fixture
async def async_client(test_db, redis_client) -> AsyncGenerator[httpx.AsyncClient, None]:
    """httpx.AsyncClient bound to real FastAPI app app.main:app."""
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    except AttributeError:
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            yield client
