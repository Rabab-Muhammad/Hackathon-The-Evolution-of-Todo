"""
Health check endpoint.
Reference: @specs/002-fullstack-web-app/quickstart.md Verification Steps
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns: {"status": "ok"}
    """
    return {"status": "ok"}
