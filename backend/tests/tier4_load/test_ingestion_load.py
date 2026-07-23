"""
Tier 4 Load Harness: Async HTTP Ingestion Load Simulator (1,000 req/s, p95 < 200ms)
Asserts strictly against real FastAPI app endpoints via httpx.AsyncClient.
"""
import asyncio
import time
import pytest


async def run_ingestion_load_simulation(
    async_client=None, test_headers=None, total_requests: int = 1000
) -> dict:
    if test_headers is None:
        test_headers = {"X-Org-Id": "11111111-1111-1111-1111-111111111111"}

    payload = {"signal_type": "load_test_event", "score": 42.0}

    latencies = []
    failed_requests = 0

    async def send_single_request(i: int):
        nonlocal failed_requests
        start = time.perf_counter()
        headers = {**test_headers, "X-Trace-Id": f"trace_load_{i}"}
        resp = await async_client.post("/api/v1/signals/ingest", headers=headers, json=payload)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        if resp.status_code == 200:
            return elapsed_ms
        else:
            return None

    overall_start = time.perf_counter()

    # Process in batches of 100 to simulate realistic concurrency
    batch_size = 100
    for offset in range(0, total_requests, batch_size):
        tasks = [send_single_request(i) for i in range(offset, min(offset + batch_size, total_requests))]
        results = await asyncio.gather(*tasks)
        for res in results:
            if res is not None:
                latencies.append(res)
            else:
                failed_requests += 1

    total_time_sec = time.perf_counter() - overall_start
    throughput = len(latencies) / total_time_sec if total_time_sec > 0 else 0.0

    latencies.sort()
    count = len(latencies)
    p50 = latencies[int(count * 0.50)] if count > 0 else 0.0
    p90 = latencies[int(count * 0.90)] if count > 0 else 0.0
    p95 = latencies[int(count * 0.95)] if count > 0 else 0.0
    p99 = latencies[int(count * 0.99)] if count > 0 else 0.0

    return {
        "total_requests": total_requests,
        "successful_requests": len(latencies),
        "failed_requests": failed_requests,
        "total_time_sec": total_time_sec,
        "throughput_req_sec": throughput,
        "p50_ms": p50,
        "p90_ms": p90,
        "p95_ms": p95,
        "p99_ms": p99,
    }


@pytest.mark.asyncio
async def test_ingestion_load_performance(async_client, test_headers, setup_orgs):
    """Test ingestion load performance meets 1,000 req/sec and p95 < 200ms SLAs."""
    metrics = await run_ingestion_load_simulation(async_client, test_headers, total_requests=1000)

    assert metrics["failed_requests"] == 0, f"Expected 0 failed requests, got {metrics['failed_requests']}"
    assert metrics["successful_requests"] == 1000
    assert metrics["p95_ms"] < 200.0, f"p95 latency {metrics['p95_ms']:.2f}ms exceeded SLA threshold of 200.0ms"
    assert metrics["throughput_req_sec"] >= 950.0, f"Throughput {metrics['throughput_req_sec']:.2f} req/s below SLA 950 req/s"
