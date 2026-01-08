"""Package entrypoint for running the InsureMate app with uvicorn.

This file imports and configures the FastAPI application with all routes and middleware.

Run with:
    uvicorn insuremate.main:app --host 127.0.0.1 --port 8000 --reload
"""

import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# Import routers
from insuremate.api.predict import router as predict_router
from insuremate.api.results import router as results_router
from insuremate.api.health import router as health_router
from insuremate.db.database import SessionLocal, engine, Base

# Basic structured logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("insuremate")

# Create database tables
logger.info("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise

# Create FastAPI app
app = FastAPI(
    title="InsureMate API",
    description="API for InsureMate Insurance Premium Prediction System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Health router already exposes /health
app.include_router(health_router)

# Frontend expects these at /predict and /results (no /api prefix)
app.include_router(predict_router, tags=["predictions"])
app.include_router(results_router, tags=["results"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to InsureMate API. Please visit /api/docs for the API documentation.",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "predict": "/predict",
            "results": "/results"
        }
    }

# Database health check endpoint
@app.get("/api/health/db")
async def db_health_check():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

logger.info("InsureMate app initialized")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
