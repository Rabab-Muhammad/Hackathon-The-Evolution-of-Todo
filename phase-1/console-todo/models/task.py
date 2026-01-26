"""Task entity for Todo Application.

This module defines the Task dataclass representing a single todo item.
Per data-model.md specifications.
"""

from dataclasses import dataclass

# Status constants per add_task.spec.md FR-003
INCOMPLETE: str = "incomplete"
COMPLETE: str = "complete"


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Auto-generated unique identifier (>= 1, never recycled)
        title: Required task title (1-100 characters)
        description: Optional task description (0-500 characters)
        status: Task completion status ("incomplete" or "complete")

    Per data-model.md Entity Design:
    - ID is immutable after creation
    - Title is required, non-empty
    - Description is optional, may be empty string
    - Status defaults to "incomplete" for new tasks
    """

    id: int
    title: str
    description: str
    status: str = INCOMPLETE
