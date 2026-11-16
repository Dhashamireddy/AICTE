from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import ApplicationCategory, ApplicationStatus, CourseLevel, InstitutionType


class InfrastructureDetails(BaseModel):
    """What the institution says it currently has. All optional, none negative."""

    classrooms: int | None = Field(default=None, ge=0, le=10000)
    laboratories: int | None = Field(default=None, ge=0, le=10000)
    faculty_count: int | None = Field(default=None, ge=0, le=100000)
    library_books: int | None = Field(default=None, ge=0, le=100000000)
    built_up_area_sqm: float | None = Field(default=None, ge=0, le=100000000)
    notes: str | None = Field(default=None, max_length=1000)


class InstitutionCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    institution_type: InstitutionType
    state: str = Field(min_length=2, max_length=80)
    city: str = Field(min_length=2, max_length=80)
    has_existing_aicte_approval: bool = False

    @field_validator("name", "state", "city")
    @classmethod
    def strip_text(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("must not be blank")
        return v


class ApplicationCreate(BaseModel):
    """The whole registration form: institution + course in one request."""

    institution: InstitutionCreate
    proposed_course: str = Field(min_length=2, max_length=200)
    course_level: CourseLevel
    category: ApplicationCategory = ApplicationCategory.NEW_COURSE
    # Sanity limits for form input only. These are NOT AICTE rules.
    proposed_intake: int = Field(gt=0, le=5000)
    infrastructure_details: InfrastructureDetails | None = None
    handbook_source_id: int | None = Field(default=None, gt=0)

    @field_validator("proposed_course")
    @classmethod
    def strip_course(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("must not be blank")
        return v


class InstitutionRead(InstitutionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution: InstitutionRead
    handbook_source_id: int | None
    proposed_course: str
    course_level: CourseLevel
    category: ApplicationCategory
    proposed_intake: int
    infrastructure_details: InfrastructureDetails | None
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    