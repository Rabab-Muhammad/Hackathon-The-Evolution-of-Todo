"""
FastAPI application entry point.
Reference: @specs/002-fullstack-web-app/plan.md
Reference: @specs/002-fullstack-web-app/architecture.md
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .core.config import get_settings
from .core.database import create_db_and_tables
from .api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Creates database tables on startup.
    """
    # Startup: Create tables
    create_db_and_tables()
    yield
    # Shutdown: Nothing to do


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
# Reference: @specs/architecture.md
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for validation errors
# Reference: @specs/api/rest-endpoints.md Error Response Format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors with consistent format.
    """
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # Skip 'body'
        details.append({"field": field, "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": details,
            }
        },
    )


# Include API router
app.include_router(api_router)


# Root endpoint redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation."""
    return {"message": "Todo API - Visit /docs for documentation"}
