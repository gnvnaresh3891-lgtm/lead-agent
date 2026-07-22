from fastapi import APIRouter
from .leads import router as leads_router
from .signals import router as signals_router
from .campaigns import router as campaigns_router
from .messages import router as messages_router
from .compliance import router as compliance_router
from .analytics import router as analytics_router
from .settings import router as settings_router

api_router = APIRouter()
api_router.include_router(leads_router, prefix="/leads", tags=["leads"])
api_router.include_router(signals_router, prefix="/signals", tags=["signals"])
api_router.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
api_router.include_router(compliance_router, prefix="/compliance", tags=["compliance"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
