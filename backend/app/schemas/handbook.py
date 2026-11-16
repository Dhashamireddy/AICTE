from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HandbookCreate(BaseModel):
    edition_name: str = Field(min_length=3, max_length=120)
    academic_year: str | None = Field(default=None, max_length=20)
    file_name: str | None = Field(default=None, max_length=255)
    source_url: str | None = Field(default=None, max_length=500)
    is_official: bool = False
    verified_on: date | None = None

    @field_validator("edition_name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class HandbookRead(HandbookCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime