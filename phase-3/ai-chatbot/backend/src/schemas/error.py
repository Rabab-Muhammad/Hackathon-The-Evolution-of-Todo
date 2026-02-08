"""
Error response schemas.
Reference: @specs/002-fullstack-web-app/api/rest-endpoints.md Error Response Format
Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
"""

from typing import Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Field-level error detail."""

    field: str
    message: str


class ErrorBody(BaseModel):
    """
    Error response body structure.

    Reference: @specs/api/rest-endpoints.md Error Response Format
    """

    code: str
    message: str
    details: Optional[list[ErrorDetail]] = None


class ErrorResponse(BaseModel):
    """
    Standard error response wrapper.

    Example:
    {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input",
            "details": [{"field": "email", "message": "Invalid email format"}]
        }
    }
    """

    error: ErrorBody


# Error codes as defined in spec
# Reference: @specs/contracts/api-contract.md Error Codes
class ErrorCode:
    """Standard error codes."""

    VALIDATION_ERROR = "VALIDATION_ERROR"  # 422
    UNAUTHORIZED = "UNAUTHORIZED"  # 401
    NOT_FOUND = "NOT_FOUND"  # 404
    CONFLICT = "CONFLICT"  # 409
    INTERNAL_ERROR = "INTERNAL_ERROR"  # 500
