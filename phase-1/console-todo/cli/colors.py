"""ANSI color utilities for Todo Application CLI.

Provides color constants and helper functions for colorful terminal output.
"""


# ANSI Color Codes
class Colors:
    """ANSI escape codes for terminal colors."""

    # Reset
    RESET = "\033[0m"

    # Regular Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright Colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"


# Emojis
class Emojis:
    """Emoji constants for CLI display."""

    # Menu
    APP_TITLE = "📋"
    ADD = "➕"
    DELETE = "🗑️"
    UPDATE = "✏️"
    VIEW = "📄"
    TOGGLE = "🔄"
    EXIT = "👋"

    # Task Status
    COMPLETE = "✅"
    INCOMPLETE = "⬜"

    # Feedback
    SUCCESS = "✨"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    PROMPT = "👉"

    # Misc
    TASK = "📌"
    ARROW = "➜"


# Color helper functions
def title(text: str) -> str:
    """Format text as a title (bold cyan)."""
    return f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}"


def header(text: str) -> str:
    """Format text as a header (bold yellow)."""
    return f"{Colors.BOLD}{Colors.YELLOW}{text}{Colors.RESET}"


def success(text: str) -> str:
    """Format text as success message (green)."""
    return f"{Colors.GREEN}{text}{Colors.RESET}"


def error(text: str) -> str:
    """Format text as error message (red)."""
    return f"{Colors.RED}{text}{Colors.RESET}"


def warning(text: str) -> str:
    """Format text as warning message (yellow)."""
    return f"{Colors.YELLOW}{text}{Colors.RESET}"


def info(text: str) -> str:
    """Format text as info message (blue)."""
    return f"{Colors.BLUE}{text}{Colors.RESET}"


def dim(text: str) -> str:
    """Format text as dimmed (gray)."""
    return f"{Colors.DIM}{text}{Colors.RESET}"


def menu_option(number: int, text: str) -> str:
    """Format a menu option."""
    return f"{Colors.BRIGHT_WHITE}{number}.{Colors.RESET} {text}"


def prompt(text: str) -> str:
    """Format a prompt text (bright cyan)."""
    return f"{Colors.BRIGHT_CYAN}{text}{Colors.RESET}"


def task_id(id_num: int) -> str:
    """Format a task ID (bright magenta)."""
    return f"{Colors.BRIGHT_MAGENTA}[{id_num}]{Colors.RESET}"


def task_title(text: str) -> str:
    """Format a task title (bright white)."""
    return f"{Colors.BRIGHT_WHITE}{text}{Colors.RESET}"


def complete_status() -> str:
    """Format complete status indicator."""
    return f"{Colors.GREEN}{Emojis.COMPLETE}{Colors.RESET}"


def incomplete_status() -> str:
    """Format incomplete status indicator."""
    return f"{Emojis.INCOMPLETE}"
