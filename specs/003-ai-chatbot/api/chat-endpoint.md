# API Specification: Chat Endpoint

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the REST API endpoint for chat interactions between frontend and backend. This endpoint handles user messages, orchestrates agent processing, invokes MCP tools, and returns assistant responses with conversation context.

## Endpoint Definition

### POST /api/{user_id}/chat

**Description**: Process user message and return assistant response with tool invocations.

**Authentication**: Required (JWT Bearer token)

**Path Parameters**:
- `user_id` (string, UUID): Authenticated user's ID (must match JWT claim)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "conversation_id": "uuid-string-optional",
  "message": "Add a task to buy groceries"
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| conversation_id | string (UUID) | No | Valid UUID or null | Existing conversation ID. If omitted, creates new conversation |
| message | string | Yes | 1-2000 characters | User's natural language message |

**Response Body** (Success - 200):
```json
{
  "conversation_id": "uuid-string",
  "response": "I've added the task 'Buy groceries' to your list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": {
        "user_id": "uuid-string",
        "title": "Buy groceries",
        "description": null
      },
      "output": {
        "id": "uuid-string",
        "user_id": "uuid-string",
        "title": "Buy groceries",
        "description": null,
        "completed": false,
        "created_at": "2026-02-08T10:30:00Z",
        "updated_at": "2026-02-08T10:30:00Z"
      }
    }
  ]
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| conversation_id | string (UUID) | Conversation ID (new or existing) |
| response | string | Assistant's natural language response |
| tool_calls | array | List of MCP tool invocations (may be empty) |
| tool_calls[].tool | string | Tool name (add_task, list_tasks, etc.) |
| tool_calls[].input | object | Tool input parameters |
| tool_calls[].output | object | Tool output result |

## Request Flow

### New Conversation Flow

1. **Request Received**: Frontend sends message without conversation_id
2. **Authentication**: Backend validates JWT token, extracts user_id
3. **Path Validation**: Verify path user_id matches JWT user_id claim
4. **Create Conversation**: Backend creates new Conversation record in database
5. **Store User Message**: Backend creates Message record (role: "user", content: message)
6. **Agent Processing**: Agent interprets message and invokes MCP tools
7. **Store Assistant Response**: Backend creates Message record (role: "assistant", content: response)
8. **Return Response**: Backend returns conversation_id, response, and tool_calls

### Existing Conversation Flow

1. **Request Received**: Frontend sends message with conversation_id
2. **Authentication**: Backend validates JWT token, extracts user_id
3. **Path Validation**: Verify path user_id matches JWT user_id claim
4. **Load Conversation**: Backend loads Conversation record, verify user_id matches
5. **Load History**: Backend loads all Message records for conversation_id
6. **Store User Message**: Backend creates new Message record (role: "user")
7. **Agent Processing**: Agent uses conversation history as context, interprets message, invokes tools
8. **Store Assistant Response**: Backend creates Message record (role: "assistant")
9. **Return Response**: Backend returns conversation_id, response, and tool_calls

## Validation & Error Handling

### Request Validation

**Missing Authorization Header**:
```json
HTTP 401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Please log in.",
    "details": []
  }
}
```

**Invalid JWT Token**:
```json
HTTP 401 Unauthorized
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired authentication token.",
    "details": []
  }
}
```

**Path user_id Mismatch**:
```json
HTTP 403 Forbidden
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You can only access your own conversations.",
    "details": []
  }
}
```

**Missing Message Field**:
```json
HTTP 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": [
      {
        "field": "message",
        "message": "Message is required."
      }
    ]
  }
}
```

**Message Too Long**:
```json
HTTP 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": [
      {
        "field": "message",
        "message": "Message must be 2000 characters or less."
      }
    ]
  }
}
```

**Empty Message**:
```json
HTTP 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": [
      {
        "field": "message",
        "message": "Message cannot be empty."
      }
    ]
  }
}
```

**Invalid conversation_id Format**:
```json
HTTP 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data.",
    "details": [
      {
        "field": "conversation_id",
        "message": "Conversation ID must be a valid UUID."
      }
    ]
  }
}
```

**Conversation Not Found**:
```json
HTTP 404 Not Found
{
  "error": {
    "code": "CONVERSATION_NOT_FOUND",
    "message": "Conversation not found.",
    "details": []
  }
}
```

**Conversation Belongs to Different User**:
```json
HTTP 404 Not Found
{
  "error": {
    "code": "CONVERSATION_NOT_FOUND",
    "message": "Conversation not found.",
    "details": []
  }
}
```
*Note: Return 404 instead of 403 to avoid leaking conversation existence*

**Database Connection Error**:
```json
HTTP 500 Internal Server Error
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again.",
    "details": []
  }
}
```

**Agent Processing Error**:
```json
HTTP 500 Internal Server Error
{
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "Unable to process your message. Please try again.",
    "details": []
  }
}
```

## Stateless Design

### No In-Memory State

- Backend does NOT store conversation state in memory
- Each request is independent and self-contained
- Conversation context reconstructed from database on every request
- Any backend instance can handle any request

### Request Independence

**Example Scenario**:
```
Request 1: User sends "Add task X" → Server A processes → Stores in DB
Request 2: User sends "Show my tasks" → Server B processes → Loads from DB
Request 3: User sends "Complete task X" → Server A processes (after restart) → Loads from DB
```

All three requests succeed because:
- No session affinity required
- All state persisted in database
- Context reconstructed on each request

## Performance Considerations

### Response Time Targets

- **P50**: <1.5 seconds
- **P95**: <3 seconds
- **P99**: <5 seconds

### Optimization Strategies

1. **Database Connection Pooling**: Reuse connections across requests
2. **Async I/O**: Non-blocking database and MCP tool calls
3. **Conversation History Limit**: Load only last 50 messages for context (configurable)
4. **Tool Call Parallelization**: Execute independent tool calls concurrently
5. **Response Streaming**: Stream assistant response as it's generated (future enhancement)

## Security Requirements

### Authentication

- JWT token MUST be validated on every request
- Token MUST contain valid user_id claim
- Expired tokens MUST be rejected with 401

### Authorization

- Path user_id MUST match JWT user_id claim
- Conversation user_id MUST match authenticated user_id
- Return 404 (not 403) for unauthorized conversation access

### Input Sanitization

- Message content MUST be sanitized to prevent injection attacks
- conversation_id MUST be validated as UUID format
- user_id MUST be validated as UUID format

### Rate Limiting

- Implement rate limiting to prevent abuse (e.g., 60 requests per minute per user)
- Return 429 Too Many Requests if limit exceeded

## Example Interactions

### Example 1: Create First Task

**Request**:
```http
POST /api/550e8400-e29b-41d4-a716-446655440000/chat
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "response": "I've added the task 'Buy groceries' to your list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Buy groceries",
        "description": null
      },
      "output": {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Buy groceries",
        "description": null,
        "completed": false,
        "created_at": "2026-02-08T10:30:00Z",
        "updated_at": "2026-02-08T10:30:00Z"
      }
    }
  ]
}
```

### Example 2: View Tasks in Same Conversation

**Request**:
```http
POST /api/550e8400-e29b-41d4-a716-446655440000/chat
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "message": "Show me my tasks"
}
```

**Response**:
```json
{
  "conversation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "response": "You have 1 task:\n1. Buy groceries (not completed)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "input": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "completed": null
      },
      "output": {
        "tasks": [
          {
            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "title": "Buy groceries",
            "description": null,
            "completed": false,
            "created_at": "2026-02-08T10:30:00Z",
            "updated_at": "2026-02-08T10:30:00Z"
          }
        ]
      }
    }
  ]
}
```

## Acceptance Criteria

- **AC-008**: Endpoint validates JWT token and rejects unauthorized requests with 401
- **AC-009**: Endpoint creates new conversation when conversation_id not provided
- **AC-010**: Endpoint loads existing conversation when conversation_id provided
- **AC-011**: Endpoint returns 404 when conversation belongs to different user
- **AC-012**: Endpoint persists user and assistant messages in database
- **AC-013**: Endpoint returns conversation_id, response, and tool_calls in response
- **AC-014**: Endpoint handles validation errors with 400 and descriptive messages
- **AC-015**: Endpoint responds within 3 seconds for 95% of requests
- **AC-016**: Endpoint is stateless and can be handled by any backend instance
