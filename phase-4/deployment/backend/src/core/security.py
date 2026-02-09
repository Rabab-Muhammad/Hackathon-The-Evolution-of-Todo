"""
Security utilities for password hashing and JWT handling.
Reference: @specs/002-fullstack-web-app/api/jwt-auth.md
Reference: @specs/002-fullstack-web-app/features/authentication.md
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

import bcrypt
import jwt
from pydantic import BaseModel

from .config import get_settings


class TokenPayload(BaseModel):
    """
    JWT token payload structure.
    Reference: @specs/api/jwt-auth.md Token Structure
    """

    sub: str  # User ID (UUID as string)
    email: str
    iat: datetime
    exp: datetime


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Reference: @specs/features/authentication.md FR-005
    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Reference: @specs/features/authentication.md - Login Flow
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hash to verify against

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(user_id: UUID, email: str) -> str:
    """
    Create a JWT access token.

    Reference: @specs/api/jwt-auth.md Token Structure
    Claims: sub (user_id), email, iat, exp

    Args:
        user_id: User's UUID
        email: User's email address

    Returns:
        Encoded JWT token string
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": expires,
    }

    token = jwt.encode(
        payload, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_token(token: str) -> Optional[TokenPayload]:
    """
    Verify and decode a JWT token.

    Reference: @specs/api/jwt-auth.md Backend Token Validation

    Args:
        token: JWT token string

    Returns:
        TokenPayload if valid, None if invalid/expired
    """
    settings = get_settings()

    try:
        payload = jwt.decode(
            token, settings.BETTER_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        return TokenPayload(
            sub=payload["sub"],
            email=payload["email"],
            iat=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
            exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )

    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid (malformed, wrong signature, etc.)
        return None
