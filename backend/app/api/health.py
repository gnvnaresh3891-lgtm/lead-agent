from fastapi import APIRouter
from app.core.db import check_db_health
from app.core.logger import metrics_collector
from app.core.redis_client import get_redis_client

router = APIRouter(tags=["health"])


@router.get("/health")
@router.get("/api/v1/health")
async def health_check():
    """Service health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


@router.get("/health/db")
@router.get("/api/v1/health/db")
async def db_health_check():
    """Database connectivity and pool health check endpoint."""
    return await check_db_health()


@router.get("/health/metrics")
@router.get("/api/v1/health/metrics")
async def metrics_health_check():
    """Metrics and observability status endpoint."""
    db_health = await check_db_health()
    redis_client = get_redis_client()
    queue_len = await redis_client.get_queue_len("signals_queue")
    metrics_summary = metrics_collector.get_summary()

    return {
        "status": "healthy",
        "metrics": metrics_summary,
        "queue": {
            "signals_queue_length": queue_len,
            "is_fallback_queue": redis_client.is_fallback,
        },
        "database": db_health,
    }
