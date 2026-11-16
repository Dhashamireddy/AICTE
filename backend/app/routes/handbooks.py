from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.handbook import HandbookCreate, HandbookRead
from app.services import handbook_service

router = APIRouter(prefix="/handbooks", tags=["Handbooks"])


@router.get("", response_model=list[HandbookRead])
def list_handbooks(db: Session = Depends(get_db)):
    return handbook_service.list_handbooks(db)


@router.post("", response_model=HandbookRead, status_code=status.HTTP_201_CREATED)
def create_handbook(payload: HandbookCreate, db: Session = Depends(get_db)):
    return handbook_service.create_handbook(db, payload)