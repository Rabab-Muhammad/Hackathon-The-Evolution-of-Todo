"""Input validation functions for Todo Application.

Per contracts/cli-interface.md Validation Contract and all spec files
Edge Cases & Validation Rules sections.
"""

from exceptions import ValidationError

# Constants from data-model.md
MAX_TITLE_LENGTH: int = 100
MAX_DESCRIPTION_LENGTH: int = 500
MIN_MENU_CHOICE: int = 1
MAX_MENU_CHOICE: int = 6


def validate_menu_choice(input_str: str) -> int:
    """Validate menu choice input and return integer 1-6.

    Args:
        input_str: User input string

    Returns:
        Valid menu choice as integer (1-6)

    Raises:
        ValidationError: If input is not a valid integer between 1 and 6

    Per contracts/cli-interface.md Main Menu Contract.
    """
    try:
        choice = int(input_str.strip())
        if choice < MIN_MENU_CHOICE or choice > MAX_MENU_CHOICE:
            raise ValidationError(
                f"Invalid choice. Please enter a number between {MIN_MENU_CHOICE} and {MAX_MENU_CHOICE}."
            )
        return choice
    except ValueError:
        raise ValidationError(
            f"Invalid choice. Please enter a number between {MIN_MENU_CHOICE} and {MAX_MENU_CHOICE}."
        )


def validate_task_id(input_str: str) -> int:
    """Validate task ID input and return positive integer.

    Args:
        input_str: User input string

    Returns:
        Valid task ID as positive integer

    Raises:
        ValidationError: If input is not a valid positive integer

    Per delete_task.spec.md, update_task.spec.md, mark_complete.spec.md
    Edge Cases & Validation Rules.
    """
    try:
        task_id = int(input_str.strip())
        if task_id <= 0:
            raise ValidationError(
                "Invalid input. Please enter a valid task ID (positive integer)."
            )
        return task_id
    except ValueError:
        raise ValidationError(
            "Invalid input. Please enter a valid task ID (positive integer)."
        )


def validate_title(title: str) -> str:
    """Validate task title and return trimmed string.

    Args:
        title: User input title string

    Returns:
        Validated and trimmed title string

    Raises:
        ValidationError: If title is empty, whitespace-only, or exceeds 100 chars

    Per add_task.spec.md Edge Cases & Validation Rules:
    - Empty title: Reject with error
    - Whitespace-only title: Treat as empty, reject
    - Title exceeds 100 characters: Reject with error
    """
    trimmed = title.strip()

    if not trimmed:
        raise ValidationError(
            "Error: Title cannot be empty. Please enter a valid title."
        )

    if len(title) > MAX_TITLE_LENGTH:
        raise ValidationError(
            f"Error: Title exceeds maximum length of {MAX_TITLE_LENGTH} characters."
        )

    return trimmed


def validate_description(description: str) -> str:
    """Validate task description and return string.

    Args:
        description: User input description string

    Returns:
        Validated description string (may be empty)

    Raises:
        ValidationError: If description exceeds 500 characters

    Per add_task.spec.md Edge Cases & Validation Rules:
    - Empty description: Accept (optional field)
    - Description exceeds 500 characters: Reject with error
    """
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Error: Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH} characters."
        )

    return description
