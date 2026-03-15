"""
Luminara — Route Dependencies
Reusable FastAPI dependencies for auth-protected routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from app.core.security import get_user_id_from_token
from app.db.database import DbSession, AsyncSession, get_db
from app.db.models import User

# Reads Bearer token from Authorization header automatically
_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency for protected routes.
    Reads the Bearer token, validates it, returns the User object.

    Usage in a route:
        async def my_route(current_user: User = Depends(get_current_user)):
    """
    token = credentials.credentials

    try:
        user_id = get_user_id_from_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is deactivated.",
        )

    return user