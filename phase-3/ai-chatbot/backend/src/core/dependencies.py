"""
FastAPI dependency injection.
Reference: @specs/002-fullstack-web-app/architecture.md Service Layer
Reference: @specs/002-fullstack-web-app/api/jwt-auth.md
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from .database import get_session
from .security import verify_token
from ..models.user import User

# HTTP Bearer token security scheme
security = HTTPBearer()


def get_db():
    """
    Dependency to get database session.
    Reference: @specs/architecture.md Service Layer
    """
    from .database import get_session

    return get_session()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """
    Validate JWT token and return current user.

    Reference: @specs/api/jwt-auth.md Backend Token Validation
    Reference: @specs/contracts/api-contract.md JWT Token Format

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    # Verify the token
    token_payload = verify_token(credentials.credentials)

    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "UNAUTHORIZED", "message": "Invalid or expired token"}},
        )

    # Get user from database
    user_id = UUID(token_payload.sub)
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "UNAUTHORIZED", "message": "User not found"}},
        )

    return user


# Type alias for dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[Session, Depends(get_session)]
