"""
Chat API endpoint for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/api/chat-endpoint.md

This module implements the POST /api/{user_id}/chat endpoint for
natural language task management via AI agent.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.core.dependencies import get_current_user
from src.models.user import User
from src.schemas.chat import ChatRequest, ChatResponse, ToolCall
from src.schemas.error import ErrorResponse
from src.agent.orchestrator import agent_orchestrator

router = APIRouter()


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden - user_id mismatch"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Send chat message",
    description="""
    Process user's natural language message and return AI assistant response.

    Creates new conversation if conversation_id not provided, or continues
    existing conversation if conversation_id provided.

    The AI agent interprets user intent and invokes appropriate MCP tools
    for task management operations (add, list, update, delete, complete).

    All conversation history is persisted in the database for stateless
    backend architecture.
    """
)
async def chat(
    user_id: UUID,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Chat endpoint for natural language task management.

    Args:
        user_id: User ID from path parameter
        request: ChatRequest with optional conversation_id and message
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool_calls

    Raises:
        HTTPException 403: If path user_id doesn't match JWT user_id
        HTTPException 404: If conversation not found or doesn't belong to user
        HTTPException 422: If message validation fails
        HTTPException 500: If agent processing fails

    Reference: @specs/003-ai-chatbot/api/chat-endpoint.md
    """
    # T026: JWT validation and user_id extraction
    # Verify path user_id matches authenticated user (user isolation)
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You can only access your own conversations.",
                    "details": []
                }
            }
        )

    # Validate message
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data.",
                    "details": [
                        {"field": "message", "message": "Message cannot be empty."}
                    ]
                }
            }
        )

    if len(request.message) > 2000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data.",
                    "details": [
                        {"field": "message", "message": "Message must be 2000 characters or less."}
                    ]
                }
            }
        )

    try:
        # T027: Conversation creation/loading logic
        # T028: Message persistence (user and assistant)
        # T029: Conversation timestamp updates
        # All handled by agent orchestrator
        result = agent_orchestrator.process_message(
            user_id=user_id,
            conversation_id=request.conversation_id,
            message=request.message,
            session=session
        )

        # Convert tool_calls to ToolCall schema
        tool_calls = [
            ToolCall(
                tool=call["tool"],
                input=call["input"],
                output=call["output"]
            )
            for call in result["tool_calls"]
        ]

        return ChatResponse(
            conversation_id=UUID(result["conversation_id"]),
            response=result["response"],
            tool_calls=tool_calls
        )

    except KeyError as e:
        # Conversation not found or task not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": str(e),
                    "details": []
                }
            }
        )
    except ValueError as e:
        # Validation error from MCP tools
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                    "details": []
                }
            }
        )
    except Exception as e:
        # Generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "PROCESSING_ERROR",
                    "message": "Unable to process your message. Please try again.",
                    "details": []
                }
            }
        )
