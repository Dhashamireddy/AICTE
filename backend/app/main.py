from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.models  # noqa: F401  (registers all tables)
from app.config import settings
from app.database import Base, engine
from app.routes import applications, handbooks, health
from app.services.exceptions import ConflictError, NotFoundError


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Creates any missing tables when the server starts.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="AI-based system for simplifying the AICTE approval process. "
    "Academic assistance prototype, not an official AICTE system.",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundError)
async def not_found_handler(_request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(_request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(health.router, prefix="/api")
app.include_router(handbooks.router, prefix="/api")
app.include_router(applications.router, prefix="/api")