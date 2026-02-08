# Research & Technology Decisions: Phase III AI Chatbot

**Feature**: Phase III AI-Powered Todo Chatbot
**Date**: 2026-02-08
**Status**: Complete

## Purpose

Document technology research, decisions, and best practices for Phase III implementation. This research resolves all technical uncertainties and provides implementation guidance for the development team.

## Research Areas

### 1. OpenAI Agents SDK Integration

**Research Question**: How to integrate OpenAI Agents SDK with FastAPI for stateless agent orchestration?

**Decision**: Use OpenAI Agents SDK with custom tool registration and stateless context management

**Rationale**:
- OpenAI Agents SDK provides robust intent interpretation and tool orchestration
- Compatible with OpenRouter via OpenAI-compatible API interface
- Supports custom tool registration (MCP tools)
- Allows stateless operation by reconstructing context from database

**Implementation Pattern**:
```python
# Agent initialization (stateless)
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Agent orchestration
def process_message(user_id: str, message: str, conversation_history: List[Message]):
    # Reconstruct context from conversation_history
    messages = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
    messages.append({"role": "user", "content": message})

    # Call agent with tools
    response = client.chat.completions.create(
        model="anthropic/claude-3-sonnet",
        messages=messages,
        tools=get_mcp_tools(),  # MCP tools as OpenAI function calling format
        tool_choice="auto"
    )

    # Process tool calls and generate response
    return handle_response(response, user_id)
```

**Best Practices**:
- Initialize agent client once at startup (singleton pattern)
- Reconstruct conversation context from database on each request
- Register MCP tools as OpenAI function calling tools
- Handle tool calls sequentially or in parallel based on dependencies
- Implement retry logic for API failures
- Set reasonable timeouts (30s for agent processing)

**Alternatives Considered**:
- LangChain: More complex, heavier dependencies, overkill for our use case
- Custom agent implementation: Reinventing the wheel, more maintenance burden
- Direct OpenAI API: Requires OpenAI API key, less provider flexibility

---

### 2. Official MCP SDK Usage

**Research Question**: How to implement MCP tools using the Official MCP SDK for Python?

**Decision**: Use Official MCP SDK with SQLModel for database operations

**Rationale**:
- Official MCP SDK provides standardized tool interface
- Compatible with OpenAI Agents SDK via function calling format
- Supports input validation and error handling
- Enables future tool extensions without agent changes

**Implementation Pattern**:
```python
# MCP tool definition
from mcp import Tool, ToolInput, ToolOutput
from pydantic import BaseModel

class AddTaskInput(BaseModel):
    user_id: str
    title: str
    description: str | None = None

@Tool(
    name="add_task",
    description="Create a new task for the user",
    input_schema=AddTaskInput
)
def add_task(input: AddTaskInput) -> ToolOutput:
    # Validate user exists
    user = db.query(User).filter(User.id == input.user_id).first()
    if not user:
        return ToolOutput(error="User not found")

    # Create task
    task = Task(
        user_id=input.user_id,
        title=input.title,
        description=input.description,
        completed=False
    )
    db.add(task)
    db.commit()

    return ToolOutput(result=task.dict())
```

**Best Practices**:
- Use Pydantic models for input validation
- Enforce user_id scoping in all tools
- Return structured ToolOutput with result or error
- Log all tool invocations for debugging
- Use database transactions for atomic operations
- Implement idempotent operations where possible (e.g., complete_task)

**Alternatives Considered**:
- Custom tool interface: Less standardized, more maintenance
- Direct function calls: No validation, harder to extend
- LangChain tools: Tied to LangChain ecosystem

---

### 3. OpenRouter Integration

**Research Question**: How to integrate OpenRouter for AI inference with OpenAI SDK compatibility?

**Decision**: Use OpenRouter with OpenAI SDK by configuring base_url

**Rationale**:
- OpenRouter provides OpenAI-compatible API interface
- Supports multiple models (Claude, GPT-4, etc.)
- Provider-agnostic (can switch models without code changes)
- Cost-effective compared to direct OpenAI API

**Implementation Pattern**:
```python
# OpenRouter configuration
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://yourdomain.com",  # Optional
        "X-Title": "Evolution of Todo"  # Optional
    }
)

# Model selection
MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-sonnet")

# Usage
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    temperature=0.7,
    max_tokens=1000
)
```

**Best Practices**:
- Store API key in environment variable (OPENROUTER_API_KEY)
- Configure model via environment variable for flexibility
- Implement retry logic with exponential backoff
- Handle rate limiting (429 errors)
- Set reasonable timeouts (30s)
- Log API usage for monitoring and cost tracking

**Model Recommendations**:
- Primary: `anthropic/claude-3-sonnet` (good balance of quality and cost)
- Alternative: `openai/gpt-4-turbo` (higher quality, higher cost)
- Fallback: `anthropic/claude-3-haiku` (faster, lower cost)

**Alternatives Considered**:
- Direct OpenAI API: Less flexible, higher cost, vendor lock-in
- Self-hosted models: Complex infrastructure, maintenance burden
- Other AI providers: Less standardized APIs, more integration work

---

### 4. ChatKit Frontend Integration

**Research Question**: How to integrate OpenAI ChatKit with custom backend endpoint and OpenRouter?

**Decision**: Use OpenAI ChatKit with custom API client for backend communication

**Rationale**:
- ChatKit provides polished chat UI out of the box
- Supports custom backend endpoints
- Handles message rendering, input, and conversation state
- Responsive design for mobile and desktop

**Implementation Pattern**:
```typescript
// Custom API client for backend
const chatApi = {
  sendMessage: async (userId: string, message: string, conversationId?: string) => {
    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        message: message
      })
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  }
};

// ChatKit integration
import { ChatInterface } from '@openai/chatkit';

function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const handleSendMessage = async (message: string) => {
    // Add user message optimistically
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    // Send to backend
    const response = await chatApi.sendMessage(userId, message, conversationId);

    // Update conversation ID and add assistant response
    setConversationId(response.conversation_id);
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response.response
    }]);
  };

  return <ChatInterface messages={messages} onSendMessage={handleSendMessage} />;
}
```

**Best Practices**:
- Use optimistic updates for better UX
- Store conversation_id in component state
- Implement error handling with retry options
- Show loading states during message processing
- Auto-scroll to bottom on new messages
- Support keyboard shortcuts (Enter to send)

**Alternatives Considered**:
- Custom chat UI: More work, less polished
- Other chat libraries: Less integration with OpenAI ecosystem
- Traditional form-based UI: Not conversational, poor UX

---

### 5. Conversation Persistence Strategy

**Research Question**: How to efficiently persist and load conversation history for stateless backend?

**Decision**: Store all messages in database with indexed queries and context window limiting

**Rationale**:
- Database persistence ensures no data loss on server restarts
- Indexed queries enable fast conversation history retrieval
- Context window limiting (last 50 messages) prevents performance degradation
- Supports conversation resumption across sessions

**Implementation Pattern**:
```python
# Load conversation history with limit
def load_conversation_context(conversation_id: str, limit: int = 50) -> List[Message]:
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()

    # Reverse to chronological order
    return list(reversed(messages))

# Store new messages
def store_message(conversation_id: str, user_id: str, role: str, content: str) -> Message:
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# Update conversation timestamp
def update_conversation_timestamp(conversation_id: str):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        db.commit()
```

**Database Indexes**:
```sql
-- For fast conversation history retrieval
CREATE INDEX idx_messages_conversation_created
ON messages(conversation_id, created_at ASC);

-- For user-scoped queries
CREATE INDEX idx_messages_user_id ON messages(user_id);

-- For recent conversations
CREATE INDEX idx_conversations_user_updated
ON conversations(user_id, updated_at DESC);
```

**Best Practices**:
- Limit context to last 50 messages (configurable)
- Use database indexes for fast queries
- Store messages immediately after generation
- Update conversation timestamp on each message
- Implement pagination for conversation list
- Archive old conversations (future enhancement)

**Performance Considerations**:
- Query time: <100ms for 50 messages (with indexes)
- Storage: ~500 bytes per message (text content)
- Scalability: Supports 10K+ conversations per user

**Alternatives Considered**:
- In-memory cache: Loses data on restart, not stateless
- Redis: Additional infrastructure, complexity
- File storage: Slower, harder to query

---

### 6. Stateless Backend Design

**Research Question**: How to design stateless backend that reconstructs context from database on each request?

**Decision**: Stateless request cycle with context reconstruction from database

**Rationale**:
- Enables horizontal scaling (any instance handles any request)
- No session affinity required (load balancer flexibility)
- Resilient to server restarts (no data loss)
- Kubernetes-ready for Phase IV deployment

**Implementation Pattern**:
```python
# Stateless chat endpoint
@router.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate user_id matches JWT
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Load or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation)\
            .filter(Conversation.id == request.conversation_id)\
            .filter(Conversation.user_id == user_id)\
            .first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Load conversation history (context reconstruction)
    history = load_conversation_context(conversation.id, limit=50)

    # Store user message
    user_message = store_message(conversation.id, user_id, "user", request.message)

    # Process with agent (stateless)
    agent_response = process_message(user_id, request.message, history)

    # Store assistant message
    assistant_message = store_message(
        conversation.id,
        user_id,
        "assistant",
        agent_response.content
    )

    # Update conversation timestamp
    update_conversation_timestamp(conversation.id)

    # Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=agent_response.content,
        tool_calls=agent_response.tool_calls
    )
```

**Best Practices**:
- No global state or class-level variables
- Reconstruct all context from database on each request
- Use dependency injection for database sessions
- Close database connections after each request
- Implement connection pooling for performance
- Use async/await for non-blocking I/O

**Scalability Benefits**:
- Horizontal scaling: Add more instances without coordination
- Load balancing: Round-robin or least-connections
- Fault tolerance: Instance failure doesn't affect other requests
- Rolling updates: Zero-downtime deployments

**Alternatives Considered**:
- Stateful sessions: Requires sticky sessions, harder to scale
- In-memory state: Loses data on restart, not resilient
- Distributed cache: Additional complexity, infrastructure

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| Backend Framework | FastAPI | 0.104+ | Async support, OpenAPI, dependency injection |
| Agent SDK | OpenAI Agents SDK | Latest | Intent interpretation, tool orchestration |
| MCP SDK | Official MCP SDK | Latest | Standardized tool interface |
| AI Provider | OpenRouter | API v1 | Provider-agnostic, cost-effective |
| ORM | SQLModel | 0.0.14+ | Type safety, Pydantic integration |
| Database | Neon PostgreSQL | Latest | Serverless, auto-scaling |
| Frontend Framework | Next.js | 16+ | App Router, SSR, TypeScript |
| Chat UI | OpenAI ChatKit | Latest | Polished chat interface |
| Styling | Tailwind CSS | 3.0+ | Utility-first, responsive |
| Testing (Backend) | pytest | 7.0+ | Async support, fixtures |
| Testing (Frontend) | Jest + RTL | Latest | React component testing |

## Environment Variables

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| OPENROUTER_API_KEY | Yes | OpenRouter API authentication | sk-or-v1-... |
| OPENROUTER_MODEL | No | AI model selection | anthropic/claude-3-sonnet |
| DATABASE_URL | Yes | PostgreSQL connection | postgresql://... |
| BETTER_AUTH_SECRET | Yes | JWT signing secret | 32+ character string |
| NEXT_PUBLIC_API_URL | Yes | Backend API URL | http://localhost:8000 |

## Implementation Recommendations

### Development Workflow

1. **Database First**: Create models and migrations before implementing logic
2. **MCP Tools Second**: Implement and test tools independently
3. **Agent Third**: Integrate agent with tested tools
4. **API Fourth**: Expose agent via chat endpoint
5. **Frontend Last**: Build UI on top of working API

### Testing Strategy

1. **Unit Tests**: Test each MCP tool independently
2. **Integration Tests**: Test agent with tools
3. **API Tests**: Test chat endpoint with mocked agent
4. **E2E Tests**: Test full conversation flows
5. **Performance Tests**: Verify response time targets

### Deployment Considerations

1. **Database Migrations**: Run migrations before deploying new code
2. **Environment Variables**: Verify all required variables are set
3. **Health Checks**: Implement /health endpoint for monitoring
4. **Logging**: Log all requests, errors, and tool invocations
5. **Monitoring**: Track response times, error rates, API usage

## Conclusion

All technology decisions are documented and justified. Implementation can proceed with confidence based on these research findings. The chosen technologies support the Phase III requirements for stateless architecture, conversation persistence, and AI-powered task management.

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Design & Contracts
