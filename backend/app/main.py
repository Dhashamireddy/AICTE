from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import health

app = FastAPI(
    title=settings.app_name,
    description="AI-based system for simplifying the AICTE approval process. "
    "Academic assistance prototype, not an official AICTE system.",
    version="0.1.0",
)

# CORS lets the React app (a different port) call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
