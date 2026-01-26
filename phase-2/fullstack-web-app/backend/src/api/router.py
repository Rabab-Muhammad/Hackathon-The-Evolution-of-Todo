"""
Main API router aggregating all endpoint routers.
Reference: @specs/002-fullstack-web-app/api/rest-endpoints.md
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as tasks_router
from .health import router as health_router

# Main API router with /api prefix
# Reference: @constitution REST API Conventions - All routes under /api/
api_router = APIRouter(prefix="/api")

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
