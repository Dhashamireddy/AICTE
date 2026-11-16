"""Allowed values for fields with a fixed set of choices.

NOTE: These are application-level choices for the form. They are NOT official AICTE
categories. Once we load the real handbook, we will reconcile them with its terminology.
"""
from enum import Enum


class InstitutionType(str, Enum):
    GOVERNMENT = "government"
    GOVERNMENT_AIDED = "government_aided"
    PRIVATE_SELF_FINANCING = "private_self_financing"
    UNIVERSITY_DEPARTMENT = "university_department"
    OTHER = "other"


class CourseLevel(str, Enum):
    DIPLOMA = "diploma"
    UNDERGRADUATE = "undergraduate"
    POSTGRADUATE = "postgraduate"


class ApplicationCategory(str, Enum):
    NEW_COURSE = "new_course"
    INCREASE_INTAKE = "increase_intake"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


def values(enum_cls) -> str:
    """Turns an Enum into a quoted list for SQL CHECK constraints: 'a','b','c'"""
    return ",".join(f"'{member.value}'" for member in enum_cls)