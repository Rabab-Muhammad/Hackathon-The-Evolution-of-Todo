"""
Task business logic.
Reference: @specs/002-fullstack-web-app/features/task-crud.md
"""

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..models.task import Task
from ..schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
    TaskData,
)


def _task_not_found_error() -> HTTPException:
    """
    Return 404 error for task not found.
    Reference: @specs/contracts/api-contract.md - Returns 404 to hide existence
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Task not found"}},
    )


async def create_task(
    session: Session, user_id: UUID, request: TaskCreateRequest
) -> TaskResponse:
    """
    Create a new task for user.

    Reference: @specs/features/task-crud.md User Story 1
    Reference: @specs/features/task-crud.md Create Task Flow

    Args:
        session: Database session
        user_id: Owner's user ID
        request: TaskCreateRequest with title and description

    Returns:
        TaskResponse with created task
    """
    task = Task(
        user_id=user_id,
        title=request.title,
        description=request.description,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(task=TaskData.model_validate(task))


async def get_user_tasks(session: Session, user_id: UUID) -> TaskListResponse:
    """
    Get all tasks for user.

    Reference: @specs/features/task-crud.md User Story 2
    Reference: @specs/features/task-crud.md Read Tasks Flow
    Reference: @constitution User Isolation - Filter by user_id

    Args:
        session: Database session
        user_id: Owner's user ID

    Returns:
        TaskListResponse with tasks array and count
    """
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = session.exec(statement).all()

    task_data = [TaskData.model_validate(task) for task in tasks]

    return TaskListResponse(tasks=task_data, count=len(task_data))


async def get_task_by_id(
    session: Session, user_id: UUID, task_id: UUID
) -> TaskResponse:
    """
    Get a single task by ID.

    Reference: @specs/contracts/api-contract.md GET /api/tasks/{task_id}
    Reference: @constitution User Isolation - Verify ownership

    Args:
        session: Database session
        user_id: Owner's user ID
        task_id: Task UUID

    Returns:
        TaskResponse with task

    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise _task_not_found_error()

    return TaskResponse(task=TaskData.model_validate(task))


async def update_task(
    session: Session, user_id: UUID, task_id: UUID, request: TaskUpdateRequest
) -> TaskResponse:
    """
    Update an existing task.

    Reference: @specs/features/task-crud.md User Story 3
    Reference: @specs/features/task-crud.md Update Task Flow

    Args:
        session: Database session
        user_id: Owner's user ID
        task_id: Task UUID
        request: TaskUpdateRequest with title and description

    Returns:
        TaskResponse with updated task

    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise _task_not_found_error()

    # Update fields
    task.title = request.title
    task.description = request.description
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(task=TaskData.model_validate(task))


async def delete_task(session: Session, user_id: UUID, task_id: UUID) -> dict:
    """
    Delete a task.

    Reference: @specs/features/task-crud.md User Story 4
    Reference: @specs/features/task-crud.md Delete Task Flow

    Args:
        session: Database session
        user_id: Owner's user ID
        task_id: Task UUID

    Returns:
        Success message

    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise _task_not_found_error()

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


async def toggle_task(session: Session, user_id: UUID, task_id: UUID) -> TaskResponse:
    """
    Toggle task completion status.

    Reference: @specs/features/task-crud.md User Story 5

    Args:
        session: Database session
        user_id: Owner's user ID
        task_id: Task UUID

    Returns:
        TaskResponse with toggled task

    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise _task_not_found_error()

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(task=TaskData.model_validate(task))
