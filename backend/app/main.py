from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.signals import router as signals_router
from app.api.agents import router as agents_router
from app.core.config import settings
from app.core.db import check_db_health, close_db_connection_pool, init_db_pool
from app.core.redis_client import redis_client
from app.core.tenancy import TenantContextMiddleware

import asyncio
from app.workers.signal_worker import run_worker_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for DB pool and Redis connection initialization and cleanup."""
    # Startup phase
    init_db_pool()
    await redis_client.connect()

    # Start background worker
    worker_stop_event = asyncio.Event()
    worker_task = asyncio.create_task(run_worker_loop(redis_client=redis_client, stop_event=worker_stop_event))

    yield

    # Shutdown phase
    worker_stop_event.set()
    try:
        await asyncio.wait_for(worker_task, timeout=5.0)
    except asyncio.TimeoutError:
        pass

    await redis_client.disconnect()
    await close_db_connection_pool()

app = FastAPI(
    title="Multi-Tenant Backend Service",
    version="0.1.0",
    description="High-Performance Multi-Tenant Architecture Service for backend_rebuild",
    lifespan=lifespan,
)

# Mount Tenant Context Middleware
app.add_middleware(TenantContextMiddleware)

# Include API Routers
app.include_router(signals_router)
app.include_router(health_router)
app.include_router(agents_router)
