# Claude Code Usage Documentation

This document explains how Claude Code is used to develop the Evolution of Todo application following Spec-Driven Development (SDD) principles.

## Current Phase: III - AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot`
**Specification**: `specs/003-ai-chatbot/`
**Constitution**: `.specify/memory/constitution.md` (v2.1.0)

## Phase III Overview

Transform Phase II web application into an AI-powered chatbot interface with:
- Natural language task management via OpenAI ChatKit
- Stateless backend architecture (no in-memory conversation state)
- MCP tools for standardized task operations
- OpenAI Agents SDK for agent orchestration
- Conversation persistence in Neon PostgreSQL
- OpenRouter as AI model provider (not OpenAI API)

## Monorepo Structure

```
hackathon-todo/
├── .specify/           # Spec-Kit Plus configuration
├── specs/              # Feature specifications
│   ├── 001-todo-console-app/      # Phase I (legacy)
│   ├── 002-fullstack-web-app/     # Phase II
│   └── 003-ai-chatbot/            # Phase III (current)
│       ├── mcp/                   # MCP tool specs
│       ├── agent/                 # Agent behavior specs
│       └── conversation/          # Conversation flow specs
├── frontend/           # Next.js 16+ App Router + ChatKit
├── backend/            # FastAPI + Agents SDK + MCP server
│   └── src/
│       ├── agent/                 # Agent orchestration (NEW)
│       └── mcp/                   # MCP server (NEW)
├── phase-1/            # Phase I console app (archived)
├── phase-2/            # Phase II web app (archived)
├── CLAUDE.md           # This file
├── docker-compose.yml  # Local development
└── README.md           # Setup instructions
```

## Technology Stack

| Layer | Technology | Reference |
|-------|------------|-----------|
| Frontend | Next.js 16+, TypeScript, Tailwind | @constitution |
| Frontend Chat UI | OpenAI ChatKit | @constitution |
| Backend | FastAPI, SQLModel, Python 3.11+ | @constitution |
| Backend Agent | OpenAI Agents SDK | @constitution |
| Backend Tools | Official MCP SDK | @constitution |
| Database | Neon PostgreSQL | @constitution |
| Auth | Better Auth, JWT (HS256) | @constitution |
| AI Model Provider | OpenRouter (NOT OpenAI API) | @constitution |

## Key Standards

### Authentication
- JWT tokens signed with `BETTER_AUTH_SECRET` (HS256)
- Token expiration: 24 hours
- Claims: `sub` (user_id), `email`, `iat`, `exp`
- AI agents MUST operate within authenticated user context

### User Isolation
- All task queries MUST filter by `user_id`
- Return 404 (not 403) for unauthorized access
- MCP tools MUST enforce user_id filtering on all operations
- AI agents MUST operate only within authenticated user's data scope

### REST API Conventions
- All routes under `/api/` prefix
- Response format: `{error: {code, message, details[]}}`
- Status codes: 200, 201, 401, 404, 409, 422
- Chat endpoint: `POST /api/{user_id}/chat`
  - Request: `conversation_id` (optional), `message` (required)
  - Response: `conversation_id`, `response`, `tool_calls`

### Stateless Architecture
- Backend MUST hold no conversation state in memory
- All conversation history persisted in database
- Any server instance can handle any request
- Server restarts MUST NOT lose conversation continuity
- Horizontal scaling possible without sticky sessions

### MCP Tools
- Tools MUST be stateless; all state in database
- Expose exactly: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- All tools MUST enforce user_id scoping
- Tool schemas documented in `specs/003-ai-chatbot/mcp/`

### Natural Language Commands
- AI agent maps user natural language to MCP tool invocations
- Agent behavior specified in `specs/003-ai-chatbot/agent/`
- Agent MUST confirm actions and handle errors gracefully
- Agent responses MUST reference specific tasks by title or ID

### Database Models
- **Task**: `user_id`, `id`, `title`, `description`, `completed`, `created_at`, `updated_at`
- **Conversation**: `user_id`, `id`, `created_at`, `updated_at`
- **Message**: `user_id`, `id`, `conversation_id`, `role` (user/assistant), `content`, `created_at`

## Environment Variables

| Variable | Layer | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | Backend | PostgreSQL connection |
| `BETTER_AUTH_SECRET` | Both | JWT signing (32+ chars) |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API URL |
| `NEXT_PUBLIC_OPENROUTER_KEY` | Frontend | OpenRouter API key (NOT OpenAI) |

## Layer-Specific Instructions

- **Frontend**: See `frontend/CLAUDE.md` (ChatKit integration)
- **Backend**: See `backend/CLAUDE.md` (Agents SDK + MCP server)
- **Specs**: See `specs/003-ai-chatbot/`

## Constitution Compliance

| Principle | Requirement |
|-----------|-------------|
| I. Spec-Driven | All features from specs (including MCP tools, agent behavior) |
| II. Traceability | Code references specs (including agent/ and mcp/ specs) |
| III. Security | JWT auth, user isolation, AI agents in user context |
| IV. Separation | Frontend/backend/database/agent/MCP tools |
| V. Scalability | Monorepo, env config, stateless architecture |
| VI. Stateless Architecture | No in-memory conversation state, DB persistence |
| VII. AI-First Interaction | Natural language primary interface, OpenRouter |
| VIII. Standardized Tool Interface | MCP tools only, no direct DB access from agent |

## Success Criteria (Phase III)

- **SC-010**: User can interact with chatbot via natural language to add, view, update, delete, and complete tasks
- **SC-011**: AI agent correctly invokes MCP tools based on user intent
- **SC-012**: Backend persists conversation and message history in database
- **SC-013**: Server is stateless; conversation resumes seamlessly after restarts
- **SC-014**: MCP tools enforce user-scoped access; users cannot access other users' tasks via chatbot
- **SC-015**: ChatKit frontend connects to backend `/api/{user_id}/chat` endpoint using OpenRouter

---

## Phase II Reference

Phase II implemented a full-stack web application:

### Phase II Overview

- User authentication (Better Auth + JWT)
- Persistent storage (Neon PostgreSQL)
- Next.js frontend + FastAPI backend
- Traditional CRUD UI (still available as fallback in Phase III)

### Phase II Success Criteria (Still Required)

- **SC-001**: Logged-in user can sign up, sign in, and manage only their own tasks
- **SC-002**: Backend rejects unauthenticated requests with HTTP 401
- **SC-003**: JWT token is required for every API call (except auth endpoints)
- **SC-004**: Repository contains organized Spec-Kit specs with full traceability
- **SC-005**: Layered CLAUDE.md files exist for root, frontend/, and backend/
- **SC-006**: Working Next.js frontend with authentication UI
- **SC-007**: Working FastAPI backend with JWT validation
- **SC-008**: Neon PostgreSQL integration with user-scoped task storage
- **SC-009**: Architecture is ready to extend into future phases

---

## Phase I Reference (Legacy)

Phase I implemented a console-based todo application:

### Architecture (Phase I)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage | In-memory Dict | O(1) lookups, simplicity |
| ID Generation | Sequential counter | Never recycled per spec |
| Module Separation | 4-layer | Maintainability principle |
| Error Handling | Custom exceptions | Clear error messages |

### Project Structure (Phase I)

```
src/
├── models/       # Task entity
├── services/     # Business logic
├── cli/          # User interface
├── validators/   # Input validation
└── exceptions/   # Custom errors
```

## Prompt History

All prompts and responses are recorded in:
- `history/prompts/constitution/` - Constitution setup and updates
- `history/prompts/001-todo-console-app/` - Phase I development
- `history/prompts/002-fullstack-web-app/` - Phase II development
- `history/prompts/003-ai-chatbot/` - Phase III development (current)

## No Manual Edits

Per Constitution SC-005: All code is generated by Claude Code with no manual edits.
