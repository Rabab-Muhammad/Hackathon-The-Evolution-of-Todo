# UI Specification: ChatKit Interface

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the user interface for the AI-powered chatbot using OpenAI ChatKit library. This specification covers the chat interface, message display, conversation management, and integration with the backend chat endpoint.

## Technology Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Chat Library**: OpenAI ChatKit
- **AI Provider**: OpenRouter (via ChatKit configuration)
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Fetch API

## Page Structure

### Chat Page (/chat)

**Route**: `/app/chat/page.tsx`

**Authentication**: Required (protected route via middleware)

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Header (with navigation to Dashboard)                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Chat Messages Area (scrollable)               │    │
│  │                                                 │    │
│  │  User: Add a task to buy groceries             │    │
│  │  Assistant: I've added the task 'Buy           │    │
│  │  groceries' to your list.                      │    │
│  │                                                 │    │
│  │  User: Show me my tasks                        │    │
│  │  Assistant: You have 1 task:                   │    │
│  │  1. Buy groceries (not completed)              │    │
│  │                                                 │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Message Input Box                             │    │
│  │  [Type your message here...]          [Send]   │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Component Structure

### ChatInterface Component

**File**: `src/components/chat/ChatInterface.tsx`

**Responsibilities**:
- Render chat messages
- Handle user input
- Send messages to backend
- Display loading states
- Handle errors
- Manage conversation state

**Props**:
```typescript
interface ChatInterfaceProps {
  userId: string;
  conversationId?: string;
}
```

**State**:
```typescript
interface ChatState {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
  inputValue: string;
}
```

**Key Functions**:
- `sendMessage()`: Send user message to backend
- `loadConversationHistory()`: Load existing conversation
- `handleInputChange()`: Update input value
- `handleKeyPress()`: Send on Enter key
- `scrollToBottom()`: Auto-scroll to latest message

---

### ChatMessage Component

**File**: `src/components/chat/ChatMessage.tsx`

**Responsibilities**:
- Display individual message
- Style based on role (user/assistant)
- Show timestamps
- Display tool invocations (optional)

**Props**:
```typescript
interface ChatMessageProps {
  message: Message;
  showToolCalls?: boolean;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  tool_calls?: ToolCall[];
}
```

**Styling**:
- User messages: Right-aligned, blue background
- Assistant messages: Left-aligned, gray background
- Timestamps: Small, gray text below message
- Tool calls: Collapsible section below assistant message

---

### ConversationList Component (Optional)

**File**: `src/components/chat/ConversationList.tsx`

**Responsibilities**:
- Display list of user's conversations
- Allow switching between conversations
- Show conversation preview (last message)
- Create new conversation

**Props**:
```typescript
interface ConversationListProps {
  userId: string;
  currentConversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
  onNewConversation: () => void;
}
```

## Data Flow

### Send Message Flow

1. **User Input**: User types message and clicks Send or presses Enter
2. **Validation**: Check message is not empty
3. **Optimistic Update**: Add user message to UI immediately
4. **API Call**: POST to `/api/{user_id}/chat` with message and conversation_id
5. **Loading State**: Show loading indicator
6. **Response**: Receive conversation_id, response, and tool_calls
7. **Update UI**: Add assistant message to UI
8. **Store conversation_id**: Save for subsequent messages
9. **Scroll**: Auto-scroll to bottom
10. **Clear Input**: Reset input field

### Load Conversation Flow

1. **Page Load**: User navigates to /chat with optional conversation_id query param
2. **Check conversation_id**: If present, load conversation history
3. **API Call**: GET `/api/{user_id}/conversations/{conversation_id}/messages` (future endpoint)
4. **Display Messages**: Render all messages in chronological order
5. **Scroll**: Scroll to bottom
6. **Ready**: Enable input for new messages

**Note**: For MVP, conversation history is loaded implicitly through backend context reconstruction. Explicit history endpoint is future enhancement.

## OpenRouter Integration

### Configuration

**Environment Variable**:
```
NEXT_PUBLIC_OPENROUTER_KEY=<OpenRouter API key>
```

**ChatKit Setup**:
```typescript
import { ChatKit } from '@openai/chatkit';

const chatkit = new ChatKit({
  apiKey: process.env.NEXT_PUBLIC_OPENROUTER_KEY,
  baseURL: 'https://openrouter.ai/api/v1',
  defaultModel: 'anthropic/claude-3-sonnet'
});
```

**Model Selection**:
- Default: `anthropic/claude-3-sonnet`
- Alternative: `openai/gpt-4`
- Configurable via environment variable

### Backend Integration

ChatKit is configured to send messages to backend endpoint instead of directly to OpenRouter:

```typescript
const sendMessage = async (message: string) => {
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

  const data = await response.json();
  return data;
};
```

## User Interactions

### Sending Messages

**Interaction**: User types message and clicks Send button or presses Enter

**Behavior**:
1. Validate message is not empty
2. Disable input and Send button
3. Add user message to chat immediately (optimistic update)
4. Show loading indicator (typing animation)
5. Send request to backend
6. On success: Add assistant response to chat
7. On error: Show error message, allow retry
8. Re-enable input and Send button
9. Clear input field
10. Auto-scroll to bottom

**Keyboard Shortcuts**:
- Enter: Send message
- Shift+Enter: New line in message (multi-line support)

### Viewing Tool Invocations

**Interaction**: User clicks "Show details" on assistant message

**Behavior**:
1. Expand collapsible section below message
2. Display tool calls in formatted list
3. Show tool name, inputs, and outputs
4. Allow collapse to hide details

**Example Display**:
```
Assistant: I've added the task 'Buy groceries' to your list.

[Show details ▼]
  Tool: add_task
  Input: { title: "Buy groceries", description: null }
  Output: { id: "...", title: "Buy groceries", completed: false }
```

### Creating New Conversation

**Interaction**: User clicks "New Conversation" button

**Behavior**:
1. Clear current messages from UI
2. Reset conversation_id to null
3. Clear input field
4. Show welcome message: "Hi! I'm your task assistant. How can I help you today?"
5. Focus input field

### Error Handling

**Network Error**:
- Display: "Connection error. Please check your internet and try again."
- Action: Show retry button

**401 Unauthorized**:
- Display: "Your session has expired. Please log in again."
- Action: Redirect to login page

**500 Server Error**:
- Display: "Something went wrong. Please try again."
- Action: Show retry button

**Timeout**:
- Display: "Request timed out. Please try again."
- Action: Show retry button

## Styling Guidelines

### Message Bubbles

**User Messages**:
```css
- Background: bg-blue-500
- Text: text-white
- Alignment: ml-auto (right-aligned)
- Max width: max-w-[80%]
- Padding: px-4 py-2
- Border radius: rounded-lg
- Margin: mb-2
```

**Assistant Messages**:
```css
- Background: bg-gray-200
- Text: text-gray-900
- Alignment: mr-auto (left-aligned)
- Max width: max-w-[80%]
- Padding: px-4 py-2
- Border radius: rounded-lg
- Margin: mb-2
```

### Input Area

```css
- Border: border border-gray-300
- Padding: px-4 py-2
- Border radius: rounded-lg
- Focus: ring-2 ring-blue-500
- Placeholder: text-gray-400
```

### Send Button

```css
- Background: bg-blue-500 (enabled), bg-gray-300 (disabled)
- Text: text-white
- Padding: px-6 py-2
- Border radius: rounded-lg
- Hover: bg-blue-600 (enabled)
- Disabled: cursor-not-allowed
```

### Loading Indicator

```css
- Typing animation: Three dots bouncing
- Color: text-gray-500
- Position: Below last message
```

## Responsive Design

### Desktop (≥1024px)

- Chat area: 800px max width, centered
- Messages: 80% max width
- Input: Full width of chat area
- Sidebar: Optional conversation list (200px)

### Tablet (768px - 1023px)

- Chat area: Full width with padding
- Messages: 85% max width
- Input: Full width
- Sidebar: Hidden, accessible via menu

### Mobile (<768px)

- Chat area: Full width, no padding
- Messages: 90% max width
- Input: Full width, sticky bottom
- Sidebar: Hidden, accessible via menu
- Font size: Slightly larger for readability

## Accessibility

### Keyboard Navigation

- Tab: Navigate between input and buttons
- Enter: Send message
- Escape: Clear input
- Arrow keys: Navigate message history (future)

### Screen Reader Support

- ARIA labels on all interactive elements
- Role="log" on message container
- Announce new messages
- Describe loading states

### Visual Accessibility

- High contrast mode support
- Minimum font size: 14px
- Focus indicators on all interactive elements
- Color is not the only indicator (use icons too)

## Performance Optimization

### Message Rendering

- Virtualize long message lists (>100 messages)
- Lazy load conversation history
- Debounce input changes
- Throttle scroll events

### Network Optimization

- Retry failed requests with exponential backoff
- Cache conversation_id in localStorage
- Prefetch conversation list
- Compress large messages

## Error States

### Empty State

**When**: User first visits chat page with no messages

**Display**:
```
Welcome! I'm your task assistant.

You can ask me to:
• Add tasks: "Add a task to buy groceries"
• View tasks: "Show me my tasks"
• Complete tasks: "Mark buy groceries as done"
• Update tasks: "Change task title to..."
• Delete tasks: "Delete the grocery task"

What would you like to do?
```

### Loading State

**When**: Waiting for assistant response

**Display**: Typing indicator (three animated dots)

### Error State

**When**: Request fails

**Display**: Error message with retry button

## Testing Requirements

### Component Tests

- Test message rendering (user and assistant)
- Test input handling and validation
- Test send message flow
- Test error handling
- Test loading states

### Integration Tests

- Test full conversation flow
- Test conversation persistence
- Test authentication integration
- Test error recovery

### Accessibility Tests

- Test keyboard navigation
- Test screen reader compatibility
- Test focus management
- Test ARIA labels

## Acceptance Criteria

- **AC-043**: Chat interface renders correctly on desktop, tablet, and mobile
- **AC-044**: Users can send messages and receive responses within 3 seconds
- **AC-045**: Messages are displayed in chronological order with correct styling
- **AC-046**: Loading states are shown during message processing
- **AC-047**: Errors are displayed with user-friendly messages and retry options
- **AC-048**: Conversation persists across page refreshes (conversation_id stored)
- **AC-049**: Input is cleared after sending message
- **AC-050**: Chat auto-scrolls to bottom when new message arrives
- **AC-051**: Keyboard shortcuts work (Enter to send, Shift+Enter for new line)
- **AC-052**: Interface is accessible via keyboard and screen readers
- **AC-053**: Tool invocations are displayed in collapsible sections
- **AC-054**: Authentication errors redirect to login page
