# API Specification: REST Endpoints

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the REST API endpoints that enable communication between the frontend application and backend services for task management and user authentication.

## Base URL

All API endpoints are prefixed with `/api/`.

## Authentication

All endpoints except authentication endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints Overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/signup | No | Register new user |
| POST | /api/auth/signin | No | Authenticate user |
| POST | /api/auth/signout | Yes | End user session |
| GET | /api/tasks | Yes | List user's tasks |
| POST | /api/tasks | Yes | Create new task |
| GET | /api/tasks/{task_id} | Yes | Get single task |
| PUT | /api/tasks/{task_id} | Yes | Update task |
| DELETE | /api/tasks/{task_id} | Yes | Delete task |
| PATCH | /api/tasks/{task_id}/toggle | Yes | Toggle task completion |

---

## Authentication Endpoints

### POST /api/auth/signup

Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2025-12-28T10:00:00Z"
  },
  "token": "jwt-token-string"
}
```

**Error Responses**:
- 422 Unprocessable Entity: Validation error (invalid email, weak password)
- 409 Conflict: Email already exists

**Validation Rules**:
- email: Required, valid email format
- password: Required, minimum 8 characters

---

### POST /api/auth/signin

Authenticate existing user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid credentials
- 422 Unprocessable Entity: Validation error

---

### POST /api/auth/signout

End the current user session.

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "message": "Successfully signed out"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token

---

## Task Endpoints

### GET /api/tasks

Retrieve all tasks for the authenticated user.

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-28T10:00:00Z",
      "updated_at": "2025-12-28T10:00:00Z"
    }
  ],
  "count": 1
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token

---

### POST /api/tasks

Create a new task for the authenticated user.

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Success Response** (201 Created):
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T10:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token
- 422 Unprocessable Entity: Validation error

**Validation Rules**:
- title: Required, non-empty, max 100 characters
- description: Optional, max 500 characters

---

### GET /api/tasks/{task_id}

Retrieve a specific task by ID.

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- task_id: UUID of the task

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T10:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Task does not exist or belongs to another user

---

### PUT /api/tasks/{task_id}

Update an existing task.

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- task_id: UUID of the task

**Request Body**:
```json
{
  "title": "Buy groceries today",
  "description": "Milk, eggs, bread, cheese"
}
```

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Buy groceries today",
    "description": "Milk, eggs, bread, cheese",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T11:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Task does not exist or belongs to another user
- 422 Unprocessable Entity: Validation error

---

### DELETE /api/tasks/{task_id}

Delete a task.

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- task_id: UUID of the task

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Task does not exist or belongs to another user

---

### PATCH /api/tasks/{task_id}/toggle

Toggle the completion status of a task.

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- task_id: UUID of the task

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid-string",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T11:30:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Task does not exist or belongs to another user

---

## Error Response Format

All error responses follow a consistent format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 422 | Input validation failed |
| UNAUTHORIZED | 401 | Authentication required or failed |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource conflict (e.g., duplicate email) |
| INTERNAL_ERROR | 500 | Unexpected server error |

## Rate Limiting

- Authentication endpoints: 5 requests per minute per IP
- Task endpoints: 100 requests per minute per user

## Data Flow

### Typical Request Flow

```
1. Client prepares request with data
2. Client adds Authorization header (for protected endpoints)
3. Client sends HTTP request
4. Server validates JWT token (if required)
5. Server validates request body
6. Server processes request
7. Server returns response with appropriate status code
```

## Acceptance Criteria

- [ ] All endpoints return correct HTTP status codes
- [ ] All endpoints accept and return JSON
- [ ] Protected endpoints reject requests without valid JWT
- [ ] Task endpoints only return/modify user's own tasks
- [ ] Error responses follow consistent format
- [ ] Validation errors include field-level details
