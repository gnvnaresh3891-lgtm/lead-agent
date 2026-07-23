"""
Tier 1 Feature Tests: Signal Ingestion API Endpoint
Asserts strictly against real FastAPI application app.main:app.
"""
import pytest
from app.workers.signal_worker import SignalWorker


@pytest.mark.asyncio
async def test_valid_signal_ingestion_single(async_client, test_headers, setup_orgs):
    """Test single valid signal ingestion endpoint returns 200 and queued status."""
    payload = {
        "signal_type": "page_view",
        "score": 1.0,
        "timestamp": 1770000000,
    }
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=payload
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "queued"
    assert body["ingested_count"] == 1
    assert "request_id" in body and isinstance(body["request_id"], str)
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_valid_signal_ingestion_batch(async_client, test_headers, setup_orgs):
    """Test batch signal ingestion (50 items) returns 200 and ingested_count == 50."""
    batch_signals = [
        {"signal_type": "click", "score": float(i), "timestamp": 1770000000 + i}
        for i in range(50)
    ]
    payload = {"signals": batch_signals}
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=payload
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "queued"
    assert body["ingested_count"] == 50


@pytest.mark.asyncio
async def test_ingestion_response_schema(async_client, test_headers, setup_orgs):
    """Test response JSON schema for valid ingestion request."""
    payload = {"signal_type": "purchase", "score": 99.99}
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=payload
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("status"), str)
    assert isinstance(body.get("ingested_count"), int)
    assert isinstance(body.get("request_id"), str)
    assert isinstance(body.get("timestamp"), (int, float))


@pytest.mark.asyncio
async def test_ingestion_dispatches_to_redis_queue(async_client, test_headers, redis_client, setup_orgs):
    """Test signal ingestion pushes payload to real Redis queue."""
    payload = {"signal_type": "signup", "score": 5.0}

    initial_len = await redis_client.get_queue_len("signals_queue")
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=payload
    )
    assert response.status_code == 200

    new_len = await redis_client.get_queue_len("signals_queue")
    assert new_len == initial_len + 1

    popped = await redis_client.pop_signal("signals_queue")
    assert popped is not None
    assert popped["signal_type"] == "signup"


@pytest.mark.asyncio
async def test_ingest_and_query_signals(async_client, test_headers, redis_client, setup_orgs):
    """Test ingestion, worker processing, and querying GET /api/v1/signals."""
    payload = {"signal_type": "conversion", "score": 10.0}
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=payload
    )
    assert response.status_code == 200

    # Run worker to process queue item into DB
    worker = SignalWorker(redis_client=redis_client)
    processed = await worker.process_next_signal()
    assert processed is not None
    assert processed["status"] == "PROCESSED"

    # Query signals endpoint
    get_resp = await async_client.get("/api/v1/signals", headers=test_headers)
    assert get_resp.status_code == 200
    signals = get_resp.json()
    assert len(signals) == 1
    assert signals[0]["signal_type"] == "conversion"


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client):
    """Test GET /api/v1/health endpoint."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
