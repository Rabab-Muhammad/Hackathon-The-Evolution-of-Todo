"""
Task request/response schemas.
Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """
    Task creation request.
    Reference: @specs/contracts/api-contract.md POST /api/tasks
    """

    title: str = Field(
        ..., min_length=1, max_length=100, description="Task title (required)"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Task description (optional)"
    )


class TaskUpdateRequest(BaseModel):
    """
    Task update request.
    Reference: @specs/contracts/api-contract.md PUT /api/tasks/{task_id}
    """

    title: str = Field(
        ..., min_length=1, max_length=100, description="Task title (required)"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Task description (optional)"
    )


class TaskData(BaseModel):
    """
    Task data in responses.
    Reference: @specs/contracts/api-contract.md
    """

    id: UUID
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    """
    Single task response wrapper.
    Reference: @specs/contracts/api-contract.md
    """

    task: TaskData


class TaskListResponse(BaseModel):
    """
    Task list response.
    Reference: @specs/contracts/api-contract.md GET /api/tasks
    """

    tasks: list[TaskData]
    count: int
