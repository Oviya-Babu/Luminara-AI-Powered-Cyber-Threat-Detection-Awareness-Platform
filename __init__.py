"""
Luminara Backend — Database Models
All SQLAlchemy ORM models for the platform.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey,
    Integer, String, Text, JSON, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ── Users ─────────────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[str] = mapped_column(String(5), default="en", nullable=False)
    knowledge_level: Mapped[str] = mapped_column(
        SAEnum("beginner", "intermediate", "advanced", name="knowledge_level_enum"),
        default="beginner", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    # Relationships
    scan_results: Mapped[list["ScanResult"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    streak: Mapped[Optional["UserStreak"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    lesson_progress: Mapped[list["LessonProgress"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# ── Scan Results ──────────────────────────────────────────────────────────────
class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    scan_type: Mapped[str] = mapped_column(
        SAEnum("phishing", "deepfake_audio", "deepfake_video", "qr_code", "notification", name="scan_type_enum"),
        nullable=False
    )
    input_summary: Mapped[str] = mapped_column(String(500), nullable=False)   # Sanitised input preview
    risk_level: Mapped[str] = mapped_column(
        SAEnum("safe", "low", "medium", "high", "critical", name="risk_level_enum"),
        nullable=False
    )
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)    # 0.0 – 1.0
    result_detail: Mapped[dict] = mapped_column(JSON, nullable=False)         # Full structured result
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)

    user: Mapped["User"] = relationship(back_populates="scan_results")


# ── Awareness Lessons ─────────────────────────────────────────────────────────
class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[dict] = mapped_column(JSON, nullable=False)                  # {"en": "...", "ta": "...", "hi": "..."}
    content: Mapped[dict] = mapped_column(JSON, nullable=False)                # Multilingual content blocks
    category: Mapped[str] = mapped_column(
        SAEnum("phishing", "deepfake", "qr_fraud", "social_engineering", "identity_theft", name="lesson_category_enum"),
        nullable=False
    )
    difficulty: Mapped[str] = mapped_column(
        SAEnum("beginner", "intermediate", "advanced", name="difficulty_enum"),
        nullable=False, index=True
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    quizzes: Mapped[list["Quiz"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
    progress_records: Mapped[list["LessonProgress"]] = relationship(back_populates="lesson")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    user: Mapped["User"] = relationship(back_populates="lesson_progress")
    lesson: Mapped["Lesson"] = relationship(back_populates="progress_records")


# ── Quizzes ───────────────────────────────────────────────────────────────────
class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    question: Mapped[dict] = mapped_column(JSON, nullable=False)               # Multilingual
    options: Mapped[dict] = mapped_column(JSON, nullable=False)                # {"en": ["a","b","c","d"], ...}
    correct_option_index: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[dict] = mapped_column(JSON, nullable=False)            # Multilingual explanation
    is_daily: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    lesson: Mapped["Lesson"] = relationship(back_populates="quizzes")
    attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="quiz", cascade="all, delete-orphan")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    selected_option_index: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)

    user: Mapped["User"] = relationship(back_populates="quiz_attempts")
    quiz: Mapped["Quiz"] = relationship(back_populates="attempts")


# ── Daily Streak ──────────────────────────────────────────────────────────────
class UserStreak(Base):
    __tablename__ = "user_streaks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_days_active: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    badges: Mapped[list] = mapped_column(JSON, default=list, nullable=False)   # ["first_scan", "week_streak", ...]
    awareness_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    user: Mapped["User"] = relationship(back_populates="streak")
