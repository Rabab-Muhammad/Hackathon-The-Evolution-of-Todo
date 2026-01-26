"""Custom exceptions for Todo Application.

Per plan.md Exception Hierarchy and contracts/cli-interface.md Error Messages.
"""


class TodoAppError(Exception):
    """Base exception class for all Todo Application errors."""

    pass


class ValidationError(TodoAppError):
    """Raised when input validation fails.

    Used for:
    - Empty or whitespace-only titles
    - Title exceeding 100 characters
    - Description exceeding 500 characters
    - Invalid task ID format (non-integer, zero, negative)
    - Invalid menu choice
    """

    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task with the specified ID does not exist.

    Per delete_task.spec.md, update_task.spec.md, mark_complete.spec.md:
    Error message format: "Task with ID {id} not found."
    """

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")


class EmptyTaskListError(TodoAppError):
    """Raised when an operation requires tasks but none exist.

    Per delete_task.spec.md, update_task.spec.md, mark_complete.spec.md:
    Operations should check for empty list before prompting for ID.
    """

    pass
