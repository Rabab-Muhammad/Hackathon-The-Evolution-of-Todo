# Phase III: AI-Powered Todo Chatbot - Overview

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft
**Phase**: III - AI-Powered Natural Language Interface

## Purpose

Transform the Evolution of Todo application from a traditional CRUD interface into an AI-powered conversational experience where users manage their tasks through natural language. This phase introduces intelligent task management via chat, enabling users to add, view, update, delete, and complete tasks by simply describing what they want in plain English.

## Objectives

1. **Natural Language Task Management**: Enable users to manage todos through conversational commands instead of forms and buttons
2. **Stateless Backend Architecture**: Design backend to persist all conversation state in database, enabling horizontal scaling and resilience
3. **Standardized Tool Interface**: Implement MCP (Model Context Protocol) tools as the exclusive interface for task operations
4. **Conversation Persistence**: Store all chat history in database so users can resume conversations across sessions and server restarts
5. **User Isolation**: Ensure AI agent operates only within authenticated user's data scope
6. **Provider Independence**: Use OpenRouter for AI inference, maintaining flexibility to switch models without backend changes

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend Chat UI | OpenAI ChatKit | Conversational interface for user interaction |
| AI Model Provider | OpenRouter | AI inference (provider-agnostic) |
| Backend Framework | FastAPI | REST API and chat endpoint |
| Agent Orchestration | OpenAI Agents SDK | Intent interpretation and tool selection |
| Tool Interface | MCP SDK (Official) | Standardized task operation tools |
| ORM | SQLModel | Database operations |
| Database | Neon PostgreSQL | Persistent storage for tasks, conversations, messages |
| Authentication | Better Auth + JWT | User authentication and authorization |

## Core Principles

### 1. Spec-Driven Development Only
All chatbot features, MCP tools, agent behaviors, and conversation flows must be fully specified before implementation. No manual coding outside of Claude Code generation.

### 2. Agent-Centric Architecture
The AI agent is the primary interface for task management. Traditional CRUD UI (Phase II) remains available as fallback, but natural language is the primary interaction model.

### 3. Stateless Backend Design
Backend holds no conversation state in memory. All conversation history, messages, and context are persisted in database. Any server instance can handle any request. Server restarts do not lose conversation continuity.

### 4. Tool-Based Intelligence
AI agent never manipulates database directly. All task operations go through MCP tools (add_task, list_tasks, update_task, delete_task, complete_task). This ensures consistent behavior, testability, and auditability.

### 5. Security & User Isolation
- JWT authentication required for all chat requests
- AI agent operates only within authenticated user's data scope
- MCP tools enforce user_id filtering on all operations
- Users cannot access other users' tasks via chatbot

### 6. Provider Independence
OpenRouter provides AI inference, compatible with OpenAI Agents SDK. Backend does not depend on specific AI model or provider. Future model changes require only configuration updates, not code changes.

## Success Criteria

### Phase III Completion Criteria

- **SC-010**: Users can manage all task operations (add, view, update, delete, complete) via natural language chat
- **SC-011**: AI agent correctly interprets user intent and invokes appropriate MCP tools with 95% accuracy for common commands
- **SC-012**: All conversation history and messages are persisted in database and retrievable across sessions
- **SC-013**: Backend is stateless; conversation resumes seamlessly after server restarts with no data loss
- **SC-014**: MCP tools enforce user-scoped access; users cannot access other users' tasks via chatbot
- **SC-015**: ChatKit frontend successfully connects to backend chat endpoint using OpenRouter for AI inference
- **SC-016**: Users receive friendly confirmations after task operations with specific task details
- **SC-017**: System handles errors gracefully with user-friendly messages (task not found, invalid input, etc.)
- **SC-018**: Chat interface responds to user messages within 3 seconds under normal load
- **SC-019**: Traditional CRUD UI (Phase II) remains functional as fallback interface

### Phase II Criteria (Still Required)

All Phase II success criteria (SC-001 through SC-009) remain required:
- User authentication and authorization
- JWT token validation
- User-scoped task storage
- Organized specifications with traceability
- Working Next.js frontend and FastAPI backend

## Architecture Summary

```
User → ChatKit UI → POST /api/{user_id}/chat → FastAPI Endpoint
                                                      ↓
                                                Agent Orchestrator
                                                      ↓
                                                MCP Tools
                                                      ↓
                                                Database (Tasks, Conversations, Messages)
```

**Key Characteristics**:
- Stateless request cycle
- Conversation context reconstructed from database on each request
- Agent selects and invokes MCP tools based on user intent
- All state persisted in Neon PostgreSQL
- OpenRouter provides AI inference via ChatKit

## Environment Variables

| Variable | Layer | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | Backend | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Both | JWT signing secret (32+ characters) |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL |
| `NEXT_PUBLIC_OPENROUTER_KEY` | Frontend | OpenRouter API key for ChatKit |

**Note**: Backend does not require direct AI model API key. OpenRouter is accessed via frontend ChatKit, and backend uses Agents SDK with MCP tools.

## Constraints

1. **No Direct Database Access from Agent**: AI agent must use MCP tools exclusively; no direct database queries
2. **No In-Memory State**: Backend must not store conversation state in memory; all state in database
3. **No Hardcoded Prompts**: Agent behavior must be configurable and specified in agent behavior specs
4. **User Isolation**: All operations must filter by authenticated user_id
5. **Stateless Design**: Any server instance must handle any request without session affinity

## Deliverables

1. Complete specifications in `specs/003-ai-chatbot/`
2. Implementation plan in `specs/003-ai-chatbot/plan.md`
3. Task breakdown in `specs/003-ai-chatbot/tasks.md`
4. Working chatbot interface with natural language task management
5. Persistent conversation history across sessions
6. Stateless backend ready for horizontal scaling
7. Documentation and prompt history records

## Next Steps

1. Review and validate this overview
2. Create detailed specifications for each component
3. Run `/sp.plan` to generate implementation plan
4. Run `/sp.tasks` to generate task breakdown
5. Run `/sp.implement` to execute implementation

## Assumptions

- Users are familiar with natural language interaction (no training required)
- OpenRouter provides reliable AI inference with acceptable latency (<2s)
- ChatKit library is compatible with OpenRouter API
- Phase II authentication and database infrastructure is functional
- Users prefer conversational interface over traditional forms for task management
