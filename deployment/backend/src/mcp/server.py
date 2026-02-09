"""
MCP Server initialization for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/mcp/tools.md

This module initializes the MCP (Model Context Protocol) server and registers
all task management tools for use by the AI agent.

The MCP server provides a standardized interface between the AI agent and
task operations, ensuring:
- Stateless tool design
- User isolation enforcement
- Consistent error handling
- Tool schema validation
"""
from typing import Dict, List

# MCP SDK will be imported once installed
# from mcp import Server, Tool


class MCPServer:
    """
    MCP Server for task management tools.

    This server registers and manages all MCP tools used by the AI agent
    for task operations. All tools are stateless and enforce user_id scoping.

    Attributes:
        tools: Dictionary of registered tools by name

    Registered Tools:
        - add_task: Create new task
        - list_tasks: Retrieve user's tasks
        - update_task: Modify task title/description
        - delete_task: Remove task
        - complete_task: Mark task as completed
    """

    def __init__(self):
        """Initialize MCP server with empty tool registry."""
        self.tools: Dict[str, callable] = {}
        self._initialize_tools()

    def _initialize_tools(self):
        """
        Initialize and register all MCP tools.

        This method imports and registers all task management tools
        from the tools module.
        """
        from .tools import (
            add_task,
            list_tasks,
            update_task,
            delete_task,
            complete_task
        )

        # Register tools
        self.tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "delete_task": delete_task,
            "complete_task": complete_task
        }

    def get_tool(self, tool_name: str) -> callable:
        """
        Get a registered tool by name.

        Args:
            tool_name: Name of the tool to retrieve

        Returns:
            Tool function

        Raises:
            KeyError: If tool not found
        """
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}")
        return self.tools[tool_name]

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def get_tool_schemas(self) -> List[Dict]:
        """
        Get OpenAI function calling schemas for all tools.

        Returns:
            List of tool schemas in OpenAI function calling format

        Reference: @specs/003-ai-chatbot/contracts/mcp-tools.md
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "format": "uuid"},
                            "title": {"type": "string", "minLength": 1, "maxLength": 100},
                            "description": {"type": "string", "maxLength": 500}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve user's tasks, optionally filtered by completion status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "format": "uuid"},
                            "completed": {"type": "boolean"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title and/or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "format": "uuid"},
                            "task_id": {"type": "string", "format": "uuid"},
                            "title": {"type": "string", "minLength": 1, "maxLength": 100},
                            "description": {"type": "string", "maxLength": 500}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Permanently remove a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "format": "uuid"},
                            "task_id": {"type": "string", "format": "uuid"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "format": "uuid"},
                            "task_id": {"type": "string", "format": "uuid"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]


# Global MCP server instance
mcp_server = MCPServer()
