# MCP Tools Specification

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the Model Context Protocol (MCP) tools that provide the standardized interface for all task operations. These tools are the exclusive mechanism for the AI agent to interact with task data, ensuring consistency, testability, and user isolation.

## Tool Interface Principles

1. **Stateless**: Tools hold no state; all state persisted in database
2. **User-Scoped**: All operations filter by user_id; no cross-user access
3. **Atomic**: Each tool performs a single, well-defined operation
4. **Idempotent**: Where possible, repeated calls with same input produce same result
5. **Validated**: All inputs validated before database operations
6. **Auditable**: All tool calls logged for debugging and compliance

## Tool Definitions

### Tool 1: add_task

**Purpose**: Create a new task for the authenticated user.

**Input Parameters**:
```json
{
  "user_id": "uuid-string",
  "title": "string",
  "description": "string or null"
}
```

**Parameter Schema**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| user_id | string (UUID) | Yes | Valid UUID | Authenticated user's ID |
| title | string | Yes | 1-100 characters | Task title |
| description | string | No | 0-500 characters or null | Task description (optional) |

**Database Interaction**:
1. Validate user_id exists in users table
2. Validate title length (1-100 characters)
3. Validate description length if provided (0-500 characters)
4. Generate new UUID for task id
5. Set completed = false
6. Set created_at and updated_at to current timestamp
7. Insert task record into tasks table
8. Return created task object

**Output**:
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T10:30:00Z"
}
```

**Error Scenarios**:

1. **Invalid user_id**: Return error "User not found"
2. **Empty title**: Return error "Title is required"
3. **Title too long**: Return error "Title must be 100 characters or less"
4. **Description too long**: Return error "Description must be 500 characters or less"
5. **Database error**: Return error "Unable to create task"

**Example Usage**:
```python
result = add_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    title="Buy groceries",
    description="Milk, eggs, bread"
)
```

---

### Tool 2: list_tasks

**Purpose**: Retrieve all tasks for the authenticated user, optionally filtered by completion status.

**Input Parameters**:
```json
{
  "user_id": "uuid-string",
  "completed": "boolean or null"
}
```

**Parameter Schema**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| user_id | string (UUID) | Yes | Valid UUID | Authenticated user's ID |
| completed | boolean | No | true, false, or null | Filter by completion status. Null returns all tasks |

**Database Interaction**:
1. Validate user_id exists in users table
2. Query tasks table WHERE user_id = {user_id}
3. If completed parameter provided, add AND completed = {completed}
4. Order by created_at DESC
5. Return list of task objects

**Output**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-02-08T10:30:00Z",
      "updated_at": "2026-02-08T10:30:00Z"
    },
    {
      "id": "uuid-string-2",
      "user_id": "uuid-string",
      "title": "Call mom",
      "description": null,
      "completed": true,
      "created_at": "2026-02-07T15:20:00Z",
      "updated_at": "2026-02-08T09:15:00Z"
    }
  ]
}
```

**Error Scenarios**:

1. **Invalid user_id**: Return error "User not found"
2. **Database error**: Return error "Unable to retrieve tasks"

**Example Usage**:
```python
# Get all tasks
result = list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    completed=None
)

# Get only incomplete tasks
result = list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    completed=False
)
```

---

### Tool 3: update_task

**Purpose**: Modify the title and/or description of an existing task.

**Input Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string",
  "title": "string or null",
  "description": "string or null"
}
```

**Parameter Schema**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| user_id | string (UUID) | Yes | Valid UUID | Authenticated user's ID |
| task_id | string (UUID) | Yes | Valid UUID | Task ID to update |
| title | string | No | 1-100 characters or null | New task title (null = no change) |
| description | string | No | 0-500 characters or null | New description (null = no change) |

**Database Interaction**:
1. Validate user_id exists in users table
2. Query task WHERE id = {task_id} AND user_id = {user_id}
3. If task not found, return error (404)
4. If title provided, validate length (1-100 characters) and update
5. If description provided, validate length (0-500 characters) and update
6. Set updated_at to current timestamp
7. Update task record in database
8. Return updated task object

**Output**:
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Buy groceries and milk",
  "description": "Milk, eggs, bread, cheese",
  "completed": false,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T11:45:00Z"
}
```

**Error Scenarios**:

1. **Invalid user_id**: Return error "User not found"
2. **Invalid task_id**: Return error "Task not found"
3. **Task belongs to different user**: Return error "Task not found" (404, not 403)
4. **Title too long**: Return error "Title must be 100 characters or less"
5. **Description too long**: Return error "Description must be 500 characters or less"
6. **No fields to update**: Return error "At least one field (title or description) must be provided"
7. **Database error**: Return error "Unable to update task"

**Example Usage**:
```python
# Update title only
result = update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    title="Buy groceries and milk",
    description=None
)

# Update both title and description
result = update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    title="Buy groceries and milk",
    description="Milk, eggs, bread, cheese"
)
```

---

### Tool 4: delete_task

**Purpose**: Permanently remove a task from the user's list.

**Input Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

**Parameter Schema**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| user_id | string (UUID) | Yes | Valid UUID | Authenticated user's ID |
| task_id | string (UUID) | Yes | Valid UUID | Task ID to delete |

**Database Interaction**:
1. Validate user_id exists in users table
2. Query task WHERE id = {task_id} AND user_id = {user_id}
3. If task not found, return error (404)
4. Delete task record from database
5. Return success confirmation

**Output**:
```json
{
  "success": true,
  "message": "Task deleted successfully",
  "deleted_task_id": "uuid-string"
}
```

**Error Scenarios**:

1. **Invalid user_id**: Return error "User not found"
2. **Invalid task_id**: Return error "Task not found"
3. **Task belongs to different user**: Return error "Task not found" (404, not 403)
4. **Database error**: Return error "Unable to delete task"

**Example Usage**:
```python
result = delete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
)
```

---

### Tool 5: complete_task

**Purpose**: Mark a task as completed.

**Input Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

**Parameter Schema**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| user_id | string (UUID) | Yes | Valid UUID | Authenticated user's ID |
| task_id | string (UUID) | Yes | Valid UUID | Task ID to mark complete |

**Database Interaction**:
1. Validate user_id exists in users table
2. Query task WHERE id = {task_id} AND user_id = {user_id}
3. If task not found, return error (404)
4. Set completed = true
5. Set updated_at to current timestamp
6. Update task record in database
7. Return updated task object

**Output**:
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T14:20:00Z"
}
```

**Error Scenarios**:

1. **Invalid user_id**: Return error "User not found"
2. **Invalid task_id**: Return error "Task not found"
3. **Task belongs to different user**: Return error "Task not found" (404, not 403)
4. **Task already completed**: Return success (idempotent operation)
5. **Database error**: Return error "Unable to complete task"

**Example Usage**:
```python
result = complete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
)
```

---

## Tool Implementation Requirements

### Technology Stack

- **MCP SDK**: Official MCP SDK for Python
- **ORM**: SQLModel for database operations
- **Database**: Neon PostgreSQL
- **Validation**: Pydantic models for input validation

### Security Requirements

1. **User Isolation**: All queries MUST filter by user_id
2. **Authorization**: Return 404 (not 403) for unauthorized access to prevent information leakage
3. **Input Validation**: Validate all inputs before database operations
4. **SQL Injection Prevention**: Use parameterized queries (SQLModel handles this)
5. **Audit Logging**: Log all tool invocations with user_id, tool name, and timestamp

### Performance Requirements

1. **Response Time**: Each tool call completes in <500ms (P95)
2. **Database Connection**: Use connection pooling
3. **Async Operations**: Support async/await for non-blocking I/O
4. **Batch Operations**: Support future batch operations (e.g., delete multiple tasks)

### Error Handling

1. **Consistent Format**: All errors return structured error objects
2. **User-Friendly Messages**: No technical jargon or stack traces
3. **Error Codes**: Use consistent error codes for client handling
4. **Logging**: Log all errors with context for debugging

### Testing Requirements

1. **Unit Tests**: Test each tool in isolation with mocked database
2. **Integration Tests**: Test tools with real database
3. **User Isolation Tests**: Verify users cannot access other users' tasks
4. **Error Scenario Tests**: Test all error scenarios
5. **Performance Tests**: Verify response time requirements

## Tool Chaining

The AI agent may chain multiple tool calls to fulfill complex requests:

**Example 1: "Complete the grocery task"**
1. Call `list_tasks` to find tasks matching "grocery"
2. Call `complete_task` with identified task_id

**Example 2: "Delete all completed tasks"**
1. Call `list_tasks` with completed=true
2. Call `delete_task` for each completed task

**Example 3: "Show me incomplete tasks and add a new one"**
1. Call `list_tasks` with completed=false
2. Call `add_task` with new task details

## Acceptance Criteria

- **AC-017**: All tools enforce user_id scoping with 100% accuracy
- **AC-018**: All tools validate inputs and return descriptive errors for invalid data
- **AC-019**: All tools complete in <500ms for 95% of requests
- **AC-020**: All tools are stateless and can be called from any backend instance
- **AC-021**: All tools return 404 (not 403) for unauthorized access
- **AC-022**: All tools log invocations for audit trail
- **AC-023**: complete_task is idempotent (repeated calls succeed)
- **AC-024**: All tools use SQLModel ORM with parameterized queries
- **AC-025**: All tools handle database errors gracefully
