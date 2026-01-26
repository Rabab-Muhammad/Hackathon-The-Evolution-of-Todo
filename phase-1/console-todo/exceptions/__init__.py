"""Exceptions package for Todo Application."""

from .errors import (
    TodoAppError,
    ValidationError,
    TaskNotFoundError,
    EmptyTaskListError,
)

__all__ = [
    "TodoAppError",
    "ValidationError",
    "TaskNotFoundError",
    "EmptyTaskListError",
]
