from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Confirms the API is running and the database is reachable."""
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "app": settings.app_name,
        "database": "connected",
        "disclaimer": "Academic assistance prototype. Not an official AICTE approval system.",
    }
