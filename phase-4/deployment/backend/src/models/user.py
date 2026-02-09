"""
User SQLModel entity.
Reference: @specs/002-fullstack-web-app/database/schema.md
Reference: @specs/002-fullstack-web-app/data-model.md
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Represents an authenticated application user.

    Table: users
    Reference: @specs/database/schema.md - User Entity
    """

    __tablename__ = "users"

    # Primary key - UUID auto-generated
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Email - unique, required
    # Reference: @specs/features/authentication.md FR-001
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
    )

    # Password hash - bcrypt hashed
    # Reference: @specs/features/authentication.md FR-005
    password_hash: str = Field(
        max_length=255,
        nullable=False,
    )

    # Timestamp - auto-set on creation
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
