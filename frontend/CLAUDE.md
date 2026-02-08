# Frontend CLAUDE.md - Next.js Application

## Overview

Next.js 16+ application with App Router, TypeScript, Tailwind CSS, and OpenAI ChatKit for Phase III AI-powered todo chatbot.

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page (/)
│   │   ├── login/page.tsx      # Login page
│   │   ├── signup/page.tsx     # Signup page
│   │   ├── dashboard/page.tsx  # Dashboard (protected)
│   │   └── chat/page.tsx       # Chat interface (Phase III)
│   ├── components/
│   │   ├── ui/                 # Base components
│   │   ├── layout/             # Header, Footer
│   │   ├── auth/               # LoginForm, SignupForm
│   │   ├── tasks/              # Task components (Phase II)
│   │   └── chat/               # ChatKit components (Phase III)
│   │       ├── ChatInterface.tsx
│   │       └── ChatMessage.tsx
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Token utilities
│   │   ├── chat.ts             # Chat API client (Phase III)
│   │   └── types.ts            # TypeScript types
│   └── middleware.ts           # Route protection
└── package.json
```

## Key Specifications

### Phase III (Current)
- **Chat Interface**: `@specs/003-ai-chatbot/ui/chat-interface.md`
- **ChatKit Integration**: `@specs/003-ai-chatbot/ui/chatkit-integration.md`
- **Conversation Flows**: `@specs/003-ai-chatbot/conversation/`

### Phase II (Still Required)
- **Pages**: `@specs/002-fullstack-web-app/ui/pages.md`
- **Components**: `@specs/002-fullstack-web-app/ui/components.md`
- **API Contract**: `@specs/002-fullstack-web-app/contracts/api-contract.md`
- **JWT Handling**: `@specs/002-fullstack-web-app/api/jwt-auth.md`

## Implementation Rules

### Authentication
- Store JWT in localStorage
- Attach `Authorization: Bearer <token>` to all API requests (including chat)
- Redirect to login on 401 responses
- Clear token on logout
- Chat interface requires authentication

### Route Protection
- `/dashboard` requires authentication
- `/chat` requires authentication (Phase III)
- Redirect authenticated users from `/login` and `/signup`
- Use Next.js middleware for route guards

### API Client
- Base URL from `NEXT_PUBLIC_API_URL`
- Handle all error responses consistently
- Support loading states
- Chat endpoint: `POST /api/{user_id}/chat`

### ChatKit Integration (Phase III)

#### OpenRouter Configuration
- Use OpenRouter as AI model provider (NOT OpenAI API)
- API key stored in `NEXT_PUBLIC_OPENROUTER_KEY`
- ChatKit configured to use OpenRouter endpoint
- Model selection: Use recommended OpenRouter models (e.g., `anthropic/claude-3-sonnet`)

#### Chat Interface
- Primary interface for task management via natural language
- Traditional CRUD UI (Phase II) remains available as fallback
- Chat messages persisted via backend `/api/{user_id}/chat` endpoint
- Display conversation history from backend
- Show tool invocations (task operations) in chat UI

#### Chat API Integration
```typescript
// POST /api/{user_id}/chat
interface ChatRequest {
  conversation_id?: string;  // Optional - creates new if not provided
  message: string;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<{
    tool: string;
    input: Record<string, any>;
    output: Record<string, any>;
  }>;
}
```

#### Conversation Management
- Load conversation history on chat page mount
- Display user and assistant messages chronologically
- Show tool invocations (e.g., "Added task: Buy groceries")
- Support creating new conversations
- Support resuming existing conversations

#### User Experience
- Natural language input for task operations
- Friendly confirmations from AI agent
- Error messages displayed in chat
- Loading states during AI processing
- Responsive design for mobile and desktop

### Components
- Use Tailwind CSS for styling
- Support responsive design (mobile-first)
- Implement loading and error states
- ChatKit components follow OpenAI ChatKit patterns

## Type Definitions

All types in `src/lib/types.ts`:

### Phase II Types (Still Required)
- `User`, `Task`, `AuthResponse`
- `SignupRequest`, `SigninRequest`
- `TaskCreateRequest`, `TaskUpdateRequest`
- `ErrorResponse`

### Phase III Types (New)
- `Conversation`, `Message`
- `ChatRequest`, `ChatResponse`
- `ToolCall`, `ToolInvocation`

```typescript
// Phase III types
interface Conversation {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface Message {
  id: string;
  user_id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

interface ChatRequest {
  conversation_id?: string;
  message: string;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}

interface ToolCall {
  tool: string;
  input: Record<string, any>;
  output: Record<string, any>;
}
```

## Environment Variables

```env
# Phase II (Required)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<32+ character secret>

# Phase III (New)
NEXT_PUBLIC_OPENROUTER_KEY=<OpenRouter API key>
```

## Navigation

### Phase III Navigation
- Landing page (/) → Login/Signup or Dashboard
- Dashboard (/dashboard) → Traditional CRUD UI (Phase II fallback)
- Chat (/chat) → AI-powered chatbot interface (Phase III primary)
- Header includes navigation to both Dashboard and Chat

### User Flow
1. User logs in
2. Redirected to Chat interface (primary)
3. Can switch to Dashboard for traditional CRUD UI
4. Both interfaces operate on same task data

## Testing

- Jest + React Testing Library for unit tests
- Test components in isolation
- Mock API responses
- Test ChatKit integration with mocked OpenRouter responses
- Test conversation persistence and loading

## Prohibited Actions

- Using OpenAI API key instead of OpenRouter key
- Direct task manipulation without going through backend API
- Storing conversation state in frontend (must load from backend)
- Bypassing authentication for chat interface
