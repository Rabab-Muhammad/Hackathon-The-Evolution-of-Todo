# Data Model: Phase II Full-Stack Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-28 | **Spec**: [database/schema.md](./database/schema.md)

## Overview

This document defines the data models for both backend (SQLModel) and frontend (TypeScript) layers, derived from the database schema specification.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────┐
│                  User                    │
├─────────────────────────────────────────┤
│ id: UUID (PK)                           │
│ email: string (unique)                  │
│ password_hash: string                   │
│ created_at: datetime                    │
└────────────────────┬────────────────────┘
                     │
                     │ 1:N (one user has many tasks)
                     │
                     ▼
┌─────────────────────────────────────────┐
│                  Task                    │
├─────────────────────────────────────────┤
│ id: UUID (PK)                           │
│ user_id: UUID (FK → User.id)            │
│ title: string (max 100)                 │
│ description: string? (max 500)          │
│ completed: boolean (default: false)     │
│ created_at: datetime                    │
│ updated_at: datetime                    │
└─────────────────────────────────────────┘
```

## Backend Models (SQLModel)

### User Entity

**Purpose**: Represents an authenticated application user

**Table Name**: `users`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique user identifier |
| email | str | unique, max 255, not null | User's email address |
| password_hash | str | max 255, not null | Bcrypt-hashed password |
| created_at | datetime | not null, auto | Account creation timestamp |

**Indexes**:
- Primary key on `id`
- Unique index on `email`

**Validation Rules** (from @specs/features/authentication.md):
- Email must be valid format
- Email must be unique
- Password minimum 8 characters (validated before hashing)

**Relationships**:
- Has many Tasks (one-to-many)

---

### Task Entity

**Purpose**: Represents a todo item owned by a user

**Table Name**: `tasks`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique task identifier |
| user_id | UUID | FK → users.id, not null | Owner reference |
| title | str | max 100, not null | Task title |
| description | str | max 500, nullable | Optional details |
| completed | bool | not null, default false | Completion status |
| created_at | datetime | not null, auto | Creation timestamp |
| updated_at | datetime | not null, auto-update | Last modification |

**Indexes**:
- Primary key on `id`
- Foreign key index on `user_id`
- Composite index on `(user_id, created_at DESC)` for efficient listing

**Foreign Key Behavior**:
- ON DELETE CASCADE: Deleting user removes all their tasks

**Validation Rules** (from @specs/features/task-crud.md):
- Title: required, non-empty, max 100 characters
- Description: optional, max 500 characters
- User ownership required for all operations

**Relationships**:
- Belongs to User (many-to-one)

---

## Frontend Types (TypeScript)

### User Type

```typescript
interface User {
  id: string;       // UUID
  email: string;
  created_at: string; // ISO 8601 datetime
}

interface AuthResponse {
  user: User;
  token: string;    // JWT token
}
```

### Task Type

```typescript
interface Task {
  id: string;           // UUID
  title: string;        // max 100 chars
  description?: string; // max 500 chars, optional
  completed: boolean;
  created_at: string;   // ISO 8601 datetime
  updated_at: string;   // ISO 8601 datetime
}

interface TaskCreateRequest {
  title: string;
  description?: string;
}

interface TaskUpdateRequest {
  title: string;
  description?: string;
}

interface TaskListResponse {
  tasks: Task[];
  count: number;
}

interface TaskResponse {
  task: Task;
}
```

### Auth Types

```typescript
interface SignupRequest {
  email: string;
  password: string;
}

interface SigninRequest {
  email: string;
  password: string;
}

interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Array<{
      field: string;
      message: string;
    }>;
  };
}
```

---

## Data Flow Mappings

### Registration Flow

| Step | Input | Output | Transformation |
|------|-------|--------|----------------|
| Frontend | SignupRequest | - | Collect email, password |
| Backend | email, password | password_hash | Hash password with bcrypt |
| Database | User model | id, created_at | Generate UUID, timestamp |
| Backend | User record | AuthResponse | Generate JWT, exclude password_hash |
| Frontend | AuthResponse | - | Store token, redirect |

### Task Creation Flow

| Step | Input | Output | Transformation |
|------|-------|--------|----------------|
| Frontend | TaskCreateRequest | - | Collect title, description |
| Backend | JWT + TaskCreateRequest | user_id | Extract from token |
| Database | Task model | id, timestamps | Generate UUID, set timestamps |
| Backend | Task record | TaskResponse | Return created task |
| Frontend | TaskResponse | - | Add to task list |

---

## State Transitions

### Task State Machine

```
                    ┌─────────────┐
     Create ──────► │  Incomplete │ ◄────── Toggle
                    │ (completed: │
                    │   false)    │
                    └──────┬──────┘
                           │
                      Toggle│
                           │
                           ▼
                    ┌─────────────┐
                    │  Complete   │
                    │ (completed: │
                    │   true)     │
                    └─────────────┘
                           │
                      Delete│
                           │
                           ▼
                    ┌─────────────┐
                    │   Deleted   │
                    │ (removed)   │
                    └─────────────┘
```

### User Session State Machine

```
                    ┌─────────────┐
     Visit ───────► │  Anonymous  │
                    └──────┬──────┘
                           │
            Login/Signup   │
                           │
                           ▼
                    ┌─────────────┐
                    │Authenticated│ ◄────── Token Valid
                    │ (has JWT)   │
                    └──────┬──────┘
                           │
            Logout/        │
            Token Expired  │
                           │
                           ▼
                    ┌─────────────┐
                    │  Logged Out │
                    └─────────────┘
```

---

## Query Patterns

### User Queries

| Operation | Pattern | Index Used |
|-----------|---------|------------|
| Find by email | `WHERE email = ?` | idx_users_email |
| Find by ID | `WHERE id = ?` | Primary key |

### Task Queries

| Operation | Pattern | Index Used |
|-----------|---------|------------|
| List user tasks | `WHERE user_id = ? ORDER BY created_at DESC` | idx_tasks_user_created |
| Get single task | `WHERE id = ? AND user_id = ?` | Primary key |
| Count user tasks | `SELECT COUNT(*) WHERE user_id = ?` | idx_tasks_user_created |

---

## Validation Summary

### Backend Validation (SQLModel/Pydantic)

| Entity | Field | Rule | Error Code |
|--------|-------|------|------------|
| User | email | Valid format | VALIDATION_ERROR |
| User | email | Unique | CONFLICT |
| User | password | Min 8 chars | VALIDATION_ERROR |
| Task | title | Non-empty | VALIDATION_ERROR |
| Task | title | Max 100 chars | VALIDATION_ERROR |
| Task | description | Max 500 chars | VALIDATION_ERROR |
| Task | user_id | Must exist | NOT_FOUND |

### Frontend Validation (Pre-submit)

| Field | Rule | Display |
|-------|------|---------|
| email | Required | "Email is required" |
| email | Valid format | "Please enter a valid email address" |
| password | Required | "Password is required" |
| password | Min 8 chars | "Password must be at least 8 characters" |
| title | Required | "Task title is required" |
| title | Max 100 chars | "Task title must be 100 characters or less" |
| description | Max 500 chars | "Task description must be 500 characters or less" |

---

## Database Migration

### Initial Schema (Version 1)

**Migration Name**: `001_initial_schema`

**Creates**:
1. Enable `uuid-ossp` extension
2. `users` table with email unique constraint
3. `tasks` table with foreign key to users
4. Required indexes for query optimization

**Down Migration**:
1. Drop `tasks` table
2. Drop `users` table
3. Disable `uuid-ossp` extension

---

## Acceptance Criteria

- [ ] User model stores email and hashed password (never plaintext)
- [ ] Task model references user via foreign key
- [ ] UUID primary keys are auto-generated
- [ ] Timestamps are automatically managed
- [ ] Cascade delete removes tasks when user is deleted
- [ ] Email uniqueness enforced at database level
- [ ] Indexes optimize common query patterns
- [ ] TypeScript types match API response shapes
- [ ] Validation rules enforced at both frontend and backend
