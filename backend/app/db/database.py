"""
Luminara — Database Connection
Connects to Supabase PostgreSQL using async SQLAlchemy.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Build connection arguments — Supabase requires SSL
connect_args = {
    "ssl": "require",          # Supabase always needs SSL
    "server_settings": {
        "application_name": "luminara_backend"
    }
}

# Create the async engine
engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.is_development,
    connect_args=connect_args,
)

# Session factory
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session to route handlers.
    Auto-commits on success, auto-rollbacks on error.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]


async def init_db() -> None:
    """Create all tables at startup if they don't exist."""
    from app.db import models  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialised successfully")


async def close_db() -> None:
    """Close all connections at shutdown."""
    await engine.dispose()
    logger.info("Database connections closed")