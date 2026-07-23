"""
Tier 4 Load Harness: Background Worker Burst Test Harness (10,000 signals within 60s)
Asserts strictly against real RedisClient, SignalWorker, and database engine.
"""
import asyncio
import time
import uuid
import pytest

from app.core.redis_client import RedisClient, get_redis_client
from app.workers.signal_worker import SignalWorker


async def run_worker_burst_simulation(redis_client=None, total_signals: int = 10000) -> dict:
    if redis_client is None:
        redis_client = get_redis_client()
        await redis_client.connect()

    # 1. Enqueue total_signals across 50 tenant orgs
    batch_size = 500
    for offset in range(0, total_signals, batch_size):
        for i in range(offset, min(offset + batch_size, total_signals)):
            org_id = f"00000000-0000-0000-0000-{i % 50 + 1:012d}"
            sig_id = str(uuid.uuid4())
            await redis_client.push_signal("signals_queue", {
                "signal_id": sig_id,
                "org_id": org_id,
                "signal_type": "burst_test",
                "score": float(i),
                "payload": {"signal_idx": i, "type": "burst_test"},
            })

    initial_q_len = await redis_client.get_queue_len("signals_queue")
    assert initial_q_len == total_signals

    start_time = time.perf_counter()

    async def worker_loop():
        worker = SignalWorker(redis_client=redis_client)
        local_count = 0
        while True:
            res = await worker.process_next_signal(timeout=0.01)
            if not res:
                break
            if res.get("status") == "PROCESSED":
                local_count += 1
        return local_count

    # Spawn 10 concurrent worker tasks
    tasks = [worker_loop() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    total_processed = sum(results)

    elapsed = time.perf_counter() - start_time
    processed_per_sec = total_processed / elapsed if elapsed > 0 else 0.0
    dlq_count = await redis_client.get_queue_len("dlq:signals")

    return {
        "total_enqueued": total_signals,
        "total_processed": total_processed,
        "elapsed_seconds": elapsed,
        "processed_per_sec": processed_per_sec,
        "dlq_count": dlq_count,
    }


@pytest.mark.asyncio
async def test_worker_burst_processing(redis_client, setup_orgs):
    """Test worker burst processing of 10,000 signals completes within 60 seconds with 0 DLQ items."""
    metrics = await run_worker_burst_simulation(redis_client, total_signals=10000)

    assert metrics["total_processed"] == 10000, f"Expected 10000 processed, got {metrics['total_processed']}"
    assert metrics["elapsed_seconds"] < 60.0, f"Duration {metrics['elapsed_seconds']:.2f}s exceeded SLA threshold of 60.0s"
    assert metrics["dlq_count"] == 0, f"Expected 0 DLQ items, got {metrics['dlq_count']}"
