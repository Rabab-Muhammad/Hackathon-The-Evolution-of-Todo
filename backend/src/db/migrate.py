"""
Database migration script.
Reference: @specs/002-fullstack-web-app/database/schema.md Migration Strategy
"""

import sys
from pathlib import Path

# Add the backend directory to the path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlmodel import SQLModel
from src.core.database import engine
from src.models import User, Task  # noqa: F401 - Import to register models


def run_migrations():
    """
    Create all database tables.

    This creates:
    1. users table with unique email constraint
    2. tasks table with foreign key to users

    Reference: @specs/database/schema.md
    """
    print("Running database migrations...")

    try:
        # Create all tables
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully!")

        # List created tables
        print("\nCreated tables:")
        for table_name in SQLModel.metadata.tables.keys():
            print(f"  - {table_name}")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_migrations()
