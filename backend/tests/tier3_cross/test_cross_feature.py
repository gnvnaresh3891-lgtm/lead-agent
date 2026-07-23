"""
Tier 3 Cross-Feature Interaction Tests
Asserts end-to-end cross-component behavior across API, Redis Queue, SignalWorker, and Database.
"""
import uuid
import pytest
from app.workers.signal_worker import SignalWorker


@pytest.mark.asyncio
async def test_cross_ingestion_api_to_redis_queue(async_client, test_headers, redis_client, setup_orgs):
    """Test API ingestion pushes validated message payload to Redis queue."""
    payload = {"signal_type": "checkout", "score": 99.0}
    trace_id = "trace_cross_001"
    headers = {**test_headers, "X-Trace-Id": trace_id}

    # 1. Ingest via FastAPI
    response = await async_client.post("/api/v1/signals/ingest", headers=headers, json=payload)
    assert response.status_code == 200

    # 2. Verify popped queue message matches
    msg = await redis_client.pop_signal("signals_queue")
    assert msg is not None
    assert msg["org_id"] == test_headers["X-Org-Id"]
    assert msg["trace_id"] == trace_id
    assert msg["signal_type"] == "checkout"


@pytest.mark.asyncio
async def test_cross_multitenant_ingestion_and_worker_isolation(
    async_client, redis_client, setup_orgs, org1_id, org2_id
):
    """Test Org A vs Org B concurrent ingestion, worker processing, and tenant-isolated GET /api/v1/signals."""
    headers_org1 = {"X-Org-Id": str(org1_id)}
    headers_org2 = {"X-Org-Id": str(org2_id)}

    # 1. Ingest 5 signals for Org 1 and 5 signals for Org 2
    for i in range(5):
        res1 = await async_client.post(
            "/api/v1/signals/ingest",
            headers=headers_org1,
            json={"signal_type": "org1_event", "score": float(i)},
        )
        assert res1.status_code == 200

        res2 = await async_client.post(
            "/api/v1/signals/ingest",
            headers=headers_org2,
            json={"signal_type": "org2_event", "score": float(i)},
        )
        assert res2.status_code == 200

    # 2. Worker pops and processes all 10 queued signals
    worker = SignalWorker(redis_client=redis_client)
    processed_count = await worker.run(max_signals=10)
    assert processed_count == 10

    # 3. Query GET /api/v1/signals for Org 1 -> receives exactly 5 Org 1 signals
    resp1 = await async_client.get("/api/v1/signals", headers=headers_org1)
    assert resp1.status_code == 200
    signals1 = resp1.json()
    assert len(signals1) == 5
    assert all(s["org_id"] == str(org1_id) for s in signals1)
    assert all(s["signal_type"] == "org1_event" for s in signals1)

    # 4. Query GET /api/v1/signals for Org 2 -> receives exactly 5 Org 2 signals
    resp2 = await async_client.get("/api/v1/signals", headers=headers_org2)
    assert resp2.status_code == 200
    signals2 = resp2.json()
    assert len(signals2) == 5
    assert all(s["org_id"] == str(org2_id) for s in signals2)
    assert all(s["signal_type"] == "org2_event" for s in signals2)


@pytest.mark.asyncio
async def test_cross_connection_pool_worker_burst(redis_client, setup_orgs, org1_id):
    """Test enqueuing and worker processing across DB connection pool."""
    total = 50
    for i in range(total):
        await redis_client.push_signal("signals_queue", {
            "signal_id": str(uuid.uuid4()),
            "org_id": str(org1_id),
            "signal_type": "burst_item",
            "score": float(i),
        })

    worker = SignalWorker(redis_client=redis_client)
    processed = await worker.run(max_signals=total)
    assert processed == total
    assert await redis_client.get_queue_len("signals_queue") == 0


@pytest.mark.asyncio
async def test_cross_structured_logging_metrics(async_client, test_headers, setup_orgs):
    """Test health metrics endpoint aggregates ingestion request metrics."""
    res_ingest = await async_client.post(
        "/api/v1/signals/ingest",
        headers=test_headers,
        json={"signal_type": "metric_test", "score": 1.0},
    )
    assert res_ingest.status_code == 200

    res_metrics = await async_client.get("/api/v1/health/metrics")
    assert res_metrics.status_code == 200
    data = res_metrics.json()
    assert data["status"] == "healthy"
    assert "metrics" in data
    assert data["metrics"]["request_count"] >= 1
