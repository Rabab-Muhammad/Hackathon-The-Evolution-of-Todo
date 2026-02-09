"""
MCP (Model Context Protocol) module for Phase III AI-Powered Todo Chatbot.

This module provides the MCP server and tools for task management operations.
All tools are stateless and enforce user_id scoping for user isolation.
"""
from .server import mcp_server, MCPServer
from .tools import add_task, list_tasks, update_task, delete_task, complete_task

__all__ = [
    "mcp_server",
    "MCPServer",
    "add_task",
    "list_tasks",
    "update_task",
    "delete_task",
    "complete_task"
]
