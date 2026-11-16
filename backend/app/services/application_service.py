from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Application, HandbookSource, Institution
from app.schemas.application import ApplicationCreate
from app.services.exceptions import NotFoundError


def create_application(db: Session, payload: ApplicationCreate) -> Application:
    """Creates the institution and the application together in ONE transaction.

    If anything fails, nothing is saved (rollback), so we never get half-created data.
    """
    if payload.handbook_source_id is not None:
        if db.get(HandbookSource, payload.handbook_source_id) is None:
            raise NotFoundError("Handbook edition")

    try:
        institution = Institution(**payload.institution.model_dump())
        db.add(institution)
        db.flush()  # gives the institution an id without committing yet

        application = Application(
            institution_id=institution.id,
            handbook_source_id=payload.handbook_source_id,
            proposed_course=payload.proposed_course,
            course_level=payload.course_level.value,
            category=payload.category.value,
            proposed_intake=payload.proposed_intake,
            infrastructure_details=(
                payload.infrastructure_details.model_dump() if payload.infrastructure_details else None
            ),
        )
        db.add(application)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return get_application(db, application.id)


def get_application(db: Session, application_id: int) -> Application:
    stmt = (
        select(Application)
        .options(joinedload(Application.institution))
        .where(Application.id == application_id)
    )
    application = db.scalars(stmt).first()
    if application is None:
        raise NotFoundError("Application")
    return application


def list_applications(db: Session, limit: int = 50, offset: int = 0) -> list[Application]:
    stmt = (
        select(Application)
        .options(joinedload(Application.institution))
        .order_by(Application.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt))