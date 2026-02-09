"""
Integration tests for chat API endpoint.
Reference: @specs/003-ai-chatbot/api/chat-endpoint.md

Tests verify:
- JWT authentication and user_id validation
- Conversation creation and continuation
- Message persistence
- Agent processing and tool invocation
- Error handling (401, 403, 404, 422, 500)
"""
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from src.main import app
from src.core.security import create_access_token


client = TestClient(app)


class TestChatEndpoint:
    """Test POST /api/{user_id}/chat endpoint."""

    def test_chat_creates_new_conversation(self, test_user):
        """Test creating new conversation when conversation_id not provided."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["tool"] == "add_task"

    def test_chat_continues_existing_conversation(self, test_user, test_conversation):
        """Test continuing existing conversation."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": str(test_conversation.id),
                "message": "Show me my tasks"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == str(test_conversation.id)

    def test_chat_requires_authentication(self, test_user):
        """Test that endpoint requires JWT token."""
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add a task"}
        )

        assert response.status_code == 401

    def test_chat_validates_user_id_match(self, test_user):
        """Test that path user_id must match JWT user_id."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
        other_user_id = str(uuid4())

        response = client.post(
            f"/api/{other_user_id}/chat",
            json={"message": "Add a task"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403
        assert "FORBIDDEN" in response.json()["detail"]["error"]["code"]

    def test_chat_validates_empty_message(self, test_user):
        """Test that empty message returns 422."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": ""},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422
        assert "VALIDATION_ERROR" in response.json()["detail"]["error"]["code"]

    def test_chat_validates_message_length(self, test_user):
        """Test that message >2000 chars returns 422."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "x" * 2001},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422

    def test_chat_conversation_not_found(self, test_user):
        """Test that non-existent conversation returns 404."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})
        fake_conversation_id = str(uuid4())

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": fake_conversation_id,
                "message": "Show me my tasks"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404

    def test_chat_persists_messages(self, session, test_user):
        """Test that user and assistant messages are persisted."""
        token = create_access_token({"sub": str(test_user.id), "email": test_user.email})

        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        conversation_id = response.json()["conversation_id"]

        # Verify messages were persisted
        from src.models.message import Message
        from sqlmodel import select

        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()

        assert len(messages) == 2  # User message + assistant message
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"
