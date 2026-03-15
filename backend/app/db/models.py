"""
Luminara — Database Models
Defines all database tables as Python classes.
SQLAlchemy reads these to create the actual tables in Supabase.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _now() -> datetime:
    """Helper — returns current UTC time."""
    return datetime.now(tz=timezone.utc)


# ── Users table ───────────────────────────────────────────
class User(Base):
    """Stores every registered Luminara user."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[str] = mapped_column(String(5), default="en")
    knowledge_level: Mapped[str] = mapped_column(String(20), default="beginner")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now
    )

    # One user has many scan results
    scan_results: Mapped[list["ScanResult"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # One user has one streak record
    streak: Mapped[Optional["UserStreak"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


# ── Scan Results table ────────────────────────────────────
class ScanResult(Base):
    """Stores every phishing/deepfake analysis result."""
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scan_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # e.g. "phishing", "deepfake_audio", "deepfake_video"

    input_summary: Mapped[str] = mapped_column(String(500), nullable=False)
    # Short preview of what was scanned (never store full message)

    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    # "safe" | "low" | "medium" | "high" | "critical"

    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    # 0.0 to 1.0

    result_detail: Mapped[dict] = mapped_column(JSON, nullable=False)
    # Full structured result from the AI model

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, index=True
    )

    user: Mapped["User"] = relationship(back_populates="scan_results")


# ── User Streak table ─────────────────────────────────────
class UserStreak(Base):
    """Tracks daily learning streaks and badges."""
    __tablename__ = "user_streaks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_days_active: Mapped[int] = mapped_column(Integer, default=0)
    awareness_score: Mapped[int] = mapped_column(Integer, default=0)
    badges: Mapped[list] = mapped_column(JSON, default=list)
    last_activity_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="streak")