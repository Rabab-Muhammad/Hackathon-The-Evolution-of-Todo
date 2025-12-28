# Database Specification: Schema Definition

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the database schema for storing users and tasks in a PostgreSQL database, ensuring data integrity, user isolation, and support for all application features.

## Database Overview

- **Type**: Relational (PostgreSQL)
- **Provider**: Neon Serverless PostgreSQL
- **Connection**: Via `DATABASE_URL` environment variable
- **ORM**: SQLModel

## Entity Relationship Diagram

```
┌─────────────────────────────────────────┐
│                 users                    │
├─────────────────────────────────────────┤
│ id          UUID          PK            │
│ email       VARCHAR(255)  UNIQUE, NOT NULL│
│ password_hash VARCHAR(255) NOT NULL      │
│ created_at  TIMESTAMP     NOT NULL       │
└────────────────────┬────────────────────┘
                     │
                     │ 1:N
                     │
                     ▼
┌─────────────────────────────────────────┐
│                 tasks                    │
├─────────────────────────────────────────┤
│ id          UUID          PK            │
│ user_id     UUID          FK → users.id │
│ title       VARCHAR(100)  NOT NULL       │
│ description VARCHAR(500)  NULL           │
│ completed   BOOLEAN       DEFAULT FALSE  │
│ created_at  TIMESTAMP     NOT NULL       │
│ updated_at  TIMESTAMP     NOT NULL       │
└─────────────────────────────────────────┘
```

## Table Definitions

### Users Table

Stores user account information for authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Account creation timestamp |

**Indexes**:
- Primary Key on `id`
- Unique index on `email`

---

### Tasks Table

Stores todo items owned by users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique task identifier |
| user_id | UUID | FOREIGN KEY → users.id, NOT NULL | Owner of the task |
| title | VARCHAR(100) | NOT NULL | Task title |
| description | VARCHAR(500) | NULL | Optional task details |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | Last modification timestamp |

**Indexes**:
- Primary Key on `id`
- Foreign Key index on `user_id`
- Index on `user_id, created_at` (for efficient user task listing)

**Foreign Key Behavior**:
- ON DELETE CASCADE: When a user is deleted, all their tasks are deleted

---

## Data Integrity Rules

### Users Table

- **DI-U001**: Email MUST be unique across all users
- **DI-U002**: Email MUST be a valid format (enforced at application level)
- **DI-U003**: Password hash MUST be generated using bcrypt
- **DI-U004**: Created_at MUST be set automatically on insert

### Tasks Table

- **DI-T001**: Task MUST belong to an existing user
- **DI-T002**: Title MUST NOT be empty
- **DI-T003**: Title MUST NOT exceed 100 characters
- **DI-T004**: Description MUST NOT exceed 500 characters if provided
- **DI-T005**: Created_at MUST be set automatically on insert
- **DI-T006**: Updated_at MUST be updated on every modification

## Data Flow / Interaction

### User Registration

```
1. Application receives email and password
2. Application validates email format and uniqueness
3. Application hashes password with bcrypt
4. INSERT INTO users (email, password_hash) VALUES (...)
5. Database generates UUID and sets created_at
6. Application receives generated user record
```

### User Authentication

```
1. Application receives email and password
2. SELECT * FROM users WHERE email = :email
3. Application verifies password against stored hash
4. If valid, application issues JWT with user.id as subject
```

### Task Creation

```
1. Application receives task data and user_id from JWT
2. Application validates title and description
3. INSERT INTO tasks (user_id, title, description) VALUES (...)
4. Database generates UUID and sets timestamps
5. Application receives generated task record
```

### Task Retrieval (User's Tasks)

```
1. Application extracts user_id from JWT
2. SELECT * FROM tasks WHERE user_id = :user_id ORDER BY created_at DESC
3. Application returns task list to client
```

### Task Update

```
1. Application extracts user_id from JWT
2. Application validates task ownership:
   SELECT id FROM tasks WHERE id = :task_id AND user_id = :user_id
3. If found, UPDATE tasks SET title = ..., updated_at = now() WHERE id = :task_id
4. Application returns updated task
```

### Task Deletion

```
1. Application extracts user_id from JWT
2. Application validates task ownership:
   SELECT id FROM tasks WHERE id = :task_id AND user_id = :user_id
3. If found, DELETE FROM tasks WHERE id = :task_id
4. Application confirms deletion
```

## Query Patterns

### Common Queries

| Operation | Query Pattern |
|-----------|---------------|
| Get user by email | `WHERE email = :email` |
| Get user's tasks | `WHERE user_id = :user_id ORDER BY created_at DESC` |
| Get single task | `WHERE id = :task_id AND user_id = :user_id` |
| Count user's tasks | `SELECT COUNT(*) WHERE user_id = :user_id` |

### Index Optimization

| Query Pattern | Index Used |
|---------------|------------|
| Login (email lookup) | `idx_users_email` |
| List user tasks | `idx_tasks_user_created` |
| Get/Update/Delete task | Primary key on `id` |

## Migration Strategy

### Initial Migration (Phase II Setup)

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Create tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Create indexes
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

## Validation Rules

| Entity | Field | Rule | Error |
|--------|-------|------|-------|
| User | email | Required, unique | "Email already exists" |
| User | email | Valid format | "Invalid email format" |
| User | password | Min 8 chars | "Password too short" |
| Task | title | Required | "Title is required" |
| Task | title | Max 100 chars | "Title too long" |
| Task | description | Max 500 chars | "Description too long" |
| Task | user_id | Must exist | "User not found" |

## Acceptance Criteria

- [ ] Users table stores email and hashed password
- [ ] Tasks table references users via foreign key
- [ ] UUID primary keys are auto-generated
- [ ] Timestamps are automatically managed
- [ ] Deleting a user cascades to delete their tasks
- [ ] Email uniqueness is enforced at database level
- [ ] Indexes support efficient queries for common operations

## Success Criteria

### Measurable Outcomes

- **SC-001**: User lookup by email completes in < 10ms
- **SC-002**: Task list query for a user completes in < 50ms (up to 100 tasks)
- **SC-003**: Data integrity constraints prevent orphaned tasks
- **SC-004**: 100% of password storage uses proper hashing
- **SC-005**: Schema supports 100,000+ users and 1,000,000+ tasks
