"""
Luminara — Authentication Endpoints
POST /api/v1/auth/register  — create new account
POST /api/v1/auth/login     — login, get JWT tokens
GET  /api/v1/auth/me        — get current user profile
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from loguru import logger

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.db.database import DbSession
from app.db.models import User, UserStreak
from app.api.v1.deps import get_current_user

router = APIRouter()


# ── Request / Response shapes ─────────────────────────────

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    language: str = "en"
    knowledge_level: str = "beginner"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    email: str


class UserProfileResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    language: str
    knowledge_level: str
    created_at: datetime


# ── POST /auth/register ───────────────────────────────────

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(request: RegisterRequest, db: DbSession):
    # Check email not already taken
    result = await db.execute(
        select(User).where(User.email == request.email.lower())
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Validate password
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters.",
        )

    # Validate knowledge level
    if request.knowledge_level not in {"beginner", "intermediate", "advanced"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="knowledge_level must be: beginner, intermediate, or advanced",
        )

    # Save user to database
    new_user = User(
        full_name=request.full_name.strip(),
        email=request.email.lower().strip(),
        hashed_password=hash_password(request.password),
        language=request.language,
        knowledge_level=request.knowledge_level,
    )
    db.add(new_user)
    await db.flush()  # assigns new_user.id

    # Create empty streak record
    db.add(UserStreak(user_id=new_user.id))

    logger.info(f"New user registered: {new_user.email}")

    return AuthResponse(
        access_token=create_access_token(new_user.id, new_user.email),
        refresh_token=create_refresh_token(new_user.id),
        user_id=str(new_user.id),
        full_name=new_user.full_name,
        email=new_user.email,
    )


# ── POST /auth/login ──────────────────────────────────────

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: DbSession):
    # Find user
    result = await db.execute(
        select(User).where(User.email == request.email.lower())
    )
    user = result.scalar_one_or_none()

    # Validate credentials
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    logger.info(f"User logged in: {user.email}")

    return AuthResponse(
        access_token=create_access_token(user.id, user.email),
        refresh_token=create_refresh_token(user.id),
        user_id=str(user.id),
        full_name=user.full_name,
        email=user.email,
    )


# ── GET /auth/me ──────────────────────────────────────────

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return UserProfileResponse(
        user_id=str(current_user.id),
        full_name=current_user.full_name,
        email=current_user.email,
        language=current_user.language,
        knowledge_level=current_user.knowledge_level,
        created_at=current_user.created_at,
    )
