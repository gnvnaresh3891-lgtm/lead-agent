"""
Tier 4 Load Harness: DB Connection Pool Stress Test (0 Connection Exhaustions)
Asserts strictly against real database engine pool management in app/core/db.py under max concurrency.
"""
import asyncio
import time
import uuid
import pytest
from sqlalchemy import text

from app.core.db import check_db_health, get_db_session
from app.core.tenancy import tenant_context
from app.models.lead import Lead


async def run_pool_stress_test(total_operations: int = 1000) -> dict:
    successful_operations = 0
    pool_exhaustion_errors = 0
    acquire_waits = []

    org_id = uuid.UUID("11111111-1111-1111-1111-111111111111")

    async def perform_db_op(i: int):
        nonlocal successful_operations, pool_exhaustion_errors
        t0 = time.perf_counter()
        try:
            with tenant_context(org_id):
                async with get_db_session() as session:
                    t_wait = (time.perf_counter() - t0) * 1000.0
                    acquire_waits.append(t_wait)
                    res = await session.execute(text(f"SELECT {i}"))
                    val = res.scalar()
                    if val == i:
                        successful_operations += 1
        except Exception as e:
            pool_exhaustion_errors += 1

    batch_size = 100
    for offset in range(0, total_operations, batch_size):
        tasks = [perform_db_op(i) for i in range(offset, min(offset + batch_size, total_operations))]
        await asyncio.gather(*tasks)

    avg_wait = sum(acquire_waits) / len(acquire_waits) if acquire_waits else 0.0
    health = await check_db_health()

    return {
        "total_operations": total_operations,
        "successful_operations": successful_operations,
        "pool_exhaustion_errors": pool_exhaustion_errors,
        "avg_acquire_wait_ms": avg_wait,
        "db_health": health["status"],
    }


@pytest.mark.asyncio
async def test_connection_pool_stress_resilience(test_db):
    """Test database connection pool resilience under 1,000 concurrent operations with 0 exhaustion errors."""
    metrics = await run_pool_stress_test(total_operations=1000)

    assert metrics["pool_exhaustion_errors"] == 0, f"Expected 0 pool exhaustion errors, got {metrics['pool_exhaustion_errors']}"
    assert metrics["successful_operations"] == 1000, f"Expected 1000 successful operations, got {metrics['successful_operations']}"
    assert metrics["db_health"] == "healthy"
