from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import InstitutionType, values
from app.models.user import utcnow


class Institution(Base):
    __tablename__ = "institutions"
    __table_args__ = (
        CheckConstraint(f"institution_type IN ({values(InstitutionType)})", name="ck_institution_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    institution_type: Mapped[str] = mapped_column(String(40))
    state: Mapped[str] = mapped_column(String(80))
    city: Mapped[str] = mapped_column(String(80))
    has_existing_aicte_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    user = relationship("User", back_populates="institutions")
    applications = relationship("Application", back_populates="institution", cascade="all, delete-orphan")