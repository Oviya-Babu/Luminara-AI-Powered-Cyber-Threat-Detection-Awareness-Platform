"""
Luminara — FastAPI Application Entry Point
This is the file you run to start the backend server.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import init_db, close_db


# ── Lifespan — runs at startup and shutdown ───────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    setup_logging()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    await init_db()
    logger.info("Luminara backend is ready")

    yield  # app runs here

    # SHUTDOWN
    await close_db()
    logger.info("Luminara backend shut down cleanly")


# ── Create the FastAPI app ────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered cyber threat detection and awareness platform.",
    docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS — allow the mobile app to talk to the backend ────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# ── Global error handler ──────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong. Please try again."},
    )


# ── Register all routes ───────────────────────────────────
from app.api.v1.router import router as api_router  # noqa
app.include_router(api_router, prefix="/api/v1")


# ── Health check ──────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    """Quick check to confirm the server is running."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
