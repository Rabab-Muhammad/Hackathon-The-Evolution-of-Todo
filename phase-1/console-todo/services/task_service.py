"""Task service for Todo Application business logic.

Per plan.md Module Responsibilities and all spec files Functional Requirements.
Implements CRUD operations with in-memory storage.
"""

from typing import Optional

from models import Task, INCOMPLETE, COMPLETE
from exceptions import TaskNotFoundError, EmptyTaskListError

# In-memory storage per research.md Architecture Decisions
_tasks: dict[int, Task] = {}
_next_id: int = 1


def add_task(title: str, description: str = "") -> Task:
    """Create a new task with auto-generated ID.

    Args:
        title: Required task title (already validated)
        description: Optional task description (default empty)

    Returns:
        Newly created Task with auto-generated ID

    Per add_task.spec.md:
    - FR-002: Auto-generate unique task ID
    - FR-003: Default status is "incomplete"
    - FR-007: IDs are sequential positive integers starting from 1
    """
    global _next_id

    task = Task(
        id=_next_id,
        title=title,
        description=description,
        status=INCOMPLETE,
    )

    _tasks[_next_id] = task
    _next_id += 1

    return task


def get_task(task_id: int) -> Task:
    """Retrieve a single task by ID.

    Args:
        task_id: The task ID to look up

    Returns:
        The Task with the given ID

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Per update_task.spec.md FR-005, delete_task.spec.md FR-002.
    """
    if task_id not in _tasks:
        raise TaskNotFoundError(task_id)

    return _tasks[task_id]


def get_all_tasks() -> list[Task]:
    """Retrieve all tasks sorted by ID ascending.

    Returns:
        List of all tasks sorted by ID

    Per view_tasks.spec.md FR-006: Tasks displayed in ascending order by ID.
    """
    return sorted(_tasks.values(), key=lambda t: t.id)


def has_tasks() -> bool:
    """Check if any tasks exist.

    Returns:
        True if at least one task exists, False otherwise

    Per delete_task.spec.md, update_task.spec.md, mark_complete.spec.md
    pre-check requirements for empty task list.
    """
    return len(_tasks) > 0


def delete_task(task_id: int) -> Task:
    """Delete a task by ID.

    Args:
        task_id: The task ID to delete

    Returns:
        The deleted Task (for confirmation display)

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Per delete_task.spec.md:
    - FR-001: Delete task by ID
    - FR-004: Permanently remove from memory (no undo)
    - FR-006: Deletion does not affect other tasks' IDs
    - Data Model: IDs are not recycled
    """
    if task_id not in _tasks:
        raise TaskNotFoundError(task_id)

    task = _tasks[task_id]
    del _tasks[task_id]
    return task


def update_task(
    task_id: int, title: Optional[str] = None, description: Optional[str] = None
) -> tuple[Task, bool]:
    """Update a task's title and/or description.

    Args:
        task_id: The task ID to update
        title: New title (None to keep current)
        description: New description (None to keep current)

    Returns:
        Tuple of (updated Task, bool indicating if changes were made)

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Per update_task.spec.md:
    - FR-001: Update title by ID
    - FR-002: Update description by ID
    - FR-003: Update both in single operation
    - FR-004: Skip field if None (keep current)
    - FR-008: Update does not change ID or status
    """
    if task_id not in _tasks:
        raise TaskNotFoundError(task_id)

    task = _tasks[task_id]
    changes_made = False

    if title is not None:
        task.title = title
        changes_made = True

    if description is not None:
        task.description = description
        changes_made = True

    return task, changes_made


def toggle_status(task_id: int) -> Task:
    """Toggle a task's completion status.

    Args:
        task_id: The task ID to toggle

    Returns:
        The updated Task with new status

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Per mark_complete.spec.md:
    - FR-002: Change "incomplete" to "complete"
    - FR-003: Change "complete" to "incomplete"
    - FR-007: Toggle does not affect ID, title, or description
    """
    if task_id not in _tasks:
        raise TaskNotFoundError(task_id)

    task = _tasks[task_id]
    old_status = task.status

    if task.status == INCOMPLETE:
        task.status = COMPLETE
    else:
        task.status = INCOMPLETE

    return task


def clear_tasks() -> None:
    """Clear all tasks and reset ID counter.

    Used for testing purposes only.
    """
    global _tasks, _next_id
    _tasks = {}
    _next_id = 1
