<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 2.0.1 → 2.1.0

  Status: Phase III expansion - AI-Powered Todo Chatbot

  Modified principles:
    - V. Scalability Ready: Expanded to include AI/MCP architecture requirements

  Added sections:
    - VI. Stateless Architecture (NEW)
    - VII. AI-First Interaction (NEW)
    - VIII. Standardized Tool Interface (NEW)
    - Conversation Management standards
    - MCP Tools standards
    - Natural Language Commands standards

  Removed sections: None

  Technology Constraints updated:
    - Added: OpenRouter (AI model provider)
    - Added: OpenAI ChatKit (frontend chat UI)
    - Added: OpenAI Agents SDK (backend agent orchestration)
    - Added: Official MCP SDK (tool interface)
    - Clarified: OpenRouter key (not OpenAI API key)

  Database Models expanded:
    - Added: Conversation (user_id, id, created_at, updated_at)
    - Added: Message (user_id, id, conversation_id, role, content, created_at)
    - Existing: Task (unchanged from Phase II)

  Success Criteria updated:
    - Added SC-010 through SC-015 for Phase III chatbot functionality

  Templates validation:
    - .specify/templates/plan-template.md: ✅ Compatible (web app structure supports AI backend)
    - .specify/templates/spec-template.md: ✅ Compatible (user stories work for chatbot interactions)
    - .specify/templates/tasks-template.md: ✅ Compatible (backend/frontend structure already supported)

  Follow-up TODOs:
    - Create Phase III specifications in specs/003-ai-chatbot/
    - Update root CLAUDE.md to reference Phase III
    - Create backend/CLAUDE.md updates for MCP server guidance
    - Create frontend/CLAUDE.md updates for ChatKit integration
-->

# Evolution of Todo – Phase III Constitution

## Core Principles

### I. Spec-Driven Development

All features MUST be defined in Spec-Kit Plus spec files before implementation.

- No manual coding is permitted; all implementation code MUST be generated from specifications
- Each feature, API endpoint, database schema, UI component, MCP tool, and agent behavior requires a complete spec before implementation
- Specifications serve as the single source of truth for all behavior across frontend, backend, database, and AI agents
- Changes to behavior MUST first be reflected in updated specifications

**Rationale**: Ensures traceability, consistency, and that all code across the full stack (including AI agents) derives from explicit, documented requirements.

### II. End-to-End Traceability

Every frontend, backend, API, database, auth, MCP tool, and agent behavior change MUST be traceable to a spec file.

- Each UI component MUST reference its spec in `specs/ui/`
- Each API endpoint MUST reference its spec in `specs/api/`
- Each database entity MUST reference its spec in `specs/database/`
- Each feature MUST reference its spec in `specs/features/`
- Each MCP tool MUST reference its spec in `specs/mcp/`
- Each agent behavior MUST reference its spec in `specs/agent/`
- All PRs MUST include references to the specs that define the changes

**Rationale**: In a multi-layer architecture with AI agents, traceability ensures that changes can be audited, debugged, and validated across all tiers including agent decision-making.

### III. Security by Design

JWT-based authentication MUST be enforced using Better Auth for all protected operations.

- All API requests (except auth endpoints) MUST include `Authorization: Bearer <token>` header
- Backend MUST verify JWT tokens using `BETTER_AUTH_SECRET` environment variable
- Tokens MUST be validated on every request before processing
- Authentication failures MUST return HTTP 401 status code
- Invalid or expired tokens MUST be rejected with clear error messages
- AI agents MUST operate within authenticated user context only
- MCP tools MUST enforce user-scoped access to tasks

**Rationale**: A multi-user AI-powered application requires robust authentication; AI agents must never access data outside user scope.

### IV. Separation of Concerns

Frontend (Next.js), Backend (FastAPI), Database (Neon PostgreSQL), AI Agent Layer, MCP Tools, and Specs MUST be clearly separated.

- Frontend MUST only contain UI logic, state management, and API client code
- Backend MUST only contain business logic, data access, API endpoints, and agent orchestration
- AI Agent Layer MUST only contain agent behavior, tool invocation, and conversation management
- MCP Tools MUST only contain stateless task operations with database persistence
- Database migrations MUST be version-controlled and separate from application code
- Specs MUST be organized by domain: features/, api/, database/, ui/, mcp/, agent/
- Cross-cutting concerns MUST be documented in shared contracts

**Rationale**: Clear separation enables independent development, testing, and deployment of each tier, including AI agent behavior as a distinct concern.

### V. Scalability Ready

Monorepo architecture MUST support current Phase III (AI Chatbot) and future Phases (Kubernetes, Dapr, Kafka).

- Project structure MUST follow the mandatory monorepo layout
- Dependencies MUST be isolated to their respective packages (frontend, backend)
- Environment configuration MUST use environment variables, not hardcoded values
- API contracts MUST be versioned and backward-compatible where possible
- Database schema MUST support future extensions without breaking changes
- AI agent architecture MUST be stateless and horizontally scalable

**Rationale**: Phase III establishes AI-powered interaction; architectural decisions now prevent costly refactoring for future cloud-native deployments.

### VI. Stateless Architecture

Backend MUST hold no conversation state in memory; all state MUST be persisted in database.

- Conversation history MUST be stored in Conversation and Message tables
- Any server instance MUST be able to handle any request without in-memory session state
- Agent context MUST be reconstructed from database on each request
- Server restarts MUST NOT lose conversation continuity
- Horizontal scaling MUST be possible without sticky sessions

**Rationale**: Stateless architecture is essential for cloud deployment, horizontal scaling, and resilience in Kubernetes environments planned for future phases.

### VII. AI-First Interaction

Users MUST manage todos via natural language; AI agent MUST map commands to MCP tools.

- Primary user interface is conversational chat, not traditional CRUD forms
- AI agent MUST interpret user intent and invoke appropriate MCP tools
- OpenRouter (not OpenAI API) MUST be used as the AI model provider
- Agent behavior MUST be specified in agent behavior specifications
- Agent responses MUST be friendly, confirmatory, and handle errors gracefully
- Traditional CRUD UI (Phase II) remains available as fallback

**Rationale**: AI-first interaction is the core value proposition of Phase III; natural language interface must be the primary interaction model.

### VIII. Standardized Tool Interface

MCP tools MUST define all task operations; AI agent MUST use only these tools.

- MCP tools MUST expose exactly: add_task, list_tasks, complete_task, delete_task, update_task
- All task operations MUST go through MCP tool interface (no direct database access from agent)
- MCP tools MUST be stateless; all state persisted in database
- MCP tools MUST enforce user-scoped access (filter by authenticated user_id)
- Tool schemas MUST be versioned and documented in specs/mcp/

**Rationale**: Standardized tool interface ensures consistent behavior, testability, and enables future tool extensions without agent logic changes.

## Key Standards

### Authentication

- Better Auth MUST issue JWT tokens upon successful authentication
- Frontend MUST attach `Authorization: Bearer <token>` header to every API call
- Backend MUST verify JWT using `BETTER_AUTH_SECRET` environment variable
- Token refresh and expiration MUST be handled gracefully
- AI agent requests MUST include user context derived from JWT

### User Isolation

- All tasks MUST be linked to a `user_id` foreign key
- API MUST only return tasks belonging to the authenticated user
- Users MUST NOT be able to access, modify, or delete other users' tasks
- Database queries MUST always include user scope filtering
- MCP tools MUST enforce user_id filtering on all operations
- AI agents MUST operate only within authenticated user's data scope

### REST API Conventions

- All routes MUST be under `/api/` prefix
- HTTP status codes MUST follow conventions:
  - 200: Successful GET, PUT, PATCH
  - 201: Successful POST (resource created)
  - 401: Unauthorized (missing or invalid token)
  - 404: Resource not found
  - 422: Validation error (invalid input)
- Error responses MUST include descriptive messages
- Chat endpoint: `POST /api/{user_id}/chat` with conversation_id (optional) and message (required)

### Database

- SQLModel ORM MUST be used for all database operations
- Neon PostgreSQL connection MUST use `DATABASE_URL` environment variable
- Migrations MUST be version-controlled and reversible
- Schema changes MUST be documented in specs/database/
- Database models MUST include:
  - Task: user_id, id, title, description, completed, created_at, updated_at
  - Conversation: user_id, id, created_at, updated_at
  - Message: user_id, id, conversation_id, role (user/assistant), content, created_at

### Conversation Management

- All conversation history MUST be persisted in database
- Conversation state MUST be reconstructable from database on any server instance
- Messages MUST be stored with role (user/assistant), content, and timestamps
- Conversations MUST be user-scoped (filter by user_id)
- Backend MUST NOT hold conversation state in memory
- Server restarts MUST NOT lose conversation continuity

### MCP Tools

- MCP server MUST use Official MCP SDK
- Tools MUST be stateless; all state in database
- Tool operations MUST be atomic and idempotent where possible
- Tools MUST expose exactly these operations:
  - add_task: Create new task for user
  - list_tasks: Retrieve user's tasks (with optional filters)
  - complete_task: Mark task as completed
  - delete_task: Remove task
  - update_task: Modify task title/description
- All tools MUST enforce user_id scoping
- Tool schemas MUST be documented in specs/mcp/

### Natural Language Commands

- AI agent MUST map user natural language to MCP tool invocations
- Agent behavior MUST be specified in specs/agent/
- Agent MUST confirm actions before execution where appropriate
- Agent MUST handle errors gracefully with user-friendly messages
- Agent MUST provide context-aware responses
- Agent responses MUST reference specific tasks by title or ID when relevant

## Mandatory Monorepo Structure

```
hackathon-todo/
├── .specify/
│   ├── memory/constitution.md
│   ├── templates/
│   └── scripts/
├── specs/
│   ├── 001-todo-console-app/      # Phase I (legacy)
│   ├── 002-fullstack-web-app/     # Phase II
│   ├── 003-ai-chatbot/            # Phase III (NEW)
│   │   ├── overview.md
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── mcp/                   # MCP tool specs
│   │   ├── agent/                 # Agent behavior specs
│   │   └── conversation/          # Conversation flow specs
│   └── ...
├── CLAUDE.md                       # Root project guidance
├── frontend/
│   ├── CLAUDE.md                   # Frontend-specific guidance
│   ├── src/
│   │   ├── components/
│   │   │   └── chat/              # ChatKit integration (NEW)
│   │   ├── pages/
│   │   └── services/
│   └── ...
├── backend/
│   ├── CLAUDE.md                   # Backend-specific guidance
│   ├── src/
│   │   ├── models/                # Task, Conversation, Message
│   │   ├── services/
│   │   ├── api/
│   │   ├── agent/                 # Agent orchestration (NEW)
│   │   └── mcp/                   # MCP server (NEW)
│   └── ...
├── docker-compose.yml
└── README.md
```

## Technology Constraints

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend | Next.js | 16+ with App Router, TypeScript, Tailwind CSS |
| Frontend Chat UI | OpenAI ChatKit | Using OpenRouter as model provider |
| Backend | FastAPI | With SQLModel ORM |
| Backend Agent | OpenAI Agents SDK | Agent orchestration and tool invocation |
| Backend Tools | Official MCP SDK | Stateless tool interface |
| Database | Neon PostgreSQL | Serverless, connection via DATABASE_URL |
| Auth | Better Auth | JWT tokens, shared BETTER_AUTH_SECRET |
| AI Model Provider | OpenRouter | NOT OpenAI API - use NEXT_PUBLIC_OPENROUTER_KEY |
| Specs | Spec-Kit Plus | All features, APIs, DB, MCP tools, agent behavior documented |

## Success Criteria

Measurable outcomes that define Phase III completion:

### Phase II Criteria (Still Required)

- **SC-001**: Logged-in user can sign up, sign in, and manage only their own tasks
- **SC-002**: Backend rejects unauthenticated requests with HTTP 401
- **SC-003**: JWT token is required for every API call (except auth endpoints)
- **SC-004**: Repository contains organized Spec-Kit specs with full traceability
- **SC-005**: Layered CLAUDE.md files exist for root, frontend/, and backend/
- **SC-006**: Working Next.js frontend with authentication UI
- **SC-007**: Working FastAPI backend with JWT validation
- **SC-008**: Neon PostgreSQL integration with user-scoped task storage
- **SC-009**: Architecture is ready to extend into future phases

### Phase III Criteria (New)

- **SC-010**: User can interact with chatbot via natural language to add, view, update, delete, and complete tasks
- **SC-011**: AI agent correctly invokes MCP tools based on user intent
- **SC-012**: Backend persists conversation and message history in database
- **SC-013**: Server is stateless; conversation resumes seamlessly after restarts
- **SC-014**: MCP tools enforce user-scoped access; users cannot access other users' tasks via chatbot
- **SC-015**: ChatKit frontend connects to backend `/api/{user_id}/chat` endpoint using OpenRouter

## Development Workflow

The following workflow MUST be followed for all feature development:

1. **Specify**: Define feature requirements in spec.md before any implementation
2. **Plan**: Create implementation plan documenting technical approach for all layers (including AI/MCP)
3. **Generate**: Use Claude Code to generate all implementation code (frontend, backend, database, MCP tools, agent behavior)
4. **Validate**: Verify generated code meets specification requirements across all tiers
5. **Document**: Record all significant decisions and prompt history

**Prohibited Actions**:
- Manual code edits outside of generated output
- Implementation without prior specification
- Skipping validation against acceptance criteria
- Hardcoding secrets or configuration values
- Bypassing authentication for protected endpoints
- Direct database access from AI agent (must use MCP tools)
- Using OpenAI API key instead of OpenRouter key
- Storing conversation state in memory (must persist in database)

## Governance

This constitution supersedes all other practices for the Evolution of Todo project.

**Amendment Process**:
1. Proposed changes MUST be documented with rationale
2. Changes MUST be reviewed for impact on existing specifications
3. Version MUST be incremented according to semantic versioning:
   - MAJOR: Principle removals or incompatible redefinitions
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording, or non-semantic refinements

**Compliance**:
- All specifications MUST reference applicable principles
- All PRs/reviews MUST verify compliance with this constitution
- Security additions MUST be justified against Security by Design principle
- Architectural changes MUST be justified against Scalability Ready and Stateless Architecture principles
- AI agent behavior MUST be justified against AI-First Interaction and Standardized Tool Interface principles

**Version**: 2.1.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-02-08
