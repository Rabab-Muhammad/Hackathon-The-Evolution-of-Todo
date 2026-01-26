"""
Database connection and session management.
Reference: @specs/002-fullstack-web-app/database/schema.md
"""

from sqlmodel import SQLModel, Session, create_engine
from .config import get_settings

# Lazy-initialized engine
# Reference: @specs/research.md - Neon Serverless PostgreSQL
_engine = None


def get_engine():
    """Get or create the database engine (lazy initialization)."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=False,  # Set to True for SQL query logging
            pool_pre_ping=True,  # Verify connection before use
        )
    return _engine


def create_db_and_tables():
    """Create all tables defined in SQLModel models."""
    SQLModel.metadata.create_all(get_engine())


def get_session():
    """
    Yield a database session for dependency injection.
    Reference: @specs/architecture.md Service Layer
    """
    with Session(get_engine()) as session:
        yield session
