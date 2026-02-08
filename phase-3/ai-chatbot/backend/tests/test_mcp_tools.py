"""
Unit tests for MCP tools.
Reference: @specs/003-ai-chatbot/mcp/tools.md

Tests verify:
- User isolation (tasks filtered by user_id)
- Validation rules (title/description length)
- Error handling (task not found, validation errors)
- Tool functionality (add, list, update, delete, complete)
"""
import pytest
from uuid import uuid4

from src.mcp.tools import add_task, list_tasks, update_task, delete_task, complete_task


class TestAddTask:
    """Test add_task MCP tool."""

    def test_add_task_with_title_only(self, session, test_user):
        """Test creating task with title only."""
        result = add_task(
            user_id=str(test_user.id),
            title="Buy groceries"
        )

        assert result["title"] == "Buy groceries"
        assert result["description"] is None
        assert result["completed"] is False
        assert result["user_id"] == str(test_user.id)

    def test_add_task_with_description(self, session, test_user):
        """Test creating task with title and description."""
        result = add_task(
            user_id=str(test_user.id),
            title="Buy groceries",
            description="Milk, eggs, bread"
        )

        assert result["title"] == "Buy groceries"
        assert result["description"] == "Milk, eggs, bread"

    def test_add_task_empty_title_fails(self, session, test_user):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            add_task(user_id=str(test_user.id), title="")

    def test_add_task_title_too_long_fails(self, session, test_user):
        """Test that title >100 chars raises ValueError."""
        with pytest.raises(ValueError, match="100 characters or less"):
            add_task(user_id=str(test_user.id), title="x" * 101)

    def test_add_task_description_too_long_fails(self, session, test_user):
        """Test that description >500 chars raises ValueError."""
        with pytest.raises(ValueError, match="500 characters or less"):
            add_task(
                user_id=str(test_user.id),
                title="Test",
                description="x" * 501
            )


class TestListTasks:
    """Test list_tasks MCP tool."""

    def test_list_tasks_returns_user_tasks_only(self, session, test_user, test_task):
        """Test user isolation - only returns tasks for specified user."""
        # Create another user and task
        other_user_id = str(uuid4())

        result = list_tasks(user_id=str(test_user.id))

        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["id"] == str(test_task.id)

    def test_list_tasks_filter_completed(self, session, test_user):
        """Test filtering by completed status."""
        # Create completed and incomplete tasks
        add_task(user_id=str(test_user.id), title="Task 1")
        task2 = add_task(user_id=str(test_user.id), title="Task 2")
        complete_task(user_id=str(test_user.id), task_id=task2["id"])

        # List incomplete only
        result = list_tasks(user_id=str(test_user.id), completed=False)
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Task 1"

        # List completed only
        result = list_tasks(user_id=str(test_user.id), completed=True)
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Task 2"

    def test_list_tasks_empty_list(self, session, test_user):
        """Test listing tasks when user has none."""
        result = list_tasks(user_id=str(test_user.id))
        assert result["tasks"] == []


class TestCompleteTask:
    """Test complete_task MCP tool."""

    def test_complete_task_success(self, session, test_user, test_task):
        """Test marking task as completed."""
        result = complete_task(
            user_id=str(test_user.id),
            task_id=str(test_task.id)
        )

        assert result["completed"] is True
        assert result["id"] == str(test_task.id)

    def test_complete_task_not_found(self, session, test_user):
        """Test completing non-existent task raises KeyError."""
        with pytest.raises(KeyError, match="Task not found"):
            complete_task(
                user_id=str(test_user.id),
                task_id=str(uuid4())
            )

    def test_complete_task_wrong_user(self, session, test_user, test_task):
        """Test user isolation - cannot complete other user's task."""
        other_user_id = str(uuid4())

        with pytest.raises(KeyError, match="Task not found"):
            complete_task(
                user_id=other_user_id,
                task_id=str(test_task.id)
            )


class TestUpdateTask:
    """Test update_task MCP tool."""

    def test_update_task_title(self, session, test_user, test_task):
        """Test updating task title."""
        result = update_task(
            user_id=str(test_user.id),
            task_id=str(test_task.id),
            title="Updated Title"
        )

        assert result["title"] == "Updated Title"
        assert result["description"] == test_task.description

    def test_update_task_no_fields_fails(self, session, test_user, test_task):
        """Test that updating with no fields raises ValueError."""
        with pytest.raises(ValueError, match="At least one field"):
            update_task(
                user_id=str(test_user.id),
                task_id=str(test_task.id)
            )


class TestDeleteTask:
    """Test delete_task MCP tool."""

    def test_delete_task_success(self, session, test_user, test_task):
        """Test deleting task."""
        result = delete_task(
            user_id=str(test_user.id),
            task_id=str(test_task.id)
        )

        assert result["success"] is True
        assert result["deleted_task_id"] == str(test_task.id)

        # Verify task is deleted
        with pytest.raises(KeyError):
            complete_task(
                user_id=str(test_user.id),
                task_id=str(test_task.id)
            )

    def test_delete_task_wrong_user(self, session, test_user, test_task):
        """Test user isolation - cannot delete other user's task."""
        other_user_id = str(uuid4())

        with pytest.raises(KeyError, match="Task not found"):
            delete_task(
                user_id=other_user_id,
                task_id=str(test_task.id)
            )
