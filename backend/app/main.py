import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.seed import seed_database
from app.database import engine, Base, SessionLocal
from app.routes import api_router
from app.config import settings

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("lead_agent")

os.makedirs("data", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("Running database seeder...")
    db = SessionLocal()
    try:
        seed_database(db)
        logger.info("Seeder check complete.")
    except Exception as e:
        logger.error(f"Seeder error: {e}")
    finally:
        db.close()
        
    yield
    logger.info("Application shutdown.")

app = FastAPI(
    title="SignalSDR — Lead Qualification & SDR Agent API",
    description="Production API for AI-powered signal detection, lead scoring, and automated outreach",
    version="1.0.0",
    lifespan=lifespan
)

# Dynamic CORS Configuration for Production & Development
cors_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://lead-agent-ecru-beta.vercel.app",
]

# Add custom origins from env if present
if hasattr(settings, "CORS_ORIGINS") and settings.CORS_ORIGINS:
    if isinstance(settings.CORS_ORIGINS, list):
        cors_origins.extend(settings.CORS_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production wildcard fallback for public API access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler for Production Safety
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "path": str(request.url.path)
        }
    )

# Include API Router
app.include_router(api_router, prefix="/api")

# Production Health Check Endpoints
@app.get("/")
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SignalSDR API",
        "version": "1.0.0",
        "environment": getattr(settings, "ENVIRONMENT", "production")
    }
