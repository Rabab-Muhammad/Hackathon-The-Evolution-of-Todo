"""
Authentication request/response schemas.
Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """
    User registration request.
    Reference: @specs/contracts/api-contract.md POST /api/auth/signup
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=8, description="Password (minimum 8 characters)"
    )


class SigninRequest(BaseModel):
    """
    User login request.
    Reference: @specs/contracts/api-contract.md POST /api/auth/signin
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """
    User data in responses.
    Reference: @specs/contracts/api-contract.md
    """

    id: UUID
    email: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """
    Authentication response with user and token.
    Reference: @specs/contracts/api-contract.md
    """

    user: UserResponse
    token: str
