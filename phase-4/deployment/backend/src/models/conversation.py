"""
Conversation model for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/database/schema.md
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    """
    Conversation represents a chat session between user and AI assistant.

    Attributes:
        id: Unique conversation identifier
        user_id: Foreign key to users table (owner of conversation)
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated

    Relationships:
        - Belongs to one User (via user_id)
        - Has many Messages (one-to-many)

    Indexes:
        - user_id (for efficient user-scoped queries)
        - updated_at (for sorting by recent activity)
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "created_at": "2026-02-08T10:30:00Z",
                "updated_at": "2026-02-08T14:20:00Z"
            }
        }
