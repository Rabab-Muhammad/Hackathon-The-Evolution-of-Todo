"""
Message model for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/database/schema.md
"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """
    Message represents a single message in a conversation.

    Attributes:
        id: Unique message identifier
        user_id: Foreign key to users table (owner of conversation)
        conversation_id: Foreign key to conversations table
        role: Message sender role ('user' or 'assistant')
        content: Message text content
        created_at: Timestamp when message was created

    Relationships:
        - Belongs to one User (via user_id)
        - Belongs to one Conversation (via conversation_id)

    Indexes:
        - conversation_id (for efficient conversation history queries)
        - created_at (for chronological ordering)
        - user_id (for user isolation enforcement)

    Validation:
        - role must be 'user' or 'assistant'
        - content max length: 2000 characters (per spec FR-012)
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(max_length=2000, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-02-08T10:30:00Z"
            }
        }
