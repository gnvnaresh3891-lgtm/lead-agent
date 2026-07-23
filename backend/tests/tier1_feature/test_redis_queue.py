"""
Tier 1 Feature Tests: Redis Queue Dispatch & Worker
Asserts strictly against real RedisClient and SignalWorker implementation.
"""
import uuid
import pytest
from app.workers.signal_worker import SignalWorker


@pytest.mark.asyncio
async def test_queue_push_pop_fifo(redis_client):
    """Test pushing and popping signals in FIFO order."""
    signal_a = {"signal_id": "sig_a", "signal_type": "event_a"}
    signal_b = {"signal_id": "sig_b", "signal_type": "event_b"}

    await redis_client.push_signal("signals_queue", signal_a)
    await redis_client.push_signal("signals_queue", signal_b)

    first = await redis_client.pop_signal("signals_queue")
    second = await redis_client.pop_signal("signals_queue")

    assert first["signal_id"] == "sig_a"
    assert second["signal_id"] == "sig_b"


@pytest.mark.asyncio
async def test_queue_len_tracking(redis_client):
    """Test queue length reporting."""
    queue_name = "signals_queue"
    for i in range(10):
        await redis_client.push_signal(queue_name, {"idx": i})

    q_len = await redis_client.get_queue_len(queue_name)
    assert q_len == 10

    for _ in range(3):
        await redis_client.pop_signal(queue_name)

    assert await redis_client.get_queue_len(queue_name) == 7


@pytest.mark.asyncio
async def test_worker_dispatch_consumption(redis_client, setup_orgs, org1_id):
    """Test SignalWorker popping and persisting signal from queue into DB."""
    sig_id = str(uuid.uuid4())
    payload = {
        "signal_id": sig_id,
        "org_id": str(org1_id),
        "signal_type": "user_signup",
        "score": 5.0,
    }
    await redis_client.push_signal("signals_queue", payload)

    worker = SignalWorker(redis_client=redis_client)
    res = await worker.process_next_signal()

    assert res is not None
    assert res["status"] == "PROCESSED"
    assert res["signal_id"] == sig_id
    assert await redis_client.get_queue_len("signals_queue") == 0


@pytest.mark.asyncio
async def test_queue_batch_dispatch(redis_client, setup_orgs, org1_id):
    """Test worker batch processing loop for 100 queued items."""
    for i in range(100):
        await redis_client.push_signal("signals_queue", {
            "signal_id": str(uuid.uuid4()),
            "org_id": str(org1_id),
            "signal_type": "batch_event",
            "score": float(i),
        })

    assert await redis_client.get_queue_len("signals_queue") == 100

    worker = SignalWorker(redis_client=redis_client)
    processed_count = await worker.run(max_signals=100)

    assert processed_count == 100
    assert await redis_client.get_queue_len("signals_queue") == 0


@pytest.mark.asyncio
async def test_queue_dlq_on_error(redis_client):
    """Test unprocessable payload is moved to Dead Letter Queue (DLQ)."""
    corrupt_payload = "{invalid_json_payload"
    await redis_client.push_signal("signals_queue", corrupt_payload)

    await redis_client.move_to_dlq("signals_queue", corrupt_payload, "JSONDecodeError")

    dlq_item = await redis_client.pop_signal("dlq:signals")
    assert dlq_item is not None
    assert dlq_item["payload"] == corrupt_payload
    assert dlq_item["error_reason"] == "JSONDecodeError"
