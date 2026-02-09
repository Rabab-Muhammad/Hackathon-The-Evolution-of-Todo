# Backend CLAUDE.md - FastAPI Application

## Overview

FastAPI backend with SQLModel ORM, OpenAI Agents SDK, and MCP server for Phase III AI-powered todo chatbot.

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI app entry
│   ├── core/
│   │   ├── config.py           # Environment config
│   │   ├── database.py         # Database connection
│   │   ├── security.py         # Password hashing, JWT
│   │   └── dependencies.py     # DI (current_user, db)
│   ├── models/
│   │   ├── user.py             # User SQLModel
│   │   ├── task.py             # Task SQLModel
│   │   ├── conversation.py     # Conversation SQLModel (Phase III)
│   │   └── message.py          # Message SQLModel (Phase III)
│   ├── schemas/
│   │   ├── auth.py             # Auth request/response
│   │   ├── task.py             # Task request/response
│   │   ├── chat.py             # Chat request/response (Phase III)
│   │   └── error.py            # Error response
│   ├── api/
│   │   ├── router.py           # Main router
│   │   ├── auth.py             # Auth endpoints
│   │   ├── tasks.py            # Task endpoints
│   │   └── chat.py             # Chat endpoint (Phase III)
│   ├── services/
│   │   ├── auth.py             # Auth business logic
│   │   └── task.py             # Task business logic
│   ├── agent/                  # Phase III: Agent orchestration
│   │   ├── orchestrator.py     # Agent orchestration logic
│   │   └── behavior.py         # Agent behavior implementation
│   ├── mcp/                    # Phase III: MCP server
│   │   ├── server.py           # MCP server setup
│   │   └── tools.py            # MCP tool implementations
│   └── db/
│       └── migrate.py          # Migration runner
└── tests/
```

## Key Specifications

### Phase III (Current)
- **MCP Tools**: `@specs/003-ai-chatbot/mcp/`
- **Agent Behavior**: `@specs/003-ai-chatbot/agent/`
- **Conversation Flows**: `@specs/003-ai-chatbot/conversation/`

### Phase II (Still Required)
- **Database Schema**: `@specs/002-fullstack-web-app/database/schema.md`
- **REST Endpoints**: `@specs/002-fullstack-web-app/api/rest-endpoints.md`
- **JWT Flow**: `@specs/002-fullstack-web-app/api/jwt-auth.md`
- **API Contract**: `@specs/002-fullstack-web-app/contracts/api-contract.md`

## Implementation Rules

### Authentication
- Hash passwords with bcrypt
- Sign JWTs with HS256 using `BETTER_AUTH_SECRET`
- Token claims: `sub` (user_id), `email`, `iat`, `exp`
- 24-hour token expiration
- AI agents MUST operate within authenticated user context

### User Isolation
- ALL task queries MUST filter by `user_id`
- Return 404 for tasks not owned by user (not 403)
- Extract user_id from JWT in middleware
- MCP tools MUST enforce user_id filtering on all operations
- AI agents MUST operate only within authenticated user's data scope

### Stateless Architecture (Phase III)
- Backend MUST hold NO conversation state in memory
- All conversation history MUST be persisted in database
- Any server instance MUST handle any request
- Agent context MUST be reconstructed from database on each request
- Server restarts MUST NOT lose conversation continuity

### Error Handling
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [{"field": "name", "message": "error"}]
  }
}
```

### Status Codes
- 200: Successful GET, PUT, PATCH, DELETE
- 201: Successful POST (resource created)
- 401: Authentication required/failed
- 404: Resource not found
- 409: Conflict (duplicate email)
- 422: Validation error

## Database Models

### User
- `id`: UUID (PK)
- `email`: str (unique)
- `password_hash`: str
- `created_at`: datetime

### Task
- `id`: UUID (PK)
- `user_id`: UUID (FK → users.id)
- `title`: str (max 100)
- `description`: str (max 500, nullable)
- `completed`: bool (default false)
- `created_at`, `updated_at`: datetime

### Conversation (Phase III)
- `id`: UUID (PK)
- `user_id`: UUID (FK → users.id)
- `created_at`: datetime
- `updated_at`: datetime

### Message (Phase III)
- `id`: UUID (PK)
- `user_id`: UUID (FK → users.id)
- `conversation_id`: UUID (FK → conversations.id)
- `role`: str (enum: "user", "assistant")
- `content`: str
- `created_at`: datetime

## MCP Tools (Phase III)

### Tool Interface
- Use Official MCP SDK
- All tools MUST be stateless
- All state persisted in database
- All tools MUST enforce user_id scoping

### Required Tools
1. **add_task**: Create new task for user
   - Input: `user_id`, `title`, `description` (optional)
   - Output: Created task object
   - Validation: title max 100 chars, description max 500 chars

2. **list_tasks**: Retrieve user's tasks
   - Input: `user_id`, `completed` (optional filter)
   - Output: List of task objects
   - Filter by user_id and optional completed status

3. **complete_task**: Mark task as completed
   - Input: `user_id`, `task_id`
   - Output: Updated task object
   - Validation: Task must belong to user (404 if not)

4. **delete_task**: Remove task
   - Input: `user_id`, `task_id`
   - Output: Success confirmation
   - Validation: Task must belong to user (404 if not)

5. **update_task**: Modify task title/description
   - Input: `user_id`, `task_id`, `title` (optional), `description` (optional)
   - Output: Updated task object
   - Validation: Task must belong to user, same constraints as add_task

## Agent Orchestration (Phase III)

### Agent Behavior
- Use OpenAI Agents SDK for agent orchestration
- Agent MUST map natural language to MCP tool invocations
- Agent behavior specified in `@specs/003-ai-chatbot/agent/`
- Agent MUST confirm actions before execution where appropriate
- Agent MUST handle errors gracefully with user-friendly messages
- Agent responses MUST reference specific tasks by title or ID

### Chat Endpoint
```
POST /api/{user_id}/chat
```

**Request**:
```json
{
  "conversation_id": "uuid-optional",
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": "uuid",
  "response": "I've added the task 'Buy groceries' to your list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": {"title": "Buy groceries"},
      "output": {"id": "uuid", "title": "Buy groceries", "completed": false}
    }
  ]
}
```

### Conversation Management
- If `conversation_id` not provided, create new conversation
- If `conversation_id` provided, load conversation history from database
- Store user message in database before processing
- Store assistant response in database after processing
- Reconstruct agent context from database messages on each request

## Environment Variables

```env
# Phase II (Required)
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=<32+ character secret>

# Phase III (New)
# Note: OpenRouter key is frontend-only (NEXT_PUBLIC_OPENROUTER_KEY)
# Backend uses MCP tools and Agents SDK without direct AI model access
```

## Testing

- pytest for all tests
- TestClient for API tests
- Test user isolation explicitly
- Test MCP tools with user_id scoping
- Test conversation persistence and reconstruction
- Test stateless behavior (no in-memory state)

## Prohibited Actions

- Direct database access from AI agent (MUST use MCP tools)
- Storing conversation state in memory
- Bypassing user_id filtering in MCP tools
- Using OpenAI API key (use OpenRouter via frontend)
