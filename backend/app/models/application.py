from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import ApplicationCategory, ApplicationStatus, CourseLevel, values
from app.models.user import utcnow


class Application(Base):
    """One application session: an institution wants to introduce one course."""

    __tablename__ = "applications"
    __table_args__ = (
        CheckConstraint(f"course_level IN ({values(CourseLevel)})", name="ck_application_level"),
        CheckConstraint(f"category IN ({values(ApplicationCategory)})", name="ck_application_category"),
        CheckConstraint(f"status IN ({values(ApplicationStatus)})", name="ck_application_status"),
        CheckConstraint("proposed_intake > 0", name="ck_application_intake_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"), index=True)
    handbook_source_id: Mapped[int | None] = mapped_column(ForeignKey("handbook_sources.id"), index=True)
    proposed_course: Mapped[str] = mapped_column(String(200))
    course_level: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30), default=ApplicationCategory.NEW_COURSE.value)
    proposed_intake: Mapped[int] = mapped_column(Integer)
    infrastructure_details: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default=ApplicationStatus.DRAFT.value)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    institution = relationship("Institution", back_populates="applications")
    handbook_source = relationship("HandbookSource")