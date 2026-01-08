from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from insuremate.db import database

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint that verifies database connectivity."""
    try:
        # Check if database is responsive
        with database.SessionLocal() as session:
            session.execute(text("SELECT 1"))
            
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-11-28T11:15:30Z"
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": "2025-11-28T11:15:30Z"
            }
        )
    return {"status": status, "database": db_ok}
