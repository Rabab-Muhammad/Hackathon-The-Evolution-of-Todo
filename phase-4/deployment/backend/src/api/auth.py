"""
Authentication API endpoints.
Reference: @specs/002-fullstack-web-app/api/rest-endpoints.md
Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..core.dependencies import DbSession, CurrentUser
from ..schemas.auth import SignupRequest, SigninRequest, AuthResponse
from ..services.auth import signup_user, signin_user

router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, session: DbSession):
    """
    Register a new user account.

    Reference: @specs/contracts/api-contract.md POST /api/auth/signup
    Reference: @specs/features/authentication.md User Story 1

    Args:
        request: SignupRequest with email and password

    Returns:
        AuthResponse with user and JWT token

    Raises:
        409: Email already exists
        422: Validation error
    """
    return await signup_user(session, request)


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, session: DbSession):
    """
    Authenticate existing user.

    Reference: @specs/contracts/api-contract.md POST /api/auth/signin
    Reference: @specs/features/authentication.md User Story 2

    Args:
        request: SigninRequest with email and password

    Returns:
        AuthResponse with user and JWT token

    Raises:
        401: Invalid credentials
        422: Validation error
    """
    return await signin_user(session, request)


@router.post("/signout")
async def signout(current_user: CurrentUser):
    """
    End user session.

    Reference: @specs/contracts/api-contract.md POST /api/auth/signout
    Reference: @specs/features/authentication.md User Story 3

    Note: JWT is stateless, so signout just confirms the request.
    Client is responsible for clearing the token.

    Returns:
        Success message
    """
    return {"message": "Successfully signed out"}
