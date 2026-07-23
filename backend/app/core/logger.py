from datetime import datetime, timezone
import json
import logging
import math
import sys
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("app")


class JSONFormatter(logging.Formatter):
    """Custom logging Formatter that produces structured JSON output."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "event_type": getattr(record, "event_type", "generic"),
            "org_id": getattr(record, "org_id", None),
            "trace_id": getattr(record, "trace_id", None),
            "latency_ms": getattr(record, "latency_ms", 0.0),
        }
        # Include extra dictionary items if provided
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_data.update(record.extra_fields)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure standard structured JSON logger output to stdout."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # Remove existing handlers to prevent duplicate outputs
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    root_logger.addHandler(handler)


def log_event(
    level: str,
    event_type: str,
    message: str,
    org_id: Optional[Any] = None,
    trace_id: Optional[str] = None,
    latency_ms: float = 0.0,
    **extra: Any,
) -> None:
    """Helper to emit structured JSON log record."""
    log_logger = logging.getLogger("app.structured")
    log_level = getattr(logging, level.upper(), logging.INFO)
    extra_dict = {
        "event_type": event_type,
        "org_id": str(org_id) if org_id is not None else None,
        "trace_id": trace_id,
        "latency_ms": latency_ms,
        "extra_fields": extra,
    }
    log_logger.log(log_level, message, extra=extra_dict)


class MetricsCollector:
    """Metrics collector tracking request counts, latencies (p50/p95/p99), and queue stats."""

    def __init__(self, max_samples: int = 10000):
        self.max_samples = max_samples
        self.request_count: int = 0
        self.error_count: int = 0
        self._latencies: List[float] = []

    def record_request(self, endpoint: str, latency_ms: float, status_code: int = 200) -> None:
        """Record an API request latency and status."""
        self.request_count += 1
        if status_code >= 400:
            self.error_count += 1

        self._latencies.append(latency_ms)
        if len(self._latencies) > self.max_samples:
            self._latencies.pop(0)

    def get_latency_percentiles(self) -> Dict[str, float]:
        """Compute p50, p95, p99 latency percentiles in ms."""
        if not self._latencies:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0}

        sorted_latencies = sorted(self._latencies)
        n = len(sorted_latencies)

        def percentile(p: float) -> float:
            k = (n - 1) * (p / 100.0)
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return sorted_latencies[int(k)]
            d0 = sorted_latencies[int(f)] * (c - k)
            d1 = sorted_latencies[int(c)] * (k - f)
            return d0 + d1

        return {
            "p50": round(percentile(50.0), 2),
            "p95": round(percentile(95.0), 2),
            "p99": round(percentile(99.0), 2),
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        percentiles = self.get_latency_percentiles()
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "latency_p50_ms": percentiles["p50"],
            "latency_p95_ms": percentiles["p95"],
            "latency_p99_ms": percentiles["p99"],
        }

    def reset(self) -> None:
        """Reset internal metric counters."""
        self.request_count = 0
        self.error_count = 0
        self._latencies.clear()


metrics_collector = MetricsCollector()
