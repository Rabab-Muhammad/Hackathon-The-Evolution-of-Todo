"""
Main API router aggregating all endpoint routers.
Reference: @specs/002-fullstack-web-app/api/rest-endpoints.md
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as tasks_router
from .health import router as health_router
from .chat import router as chat_router  # Phase III

# Main API router with /api prefix
# Reference: @constitution REST API Conventions - All routes under /api/
api_router = APIRouter(prefix="/api")

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(chat_router, tags=["Chat"])  # Phase III: AI-powered chat
