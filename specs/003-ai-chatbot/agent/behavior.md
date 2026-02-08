# Agent Behavior Specification

**Feature Branch**: `003-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft

## Purpose

Define the behavior and decision-making logic for the AI agent that interprets user messages, selects appropriate MCP tools, and generates natural language responses. This specification ensures consistent, user-friendly, and predictable agent behavior.

## Agent Responsibilities

1. **Intent Interpretation**: Understand user's natural language message and identify intended task operation
2. **Tool Selection**: Choose appropriate MCP tool(s) to fulfill user's intent
3. **Tool Chaining**: Execute multiple tools in sequence when necessary
4. **Context Management**: Use conversation history to understand references and context
5. **Response Generation**: Create friendly, confirmatory responses with specific details
6. **Error Handling**: Handle errors gracefully with user-friendly messages and suggestions

## Intent Recognition

### Task Creation Intents

**Trigger Phrases**:
- "Add a task to [description]"
- "Create task: [description]"
- "Remind me to [description]"
- "I need to [description]"
- "Add [description] to my list"
- "New task: [description]"

**Agent Action**:
1. Extract task title from description
2. Extract optional description if provided (e.g., "with description: [text]")
3. Call `add_task` tool with user_id, title, and description
4. Generate confirmation response with task title

**Example**:
- User: "Add a task to buy groceries"
- Agent: Calls `add_task(user_id, "Buy groceries", null)`
- Response: "I've added the task 'Buy groceries' to your list."

### Task Viewing Intents

**Trigger Phrases**:
- "Show me my tasks"
- "What tasks do I have?"
- "List my tasks"
- "What's on my list?"
- "Show incomplete tasks"
- "Show completed tasks"

**Agent Action**:
1. Determine filter (all, incomplete, completed) from phrasing
2. Call `list_tasks` tool with user_id and completed filter
3. Format task list in readable format
4. Generate response with task count and list

**Example**:
- User: "Show me my tasks"
- Agent: Calls `list_tasks(user_id, completed=null)`
- Response: "You have 3 tasks:\n1. Buy groceries (not completed)\n2. Call mom (not completed)\n3. Finish report (completed)"

### Task Completion Intents

**Trigger Phrases**:
- "Mark [task] as done"
- "Complete [task]"
- "I finished [task]"
- "Done with [task]"
- "[task] is complete"

**Agent Action**:
1. Extract task reference from message
2. If reference is ambiguous, call `list_tasks` to find matching tasks
3. If multiple matches, ask user for clarification
4. If single match, call `complete_task` with task_id
5. Generate confirmation response with task title

**Example**:
- User: "Mark buy groceries as done"
- Agent: Calls `list_tasks` to find task, then `complete_task(user_id, task_id)`
- Response: "Great! I've marked 'Buy groceries' as complete."

### Task Update Intents

**Trigger Phrases**:
- "Change [task] to [new title]"
- "Update [task] description to [text]"
- "Rename [task] to [new title]"
- "Edit [task]"

**Agent Action**:
1. Extract task reference and new values
2. Call `list_tasks` to find matching task
3. If ambiguous, ask for clarification
4. Call `update_task` with task_id and new values
5. Generate confirmation response

**Example**:
- User: "Change buy groceries to buy groceries and milk"
- Agent: Calls `list_tasks`, then `update_task(user_id, task_id, "Buy groceries and milk", null)`
- Response: "I've updated the task to 'Buy groceries and milk'."

### Task Deletion Intents

**Trigger Phrases**:
- "Delete [task]"
- "Remove [task]"
- "Get rid of [task]"
- "Delete all completed tasks"

**Agent Action**:
1. Extract task reference
2. Call `list_tasks` to find matching task(s)
3. If ambiguous, ask for clarification
4. Call `delete_task` for each matching task
5. Generate confirmation response

**Example**:
- User: "Delete buy groceries"
- Agent: Calls `list_tasks`, then `delete_task(user_id, task_id)`
- Response: "I've deleted 'Buy groceries' from your list."

## Tool Chaining Logic

### Scenario 1: Ambiguous Task Reference

**User Message**: "Complete the grocery task"

**Agent Logic**:
1. Call `list_tasks(user_id, completed=false)` to get incomplete tasks
2. Search for tasks containing "grocery" in title
3. If 0 matches: Respond "I couldn't find a task matching 'grocery'. Could you describe it differently?"
4. If 1 match: Call `complete_task(user_id, task_id)` and confirm
5. If 2+ matches: Ask "I found multiple tasks: [list]. Which one did you mean?"

### Scenario 2: Batch Operations

**User Message**: "Delete all completed tasks"

**Agent Logic**:
1. Call `list_tasks(user_id, completed=true)` to get completed tasks
2. If 0 tasks: Respond "You don't have any completed tasks."
3. If 1+ tasks: Call `delete_task(user_id, task_id)` for each task
4. Respond "I've deleted [count] completed task(s) from your list."

### Scenario 3: Multiple Operations

**User Message**: "Add task to buy milk and show me my tasks"

**Agent Logic**:
1. Call `add_task(user_id, "Buy milk", null)`
2. Call `list_tasks(user_id, completed=null)`
3. Respond "I've added 'Buy milk' to your list. You now have [count] tasks: [list]"

## Context Management

### Conversation History Usage

The agent uses conversation history to:
1. **Resolve References**: "Also add buy milk" → understands "also" refers to previous add operation
2. **Maintain Context**: "What about the other one?" → refers to previously mentioned task
3. **Clarification Follow-up**: After asking "Which task?", understand user's response

**Example Conversation**:
```
User: "Add a task to buy groceries"
Agent: "I've added the task 'Buy groceries' to your list."
User: "Also add buy milk"
Agent: [Understands "also add" means another task] "I've added the task 'Buy milk' to your list."
```

### History Limit

- Load last 50 messages for context (configurable)
- Older messages not included to optimize performance
- Critical context (task references) extracted and maintained

## Response Generation Guidelines

### Confirmation Responses

**After Task Creation**:
- Template: "I've added the task '[title]' to your list."
- Include description if provided: "I've added the task '[title]' with description '[description]' to your list."

**After Task Completion**:
- Template: "Great! I've marked '[title]' as complete."
- Variations: "Awesome! '[title]' is now complete.", "Done! I've completed '[title]'."

**After Task Update**:
- Template: "I've updated the task to '[new title]'."
- If description updated: "I've updated the description for '[title]'."

**After Task Deletion**:
- Template: "I've deleted '[title]' from your list."
- For batch: "I've deleted [count] task(s) from your list."

**After Task Listing**:
- Template: "You have [count] task(s): [list]"
- If empty: "You don't have any tasks yet. Would you like to add one?"
- If filtered: "You have [count] [completed/incomplete] task(s): [list]"

### Error Responses

**Task Not Found**:
- "I couldn't find a task matching '[reference]'. Could you describe it differently?"
- "I don't see a task called '[reference]' in your list. Would you like to see all your tasks?"

**Ambiguous Reference**:
- "I found multiple tasks matching '[reference]': [list]. Which one did you mean?"
- "Could you be more specific? I found these tasks: [list]"

**Invalid Input**:
- "I need more information. Could you provide [specific detail]?"
- "Task titles must be 100 characters or less. Could you shorten it?"

**System Error**:
- "I'm having trouble processing that right now. Could you try again?"
- "Something went wrong. Please try again in a moment."

### Tone and Style

- **Friendly**: Use conversational language, not robotic
- **Confirmatory**: Always confirm actions taken
- **Specific**: Include task titles and details in responses
- **Helpful**: Offer suggestions when user seems stuck
- **Concise**: Keep responses brief but informative
- **Positive**: Use encouraging language ("Great!", "Awesome!")

## Error Handling

### MCP Tool Errors

**Tool Returns Error**:
1. Parse error message from tool
2. Translate technical error to user-friendly message
3. Offer suggestion or alternative action
4. Log error for debugging

**Example**:
- Tool Error: "Title must be 100 characters or less"
- Agent Response: "That task title is too long. Could you shorten it to 100 characters or less?"

### Database Errors

**Connection Failure**:
- Response: "I'm having trouble connecting right now. Please try again in a moment."
- Log error with context

**Query Timeout**:
- Response: "That's taking longer than expected. Could you try again?"
- Log error with query details

### Agent Processing Errors

**Intent Not Recognized**:
- Response: "I'm not sure what you'd like me to do. You can ask me to add, view, update, complete, or delete tasks."
- Offer examples: "For example, try 'Add a task to buy groceries' or 'Show me my tasks'."

**Parsing Failure**:
- Response: "I didn't quite understand that. Could you rephrase it?"
- Log message for analysis

## Prohibited Actions

1. **No Direct Database Access**: Agent MUST use MCP tools exclusively
2. **No Cross-User Access**: Agent MUST only operate on authenticated user's data
3. **No Hardcoded Responses**: Responses MUST be generated dynamically based on tool results
4. **No Sensitive Data Exposure**: Never include user_id, JWT tokens, or internal IDs in responses
5. **No Assumptions**: If intent is unclear, ask for clarification rather than guessing

## Configuration

### Agent Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_history_messages | 50 | Maximum conversation messages to load for context |
| response_timeout | 30s | Maximum time for agent processing |
| tool_call_timeout | 10s | Maximum time for single tool call |
| max_tool_calls | 10 | Maximum tool calls per request |
| enable_tool_chaining | true | Allow multiple tool calls in sequence |

### Behavior Flags

| Flag | Default | Description |
|------|---------|-------------|
| ask_for_clarification | true | Ask user when intent is ambiguous |
| suggest_alternatives | true | Offer suggestions when task not found |
| use_friendly_tone | true | Use conversational, encouraging language |
| include_task_details | true | Include task titles in confirmations |
| log_tool_calls | true | Log all tool invocations for debugging |

## Testing Requirements

### Intent Recognition Tests

- Test each trigger phrase pattern
- Test variations and synonyms
- Test multi-operation messages
- Test ambiguous messages

### Tool Chaining Tests

- Test single tool calls
- Test sequential tool calls
- Test error handling in chains
- Test timeout handling

### Context Tests

- Test reference resolution
- Test conversation continuity
- Test history limit handling

### Error Handling Tests

- Test all error scenarios
- Test error message clarity
- Test recovery suggestions

## Acceptance Criteria

- **AC-026**: Agent correctly interprets 95% of common task operation phrases
- **AC-027**: Agent uses only MCP tools for task operations (no direct database access)
- **AC-028**: Agent generates friendly, specific confirmation messages for all operations
- **AC-029**: Agent asks for clarification when intent is ambiguous
- **AC-030**: Agent handles errors gracefully with user-friendly messages
- **AC-031**: Agent maintains conversation context across multiple messages
- **AC-032**: Agent completes processing within 3 seconds for 95% of requests
- **AC-033**: Agent never exposes sensitive data (user_id, tokens) in responses
- **AC-034**: Agent operates only on authenticated user's data (user isolation)
