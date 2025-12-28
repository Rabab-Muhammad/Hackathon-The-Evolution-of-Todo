"""
Database connection and session management.
Reference: @specs/002-fullstack-web-app/database/schema.md
"""

from sqlmodel import SQLModel, Session, create_engine
from .config import get_settings

# Create engine with connection pool settings
# Reference: @specs/research.md - Neon Serverless PostgreSQL
settings = get_settings()
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connection before use
)


def create_db_and_tables():
    """Create all tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yield a database session for dependency injection.
    Reference: @specs/architecture.md Service Layer
    """
    with Session(engine) as session:
        yield session
