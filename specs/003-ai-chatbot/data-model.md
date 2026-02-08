# Data Model: Phase III AI Chatbot

**Feature**: Phase III AI-Powered Todo Chatbot
**Date**: 2026-02-08
**Status**: Complete

## Purpose

Define the data entities, relationships, and validation rules for Phase III conversation and message persistence. This document extends the Phase II data model (users, tasks) with new entities for chat functionality.

## Entity Definitions

### Existing Entities (Phase II)

#### User
**Purpose**: Store user account information for authentication.

**Attributes**:
- `id`: UUID, primary key, auto-generated
- `email`: String (255), unique, required
- `password_hash`: String (255), required
- `created_at`: Timestamp, required, default now()

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must be hashed with bcrypt before storage

**Relationships**:
- One user has many tasks
- One user has many conversations
- One user has many messages

---

#### Task
**Purpose**: Store todo items for users.

**Attributes**:
- `id`: UUID, primary key, auto-generated
- `user_id`: UUID, foreign key to users.id, required
- `title`: String (100), required
- `description`: String (500), nullable
- `completed`: Boolean, required, default false
- `created_at`: Timestamp, required, default now()
- `updated_at`: Timestamp, required, default now()

**Validation Rules**:
- Title must be 1-100 characters
- Description must be 0-500 characters if provided
- user_id must reference existing user
- completed must be boolean

**Relationships**:
- Many tasks belong to one user
- Tasks are accessed only via MCP tools (no direct agent access)

---

### New Entities (Phase III)

#### Conversation
**Purpose**: Represent a chat session between user and AI chatbot.

**Attributes**:
- `id`: UUID, primary key, auto-generated
- `user_id`: UUID, foreign key to users.id, required
- `created_at`: Timestamp, required, default now()
- `updated_at`: Timestamp, required, default now()

**Validation Rules**:
- user_id must reference existing user
- updated_at must be >= created_at
- Conversation belongs to exactly one user

**Relationships**:
- Many conversations belong to one user
- One conversation has many messages

**Indexes**:
- Primary key on id
- Index on user_id (for user-scoped queries)
- Composite index on (user_id, updated_at DESC) for recent conversations

**Business Rules**:
- Conversations are never deleted (soft delete in future if needed)
- updated_at is updated whenever a new message is added
- Conversations are user-scoped (queries must filter by user_id)

---

#### Message
**Purpose**: Store individual messages within conversations.

**Attributes**:
- `id`: UUID, primary key, auto-generated
- `user_id`: UUID, foreign key to users.id, required
- `conversation_id`: UUID, foreign key to conversations.id, required
- `role`: String (20), required, enum: ['user', 'assistant']
- `content`: Text, required, non-empty
- `created_at`: Timestamp, required, default now()

**Validation Rules**:
- user_id must reference existing user
- conversation_id must reference existing conversation
- user_id must match conversation's user_id
- role must be either 'user' or 'assistant'
- content must not be empty (length > 0)
- content must be <= 10,000 characters

**Relationships**:
- Many messages belong to one user
- Many messages belong to one conversation
- Messages are ordered chronologically within conversation

**Indexes**:
- Primary key on id
- Composite index on (conversation_id, created_at ASC) for chronological retrieval
- Index on user_id (for user-scoped queries)

**Business Rules**:
- Messages are immutable (never updated after creation)
- Messages are never deleted (conversation history is permanent)
- Messages are user-scoped (queries must filter by user_id)
- User messages are stored before agent processing
- Assistant messages are stored after agent generates response

---

### Request/Response DTOs

#### ChatRequest
**Purpose**: Request payload for chat endpoint.

**Attributes**:
- `conversation_id`: UUID, optional
- `message`: String, required

**Validation Rules**:
- message must be 1-2000 characters
- message must not be empty
- conversation_id must be valid UUID format if provided

**Usage**:
- If conversation_id is null/missing, create new conversation
- If conversation_id is provided, load existing conversation

---

#### ChatResponse
**Purpose**: Response payload from chat endpoint.

**Attributes**:
- `conversation_id`: UUID, required
- `response`: String, required
- `tool_calls`: Array of ToolCall, optional

**Validation Rules**:
- conversation_id must be valid UUID
- response must not be empty
- tool_calls array may be empty

**Usage**:
- conversation_id is returned for subsequent requests
- response contains assistant's natural language message
- tool_calls contains details of MCP tool invocations

---

#### ToolCall
**Purpose**: Record of MCP tool invocation.

**Attributes**:
- `tool`: String, required (tool name)
- `input`: Object, required (tool input parameters)
- `output`: Object, required (tool output result)

**Validation Rules**:
- tool must be one of: add_task, list_tasks, update_task, delete_task, complete_task
- input must match tool's input schema
- output must match tool's output schema

**Usage**:
- Included in ChatResponse for transparency
- Used for debugging and auditing
- Displayed in UI (optional, collapsible)

---

## Entity Relationships

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ├─────────────┐
     │             │
     ▼             ▼
┌─────────┐   ┌──────────────┐
│  Task   │   │ Conversation │
└─────────┘   └──────┬───────┘
                     │
                     ▼
              ┌──────────┐
              │ Message  │
              └─────────┘
```

**Relationship Details**:
- User → Task: One-to-Many (user_id foreign key)
- User → Conversation: One-to-Many (user_id foreign key)
- User → Message: One-to-Many (user_id foreign key)
- Conversation → Message: One-to-Many (conversation_id foreign key)

**Cascade Behavior**:
- Delete User → Cascade delete all Tasks, Conversations, Messages
- Delete Conversation → Cascade delete all Messages
- Delete Task → No cascade (independent of conversations)

---

## State Transitions

### Conversation Lifecycle

```
[Created] → [Active] → [Archived (future)]
```

**States**:
1. **Created**: New conversation created, no messages yet
2. **Active**: Conversation has messages, can receive new messages
3. **Archived**: (Future) Conversation older than 90 days, read-only

**Transitions**:
- Created → Active: When first message is added
- Active → Archived: (Future) After 90 days of inactivity

---

### Message Lifecycle

```
[Created] → [Immutable]
```

**States**:
1. **Created**: Message stored in database
2. **Immutable**: Message never changes after creation

**No Transitions**: Messages are immutable and never deleted

---

### Task Lifecycle (Existing from Phase II)

```
[Created] → [Active] → [Completed]
                ↓
            [Deleted]
```

**States**:
1. **Created**: New task created
2. **Active**: Task exists, not completed
3. **Completed**: Task marked as done (completed = true)
4. **Deleted**: Task removed from database

**Transitions**:
- Created → Active: Immediately after creation
- Active → Completed: Via complete_task MCP tool
- Active → Deleted: Via delete_task MCP tool
- Completed → Deleted: Via delete_task MCP tool

---

## Validation Rules Summary

### Field-Level Validation

| Entity | Field | Rule |
|--------|-------|------|
| User | email | Valid email format, unique |
| User | password_hash | Bcrypt hash, 60 characters |
| Task | title | 1-100 characters, required |
| Task | description | 0-500 characters, nullable |
| Conversation | user_id | Must reference existing user |
| Message | role | Must be 'user' or 'assistant' |
| Message | content | 1-10,000 characters, required |
| ChatRequest | message | 1-2000 characters, required |

### Entity-Level Validation

| Entity | Rule |
|--------|------|
| Task | user_id must reference existing user |
| Conversation | user_id must reference existing user |
| Message | user_id must match conversation's user_id |
| Message | conversation_id must reference existing conversation |

### Business Rule Validation

| Rule | Enforcement |
|------|-------------|
| User isolation | All queries filter by user_id |
| Conversation ownership | conversation_id must belong to authenticated user |
| Message immutability | No UPDATE operations on messages table |
| Task access via MCP tools only | Agent cannot query tasks table directly |

---

## Database Schema (SQL)

```sql
-- Existing tables (Phase II)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- New tables (Phase III)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (LENGTH(content) > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

---

## SQLModel Definitions (Python)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

# Existing models (Phase II)
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")
    messages: List["Message"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="tasks")

# New models (Phase III)
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str  # TEXT type
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="messages")
    conversation: Conversation = Relationship(back_populates="messages")
```

---

## Data Access Patterns

### Common Queries

1. **Get user's recent conversations**:
```sql
SELECT * FROM conversations
WHERE user_id = ?
ORDER BY updated_at DESC
LIMIT 10;
```

2. **Get conversation messages (chronological)**:
```sql
SELECT * FROM messages
WHERE conversation_id = ?
ORDER BY created_at ASC;
```

3. **Get conversation context (last 50 messages)**:
```sql
SELECT * FROM messages
WHERE conversation_id = ?
ORDER BY created_at DESC
LIMIT 50;
-- Then reverse in application code
```

4. **Get user's tasks (via MCP tool)**:
```sql
SELECT * FROM tasks
WHERE user_id = ?
ORDER BY created_at DESC;
```

5. **Get incomplete tasks (via MCP tool)**:
```sql
SELECT * FROM tasks
WHERE user_id = ? AND completed = FALSE
ORDER BY created_at DESC;
```

---

## Performance Considerations

### Query Performance

- All queries use indexed columns (user_id, conversation_id, created_at)
- Conversation history limited to last 50 messages
- No full table scans expected
- Query time target: <100ms (P95)

### Storage Estimates

- Message: ~500 bytes average (text content)
- Conversation: ~100 bytes
- Task: ~200 bytes
- Total for 1000 users: ~250MB (messages) + 1MB (conversations) + 4MB (tasks) = ~255MB

### Scalability

- Supports 10,000+ conversations per user
- Supports 500,000+ messages total
- Database indexes ensure consistent performance at scale

---

## Migration Strategy

### Phase III Migration

**Migration File**: `003_add_conversations_and_messages.sql`

**Steps**:
1. Create conversations table
2. Create indexes for conversations
3. Create messages table
4. Create indexes for messages
5. Verify foreign key constraints

**Rollback**:
1. Drop messages table (cascade)
2. Drop conversations table

**Testing**:
1. Verify tables created
2. Verify indexes created
3. Test foreign key constraints
4. Test cascade deletes
5. Test query performance

---

## Conclusion

Data model is complete and ready for implementation. All entities, relationships, validation rules, and indexes are defined. The model supports Phase III requirements for conversation persistence, user isolation, and stateless backend architecture.

**Data Model Status**: ✅ Complete
**Next Step**: Generate API contracts
