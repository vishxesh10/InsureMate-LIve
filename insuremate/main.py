import logging
import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from insuremate.api.predict import router as predict_router
from insuremate.api.results import router as results_router
from insuremate.api.health import router as health_router
from insuremate.db.database import SessionLocal, engine, Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("insuremate")

logger.info("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise

app = FastAPI(
    title="InsureMate API",
    description="API for InsureMate Insurance Premium Prediction System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

app.include_router(predict_router, tags=["predictions"])
app.include_router(results_router, tags=["results"])

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
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting uvicorn on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
