# Implementation Plan: Phase III AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

## Summary

Phase III transforms the Evolution of Todo application into an AI-powered conversational experience. Users manage tasks through natural language chat powered by OpenAI Agents SDK, MCP tools, and OpenRouter. The implementation adds:

- **Stateless Backend**: All conversation state persisted in database (Neon PostgreSQL)
- **MCP Tools**: 5 standardized tools for task operations (add, list, update, delete, complete)
- **AI Agent**: OpenAI Agents SDK for intent interpretation and tool orchestration
- **ChatKit UI**: OpenAI ChatKit frontend with OpenRouter integration
- **Conversation Persistence**: Resume conversations across sessions and server restarts

**Technical Approach**: Extend existing Phase II FastAPI backend and Next.js frontend with new conversation/message models, MCP server, agent orchestration layer, and chat endpoint. Frontend adds ChatKit-based chat interface alongside existing CRUD UI.

## Technical Context

**Language/Version**:
- Backend: Python 3.11+
- Frontend: TypeScript 5.0+ with Next.js 16+

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, Pydantic
- Frontend: Next.js, React, OpenAI ChatKit, Tailwind CSS
- Database: Neon PostgreSQL (serverless)
- Auth: Better Auth (existing from Phase II)

**Storage**: Neon PostgreSQL with new tables (conversations, messages) and existing tables (users, tasks from Phase II)

**Testing**:
- Backend: pytest for unit/integration tests
- Frontend: Jest + React Testing Library
- E2E: Playwright for full conversation flows

**Target Platform**:
- Backend: Linux server (containerized for future Kubernetes deployment)
- Frontend: Web browsers (desktop, tablet, mobile)

**Project Type**: Web application (existing frontend/ and backend/ directories)

**Performance Goals**:
- Chat response time: <3s (P95)
- MCP tool execution: <500ms (P95)
- Database queries: <100ms (P95)
- Support 100 concurrent users

**Constraints**:
- Stateless backend (no in-memory conversation state)
- Agent must use only MCP tools (no direct database access)
- User isolation enforced at all layers
- OpenRouter (not OpenAI API) for AI inference
- Conversation history limited to last 50 messages for context

**Scale/Scope**:
- Target: 1000 users with 10+ conversations each
- Database: ~500K messages, ~10K conversations, ~20K tasks
- Codebase: ~5K new lines (backend), ~3K new lines (frontend)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
✅ **PASS**: All features defined in specs/003-ai-chatbot/ before implementation
- 9 specification documents covering all components
- No implementation without prior specification

### Principle II: End-to-End Traceability
✅ **PASS**: All changes traceable to spec files
- MCP tools → specs/003-ai-chatbot/mcp/tools.md
- Agent behavior → specs/003-ai-chatbot/agent/behavior.md
- Chat API → specs/003-ai-chatbot/api/chat-endpoint.md
- Database schema → specs/003-ai-chatbot/database/schema.md
- UI components → specs/003-ai-chatbot/ui/chatkit.md

### Principle III: Security by Design
✅ **PASS**: JWT authentication enforced, user isolation at all layers
- Chat endpoint validates JWT on every request
- MCP tools enforce user_id filtering
- Agent operates only within authenticated user context
- Database queries filter by user_id

### Principle IV: Separation of Concerns
✅ **PASS**: Clear separation of frontend, backend, agent, MCP tools, database
- Frontend: ChatKit UI (src/components/chat/)
- Backend: FastAPI endpoints (src/api/chat.py)
- Agent: Orchestration logic (src/agent/)
- MCP Tools: Tool implementations (src/mcp/)
- Database: SQLModel models (src/models/)

### Principle V: Scalability Ready
✅ **PASS**: Stateless architecture supports horizontal scaling
- No in-memory conversation state
- Any backend instance can handle any request
- Database connection pooling
- Ready for Kubernetes deployment (Phase IV)

### Principle VI: Stateless Architecture
✅ **PASS**: Backend holds no conversation state in memory
- All conversation history in database
- Context reconstructed from database on each request
- Server restarts do not lose conversation continuity

### Principle VII: AI-First Interaction
✅ **PASS**: Natural language as primary interface
- ChatKit UI for conversational interaction
- OpenRouter for AI inference
- Traditional CRUD UI remains as fallback

### Principle VIII: Standardized Tool Interface
✅ **PASS**: MCP tools define all task operations
- 5 tools: add_task, list_tasks, update_task, delete_task, complete_task
- Agent uses only MCP tools (no direct database access)
- Stateless tool design

**Constitution Check Result**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.yaml   # MCP tool schemas
├── spec.md              # Main specification (already exists)
├── overview.md          # Phase III overview (already exists)
├── architecture.md      # System architecture (already exists)
├── features/            # Feature specs (already exist)
├── api/                 # API specs (already exist)
├── mcp/                 # MCP tool specs (already exist)
├── agent/               # Agent behavior specs (already exist)
├── database/            # Database specs (already exist)
└── ui/                  # UI specs (already exist)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py              # Existing (Phase II)
│   │   ├── task.py              # Existing (Phase II)
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── schemas/
│   │   ├── auth.py              # Existing (Phase II)
│   │   ├── task.py              # Existing (Phase II)
│   │   ├── chat.py              # NEW: Chat request/response schemas
│   │   └── error.py             # Existing (Phase II)
│   ├── api/
│   │   ├── router.py            # Existing (Phase II)
│   │   ├── auth.py              # Existing (Phase II)
│   │   ├── tasks.py             # Existing (Phase II)
│   │   └── chat.py              # NEW: Chat endpoint
│   ├── services/
│   │   ├── auth.py              # Existing (Phase II)
│   │   └── task.py              # Existing (Phase II)
│   ├── agent/                   # NEW: Agent orchestration
│   │   ├── __init__.py
│   │   ├── orchestrator.py      # Agent orchestration logic
│   │   └── behavior.py          # Agent behavior implementation
│   ├── mcp/                     # NEW: MCP server
│   │   ├── __init__.py
│   │   ├── server.py            # MCP server setup
│   │   └── tools.py             # MCP tool implementations
│   ├── core/
│   │   ├── config.py            # Existing (Phase II)
│   │   ├── database.py          # Existing (Phase II)
│   │   ├── security.py          # Existing (Phase II)
│   │   └── dependencies.py      # Existing (Phase II)
│   ├── db/
│   │   └── migrate.py           # Existing (Phase II)
│   └── main.py                  # Existing (Phase II)
└── tests/
    ├── test_mcp_tools.py        # NEW: MCP tool tests
    ├── test_agent.py            # NEW: Agent behavior tests
    └── test_chat_api.py         # NEW: Chat endpoint tests

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Existing (Phase II)
│   │   ├── page.tsx             # Existing (Phase II)
│   │   ├── login/               # Existing (Phase II)
│   │   ├── signup/              # Existing (Phase II)
│   │   ├── dashboard/           # Existing (Phase II)
│   │   └── chat/                # NEW: Chat page
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/                  # Existing (Phase II)
│   │   ├── layout/              # Existing (Phase II)
│   │   ├── auth/                # Existing (Phase II)
│   │   ├── tasks/               # Existing (Phase II)
│   │   └── chat/                # NEW: Chat components
│   │       ├── ChatInterface.tsx
│   │       ├── ChatMessage.tsx
│   │       └── ConversationList.tsx
│   ├── lib/
│   │   ├── api.ts               # Existing (Phase II)
│   │   ├── auth.ts              # Existing (Phase II)
│   │   ├── chat.ts              # NEW: Chat API client
│   │   └── types.ts             # Existing (Phase II) - extend with chat types
│   └── middleware.ts            # Existing (Phase II)
└── tests/
    └── chat/                    # NEW: Chat component tests
        ├── ChatInterface.test.tsx
        └── ChatMessage.test.tsx
```

**Structure Decision**: Web application structure (Option 2). Existing frontend/ and backend/ directories from Phase II are extended with new chat, agent, and MCP components. No new top-level directories created.

## Complexity Tracking

> **No violations detected. This section is empty.**

All constitution principles are satisfied without exceptions.

## Phase 0: Research & Technology Decisions

**Objective**: Research and document technology choices for Phase III implementation.

### Research Tasks

1. **OpenAI Agents SDK Integration**
   - Research: How to integrate OpenAI Agents SDK with FastAPI
   - Research: Agent configuration and tool registration patterns
   - Research: Stateless agent context management
   - Output: Best practices for agent orchestration

2. **Official MCP SDK Usage**
   - Research: MCP SDK installation and setup for Python
   - Research: Tool definition and registration patterns
   - Research: Error handling and validation in MCP tools
   - Output: MCP tool implementation patterns

3. **OpenRouter Integration**
   - Research: OpenRouter API compatibility with OpenAI SDK
   - Research: Model selection and configuration
   - Research: Rate limiting and error handling
   - Output: OpenRouter integration guide

4. **ChatKit Frontend Integration**
   - Research: OpenAI ChatKit installation and setup
   - Research: Custom backend endpoint configuration
   - Research: Message rendering and conversation management
   - Output: ChatKit integration patterns

5. **Conversation Persistence Strategy**
   - Research: Efficient conversation history loading
   - Research: Message pagination and context window management
   - Research: Database indexing for conversation queries
   - Output: Conversation persistence best practices

6. **Stateless Backend Design**
   - Research: Stateless session management patterns
   - Research: Context reconstruction from database
   - Research: Horizontal scaling considerations
   - Output: Stateless architecture patterns

**Output**: `research.md` with all technology decisions documented

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts, and setup guide.

### Data Model Design

**Entities to Define**:
1. Conversation (user_id, id, created_at, updated_at)
2. Message (user_id, id, conversation_id, role, content, created_at)
3. ChatRequest (conversation_id, message)
4. ChatResponse (conversation_id, response, tool_calls)
5. ToolCall (tool, input, output)

**Output**: `data-model.md` with entity definitions, relationships, and validation rules

### API Contracts

**Contracts to Generate**:
1. **Chat API** (OpenAPI 3.0):
   - POST /api/{user_id}/chat
   - Request/response schemas
   - Error responses
   - Authentication requirements

2. **MCP Tools** (JSON Schema):
   - add_task tool schema
   - list_tasks tool schema
   - update_task tool schema
   - delete_task tool schema
   - complete_task tool schema

**Output**: `contracts/chat-api.yaml` and `contracts/mcp-tools.yaml`

### Quickstart Guide

**Content**:
1. Prerequisites (Phase II setup complete)
2. Environment variables (OPENROUTER_API_KEY, etc.)
3. Database migration steps
4. Backend setup (install dependencies, run migrations)
5. Frontend setup (install dependencies, configure ChatKit)
6. Testing the chatbot (example conversations)

**Output**: `quickstart.md` with step-by-step setup instructions

### Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude` to update CLAUDE.md with Phase III technologies

**Output**: Updated CLAUDE.md with Phase III context

## Phase 2: Implementation Sequence

**Note**: This section outlines the implementation sequence. Actual task breakdown will be generated by `/sp.tasks` command.

### Sequence Overview

1. **Database Layer** (Foundation)
   - Create Conversation and Message models
   - Generate and run database migrations
   - Add indexes for performance

2. **MCP Tools Layer** (Tool Interface)
   - Implement 5 MCP tools with user_id scoping
   - Add input validation and error handling
   - Write unit tests for each tool

3. **Agent Layer** (Intelligence)
   - Implement agent orchestrator with OpenAI Agents SDK
   - Configure tool registration and intent mapping
   - Implement response generation logic
   - Add error handling and context management

4. **API Layer** (Backend Endpoint)
   - Implement POST /api/{user_id}/chat endpoint
   - Add JWT validation and user_id extraction
   - Implement conversation persistence logic
   - Add request/response validation

5. **Frontend Layer** (User Interface)
   - Create chat page and components
   - Integrate OpenAI ChatKit with OpenRouter
   - Implement message display and input handling
   - Add error handling and loading states

6. **Integration & Testing** (Validation)
   - Test full conversation flows
   - Test conversation persistence across restarts
   - Test user isolation and security
   - Test error scenarios

## Dependencies & Prerequisites

### External Dependencies

- Phase II implementation complete (users, tasks, authentication)
- Neon PostgreSQL database accessible
- OpenRouter API key obtained
- OpenAI Agents SDK available
- Official MCP SDK available
- OpenAI ChatKit library available

### Internal Dependencies

- Phase II database schema (users, tasks tables)
- Phase II authentication system (Better Auth + JWT)
- Phase II API infrastructure (FastAPI, SQLModel)
- Phase II frontend infrastructure (Next.js, Tailwind)

## Risk Assessment

### Technical Risks

1. **OpenAI Agents SDK Integration** (Medium)
   - Risk: SDK may have limited documentation or examples
   - Mitigation: Research SDK thoroughly in Phase 0, create proof of concept

2. **MCP SDK Compatibility** (Medium)
   - Risk: Official MCP SDK may have breaking changes or limited Python support
   - Mitigation: Verify SDK version compatibility, implement adapter layer if needed

3. **OpenRouter Reliability** (Low)
   - Risk: OpenRouter API may have downtime or rate limits
   - Mitigation: Implement retry logic, graceful error handling, fallback messages

4. **Stateless Context Reconstruction** (Medium)
   - Risk: Loading conversation history may be slow for long conversations
   - Mitigation: Limit context to last 50 messages, implement pagination

5. **ChatKit Customization** (Low)
   - Risk: ChatKit may have limited customization options
   - Mitigation: Research ChatKit capabilities in Phase 0, implement custom components if needed

### Mitigation Strategies

- Thorough research in Phase 0 before implementation
- Incremental implementation with testing at each layer
- Fallback to Phase II CRUD UI if chatbot unavailable
- Comprehensive error handling at all layers
- Performance monitoring and optimization

## Success Criteria

Implementation is complete when:

1. ✅ All 28 Phase III success criteria (SC-010 through SC-028) are met
2. ✅ All Phase II success criteria (SC-001 through SC-009) remain met
3. ✅ All acceptance criteria from specifications are validated
4. ✅ All unit, integration, and E2E tests pass
5. ✅ Conversation persistence works across server restarts
6. ✅ User isolation is enforced at all layers
7. ✅ Performance targets are met (<3s response time)
8. ✅ Documentation is complete and accurate

## Next Steps

1. **Complete Phase 0**: Generate `research.md` with technology decisions
2. **Complete Phase 1**: Generate `data-model.md`, `contracts/`, and `quickstart.md`
3. **Run `/sp.tasks`**: Generate detailed task breakdown for implementation
4. **Run `/sp.implement`**: Execute implementation tasks
5. **Validate**: Test against all success criteria
6. **Document**: Update README and create deployment guide

---

**Plan Status**: ✅ Ready for Phase 0 Research
**Next Command**: Continue with Phase 0 research generation
