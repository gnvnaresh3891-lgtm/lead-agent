"""
Tier 2 Boundary Tests: Signal Ingestion Boundary Cases
Asserts strictly against real FastAPI application app.main:app endpoints.
"""
import uuid
import pytest


@pytest.mark.asyncio
async def test_missing_org_id_header(async_client):
    """Missing X-Org-Id header returns 401 Unauthorized."""
    payload = {"signal_type": "click"}
    response = await async_client.post("/api/v1/signals/ingest", json=payload)

    assert response.status_code == 401
    assert "Missing X-Org-Id header" in response.json()["detail"]


@pytest.mark.asyncio
async def test_invalid_org_id_header_format(async_client):
    """Invalid org ID format in header returns 400 Bad Request."""
    headers = {"X-Org-Id": "!!!INVALID_CHARACTERS!!!"}
    payload = {"signal_type": "click"}
    response = await async_client.post("/api/v1/signals/ingest", headers=headers, json=payload)

    assert response.status_code == 400
    assert "Invalid tenant/org ID format" in response.json()["detail"]


@pytest.mark.asyncio
async def test_malformed_json_payload(async_client, test_headers):
    """Malformed/non-object JSON payload returns 400 Bad Request."""
    response = await async_client.post(
        "/api/v1/signals/ingest",
        headers=test_headers,
        content="this_is_not_valid_json",
        headers_dict={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert "Malformed JSON payload" in response.json()["detail"]


@pytest.mark.asyncio
async def test_zero_empty_signals_list(async_client, test_headers):
    """Empty signals list returns 400 Bad Request."""
    payload = {"signals": []}
    response = await async_client.post("/api/v1/signals/ingest", headers=test_headers, json=payload)

    assert response.status_code == 400
    assert "signals array must contain at least 1 item" in response.json()["detail"]


@pytest.mark.asyncio
async def test_max_batch_size_boundary(async_client, test_headers):
    """Batch size 500 returns 200 OK; Batch size 501 returns 413 Payload Too Large."""
    # 500 items (Max allowed boundary)
    batch_500 = [{"signal_type": "click", "score": float(i)} for i in range(500)]
    resp_500 = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json={"signals": batch_500}
    )
    assert resp_500.status_code == 200
    assert resp_500.json()["ingested_count"] == 500

    # 501 items (Exceeds boundary)
    batch_501 = [{"signal_type": "click", "score": float(i)} for i in range(501)]
    resp_501 = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json={"signals": batch_501}
    )
    assert resp_501.status_code == 413
    assert "exceeds max batch size 500" in resp_501.json()["detail"]


@pytest.mark.asyncio
async def test_signal_not_found(async_client, test_headers):
    """GET /api/v1/signals/{non_existent_uuid} returns 404 Not Found."""
    random_uuid = str(uuid.uuid4())
    response = await async_client.get(f"/api/v1/signals/{random_uuid}", headers=test_headers)

    assert response.status_code == 404
    assert "Signal not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_edge_payload_special_chars(async_client, test_headers):
    """Special characters and unicode text in signal payload succeed."""
    special_payload = {
        "signal_type": "special_char_test",
        "score": 1.0,
        "payload": {
            "emoji": "🚀🔥💡🎉",
            "zero_width": "a\u200Bb\u200Cc",
            "large_text": "x" * 10000,
        },
    }
    response = await async_client.post(
        "/api/v1/signals/ingest", headers=test_headers, json=special_payload
    )
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
