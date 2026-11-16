# Importing every model here makes sure SQLAlchemy knows about all tables.
from app.models.application import Application
from app.models.handbook_source import HandbookSource
from app.models.institution import Institution
from app.models.user import User

__all__ = ["Application", "HandbookSource", "Institution", "User"]