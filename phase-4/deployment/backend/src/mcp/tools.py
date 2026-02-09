"""
MCP Tools implementation for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/mcp/tools.md

This module implements all 5 MCP tools for task management:
- add_task: Create new task
- list_tasks: Retrieve user's tasks
- update_task: Modify task title/description
- delete_task: Remove task
- complete_task: Mark task as completed

All tools are stateless and enforce user_id scoping for user isolation.
"""
from typing import Dict, List, Optional, Any
from uuid import UUID

from sqlmodel import Session, select
from src.core.database import get_engine
from src.models.task import Task


def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        user_id: UUID of the authenticated user
        title: Task title (1-100 characters)
        description: Optional task description (max 500 characters)

    Returns:
        Dict containing created task data

    Raises:
        ValueError: If validation fails (title empty, too long, etc.)

    Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md (Tool 1)
    """
    # Validation
    if not title or len(title.strip()) == 0:
        raise ValueError("Title is required")
    if len(title) > 100:
        raise ValueError("Title must be 100 characters or less")
    if description and len(description) > 500:
        raise ValueError("Description must be 500 characters or less")

    # Create task
    with Session(get_engine()) as session:
        task = Task(
            user_id=UUID(user_id),
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


def list_tasks(user_id: str, completed: Optional[bool] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieve all tasks for the authenticated user, optionally filtered by completion status.

    Args:
        user_id: UUID of the authenticated user
        completed: Optional filter - True (completed only), False (incomplete only), None (all)

    Returns:
        Dict with "tasks" key containing list of task objects

    Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md (Tool 2)
    """
    with Session(get_engine()) as session:
        # Build query with user_id filter
        statement = select(Task).where(Task.user_id == UUID(user_id))

        # Add completed filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Order by created_at descending (newest first)
        statement = statement.order_by(Task.created_at.desc())

        tasks = session.exec(statement).all()

        return {
            "tasks": [
                {
                    "id": str(task.id),
                    "user_id": str(task.user_id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]
        }


def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Modify the title and/or description of an existing task.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to update
        title: New task title (optional, 1-100 characters if provided)
        description: New task description (optional, max 500 characters if provided)

    Returns:
        Dict containing updated task data

    Raises:
        ValueError: If validation fails or no fields provided
        KeyError: If task not found or doesn't belong to user (404)

    Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md (Tool 3)
    """
    # Validation
    if title is None and description is None:
        raise ValueError("At least one field (title or description) must be provided")
    if title is not None and len(title) > 100:
        raise ValueError("Title must be 100 characters or less")
    if description is not None and len(description) > 500:
        raise ValueError("Description must be 500 characters or less")

    with Session(get_engine()) as session:
        # Find task with user_id scoping (user isolation)
        statement = select(Task).where(
            Task.id == UUID(task_id),
            Task.user_id == UUID(user_id)
        )
        task = session.exec(statement).first()

        if not task:
            raise KeyError("Task not found")

        # Update fields
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Permanently remove a task from the user's list.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to delete

    Returns:
        Dict with success confirmation and deleted task ID

    Raises:
        KeyError: If task not found or doesn't belong to user (404)

    Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md (Tool 4)
    """
    with Session(get_engine()) as session:
        # Find task with user_id scoping (user isolation)
        statement = select(Task).where(
            Task.id == UUID(task_id),
            Task.user_id == UUID(user_id)
        )
        task = session.exec(statement).first()

        if not task:
            raise KeyError("Task not found")

        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": "Task deleted successfully",
            "deleted_task_id": str(task_id)
        }


def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: UUID of the authenticated user
        task_id: UUID of the task to mark complete

    Returns:
        Dict containing updated task data with completed=True

    Raises:
        KeyError: If task not found or doesn't belong to user (404)

    Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md (Tool 5)
    """
    with Session(get_engine()) as session:
        # Find task with user_id scoping (user isolation)
        statement = select(Task).where(
            Task.id == UUID(task_id),
            Task.user_id == UUID(user_id)
        )
        task = session.exec(statement).first()

        if not task:
            raise KeyError("Task not found")

        # Mark as completed
        task.completed = True

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
