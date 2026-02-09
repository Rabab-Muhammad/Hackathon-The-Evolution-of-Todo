"""
Agent module for Phase III AI-Powered Todo Chatbot.

This module provides the AI agent orchestration and behavior logic
for processing natural language task management requests.
"""
from .orchestrator import agent_orchestrator, AgentOrchestrator
from .behavior import process_user_intent

__all__ = [
    "agent_orchestrator",
    "AgentOrchestrator",
    "process_user_intent"
]
