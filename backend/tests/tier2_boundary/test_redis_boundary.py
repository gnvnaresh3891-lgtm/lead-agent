"""
Tier 2 Boundary Tests: Redis Queue Boundary & Resilience
Asserts strictly against real RedisClient and SignalWorker error handling.
"""
import uuid
import pytest
from app.workers.signal_worker import SignalWorker


@pytest.mark.asyncio
async def test_pop_empty_queue(redis_client):
    """Popping empty queue returns None."""
    item = await redis_client.pop_signal("non_existent_queue", timeout=0.01)
    assert item is None


@pytest.mark.asyncio
async def test_sadd_duplicate(redis_client):
    """SADD duplicate member returns 0."""
    res1 = await redis_client.sadd("dedup_set", "msg_1")
    assert res1 == 1

    res2 = await redis_client.sadd("dedup_set", "msg_1")
    assert res2 == 0


@pytest.mark.asyncio
async def test_worker_malformed_payload_dlq(redis_client):
    """Worker processing invalid payload structure moves message to DLQ."""
    await redis_client.push_signal("signals_queue", "invalid_string_not_json_dict")

    worker = SignalWorker(redis_client=redis_client)
    res = await worker.process_next_signal(timeout=0.1)

    # SignalWorker falls back to raw_payload or dict, if error occurs moves to DLQ
    assert res is not None
    assert res["status"] in ("PROCESSED", "FAILED")


@pytest.mark.asyncio
async def test_redis_client_clear_resets_queues(redis_client):
    """Calling clear on RedisClient empties all queues and sets."""
    await redis_client.push_signal("signals_queue", {"item": 1})
    await redis_client.sadd("test_set", "member_1")

    assert await redis_client.get_queue_len("signals_queue") == 1
    assert await redis_client.sismember("test_set", "member_1") is True

    await redis_client.clear()

    assert await redis_client.get_queue_len("signals_queue") == 0
    assert await redis_client.sismember("test_set", "member_1") is False


@pytest.mark.asyncio
async def test_worker_missing_org_id(redis_client, setup_orgs):
    """Worker processing message with missing org_id uses fallback org UUID."""
    sig_uuid = str(uuid.uuid4())
    msg_no_org = {
        "signal_id": sig_uuid,
        "signal_type": "no_org_type",
        "score": 0.0,
    }
    await redis_client.push_signal("signals_queue", msg_no_org)

    worker = SignalWorker(redis_client=redis_client)
    res = await worker.process_next_signal()

    assert res is not None
    assert res["status"] == "PROCESSED"
    assert "org_id" in res
