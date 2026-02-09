"""
Agent Behavior Module for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/agent/behavior.md

This module implements the AI agent's natural language understanding
and intent processing logic. It maps user messages to MCP tool invocations.
"""
from typing import Dict, List, Tuple, Any
from uuid import UUID
import re


def process_user_intent(
    user_id: UUID,
    message: str,
    context: List[Dict[str, str]],
    orchestrator: Any
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Process user's natural language message and determine appropriate actions.

    This function analyzes the user's message, determines their intent,
    invokes appropriate MCP tools, and generates a natural language response.

    Args:
        user_id: UUID of the authenticated user
        message: User's natural language message
        context: Conversation history (list of {"role": "user/assistant", "content": "..."})
        orchestrator: AgentOrchestrator instance for tool invocation

    Returns:
        Tuple of (response_text, tool_calls)
        - response_text: Natural language response to user
        - tool_calls: List of tool invocations [{"tool": "...", "input": {...}, "output": {...}}]

    Reference: @specs/003-ai-chatbot/agent/behavior.md
    """
    message_lower = message.lower().strip()
    tool_calls = []
    response_text = ""

    # Intent: Add task
    if any(keyword in message_lower for keyword in ["add", "create", "new task", "remind me"]):
        # Extract task title from message
        title = extract_task_title(message)

        if title:
            try:
                result = orchestrator.invoke_tool("add_task", {
                    "user_id": str(user_id),
                    "title": title
                })
                tool_calls.append({
                    "tool": "add_task",
                    "input": {"title": title},
                    "output": result
                })
                response_text = f"I've added the task '{title}' to your list."
            except Exception as e:
                response_text = f"Sorry, I couldn't add that task. Error: {str(e)}"
        else:
            response_text = "I'd be happy to add a task! Could you tell me what you'd like to add?"

    # Intent: List tasks
    elif any(keyword in message_lower for keyword in ["show", "list", "view", "what are", "my tasks", "see tasks"]):
        try:
            result = orchestrator.invoke_tool("list_tasks", {
                "user_id": str(user_id)
            })
            tool_calls.append({
                "tool": "list_tasks",
                "input": {},
                "output": result
            })

            tasks = result.get("tasks", [])
            if not tasks:
                response_text = "You don't have any tasks yet. Would you like to add one?"
            else:
                task_list = "\n".join([
                    f"- {task['title']}" + (" ✓" if task['completed'] else "")
                    for task in tasks
                ])
                response_text = f"Here are your tasks:\n{task_list}"
        except Exception as e:
            response_text = f"Sorry, I couldn't retrieve your tasks. Error: {str(e)}"

    # Intent: Complete task
    elif any(keyword in message_lower for keyword in ["complete", "done", "finish", "mark as complete"]):
        # Check if user wants to complete ALL tasks
        if any(keyword in message_lower for keyword in ["all tasks", "all", "everything"]):
            try:
                # Get all incomplete tasks
                list_result = orchestrator.invoke_tool("list_tasks", {
                    "user_id": str(user_id),
                    "completed": False
                })
                incomplete_tasks = list_result.get("tasks", [])

                if not incomplete_tasks:
                    response_text = "You don't have any incomplete tasks. Great job!"
                else:
                    # Complete all tasks
                    completed_count = 0
                    for task in incomplete_tasks:
                        try:
                            result = orchestrator.invoke_tool("complete_task", {
                                "user_id": str(user_id),
                                "task_id": task['id']
                            })
                            tool_calls.append({
                                "tool": "complete_task",
                                "input": {"task_id": task['id']},
                                "output": result
                            })
                            completed_count += 1
                        except Exception as e:
                            print(f"Error completing task {task['id']}: {e}")

                    response_text = f"Great! I've marked all {completed_count} tasks as completed."
            except Exception as e:
                response_text = f"Sorry, I couldn't complete all tasks. Error: {str(e)}"
        else:
            # Complete specific task
            task_title = extract_task_reference(message)

            if task_title:
                try:
                    # First, list tasks to find matching task
                    list_result = orchestrator.invoke_tool("list_tasks", {
                        "user_id": str(user_id)
                    })
                    tasks = list_result.get("tasks", [])

                    # Find task by title (case-insensitive partial match)
                    matching_task = None
                    for task in tasks:
                        if task_title.lower() in task['title'].lower():
                            matching_task = task
                            break

                    if matching_task:
                        result = orchestrator.invoke_tool("complete_task", {
                            "user_id": str(user_id),
                            "task_id": matching_task['id']
                        })
                        tool_calls.append({
                            "tool": "complete_task",
                            "input": {"task_id": matching_task['id']},
                            "output": result
                        })
                        response_text = f"Great! I've marked '{matching_task['title']}' as completed."
                    else:
                        response_text = f"I couldn't find a task matching '{task_title}'. Could you be more specific?"
                except Exception as e:
                    response_text = f"Sorry, I couldn't complete that task. Error: {str(e)}"
            else:
                response_text = "Which task would you like to mark as complete?"

    # Intent: Delete task
    elif any(keyword in message_lower for keyword in ["delete", "remove", "cancel"]):
        # Check if user wants to delete ALL tasks
        if any(keyword in message_lower for keyword in ["all tasks", "all", "everything"]):
            try:
                # Get all tasks
                list_result = orchestrator.invoke_tool("list_tasks", {
                    "user_id": str(user_id)
                })
                all_tasks = list_result.get("tasks", [])

                if not all_tasks:
                    response_text = "You don't have any tasks to delete."
                else:
                    # Delete all tasks
                    deleted_count = 0
                    for task in all_tasks:
                        try:
                            result = orchestrator.invoke_tool("delete_task", {
                                "user_id": str(user_id),
                                "task_id": task['id']
                            })
                            tool_calls.append({
                                "tool": "delete_task",
                                "input": {"task_id": task['id']},
                                "output": result
                            })
                            deleted_count += 1
                        except Exception as e:
                            print(f"Error deleting task {task['id']}: {e}")

                    response_text = f"I've deleted all {deleted_count} tasks from your list."
            except Exception as e:
                response_text = f"Sorry, I couldn't delete all tasks. Error: {str(e)}"
        else:
            # Delete specific task
            task_title = extract_task_reference(message)

            if task_title:
                try:
                    # First, list tasks to find matching task
                    list_result = orchestrator.invoke_tool("list_tasks", {
                        "user_id": str(user_id)
                    })
                    tasks = list_result.get("tasks", [])

                    # Find task by title
                    matching_task = None
                    for task in tasks:
                        if task_title.lower() in task['title'].lower():
                            matching_task = task
                            break

                    if matching_task:
                        result = orchestrator.invoke_tool("delete_task", {
                            "user_id": str(user_id),
                            "task_id": matching_task['id']
                        })
                        tool_calls.append({
                            "tool": "delete_task",
                            "input": {"task_id": matching_task['id']},
                            "output": result
                        })
                        response_text = f"I've deleted the task '{matching_task['title']}'."
                    else:
                        response_text = f"I couldn't find a task matching '{task_title}'. Could you be more specific?"
                except Exception as e:
                    response_text = f"Sorry, I couldn't delete that task. Error: {str(e)}"
            else:
                response_text = "Which task would you like to delete?"

    # Intent: Update task
    elif any(keyword in message_lower for keyword in ["update", "change", "edit", "modify", "rename"]):
        # Try to extract old and new task names
        old_name, new_name = extract_update_task_names(message)

        if old_name and new_name:
            try:
                # First, list tasks to find matching task
                list_result = orchestrator.invoke_tool("list_tasks", {
                    "user_id": str(user_id)
                })
                tasks = list_result.get("tasks", [])

                # Find task by old title
                matching_task = None
                for task in tasks:
                    if old_name.lower() in task['title'].lower():
                        matching_task = task
                        break

                if matching_task:
                    result = orchestrator.invoke_tool("update_task", {
                        "user_id": str(user_id),
                        "task_id": matching_task['id'],
                        "title": new_name
                    })
                    tool_calls.append({
                        "tool": "update_task",
                        "input": {"task_id": matching_task['id'], "title": new_name},
                        "output": result
                    })
                    response_text = f"I've updated the task from '{matching_task['title']}' to '{new_name}'."
                else:
                    response_text = f"I couldn't find a task matching '{old_name}'. Could you be more specific?"
            except Exception as e:
                response_text = f"Sorry, I couldn't update that task. Error: {str(e)}"
        else:
            response_text = "I can help you update a task. Please tell me which task you'd like to update and what the new name should be. For example: 'update hackathon to hackathons'"

    # Default: Greeting or unclear intent
    else:
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "help"]):
            response_text = """Hello! I'm your AI todo assistant. I can help you:
- Add tasks (e.g., "Add a task to buy groceries")
- Show your tasks (e.g., "Show me my tasks")
- Complete tasks (e.g., "Mark buy groceries as complete")
- Update tasks (e.g., "Update hackathon as hackathons")
- Delete tasks (e.g., "Delete the groceries task")

What would you like to do?"""
        else:
            response_text = "I'm not sure what you'd like me to do. I can help you add, view, complete, or delete tasks. What would you like to do?"

    return response_text, tool_calls


def extract_task_title(message: str) -> str:
    """
    Extract task title from user message.

    Examples:
        "Add a task to buy groceries" -> "buy groceries"
        "Create task: finish report" -> "finish report"
        "Remind me to call mom" -> "call mom"
    """
    message = message.strip()

    # Remove common prefixes
    patterns = [
        r"(?:add|create|new)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)",
        r"(?:remind me to|remember to)\s+(.+)",
        r"(?:add|create):\s*(.+)",
        r"(?:task|todo):\s*(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # If no pattern matches, try to extract after common keywords
    keywords = ["add", "create", "new task", "remind me", "remember"]
    for keyword in keywords:
        if keyword in message.lower():
            parts = message.lower().split(keyword, 1)
            if len(parts) > 1:
                # Remove "to" if it's the first word
                title = parts[1].strip()
                if title.startswith("to "):
                    title = title[3:].strip()
                if title:
                    return title

    return message


def extract_task_reference(message: str) -> str:
    """
    Extract task reference (title or description) from user message.

    Examples:
        "Complete buy groceries" -> "buy groceries"
        "Mark the report task as done" -> "report"
        "Delete groceries" -> "groceries"
        "Mark complete to hackathon_1" -> "hackathon_1"
    """
    message = message.strip()

    # Remove common action words
    patterns = [
        # Handle "mark complete to X" pattern
        r"mark\s+complete\s+to\s+(.+)",
        r"mark\s+(?:as\s+)?(?:complete|done)\s+(?:to\s+)?(.+)",
        # Standard patterns
        r"(?:complete|done|finish|mark)\s+(?:the\s+)?(?:task\s+)?(.+?)(?:\s+as\s+(?:complete|done))?$",
        r"(?:delete|remove|cancel)\s+(?:the\s+)?(?:task\s+)?(.+)",
        r"(?:update|change|edit|modify)\s+(?:the\s+)?(?:task\s+)?(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            task_ref = match.group(1).strip()
            # Remove leading "to" if present
            if task_ref.lower().startswith("to "):
                task_ref = task_ref[3:].strip()
            return task_ref

    # Fallback: return the message after removing common words
    words_to_remove = ["complete", "done", "finish", "mark", "delete", "remove", "cancel", "the", "task", "as", "to"]
    words = message.lower().split()
    filtered_words = [w for w in words if w not in words_to_remove]

    return " ".join(filtered_words) if filtered_words else message


def extract_update_task_names(message: str) -> tuple:
    """
    Extract old and new task names from update command.

    Examples:
        "update hackathon as hackathons" -> ("hackathon", "hackathons")
        "change buy groceries to buy milk" -> ("buy groceries", "buy milk")
        "rename task1 to task2" -> ("task1", "task2")

    Returns:
        Tuple of (old_name, new_name) or (None, None) if pattern not found
    """
    message = message.strip()

    # Patterns to extract old and new task names
    patterns = [
        r"(?:update|change|rename|modify)\s+(.+?)\s+(?:as|to)\s+(.+)",
        r"(?:update|change|rename|modify)\s+(?:the\s+)?(?:task\s+)?(.+?)\s+(?:as|to)\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            old_name = match.group(1).strip()
            new_name = match.group(2).strip()

            # Clean up common words from old_name
            old_name = old_name.replace("the task", "").replace("task", "").strip()

            return (old_name, new_name)

    return (None, None)
