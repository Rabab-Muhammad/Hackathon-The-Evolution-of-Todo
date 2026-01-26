"""Services package for Todo Application."""

from .task_service import (
    add_task,
    delete_task,
    update_task,
    get_task,
    get_all_tasks,
    toggle_status,
    has_tasks,
    clear_tasks,
)

__all__ = [
    "add_task",
    "delete_task",
    "update_task",
    "get_task",
    "get_all_tasks",
    "toggle_status",
    "has_tasks",
    "clear_tasks",
]
