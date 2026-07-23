"""
Master Test Runner for backend_rebuild E2E Test Suite.
Executes pytest programmatically across all test tiers with ZERO synthetic mocks,
collects pass/fail statistics, measures real-world SLAs, asserts 100% pass rate,
and outputs test_results.json at project root.
"""
import asyncio
import datetime
import json
import os
import sys
import time
import uuid
from pathlib import Path

import httpx
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.db import (
    close_db_connection_pool,
    get_db_session,
    init_db_pool,
)
from app.core.redis_client import RedisClient
from app.main import app
from app.models.base import Base
from app.models.organization import Organization
from tests.tier4_load.test_connection_pool_stress import run_pool_stress_test
from tests.tier4_load.test_ingestion_load import run_ingestion_load_simulation
from tests.tier4_load.test_multi_tenant_isolation import run_isolation_verification
from tests.tier4_load.test_worker_burst import run_worker_burst_simulation


class PytestResultsCollector:
    """Pytest plugin collecting pass/fail statistics per test tier."""

    def __init__(self):
        self.results = {
            "unit": {"total": 0, "passed": 0, "failed": 0},
            "tier1_feature": {"total": 0, "passed": 0, "failed": 0},
            "tier2_boundary": {"total": 0, "passed": 0, "failed": 0},
            "tier3_cross": {"total": 0, "passed": 0, "failed": 0},
            "tier4_load": {"total": 0, "passed": 0, "failed": 0},
        }
        self.total_passed = 0
        self.total_failed = 0
        self.total_tests = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            fpath = str(report.fspath)
            if "tier1_feature" in fpath:
                tier = "tier1_feature"
            elif "tier2_boundary" in fpath:
                tier = "tier2_boundary"
            elif "tier3_cross" in fpath:
                tier = "tier3_cross"
            elif "tier4_load" in fpath:
                tier = "tier4_load"
            else:
                tier = "unit"

            self.results[tier]["total"] += 1
            self.total_tests += 1
            if report.passed:
                self.results[tier]["passed"] += 1
                self.total_passed += 1
            else:
                self.results[tier]["failed"] += 1
                self.total_failed += 1
                print(f"  [FAIL] {report.nodeid}: {report.longreprtext}")


async def gather_tier4_sla_metrics():
    """Gather real-world Tier 4 SLA performance metrics against application code."""
    engine = init_db_pool("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    r_client = RedisClient()
    await r_client.connect()
    await r_client.clear()

    org1_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    async with get_db_session() as session:
        org1 = Organization(id=org1_id, name="SLA Org Alpha")
        session.add(org1)

    headers = {"X-Org-Id": str(org1_id)}

    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            ingest_metrics = await run_ingestion_load_simulation(client, headers, total_requests=1000)
    except AttributeError:
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            ingest_metrics = await run_ingestion_load_simulation(client, headers, total_requests=1000)

    burst_metrics = await run_worker_burst_simulation(r_client, total_signals=10000)
    isolation_metrics = await run_isolation_verification(org_count=1000)
    stress_metrics = await run_pool_stress_test(total_operations=1000)

    await r_client.clear()
    await r_client.disconnect()
    await close_db_connection_pool()

    return ingest_metrics, burst_metrics, isolation_metrics, stress_metrics


def run_suite():
    overall_start = time.perf_counter()
    print("=" * 80)
    print("      EXECUTING BACKEND_REBUILD REAL E2E TEST SUITE (ZERO MOCKS)")
    print("=" * 80)

    # 1. Collect Tier 4 Real Performance Metrics
    print("Running Tier 4 SLA Performance & Load Harnesses...")
    ingest_m, burst_m, iso_m, stress_m = asyncio.run(gather_tier4_sla_metrics())

    # 2. Run pytest programmatically across all test tiers
    print("\nExecuting Pytest Test Specifications Across All Tiers...")
    collector = PytestResultsCollector()
    exit_code = pytest.main(
        [
            "-q",
            "--tb=short",
            str(PROJECT_ROOT / "tests"),
        ],
        plugins=[collector],
    )

    total_duration = time.perf_counter() - overall_start

    # Evaluate SLAs
    sla_ingestion_pass = ingest_m["p95_ms"] < 200.0 and ingest_m["failed_requests"] == 0
    sla_burst_pass = burst_m["elapsed_seconds"] < 60.0 and burst_m["dlq_count"] == 0
    sla_isolation_pass = iso_m["cross_tenant_leaks"] == 0
    sla_stress_pass = stress_m["pool_exhaustion_errors"] == 0

    tier_results = collector.results
    u_res = tier_results["unit"]
    t1_res = tier_results["tier1_feature"]
    t2_res = tier_results["tier2_boundary"]
    t3_res = tier_results["tier3_cross"]
    t4_res = tier_results["tier4_load"]

    u_status = "PASS" if u_res["failed"] == 0 and u_res["total"] > 0 else "FAIL"
    t1_status = "PASS" if t1_res["failed"] == 0 and t1_res["total"] > 0 else "FAIL"
    t2_status = "PASS" if t2_res["failed"] == 0 and t2_res["total"] > 0 else "FAIL"
    t3_status = "PASS" if t3_res["failed"] == 0 and t3_res["total"] > 0 else "FAIL"
    t4_status = (
        "PASS"
        if (
            t4_res["failed"] == 0
            and t4_res["total"] > 0
            and sla_ingestion_pass
            and sla_burst_pass
            and sla_isolation_pass
            and sla_stress_pass
        )
        else "FAIL"
    )

    overall_passed = collector.total_passed
    overall_failed = collector.total_failed
    overall_total = collector.total_tests

    overall_status = (
        "PASS"
        if (
            exit_code == 0
            and overall_failed == 0
            and u_status == "PASS"
            and t1_status == "PASS"
            and t2_status == "PASS"
            and t3_status == "PASS"
            and t4_status == "PASS"
        )
        else "FAIL"
    )

    # Print Summary Table
    print("\n" + "=" * 80)
    print("                    E2E TEST SUITE EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Unit Tests                        | Total: {u_res['total']:2d} | Passed: {u_res['passed']:2d} | Failed: {u_res['failed']:2d} | STATUS: {u_status}")
    print(f"Tier 1: Feature Tests             | Total: {t1_res['total']:2d} | Passed: {t1_res['passed']:2d} | Failed: {t1_res['failed']:2d} | STATUS: {t1_status}")
    print(f"Tier 2: Boundary & Edge Tests     | Total: {t2_res['total']:2d} | Passed: {t2_res['passed']:2d} | Failed: {t2_res['failed']:2d} | STATUS: {t2_status}")
    print(f"Tier 3: Cross-Feature Interactions| Total: {t3_res['total']:2d} | Passed: {t3_res['passed']:2d} | Failed: {t3_res['failed']:2d} | STATUS: {t3_status}")
    print(f"Tier 4: Load & Stress Harnesses  | Total: {t4_res['total']:2d} | Passed: {t4_res['passed']:2d} | Failed: {t4_res['failed']:2d} | STATUS: {t4_status}")
    print("-" * 80)
    print("REAL-WORLD SLA METRICS EVALUATION:")
    print(f"  - Ingestion Load Test (1k req) : p95 Latency = {ingest_m['p95_ms']:.1f}ms (Threshold: <200.0ms) [{'PASS' if sla_ingestion_pass else 'FAIL'}]")
    print(f"  - Ingestion Throughput         : {ingest_m['throughput_req_sec']:.1f} req/s")
    print(f"  - Worker Burst Processing (10k): Duration = {burst_m['elapsed_seconds']:.2f}s (Threshold: <60.0s)   [{'PASS' if sla_burst_pass else 'FAIL'}]")
    print(f"  - Worker Throughput            : {burst_m['processed_per_sec']:.1f} signals/s")
    print(f"  - Multi-Tenant Isolation (1k)  : Leaks = {iso_m['cross_tenant_leaks']} / {iso_m['total_orgs_tested']} orgs                  [{'PASS' if sla_isolation_pass else 'FAIL'}]")
    print(f"  - Connection Pool Stress (1k)  : Errors = {stress_m['pool_exhaustion_errors']} / {stress_m['total_operations']} ops             [{'PASS' if sla_stress_pass else 'FAIL'}]")
    print("=" * 80)
    print(f"OVERALL RESULT: {'ALL SUITES PASSED (' + str(overall_passed) + '/' + str(overall_total) + ' Test Specifications Verified)' if overall_status == 'PASS' else 'TEST SUITE FAILED'}")
    print("=" * 80 + "\n")

    # Export test_results.json
    results_json = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_status": overall_status,
        "summary": {
            "total_tests": overall_total,
            "passed": overall_passed,
            "failed": overall_failed,
            "duration_seconds": round(total_duration, 2),
        },
        "tiers": {
            "unit": u_res,
            "tier1_feature": t1_res,
            "tier2_boundary": t2_res,
            "tier3_cross": t3_res,
            "tier4_load": t4_res,
        },
        "sla_metrics": {
            "ingestion_p95_latency_ms": round(ingest_m["p95_ms"], 2),
            "ingestion_throughput_req_sec": round(ingest_m["throughput_req_sec"], 2),
            "worker_burst_duration_sec": round(burst_m["elapsed_seconds"], 2),
            "worker_burst_processed_per_sec": round(burst_m["processed_per_sec"], 2),
            "cross_tenant_leak_count": iso_m["cross_tenant_leaks"],
            "isolation_percentage": iso_m["isolation_percentage"],
            "pool_exhaustion_error_count": stress_m["pool_exhaustion_errors"],
        },
    }

    results_file_root = PROJECT_ROOT / "test_results.json"
    results_file_tests = PROJECT_ROOT / "tests" / "test_results.json"

    with open(results_file_root, "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=2)

    with open(results_file_tests, "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=2)

    print(f"Results exported successfully to:\n  - {results_file_root}\n  - {results_file_tests}")

    if overall_status != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    run_suite()
