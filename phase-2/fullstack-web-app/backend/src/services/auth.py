"""
Authentication business logic.
Reference: @specs/002-fullstack-web-app/features/authentication.md
"""

from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..models.user import User
from ..schemas.auth import SignupRequest, SigninRequest, AuthResponse, UserResponse
from ..core.security import hash_password, verify_password, create_access_token


async def signup_user(session: Session, request: SignupRequest) -> AuthResponse:
    """
    Register a new user.

    Reference: @specs/features/authentication.md User Story 1
    Reference: @specs/features/authentication.md Registration Flow

    Args:
        session: Database session
        request: SignupRequest with email and password

    Returns:
        AuthResponse with user and JWT token

    Raises:
        HTTPException 409: Email already exists
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "CONFLICT",
                    "message": "An account with this email already exists",
                }
            },
        )

    # Hash password and create user
    password_hash = hash_password(request.password)
    user = User(email=request.email, password_hash=password_hash)

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email, created_at=user.created_at),
        token=token,
    )


async def signin_user(session: Session, request: SigninRequest) -> AuthResponse:
    """
    Authenticate existing user.

    Reference: @specs/features/authentication.md User Story 2
    Reference: @specs/features/authentication.md Login Flow

    Args:
        session: Database session
        request: SigninRequest with email and password

    Returns:
        AuthResponse with user and JWT token

    Raises:
        HTTPException 401: Invalid credentials
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    # Generic error message to prevent email enumeration
    # Reference: @specs/features/authentication.md - Security
    invalid_credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Invalid credentials",
            }
        },
    )

    if not user:
        raise invalid_credentials_error

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise invalid_credentials_error

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email),
        token=token,
    )
