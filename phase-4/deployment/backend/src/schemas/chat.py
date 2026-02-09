"""
Chat schemas for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/contracts/chat-api.yaml
"""
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request schema for chat endpoint.

    Attributes:
        conversation_id: Optional UUID of existing conversation to continue.
                        If not provided, a new conversation will be created.
        message: User's natural language message (1-2000 characters)

    Validation:
        - message: Required, 1-2000 characters
        - conversation_id: Optional, must be valid UUID if provided

    Example:
        {
            "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
            "message": "Add a task to buy groceries"
        }
    """
    conversation_id: Optional[UUID] = Field(
        None,
        description="Optional conversation ID to continue existing conversation"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "message": "Add a task to buy groceries"
            }
        }


class ToolCall(BaseModel):
    """
    Schema for MCP tool invocation details.

    Attributes:
        tool: Name of the MCP tool invoked
        input: Input parameters passed to the tool
        output: Output result returned by the tool

    Valid tool names:
        - add_task
        - list_tasks
        - update_task
        - delete_task
        - complete_task

    Example:
        {
            "tool": "add_task",
            "input": {"user_id": "...", "title": "Buy groceries"},
            "output": {"id": "...", "title": "Buy groceries", "completed": false}
        }
    """
    tool: str = Field(
        ...,
        description="MCP tool name (add_task, list_tasks, update_task, delete_task, complete_task)"
    )
    input: Dict[str, Any] = Field(
        ...,
        description="Tool input parameters"
    )
    output: Dict[str, Any] = Field(
        ...,
        description="Tool output result"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tool": "add_task",
                "input": {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Buy groceries"
                },
                "output": {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "title": "Buy groceries",
                    "completed": False
                }
            }
        }


class ChatResponse(BaseModel):
    """
    Response schema for chat endpoint.

    Attributes:
        conversation_id: UUID of the conversation (new or existing)
        response: AI assistant's natural language response
        tool_calls: List of MCP tool invocations made during processing

    The response includes:
    - conversation_id: For conversation continuity
    - response: User-friendly message from AI agent
    - tool_calls: Transparency into what actions were taken

    Example:
        {
            "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
            "response": "I've added the task 'Buy groceries' to your list.",
            "tool_calls": [
                {
                    "tool": "add_task",
                    "input": {"title": "Buy groceries"},
                    "output": {"id": "...", "title": "Buy groceries", "completed": false}
                }
            ]
        }
    """
    conversation_id: UUID = Field(
        ...,
        description="Conversation ID (new or existing)"
    )
    response: str = Field(
        ...,
        description="AI assistant's natural language response"
    )
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="List of MCP tool invocations (may be empty)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "response": "I've added the task 'Buy groceries' to your list.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "input": {
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "Buy groceries"
                        },
                        "output": {
                            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                            "title": "Buy groceries",
                            "completed": False
                        }
                    }
                ]
            }
        }
