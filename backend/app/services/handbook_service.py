from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import HandbookSource
from app.schemas.handbook import HandbookCreate
from app.services.exceptions import ConflictError


def list_handbooks(db: Session) -> list[HandbookSource]:
    return list(db.scalars(select(HandbookSource).order_by(HandbookSource.id)))


def create_handbook(db: Session, payload: HandbookCreate) -> HandbookSource:
    handbook = HandbookSource(**payload.model_dump())
    db.add(handbook)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A handbook with this edition name already exists")
    db.refresh(handbook)
    return handbook