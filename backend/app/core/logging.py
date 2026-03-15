"""
Luminara — Logging Setup
Call setup_logging() once at app startup.
Then use: from loguru import logger
"""

import sys
from app.core.config import settings


def setup_logging() -> None:
    """Configure loguru for clean, readable log output."""
    from loguru import logger

    # Remove the default loguru handler
    logger.remove()

    # Add our custom handler
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> — "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    logger.info(f"Luminara logging started — level: {settings.log_level}")