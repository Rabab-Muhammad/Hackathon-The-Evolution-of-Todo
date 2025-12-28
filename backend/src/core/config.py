"""
Configuration module for environment variables.
Reference: @specs/002-fullstack-web-app/plan.md Section 9
"""

import os
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database configuration
    # Reference: @specs/database/schema.md
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # JWT configuration
    # Reference: @specs/api/jwt-auth.md
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # CORS configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    def __init__(self):
        """Validate required settings on initialization."""
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        if not self.BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required")
        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
