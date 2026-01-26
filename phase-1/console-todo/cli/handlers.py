"""CLI handlers for Todo Application operations.

Per contracts/cli-interface.md Operation Contracts and all spec files CLI Flow Examples.
"""

from models import INCOMPLETE, COMPLETE
from services import (
    add_task,
    get_task,
    get_all_tasks,
    has_tasks,
    delete_task,
    update_task,
    toggle_status,
)
from validators import validate_task_id, validate_title, validate_description
from exceptions import ValidationError, TaskNotFoundError
from cli.colors import (
    header,
    success,
    error,
    warning,
    info,
    dim,
    prompt,
    task_id as fmt_task_id,
    task_title as fmt_task_title,
    complete_status,
    incomplete_status,
    Emojis,
    Colors,
)


def _get_status_symbol(status: str) -> str:
    """Get display symbol for task status.

    Per view_tasks.spec.md Status Display:
    - incomplete: [X]
    - complete: [checkmark]
    """
    return complete_status() if status == COMPLETE else incomplete_status()


def _wait_for_enter() -> None:
    """Wait for user to press Enter to continue.

    Per contracts/cli-interface.md Common Patterns.
    """
    input(dim("\nPress Enter to continue..."))


def _show_task_list_compact() -> None:
    """Show compact task list with IDs for selection.

    Helper function to display tasks before ID-based operations.
    """
    tasks = get_all_tasks()
    if tasks:
        print(f"\n{info(f'{Emojis.INFO}  Available tasks:')}")
        for task in tasks:
            status_symbol = _get_status_symbol(task.status)
            print(f"  {fmt_task_id(task.id)} {status_symbol} {fmt_task_title(task.title)}")
        print()


def handle_add_task() -> None:
    """Handle Add Task operation.

    Per add_task.spec.md CLI Flow Examples and contracts/cli-interface.md Add Task Contract.
    """
    print(f"\n{header(f'{Emojis.ADD} --- Add New Task ---')}")

    # Get title with validation loop
    while True:
        title_input = input(prompt(f"{Emojis.PROMPT} Enter task title: "))
        try:
            title = validate_title(title_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Get description with validation loop
    while True:
        description_input = input(prompt(f"{Emojis.PROMPT} Enter description (press Enter to skip): "))
        try:
            description = validate_description(description_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Create task
    task = add_task(title, description)

    # Success confirmation per add_task.spec.md
    print(f"\n{success(f'{Emojis.SUCCESS} Task added successfully!')}")
    print(f"  {info('ID:')} {fmt_task_id(task.id)}")
    print(f"  {info('Title:')} {fmt_task_title(task.title)}")
    print(f"  {info('Description:')} {task.description if task.description else dim('(none)')}")
    print(f"  {info('Status:')} {_get_status_symbol(task.status)} {task.status}")

    _wait_for_enter()


def handle_view_tasks() -> None:
    """Handle View Tasks operation.

    Per view_tasks.spec.md CLI Flow Examples and contracts/cli-interface.md View Tasks Contract.
    """
    print(f"\n{header(f'{Emojis.VIEW} --- Task List ---')}")

    tasks = get_all_tasks()

    if not tasks:
        # Empty list message per view_tasks.spec.md FR-005
        print(f"{warning(f'{Emojis.WARNING} No tasks found. Add a task to get started!')}")
        _wait_for_enter()
        return

    # Count completed/incomplete for summary
    complete_count = sum(1 for t in tasks if t.status == COMPLETE)
    incomplete_count = len(tasks) - complete_count

    # Grammar: "1 task" vs "X tasks" per view_tasks.spec.md Edge Cases
    task_word = "task" if len(tasks) == 1 else "tasks"
    print(f"{info('Total:')} {Colors.BRIGHT_WHITE}{len(tasks)}{Colors.RESET} {task_word} ({Colors.GREEN}{complete_count} completed{Colors.RESET}, {Colors.YELLOW}{incomplete_count} incomplete{Colors.RESET})")
    print()

    # Display each task per view_tasks.spec.md FR-002
    for task in tasks:
        status_symbol = _get_status_symbol(task.status)
        print(f"{fmt_task_id(task.id)} {status_symbol} {fmt_task_title(task.title)}")
        print(f"    {info('Description:')} {task.description if task.description else dim('(none)')}")
        print()

    _wait_for_enter()


def handle_delete_task() -> None:
    """Handle Delete Task operation.

    Per delete_task.spec.md CLI Flow Examples and contracts/cli-interface.md Delete Task Contract.
    """
    print(f"\n{header(f'{Emojis.DELETE} --- Delete Task ---')}")

    # Pre-check for empty list per delete_task.spec.md Edge Cases
    if not has_tasks():
        print(f"{warning(f'{Emojis.WARNING} No tasks available to delete.')}")
        _wait_for_enter()
        return

    # Show available tasks with IDs
    _show_task_list_compact()

    # Get task ID with validation loop
    while True:
        id_input = input(prompt(f"{Emojis.PROMPT} Enter task ID to delete: "))
        try:
            task_id = validate_task_id(id_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Attempt to delete
    try:
        task = delete_task(task_id)
        print(f"\n{success(f'{Emojis.SUCCESS} Task deleted successfully!')}")
        print(f"  {info('Deleted:')} {fmt_task_id(task.id)} {fmt_task_title(task.title)}")
    except TaskNotFoundError as e:
        print(f"\n{error(f'{Emojis.ERROR} Error: {e}')}")

    _wait_for_enter()


def handle_update_task() -> None:
    """Handle Update Task operation.

    Per update_task.spec.md CLI Flow Examples and contracts/cli-interface.md Update Task Contract.
    """
    print(f"\n{header(f'{Emojis.UPDATE} --- Update Task ---')}")

    # Pre-check for empty list per update_task.spec.md Edge Cases
    if not has_tasks():
        print(f"{warning(f'{Emojis.WARNING} No tasks available to update.')}")
        _wait_for_enter()
        return

    # Show available tasks with IDs
    _show_task_list_compact()

    # Get task ID with validation loop
    while True:
        id_input = input(prompt(f"{Emojis.PROMPT} Enter task ID to update: "))
        try:
            task_id = validate_task_id(id_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Verify task exists
    try:
        task = get_task(task_id)
    except TaskNotFoundError as e:
        print(f"\n{error(f'{Emojis.ERROR} Error: {e}')}")
        _wait_for_enter()
        return

    # Display current task details per update_task.spec.md CLI Flow
    print(f"\n{info(f'{Emojis.TASK} Current task:')}")
    print(f"  {info('ID:')} {fmt_task_id(task.id)}")
    print(f"  {info('Title:')} {fmt_task_title(task.title)}")
    print(f"  {info('Description:')} {task.description if task.description else dim('(none)')}")
    print(f"  {info('Status:')} {_get_status_symbol(task.status)} {task.status}")
    print()

    # Get new title (Enter to skip)
    new_title = None
    while True:
        title_input = input(prompt(f"{Emojis.PROMPT} Enter new title (press Enter to keep current): "))
        if not title_input:
            # Skip - keep current
            break
        try:
            new_title = validate_title(title_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Get new description (Enter to skip)
    new_description = None
    while True:
        desc_input = input(prompt(f"{Emojis.PROMPT} Enter new description (press Enter to keep current): "))
        if not desc_input:
            # Skip - keep current
            break
        try:
            new_description = validate_description(desc_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Perform update
    task, changes_made = update_task(task_id, new_title, new_description)

    if changes_made:
        print(f"\n{success(f'{Emojis.SUCCESS} Task updated successfully!')}")
        print(f"  {info('ID:')} {fmt_task_id(task.id)}")
        print(f"  {info('Title:')} {fmt_task_title(task.title)}")
        print(f"  {info('Description:')} {task.description if task.description else dim('(none)')}")
        print(f"  {info('Status:')} {_get_status_symbol(task.status)} {task.status}")
    else:
        # No changes message per update_task.spec.md Example 5
        print(f"\n{warning(f'{Emojis.INFO} No changes made. Task remains unchanged.')}")

    _wait_for_enter()


def handle_toggle_status() -> None:
    """Handle Mark Complete/Incomplete (Toggle) operation.

    Per mark_complete.spec.md CLI Flow Examples and contracts/cli-interface.md Toggle Contract.
    """
    print(f"\n{header(f'{Emojis.TOGGLE} --- Toggle Task Status ---')}")

    # Pre-check for empty list per mark_complete.spec.md Edge Cases
    if not has_tasks():
        print(f"{warning(f'{Emojis.WARNING} No tasks available. Add a task first!')}")
        _wait_for_enter()
        return

    # Show available tasks with IDs
    _show_task_list_compact()

    # Get task ID with validation loop
    while True:
        id_input = input(prompt(f"{Emojis.PROMPT} Enter task ID: "))
        try:
            task_id = validate_task_id(id_input)
            break
        except ValidationError as e:
            print(f"\n{error(f'{Emojis.ERROR} {e}')}")

    # Get current status before toggle
    try:
        task = get_task(task_id)
        old_status = task.status
        old_symbol = _get_status_symbol(old_status)

        # Perform toggle
        task = toggle_status(task_id)
        new_status = task.status
        new_symbol = _get_status_symbol(new_status)

        # Success confirmation per mark_complete.spec.md
        print(f"\n{success(f'{Emojis.SUCCESS} Status changed!')}")
        print(f"  {info('Task:')} {fmt_task_id(task.id)} {fmt_task_title(task.title)}")
        print(f"  {info('Status:')} {old_symbol} {old_status} {Emojis.ARROW} {new_symbol} {new_status}")

    except TaskNotFoundError as e:
        print(f"\n{error(f'{Emojis.ERROR} Error: {e}')}")

    _wait_for_enter()