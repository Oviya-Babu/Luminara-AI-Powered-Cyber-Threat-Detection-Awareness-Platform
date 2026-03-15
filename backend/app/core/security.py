"""
Luminara — Security Utilities
Handles JWT token creation/validation and password hashing.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ── Password Hashing ──────────────────────────────────────
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches its stored hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# ── JWT Tokens ────────────────────────────────────────────

def decode_token(token: str, expected_type: str = "access") -> dict:
    """
    Decode and validate a JWT token.
    Raises ValueError if token is invalid, expired, or wrong type.
    This function MUST be defined before any function that calls it.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as e:
        raise ValueError(f"Invalid or expired token: {e}")

    if payload.get("type") != expected_type:
        raise ValueError(
            f"Expected token type '{expected_type}', "
            f"got '{payload.get('type')}'"
        )

    return payload


def create_access_token(user_id: UUID, email: str) -> str:
    """
    Create a short-lived access token (default 60 minutes).
    The mobile app sends this on every API request.
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(user_id: UUID) -> str:
    """
    Create a long-lived refresh token (default 30 days).
    Used to get a new access token without logging in again.
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def get_user_id_from_token(token: str) -> UUID:
    """
    Decode an access token and return the user's UUID.
    Used in protected route dependencies.
    """
    payload = decode_token(token, expected_type="access")
    try:
        return UUID(payload["sub"])
    except (KeyError, ValueError):
        raise ValueError("Token does not contain a valid user ID")