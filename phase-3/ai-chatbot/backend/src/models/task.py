"""
Task SQLModel entity.
Reference: @specs/002-fullstack-web-app/database/schema.md
Reference: @specs/002-fullstack-web-app/data-model.md
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """
    Represents a todo item owned by a user.

    Table: tasks
    Reference: @specs/database/schema.md - Task Entity
    """

    __tablename__ = "tasks"

    # Primary key - UUID auto-generated
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Foreign key to user
    # Reference: @specs/database/schema.md - ON DELETE CASCADE
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
    )

    # Task title - required, max 100 chars
    # Reference: @specs/features/task-crud.md FR-CRUD-002
    title: str = Field(
        max_length=100,
        nullable=False,
    )

    # Task description - optional, max 500 chars
    # Reference: @specs/features/task-crud.md FR-CRUD-003
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        nullable=True,
    )

    # Completion status - default false
    # Reference: @specs/features/task-crud.md FR-CRUD-004
    completed: bool = Field(
        default=False,
        nullable=False,
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
