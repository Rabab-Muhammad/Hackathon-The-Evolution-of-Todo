"""
Phase III Migration: Add conversations and messages tables.
Reference: @specs/003-ai-chatbot/database/schema.md

This migration adds support for AI-powered chatbot conversations:
- conversations table: Stores conversation sessions
- messages table: Stores individual messages in conversations

Both tables enforce user isolation via user_id foreign keys.
"""

def upgrade(connection):
    """
    Create conversations and messages tables for Phase III.
    """
    # Create conversations table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """)

    # Create indexes for conversations
    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversations_user_id
        ON conversations(user_id);
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversations_updated_at
        ON conversations(updated_at DESC);
    """)

    # Create messages table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL CHECK (LENGTH(content) <= 2000),
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """)

    # Create indexes for messages
    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_user_id
        ON messages(user_id);
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
        ON messages(conversation_id);
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_created_at
        ON messages(created_at);
    """)

    print("✅ Phase III migration complete: conversations and messages tables created")


def downgrade(connection):
    """
    Drop conversations and messages tables (rollback Phase III).
    """
    # Drop tables in reverse order (messages first due to foreign key)
    connection.execute("DROP TABLE IF EXISTS messages CASCADE;")
    connection.execute("DROP TABLE IF EXISTS conversations CASCADE;")

    print("✅ Phase III migration rolled back: conversations and messages tables dropped")
