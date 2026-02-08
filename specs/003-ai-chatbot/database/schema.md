# Database Schema Specification

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the database schema for Phase III AI chatbot, including new tables for conversations and messages, and relationships with existing Phase II tables (users and tasks).

## Database Technology

- **Database**: Neon PostgreSQL (Serverless)
- **ORM**: SQLModel
- **Connection**: Via `DATABASE_URL` environment variable
- **Migrations**: Version-controlled, reversible migrations

## Schema Overview

Phase III adds two new tables to support conversation persistence:
- `conversations`: Stores chat sessions
- `messages`: Stores individual messages within conversations

Phase II tables remain unchanged:
- `users`: User accounts (existing)
- `tasks`: Todo items (existing)

## Table Definitions

### Table: users (Phase II - Existing)

**Purpose**: Store user account information for authentication.

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`

**Notes**: This table exists from Phase II and is not modified in Phase III.

---

### Table: tasks (Phase II - Existing)

**Purpose**: Store todo items for users.

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique task identifier |
| user_id | UUID | FOREIGN KEY → users.id, NOT NULL | Owner of the task |
| title | VARCHAR(100) | NOT NULL | Task title |
| description | VARCHAR(500) | NULL | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for user-scoped queries)
- INDEX on `user_id, completed` (for filtered queries)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Notes**: This table exists from Phase II and is not modified in Phase III. All task operations go through MCP tools.

---

### Table: conversations (Phase III - New)

**Purpose**: Store chat sessions between users and the AI chatbot.

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique conversation identifier |
| user_id | UUID | FOREIGN KEY → users.id, NOT NULL | Owner of the conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation start timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for user-scoped queries)
- INDEX on `user_id, updated_at DESC` (for recent conversations)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Constraints**:
- `user_id` must exist in `users` table
- `updated_at` must be >= `created_at`

**Usage**:
- Created when user starts new chat (no conversation_id provided)
- Loaded when user continues existing chat (conversation_id provided)
- Updated timestamp when new message added

---

### Table: messages (Phase III - New)

**Purpose**: Store individual messages within conversations.

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique message identifier |
| user_id | UUID | FOREIGN KEY → users.id, NOT NULL | Owner of the conversation |
| conversation_id | UUID | FOREIGN KEY → conversations.id, NOT NULL | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender role |
| content | TEXT | NOT NULL | Message content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id, created_at ASC` (for chronological message retrieval)
- INDEX on `user_id` (for user-scoped queries)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- `conversation_id` REFERENCES `conversations(id)` ON DELETE CASCADE

**Constraints**:
- `role` must be either 'user' or 'assistant'
- `content` must not be empty (length > 0)
- `user_id` must match conversation's user_id

**Usage**:
- User message stored before agent processing
- Assistant message stored after agent generates response
- Messages loaded in chronological order for conversation context

---

## Relationships

```
users (1) ──< (many) tasks
users (1) ──< (many) conversations
users (1) ──< (many) messages
conversations (1) ──< (many) messages
```

**Cascade Behavior**:
- Delete user → Delete all user's tasks, conversations, and messages
- Delete conversation → Delete all conversation's messages
- Delete task → No cascade (independent of conversations)

## Data Integrity

### User Isolation

All queries MUST filter by `user_id`:
- Tasks: `WHERE user_id = {authenticated_user_id}`
- Conversations: `WHERE user_id = {authenticated_user_id}`
- Messages: `WHERE user_id = {authenticated_user_id}`

### Referential Integrity

- All foreign keys enforced at database level
- Cascade deletes configured for cleanup
- No orphaned records allowed

### Data Validation

**At Database Level**:
- NOT NULL constraints on required fields
- CHECK constraints on enum fields (role)
- UNIQUE constraints on email
- Foreign key constraints

**At Application Level** (SQLModel):
- String length validation (title, description, email)
- UUID format validation
- Timestamp validation
- Content validation (non-empty)

## Migration Strategy

### Phase III Migration

**Migration File**: `003_add_conversations_and_messages.sql`

**Up Migration**:
```sql
-- Create conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for conversations
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Create messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (LENGTH(content) > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for messages
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
CREATE INDEX idx_messages_user_id ON messages(user_id);

-- Add constraint to ensure message user_id matches conversation user_id
-- (This would be enforced at application level for simplicity)
```

**Down Migration**:
```sql
-- Drop tables in reverse order (messages first due to foreign key)
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
```

### Migration Execution

1. Backup database before migration
2. Run migration in transaction
3. Verify schema changes
4. Test with sample data
5. Rollback if issues detected

## Performance Considerations

### Query Optimization

**Common Queries**:
1. Get user's conversations: `SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC`
2. Get conversation messages: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC`
3. Get user's tasks: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`

**Index Usage**:
- All queries use indexed columns (user_id, conversation_id)
- Sorting uses indexed columns (updated_at, created_at)
- No full table scans expected

### Connection Pooling

- Use connection pool for concurrent requests
- Pool size: 10-20 connections (configurable)
- Connection timeout: 30 seconds
- Idle timeout: 10 minutes

### Data Growth

**Estimated Growth**:
- 1000 users × 10 conversations each = 10,000 conversations
- 10,000 conversations × 50 messages each = 500,000 messages
- 1000 users × 20 tasks each = 20,000 tasks

**Storage Estimates**:
- Messages: ~500KB per 1000 messages (text content)
- Conversations: ~100 bytes per conversation
- Total for 1000 users: ~250MB (messages) + 1MB (conversations) = ~251MB

**Archival Strategy** (Future):
- Archive conversations older than 90 days
- Keep last 10 conversations per user active
- Compress archived data

## Security Considerations

### Data Protection

- Passwords stored as bcrypt hashes (Phase II)
- No sensitive data in messages (user responsibility)
- User isolation enforced at query level
- No cross-user data access

### Audit Trail

- All tables include timestamps (created_at, updated_at)
- Message history provides audit trail of user interactions
- Tool invocations logged separately (application level)

### Compliance

- GDPR: User can request data deletion (CASCADE DELETE)
- Data retention: Configurable per deployment
- Privacy: Messages contain user-generated content only

## Testing Requirements

### Schema Tests

- Verify all tables created successfully
- Verify all indexes created
- Verify foreign key constraints work
- Verify cascade deletes work correctly

### Data Integrity Tests

- Test user isolation (users cannot access other users' data)
- Test referential integrity (orphaned records prevented)
- Test constraint validation (invalid data rejected)

### Performance Tests

- Test query performance with 10,000+ records
- Test concurrent access (100+ simultaneous queries)
- Test connection pool behavior under load

## Acceptance Criteria

- **AC-035**: All Phase III tables (conversations, messages) created successfully
- **AC-036**: All indexes created and used by queries
- **AC-037**: Foreign key constraints enforce referential integrity
- **AC-038**: Cascade deletes work correctly (delete user → delete conversations → delete messages)
- **AC-039**: User isolation enforced at database level (queries filter by user_id)
- **AC-040**: Migration is reversible (down migration works)
- **AC-041**: Schema supports 1000+ users with 10+ conversations each
- **AC-042**: Queries complete in <100ms for 95% of requests
