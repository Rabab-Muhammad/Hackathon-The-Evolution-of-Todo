"""
Test fixtures for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/plan.md (Testing section)

This module provides pytest fixtures for database models, sessions,
and test data used across all test modules.
"""
import pytest
from uuid import uuid4
from datetime import datetime
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message


@pytest.fixture(name="engine")
def engine_fixture():
    """
    Create in-memory SQLite engine for testing.

    Uses StaticPool to maintain single connection across test.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """
    Create database session for testing.

    Yields session and rolls back after test.
    """
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """
    Create test user.

    Returns:
        User instance with test data
    """
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="$2b$12$test_hash"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_task")
def test_task_fixture(session: Session, test_user: User):
    """
    Create test task for test user.

    Returns:
        Task instance with test data
    """
    task = Task(
        id=uuid4(),
        user_id=test_user.id,
        title="Test Task",
        description="Test Description",
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="test_conversation")
def test_conversation_fixture(session: Session, test_user: User):
    """
    Create test conversation for test user.

    Returns:
        Conversation instance with test data
    """
    conversation = Conversation(
        id=uuid4(),
        user_id=test_user.id
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


@pytest.fixture(name="test_message")
def test_message_fixture(session: Session, test_user: User, test_conversation: Conversation):
    """
    Create test message in test conversation.

    Returns:
        Message instance with test data
    """
    message = Message(
        id=uuid4(),
        user_id=test_user.id,
        conversation_id=test_conversation.id,
        role="user",
        content="Test message"
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
