"""
Task API endpoints.
Reference: @specs/002-fullstack-web-app/api/rest-endpoints.md
Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ..core.dependencies import DbSession, CurrentUser
from ..schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
)
from ..services.task import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task,
)

router = APIRouter()


@router.get("", response_model=TaskListResponse)
async def list_tasks(current_user: CurrentUser, session: DbSession):
    """
    List all tasks for authenticated user.

    Reference: @specs/contracts/api-contract.md GET /api/tasks
    Reference: @specs/features/task-crud.md User Story 2

    Returns:
        TaskListResponse with tasks array and count
    """
    return await get_user_tasks(session, current_user.id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    request: TaskCreateRequest, current_user: CurrentUser, session: DbSession
):
    """
    Create a new task.

    Reference: @specs/contracts/api-contract.md POST /api/tasks
    Reference: @specs/features/task-crud.md User Story 1

    Args:
        request: TaskCreateRequest with title and optional description

    Returns:
        TaskResponse with created task
    """
    return await create_task(session, current_user.id, request)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, current_user: CurrentUser, session: DbSession):
    """
    Get a single task by ID.

    Reference: @specs/contracts/api-contract.md GET /api/tasks/{task_id}

    Args:
        task_id: UUID of the task

    Returns:
        TaskResponse with task

    Raises:
        404: Task not found or not owned by user
    """
    return await get_task_by_id(session, current_user.id, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: UUID,
    request: TaskUpdateRequest,
    current_user: CurrentUser,
    session: DbSession,
):
    """
    Update an existing task.

    Reference: @specs/contracts/api-contract.md PUT /api/tasks/{task_id}
    Reference: @specs/features/task-crud.md User Story 3

    Args:
        task_id: UUID of the task
        request: TaskUpdateRequest with title and optional description

    Returns:
        TaskResponse with updated task

    Raises:
        404: Task not found or not owned by user
    """
    return await update_task(session, current_user.id, task_id, request)


@router.delete("/{task_id}")
async def delete_existing_task(
    task_id: UUID, current_user: CurrentUser, session: DbSession
):
    """
    Delete a task.

    Reference: @specs/contracts/api-contract.md DELETE /api/tasks/{task_id}
    Reference: @specs/features/task-crud.md User Story 4

    Args:
        task_id: UUID of the task

    Returns:
        Success message

    Raises:
        404: Task not found or not owned by user
    """
    return await delete_task(session, current_user.id, task_id)


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: UUID, current_user: CurrentUser, session: DbSession
):
    """
    Toggle task completion status.

    Reference: @specs/contracts/api-contract.md PATCH /api/tasks/{task_id}/toggle
    Reference: @specs/features/task-crud.md User Story 5

    Args:
        task_id: UUID of the task

    Returns:
        TaskResponse with toggled task

    Raises:
        404: Task not found or not owned by user
    """
    return await toggle_task(session, current_user.id, task_id)
