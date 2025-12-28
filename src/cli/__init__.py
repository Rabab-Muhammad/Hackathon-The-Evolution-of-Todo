"""CLI package for Todo Application."""

from .menu import run
from .handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_delete_task,
    handle_update_task,
    handle_toggle_status,
)

from .colors import Colors, Emojis

__all__ = [
    "run",
    "handle_add_task",
    "handle_view_tasks",
    "handle_delete_task",
    "handle_update_task",
    "handle_toggle_status",
]
