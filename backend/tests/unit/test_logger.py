import json
import logging
import pytest
from app.core.logger import JSONFormatter, log_event, MetricsCollector, metrics_collector


def test_json_formatter():
    """Test JSONFormatter outputs valid structured JSON string."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test structured log message",
        args=(),
        exc_info=None,
    )
    record.event_type = "unit_test"
    record.org_id = "11111111-1111-1111-1111-111111111111"
    record.trace_id = "trace_001"
    record.latency_ms = 12.34

    output = formatter.format(record)
    parsed = json.loads(output)

    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test structured log message"
    assert parsed["event_type"] == "unit_test"
    assert parsed["org_id"] == "11111111-1111-1111-1111-111111111111"
    assert parsed["trace_id"] == "trace_001"
    assert parsed["latency_ms"] == 12.34


def test_log_event():
    """Test log_event helper executes cleanly."""
    log_event(
        level="info",
        event_type="test_event",
        message="System event test",
        org_id="11111111-1111-1111-1111-111111111111",
        trace_id="trace_999",
        latency_ms=5.0,
    )


def test_metrics_collector():
    """Test MetricsCollector recording, percentile calculations, and reset."""
    collector = MetricsCollector()
    collector.reset()

    assert collector.request_count == 0

    # Record 100 requests with latencies 1..100
    for i in range(1, 101):
        collector.record_request("/test", float(i), status_code=200 if i <= 95 else 500)

    summary = collector.get_summary()
    assert summary["request_count"] == 100
    assert summary["error_count"] == 5
    assert summary["latency_p50_ms"] >= 49.0
    assert summary["latency_p95_ms"] >= 94.0

    collector.reset()
    assert collector.request_count == 0
    assert collector.error_count == 0
