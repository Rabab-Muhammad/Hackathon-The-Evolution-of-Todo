# Architecture Specification: Phase III AI Chatbot

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the architectural design for Phase III AI-powered chatbot, including component interactions, data flow, stateless backend design, and integration patterns between ChatKit frontend, FastAPI backend, OpenAI Agents SDK, MCP tools, and Neon PostgreSQL database.

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  ChatKit UI (Next.js)                                   │    │
│  │  - Chat interface                                       │    │
│  │  - Message display                                      │    │
│  │  - OpenRouter integration                               │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS + JWT
                              │ POST /api/{user_id}/chat
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Stateless)                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Chat Endpoint (/api/{user_id}/chat)                   │    │
│  │  - JWT validation                                       │    │
│  │  - Request parsing                                      │    │
│  │  - Response formatting                                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Agent Orchestrator (OpenAI Agents SDK)                │    │
│  │  - Load conversation history from DB                    │    │
│  │  - Interpret user intent                                │    │
│  │  - Select appropriate MCP tools                         │    │
│  │  - Execute tool calls                                   │    │
│  │  - Generate response                                    │    │
│  │  - Store messages in DB                                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ↓                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  MCP Server (Official MCP SDK)                         │    │
│  │  - add_task                                             │    │
│  │  - list_tasks                                           │    │
│  │  - update_task                                          │    │
│  │  - delete_task                                          │    │
│  │  - complete_task                                        │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ SQLModel ORM
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Neon PostgreSQL (Persistent Storage)                │
│  - users (Phase II)                                              │
│  - tasks (Phase II, accessed via MCP tools)                      │
│  - conversations (Phase III)                                     │
│  - messages (Phase III)                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. ChatKit Frontend (Next.js)

**Responsibilities**:
- Render chat interface for user interaction
- Send user messages to backend chat endpoint
- Display assistant responses and conversation history
- Handle authentication (JWT token management)
- Integrate with OpenRouter for AI inference

**Technology**:
- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- OpenAI ChatKit library
- OpenRouter API client

**Key Characteristics**:
- Stateless (loads conversation history from backend)
- Responsive design (mobile and desktop)
- Real-time message updates
- Error handling for network/API failures

### 2. FastAPI Backend

**Responsibilities**:
- Expose chat endpoint (`POST /api/{user_id}/chat`)
- Validate JWT tokens
- Orchestrate agent and MCP tool interactions
- Persist conversation and message data
- Return formatted responses to frontend

**Technology**:
- FastAPI
- SQLModel ORM
- OpenAI Agents SDK
- Official MCP SDK
- Better Auth (JWT validation)

**Key Characteristics**:
- **Stateless**: No in-memory conversation state
- **Horizontally Scalable**: Any instance can handle any request
- **Resilient**: Server restarts do not lose conversation continuity
- **Secure**: JWT validation on every request

### 3. Agent Orchestrator (OpenAI Agents SDK)

**Responsibilities**:
- Reconstruct conversation context from database
- Interpret user intent from natural language message
- Select appropriate MCP tool(s) to fulfill intent
- Chain multiple tools when necessary (e.g., find then delete)
- Generate friendly, confirmatory responses
- Handle errors gracefully

**Technology**:
- OpenAI Agents SDK
- Custom agent behavior configuration

**Key Characteristics**:
- Stateless (context from database)
- Tool-based (never direct database access)
- User-scoped (operates only on authenticated user's data)
- Configurable behavior (no hardcoded prompts)

### 4. MCP Server (Official MCP SDK)

**Responsibilities**:
- Provide standardized tool interface for task operations
- Enforce user_id scoping on all operations
- Validate tool inputs
- Execute database operations via SQLModel
- Return structured tool outputs

**Technology**:
- Official MCP SDK
- SQLModel ORM

**Tools Provided**:
1. `add_task`: Create new task
2. `list_tasks`: Retrieve user's tasks (with optional filters)
3. `update_task`: Modify task title/description
4. `delete_task`: Remove task
5. `complete_task`: Mark task as completed

**Key Characteristics**:
- Stateless (all state in database)
- Atomic operations
- User-scoped (all queries filter by user_id)
- Idempotent where possible

### 5. Neon PostgreSQL Database

**Responsibilities**:
- Persist all application data
- Store conversation history and messages
- Maintain task data with user isolation
- Support concurrent access from multiple backend instances

**Schema**:
- `users` (Phase II)
- `tasks` (Phase II)
- `conversations` (Phase III)
- `messages` (Phase III)

**Key Characteristics**:
- Serverless PostgreSQL
- Connection pooling
- ACID transactions
- User-scoped data isolation

## Data Flow

### Request Flow: User Sends Message

1. **User Input**: User types message in ChatKit UI
2. **Frontend**: ChatKit sends POST request to `/api/{user_id}/chat` with JWT token
3. **Backend - Authentication**: FastAPI validates JWT, extracts user_id
4. **Backend - Load Context**: If conversation_id provided, load conversation history from database
5. **Backend - Agent**: Agent Orchestrator receives message and conversation context
6. **Agent - Intent**: Agent interprets user intent (e.g., "add task to buy groceries")
7. **Agent - Tool Selection**: Agent selects `add_task` MCP tool
8. **MCP Tool - Execution**: `add_task` tool creates task in database (filtered by user_id)
9. **MCP Tool - Response**: Tool returns created task object
10. **Agent - Response Generation**: Agent generates friendly confirmation message
11. **Backend - Persist**: Store user message and assistant response in database
12. **Backend - Response**: Return conversation_id, response, and tool_calls to frontend
13. **Frontend - Display**: ChatKit displays assistant response to user

### Stateless Request Cycle

Each request is independent:
- No session state stored in backend memory
- Conversation context reconstructed from database on each request
- Any backend instance can handle any request
- Server restarts do not affect conversation continuity

**Example**:
```
Request 1 → Server Instance A → Database
Request 2 → Server Instance B → Database (loads same conversation)
Request 3 → Server Instance A → Database (after restart, loads conversation)
```

### Conversation Persistence

**New Conversation**:
1. User sends message without conversation_id
2. Backend creates new Conversation record in database
3. Backend stores user message as Message record
4. Agent processes and generates response
5. Backend stores assistant response as Message record
6. Backend returns conversation_id to frontend

**Existing Conversation**:
1. User sends message with conversation_id
2. Backend loads all Message records for conversation_id
3. Agent uses message history as context
4. Agent processes new message and generates response
5. Backend appends new user and assistant messages to database
6. Backend returns updated conversation_id

## Authentication Flow

1. User logs in via Phase II authentication (Better Auth)
2. Backend issues JWT token with user_id claim
3. Frontend stores JWT token (localStorage)
4. Frontend includes JWT in Authorization header for all chat requests
5. Backend validates JWT on every chat request
6. Backend extracts user_id from JWT
7. Agent and MCP tools operate only on authenticated user's data

**Security**:
- JWT required for all chat endpoints
- user_id extracted from JWT (not from request body)
- MCP tools enforce user_id filtering
- 401 response if JWT invalid or missing

## Error Handling

### Frontend Errors
- Network failure: Display "Connection error, please try again"
- 401 Unauthorized: Redirect to login
- 500 Server error: Display "Something went wrong, please try again"
- Timeout: Display "Request timed out, please try again"

### Backend Errors
- Invalid JWT: Return 401 with error message
- Missing message: Return 400 with validation error
- Database connection failure: Return 500 with generic error
- MCP tool error: Agent catches and generates user-friendly response

### Agent Errors
- Task not found: "I couldn't find that task. Could you describe it differently?"
- Invalid input: "I need more information. Could you provide [specific detail]?"
- Ambiguous intent: "Did you mean [option A] or [option B]?"

## Scalability Considerations

### Horizontal Scaling
- Stateless backend enables multiple instances
- Load balancer distributes requests across instances
- Database connection pooling handles concurrent access
- No session affinity required

### Performance Optimization
- Database indexes on user_id, conversation_id
- Connection pooling for database
- Async I/O for database and MCP tool calls
- Response caching where appropriate (future enhancement)

### Future Enhancements (Phase IV+)
- Message queue for async processing (Kafka)
- Distributed tracing (Dapr observability)
- Service mesh for microservices (Kubernetes + Dapr)
- Multi-region deployment

## Technology Constraints

| Constraint | Rationale |
|------------|-----------|
| OpenRouter (not OpenAI API) | Provider independence, cost optimization |
| Official MCP SDK | Standardized tool interface, future compatibility |
| Stateless backend | Horizontal scaling, resilience, cloud-native |
| SQLModel ORM | Type safety, Pydantic integration, simplicity |
| Neon PostgreSQL | Serverless, auto-scaling, cost-effective |

## Acceptance Criteria

- **AC-001**: Architecture supports stateless backend with conversation persistence in database
- **AC-002**: Any backend instance can handle any chat request without session affinity
- **AC-003**: Server restarts do not lose conversation history or continuity
- **AC-004**: Agent uses only MCP tools for task operations (no direct database access)
- **AC-005**: All components enforce user_id scoping and JWT authentication
- **AC-006**: System handles 100 concurrent users with <3s response time
- **AC-007**: Architecture is ready for Phase IV Kubernetes deployment
