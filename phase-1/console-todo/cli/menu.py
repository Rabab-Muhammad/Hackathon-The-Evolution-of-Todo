"""Main menu for Todo Application.

Per contracts/cli-interface.md Main Menu Contract and all spec files CLI Flow Examples.
"""

import sys

from validators import validate_menu_choice
from exceptions import ValidationError
from cli.handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_delete_task,
    handle_update_task,
    handle_toggle_status,
)
from cli.colors import (
    title,
    menu_option,
    prompt,
    error,
    success,
    Emojis,
)


def display_menu() -> None:
    """Display the main menu.

    Per contracts/cli-interface.md Main Menu Contract Display.
    """
    print(f"\n{title(f'{Emojis.APP_TITLE} === Todo Application === {Emojis.APP_TITLE}')}")
    print(menu_option(1, f"{Emojis.ADD} Add Task"))
    print(menu_option(2, f"{Emojis.DELETE}  Delete Task"))
    print(menu_option(3, f"{Emojis.UPDATE}  Update Task"))
    print(menu_option(4, f"{Emojis.VIEW} View Tasks"))
    print(menu_option(5, f"{Emojis.TOGGLE} Mark Complete/Incomplete"))
    print(menu_option(6, f"{Emojis.EXIT} Exit"))
    print()


def get_menu_choice() -> int:
    """Get and validate menu choice from user.

    Returns:
        Valid menu choice as integer (1-6)

    Per contracts/cli-interface.md Main Menu Contract Input.
    Re-prompts on invalid input per Common Patterns.
    """
    while True:
        choice_input = input(prompt(f"{Emojis.PROMPT} Enter choice: "))
        try:
            return validate_menu_choice(choice_input)
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")
            print()


def run() -> None:
    """Run the main application loop.

    Per spec.md FR-006: System returns to main menu after each operation.
    Per contracts/cli-interface.md Exit Contract.
    """
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == 1:
            handle_add_task()
        elif choice == 2:
            handle_delete_task()
        elif choice == 3:
            handle_update_task()
        elif choice == 4:
            handle_view_tasks()
        elif choice == 5:
            handle_toggle_status()
        elif choice == 6:
            # Exit per contracts/cli-interface.md Exit Contract
            print(f"\n{success(f'{Emojis.EXIT} Goodbye!')}\n")
            sys.exit(0)
