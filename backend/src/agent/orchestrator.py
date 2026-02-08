"""
Agent Orchestrator for Phase III AI-Powered Todo Chatbot.
Reference: @specs/003-ai-chatbot/agent/behavior.md

This module orchestrates the AI agent's interaction with users, managing:
- Conversation context loading from database
- Tool selection and invocation via MCP server
- Response generation
- Error handling

The orchestrator is stateless - all context is reconstructed from the database
on each request, enabling horizontal scaling.
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import os

from sqlmodel import Session, select
from openai import OpenAI

from src.core.database import get_engine
from src.models.conversation import Conversation
from src.models.message import Message
from src.mcp.server import mcp_server


class AgentOrchestrator:
    """
    Orchestrates AI agent interactions with users.

    This class manages the complete request cycle:
    1. Load conversation history from database
    2. Process user message with AI agent
    3. Invoke MCP tools as needed
    4. Generate response
    5. Persist messages to database

    Attributes:
        client: OpenAI client configured for OpenRouter
        mcp_server: MCP server instance for tool access
        max_context_messages: Maximum messages to load for context (default: 50)
    """

    def __init__(self):
        """
        Initialize agent orchestrator with OpenRouter configuration.

        Note: OpenRouter is OpenAI-compatible, so we use the OpenAI SDK
        with a custom base_url pointing to OpenRouter.
        """
        # OpenRouter configuration (OpenAI-compatible API)
        # Note: In production, the frontend uses OpenRouter directly via ChatKit
        # Backend agent uses OpenRouter for server-side processing if needed
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            base_url="https://openrouter.ai/api/v1"
        )
        self.mcp_server = mcp_server
        self.max_context_messages = 50  # Limit context window per spec

    def load_conversation_context(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID
    ) -> List[Dict[str, str]]:
        """
        Load conversation history from database for context.

        Args:
            session: Database session
            conversation_id: UUID of the conversation
            user_id: UUID of the authenticated user (for isolation)

        Returns:
            List of message dicts in OpenAI format [{"role": "user", "content": "..."}]

        Raises:
            KeyError: If conversation not found or doesn't belong to user

        Reference: @specs/003-ai-chatbot/plan.md (Stateless Architecture)
        """
        # Verify conversation belongs to user (user isolation)
        conv_statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(conv_statement).first()

        if not conversation:
            raise KeyError("Conversation not found")

        # Load last N messages for context
        msg_statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
            .order_by(Message.created_at.desc())
            .limit(self.max_context_messages)
        )
        messages = session.exec(msg_statement).all()

        # Reverse to chronological order and convert to OpenAI format
        return [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(messages)
        ]

    def invoke_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke an MCP tool with the given arguments.

        Args:
            tool_name: Name of the MCP tool to invoke
            tool_args: Arguments to pass to the tool

        Returns:
            Tool execution result

        Raises:
            KeyError: If tool not found
            ValueError: If tool validation fails
            Exception: If tool execution fails

        Reference: @specs/003-ai-chatbot/mcp/tools.md
        """
        try:
            tool_func = self.mcp_server.get_tool(tool_name)
            result = tool_func(**tool_args)
            return result
        except KeyError as e:
            raise KeyError(f"Tool '{tool_name}' not found: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Tool validation failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Tool execution failed: {str(e)}")

    def process_message(
        self,
        user_id: UUID,
        conversation_id: Optional[UUID],
        message: str,
        session: Session
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.

        This is the main entry point for the agent orchestrator. It:
        1. Loads or creates conversation
        2. Loads conversation context
        3. Processes message with AI agent
        4. Invokes MCP tools as needed
        5. Generates response
        6. Persists messages

        Args:
            user_id: UUID of the authenticated user
            conversation_id: Optional UUID of existing conversation
            message: User's message text
            session: Database session

        Returns:
            Dict with conversation_id, response, and tool_calls

        Reference: @specs/003-ai-chatbot/api/chat-endpoint.md
        """
        # Load or create conversation
        if conversation_id:
            # Load existing conversation context
            context_messages = self.load_conversation_context(
                session, conversation_id, user_id
            )
            conversation = session.get(Conversation, conversation_id)
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            context_messages = []
            conversation_id = conversation.id

        # Store user message
        user_message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="user",
            content=message
        )
        session.add(user_message)
        session.commit()

        # Add user message to context
        context_messages.append({"role": "user", "content": message})

        # Process with agent behavior module
        from .behavior import process_user_intent

        response_text, tool_calls = process_user_intent(
            user_id=user_id,
            message=message,
            context=context_messages,
            orchestrator=self
        )

        # Store assistant response
        assistant_message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = assistant_message.created_at
        session.add(conversation)
        session.commit()

        return {
            "conversation_id": str(conversation_id),
            "response": response_text,
            "tool_calls": tool_calls
        }


# Global orchestrator instance
agent_orchestrator = AgentOrchestrator()
