# MCP Tools Contract Specification

**Feature**: Phase III AI-Powered Todo Chatbot
**Date**: 2026-02-08
**Format**: JSON Schema

## Purpose

Define the input and output schemas for all 5 MCP tools used by the AI agent. These schemas ensure consistent tool interfaces and enable validation.

---

## Tool 1: add_task

**Description**: Create a new task for the authenticated user.

### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["user_id", "title"],
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user's ID"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "Task title"
    },
    "description": {
      "type": ["string", "null"],
      "maxLength": 500,
      "description": "Optional task description"
    }
  }
}
```

### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Task ID"
    },
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Owner user ID"
    },
    "title": {
      "type": "string",
      "description": "Task title"
    },
    "description": {
      "type": ["string", "null"],
      "description": "Task description"
    },
    "completed": {
      "type": "boolean",
      "description": "Completion status"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last update timestamp"
    }
  }
}
```

### Error Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "enum": [
        "User not found",
        "Title is required",
        "Title must be 100 characters or less",
        "Description must be 500 characters or less",
        "Unable to create task"
      ]
    }
  }
}
```

---

## Tool 2: list_tasks

**Description**: Retrieve all tasks for the authenticated user, optionally filtered by completion status.

### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["user_id"],
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user's ID"
    },
    "completed": {
      "type": ["boolean", "null"],
      "description": "Filter by completion status (null = all tasks)"
    }
  }
}
```

### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["tasks"],
  "properties": {
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"],
        "properties": {
          "id": {
            "type": "string",
            "format": "uuid"
          },
          "user_id": {
            "type": "string",
            "format": "uuid"
          },
          "title": {
            "type": "string"
          },
          "description": {
            "type": ["string", "null"]
          },
          "completed": {
            "type": "boolean"
          },
          "created_at": {
            "type": "string",
            "format": "date-time"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time"
          }
        }
      }
    }
  }
}
```

### Error Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "enum": [
        "User not found",
        "Unable to retrieve tasks"
      ]
    }
  }
}
```

---

## Tool 3: update_task

**Description**: Modify the title and/or description of an existing task.

### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["user_id", "task_id"],
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Task ID to update"
    },
    "title": {
      "type": ["string", "null"],
      "minLength": 1,
      "maxLength": 100,
      "description": "New task title (null = no change)"
    },
    "description": {
      "type": ["string", "null"],
      "maxLength": 500,
      "description": "New task description (null = no change)"
    }
  }
}
```

### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "user_id": {
      "type": "string",
      "format": "uuid"
    },
    "title": {
      "type": "string"
    },
    "description": {
      "type": ["string", "null"]
    },
    "completed": {
      "type": "boolean"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### Error Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "enum": [
        "User not found",
        "Task not found",
        "Title must be 100 characters or less",
        "Description must be 500 characters or less",
        "At least one field (title or description) must be provided",
        "Unable to update task"
      ]
    }
  }
}
```

---

## Tool 4: delete_task

**Description**: Permanently remove a task from the user's list.

### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["user_id", "task_id"],
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Task ID to delete"
    }
  }
}
```

### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success", "message", "deleted_task_id"],
  "properties": {
    "success": {
      "type": "boolean",
      "const": true
    },
    "message": {
      "type": "string",
      "const": "Task deleted successfully"
    },
    "deleted_task_id": {
      "type": "string",
      "format": "uuid"
    }
  }
}
```

### Error Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "enum": [
        "User not found",
        "Task not found",
        "Unable to delete task"
      ]
    }
  }
}
```

---

## Tool 5: complete_task

**Description**: Mark a task as completed.

### Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["user_id", "task_id"],
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Task ID to mark complete"
    }
  }
}
```

### Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "user_id": {
      "type": "string",
      "format": "uuid"
    },
    "title": {
      "type": "string"
    },
    "description": {
      "type": ["string", "null"]
    },
    "completed": {
      "type": "boolean",
      "const": true
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### Error Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "enum": [
        "User not found",
        "Task not found",
        "Unable to complete task"
      ]
    }
  }
}
```

---

## Tool Registration (OpenAI Function Calling Format)

For integration with OpenAI Agents SDK, tools are registered in function calling format:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "title": {"type": "string", "minLength": 1, "maxLength": 100},
                    "description": {"type": "string", "maxLength": 500}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve user's tasks, optionally filtered by completion status",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "completed": {"type": "boolean"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Modify task title and/or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "string", "format": "uuid"},
                    "title": {"type": "string", "minLength": 1, "maxLength": 100},
                    "description": {"type": "string", "maxLength": 500}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently remove a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "string", "format": "uuid"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "string", "format": "uuid"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]
```

---

## Validation Rules

### Common Rules (All Tools)

- `user_id` must be valid UUID format
- `user_id` must reference existing user in database
- All operations must filter by `user_id` (user isolation)
- Return 404 (not 403) for unauthorized access

### Tool-Specific Rules

**add_task**:
- `title` required, 1-100 characters
- `description` optional, 0-500 characters

**list_tasks**:
- `completed` optional, boolean or null
- Returns empty array if no tasks found

**update_task**:
- `task_id` must reference existing task owned by user
- At least one of `title` or `description` must be provided
- `title` if provided: 1-100 characters
- `description` if provided: 0-500 characters

**delete_task**:
- `task_id` must reference existing task owned by user
- Operation is idempotent (returns success even if already deleted)

**complete_task**:
- `task_id` must reference existing task owned by user
- Operation is idempotent (returns success even if already completed)

---

## Usage Examples

### Example 1: Add Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Output**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T10:30:00Z"
}
```

### Example 2: List Tasks (All)

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "completed": null
}
```

**Output**:
```json
{
  "tasks": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-02-08T10:30:00Z",
      "updated_at": "2026-02-08T10:30:00Z"
    }
  ]
}
```

### Example 3: Complete Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Output**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T14:20:00Z"
}
```

---

## Contract Status

✅ All 5 MCP tools have complete input/output schemas
✅ Error schemas defined for all tools
✅ OpenAI function calling format provided
✅ Validation rules documented
✅ Usage examples included

**Next Step**: Create quickstart.md
