from datetime import date, datetime

from sqlalchemy import Boolean, Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utcnow


class HandbookSource(Base):
    """One row per official AICTE handbook edition. Requirements and fees link to this."""

    __tablename__ = "handbook_sources"
    __table_args__ = (UniqueConstraint("edition_name", name="uq_handbook_edition_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    edition_name: Mapped[str] = mapped_column(String(120))
    academic_year: Mapped[str | None] = mapped_column(String(20))
    file_name: Mapped[str | None] = mapped_column(String(255))
    source_url: Mapped[str | None] = mapped_column(String(500))
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_on: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)