import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.seed import seed_database
from app.database import engine, Base, SessionLocal
from app.routes import api_router

os.makedirs("data", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create database tables
    Base.metadata.create_all(bind=engine)
    
    # 2. Run idempotent seeder
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
        
    yield

app = FastAPI(
    title="Lead Agent API",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(api_router, prefix="/api")

# Root health check
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Lead Agent API is running"}
