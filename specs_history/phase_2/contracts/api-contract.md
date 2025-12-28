# API Contract: Frontend-Backend Interface

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-28
**Source**: [@specs/api/rest-endpoints.md](../api/rest-endpoints.md)

## Overview

This contract defines the HTTP interface between the Next.js frontend and FastAPI backend. All implementations MUST conform to this contract.

## Base Configuration

- **Base URL**: `{NEXT_PUBLIC_API_URL}/api`
- **Content-Type**: `application/json`
- **Authorization**: `Bearer <jwt-token>` for protected endpoints

---

## Authentication Endpoints

### POST /api/auth/signup

**Purpose**: Register a new user account

**Authentication**: None required

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Validation**:
- `email`: Required, valid email format
- `password`: Required, minimum 8 characters

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2025-12-28T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:
- 409 Conflict: `{"error": {"code": "CONFLICT", "message": "An account with this email already exists"}}`
- 422 Unprocessable Entity: `{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}}`

---

### POST /api/auth/signin

**Purpose**: Authenticate existing user

**Authentication**: None required

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Validation**:
- `email`: Required
- `password`: Required

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:
- 401 Unauthorized: `{"error": {"code": "UNAUTHORIZED", "message": "Invalid credentials"}}`
- 422 Unprocessable Entity: `{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}}`

---

### POST /api/auth/signout

**Purpose**: End user session

**Authentication**: Required

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
- 401 Unauthorized: `{"error": {"code": "UNAUTHORIZED", "message": "Authentication required"}}`

---

## Task Endpoints

### GET /api/tasks

**Purpose**: List all tasks for authenticated user

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
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
- 401 Unauthorized: `{"error": {"code": "UNAUTHORIZED", "message": "Authentication required"}}`

---

### POST /api/tasks

**Purpose**: Create a new task

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation**:
- `title`: Required, non-empty, max 100 characters
- `description`: Optional, max 500 characters

**Success Response** (201 Created):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T10:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized
- 422 Unprocessable Entity

---

### GET /api/tasks/{task_id}

**Purpose**: Retrieve a single task by ID

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id`: UUID of the task

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T10:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized
- 404 Not Found: `{"error": {"code": "NOT_FOUND", "message": "Task not found"}}`

---

### PUT /api/tasks/{task_id}

**Purpose**: Update an existing task

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id`: UUID of the task

**Request**:
```json
{
  "title": "Buy groceries today",
  "description": "Milk, eggs, bread, cheese"
}
```

**Validation**:
- `title`: Required, non-empty, max 100 characters
- `description`: Optional, max 500 characters

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries today",
    "description": "Milk, eggs, bread, cheese",
    "completed": false,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T11:00:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized
- 404 Not Found
- 422 Unprocessable Entity

---

### DELETE /api/tasks/{task_id}

**Purpose**: Delete a task

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id`: UUID of the task

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401 Unauthorized
- 404 Not Found

---

### PATCH /api/tasks/{task_id}/toggle

**Purpose**: Toggle task completion status

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `task_id`: UUID of the task

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-28T11:30:00Z"
  }
}
```

**Error Responses**:
- 401 Unauthorized
- 404 Not Found

---

## Error Response Format

All error responses follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
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
| VALIDATION_ERROR | 422 | Request body validation failed |
| UNAUTHORIZED | 401 | Missing or invalid authentication |
| NOT_FOUND | 404 | Resource not found or not owned by user |
| CONFLICT | 409 | Resource already exists (e.g., duplicate email) |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## JWT Token Format

### Claims

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1703764800,
  "exp": 1703851200
}
```

| Claim | Type | Description |
|-------|------|-------------|
| sub | string (UUID) | User's unique identifier |
| email | string | User's email address |
| iat | number | Issued at (Unix timestamp) |
| exp | number | Expiration (Unix timestamp) |

### Token Validation

Backend MUST:
1. Extract token from `Authorization: Bearer <token>` header
2. Verify signature using `BETTER_AUTH_SECRET`
3. Check expiration (`exp > current_time`)
4. Extract `sub` claim as `user_id` for data scoping

---

## Rate Limits

| Endpoint Group | Limit | Scope |
|----------------|-------|-------|
| /api/auth/* | 5/minute | Per IP |
| /api/tasks/* | 100/minute | Per user |

---

## Acceptance Criteria

- [ ] All endpoints return correct HTTP status codes
- [ ] All responses are valid JSON
- [ ] Protected endpoints reject requests without valid JWT
- [ ] Task endpoints only access user's own tasks
- [ ] Error responses follow consistent format
- [ ] Validation errors include field-level details
- [ ] UUID format used for all resource IDs
- [ ] Timestamps in ISO 8601 format
