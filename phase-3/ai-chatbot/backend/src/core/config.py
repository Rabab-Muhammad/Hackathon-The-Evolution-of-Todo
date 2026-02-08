"""
Configuration module for environment variables.
Reference: @specs/002-fullstack-web-app/plan.md Section 9
"""

import os
import sys
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # JWT configuration
    # Reference: @specs/api/jwt-auth.md
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # CORS configuration
    # Can be overridden via CORS_ORIGINS env var (comma-separated)
    CORS_ORIGINS: list[str] = []

    def _load_cors_origins(self) -> list[str]:
        """Load CORS origins from environment or use defaults."""
        env_origins = os.getenv("CORS_ORIGINS", "")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

    def __init__(self):
        """Load and validate required settings on initialization."""
        # Database configuration
        # Reference: @specs/database/schema.md
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")

        # JWT secret
        # Reference: @specs/api/jwt-auth.md
        self.BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

        # Validate required settings
        errors = []
        if not self.DATABASE_URL:
            errors.append("DATABASE_URL environment variable is required")
        if not self.BETTER_AUTH_SECRET:
            errors.append("BETTER_AUTH_SECRET environment variable is required")
        elif len(self.BETTER_AUTH_SECRET) < 32:
            errors.append("BETTER_AUTH_SECRET must be at least 32 characters")

        if errors:
            # Print errors to stderr for Railway logs
            for error in errors:
                print(f"Configuration Error: {error}", file=sys.stderr)
            raise ValueError("; ".join(errors))

        # Load CORS origins
        self.CORS_ORIGINS = self._load_cors_origins()


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
