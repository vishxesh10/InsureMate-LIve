from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from insuremate.db import session as db_session
from insuremate.db import crud

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    import datetime
    
    try:
        # Check if database is responsive
        with db_session.SessionLocal() as session:
            session.execute(text("SELECT 1"))
            
        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.datetime.now().isoformat()
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
