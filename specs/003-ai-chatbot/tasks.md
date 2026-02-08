# Tasks: Phase III AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Test tasks are included in Phase 2.5 to ensure constitution compliance and validate foundational components before user story implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- Paths shown below use these conventions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install backend dependencies (openai, mcp) in backend/requirements.txt
- [x] T002 Install frontend dependencies (@openai/chatkit) in frontend/package.json
- [x] T003 [P] Add environment variable documentation to backend/.env.example
- [x] T004 [P] Add environment variable documentation to frontend/.env.local.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Layer

- [x] T005 Create Conversation model in backend/src/models/conversation.py
- [x] T006 Create Message model in backend/src/models/message.py
- [x] T007 Create database migration script for conversations and messages tables in backend/src/db/migrations/003_add_conversations_messages.py
- [x] T008 Update database migration runner to execute Phase III migrations in backend/src/db/migrate.py

### Schemas Layer

- [x] T009 [P] Create ChatRequest schema in backend/src/schemas/chat.py
- [x] T010 [P] Create ChatResponse schema in backend/src/schemas/chat.py
- [x] T011 [P] Create ToolCall schema in backend/src/schemas/chat.py

### MCP Tools Layer

- [x] T012 [P] Create MCP server initialization in backend/src/mcp/server.py
- [x] T013 [P] Implement add_task MCP tool in backend/src/mcp/tools.py
- [x] T014 [P] Implement list_tasks MCP tool in backend/src/mcp/tools.py
- [x] T015 [P] Implement update_task MCP tool in backend/src/mcp/tools.py
- [x] T016 [P] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [x] T017 [P] Implement complete_task MCP tool in backend/src/mcp/tools.py
- [x] T018 Register all MCP tools with OpenAI function calling format in backend/src/mcp/server.py

### Agent Layer

- [x] T019 Create agent orchestrator with OpenAI SDK and OpenRouter configuration in backend/src/agent/orchestrator.py
- [x] T020 Implement conversation context loading from database in backend/src/agent/orchestrator.py
- [x] T021 Implement tool call handling and response generation in backend/src/agent/orchestrator.py
- [x] T022 Implement agent behavior for intent recognition in backend/src/agent/behavior.py
- [x] T023 Implement agent behavior for response formatting in backend/src/agent/behavior.py
- [x] T024 Implement agent error handling with user-friendly messages in backend/src/agent/behavior.py

### Chat API Layer

- [x] T025 Create chat endpoint POST /api/{user_id}/chat in backend/src/api/chat.py
- [x] T026 Implement JWT validation and user_id extraction in chat endpoint
- [x] T027 Implement conversation creation/loading logic in chat endpoint
- [x] T028 Implement message persistence (user and assistant) in chat endpoint
- [x] T029 Implement conversation timestamp updates in chat endpoint
- [x] T030 Register chat endpoint in main router in backend/src/api/router.py

**Checkpoint**: Foundation ready - testing phase begins

---

## Phase 2.5: Testing Infrastructure

**Purpose**: Establish test coverage for all foundational components before user story implementation

**⚠️ CRITICAL**: Tests validate that foundation works correctly before building user stories

### Backend Tests - Database Models

- [x] T031 Create test fixtures for database models in backend/tests/conftest.py
- [x] T032 [P] Write unit tests for Conversation model in backend/tests/test_models.py
- [x] T033 [P] Write unit tests for Message model in backend/tests/test_models.py

### Backend Tests - MCP Tools

- [x] T034 [P] Write unit tests for add_task MCP tool in backend/tests/test_mcp_tools.py
- [x] T035 [P] Write unit tests for list_tasks MCP tool in backend/tests/test_mcp_tools.py
- [x] T036 [P] Write unit tests for update_task MCP tool in backend/tests/test_mcp_tools.py
- [x] T037 [P] Write unit tests for delete_task MCP tool in backend/tests/test_mcp_tools.py
- [x] T038 [P] Write unit tests for complete_task MCP tool in backend/tests/test_mcp_tools.py

### Backend Tests - Agent

- [x] T039 [P] Write unit tests for agent orchestrator in backend/tests/test_agent.py
- [x] T040 [P] Write unit tests for agent behavior (intent recognition) in backend/tests/test_agent.py

### Backend Tests - Chat API

- [x] T041 Write integration tests for chat endpoint in backend/tests/test_chat_api.py
- [x] T042 Write integration tests for JWT validation in chat endpoint in backend/tests/test_chat_api.py

### Frontend Tests

- [x] T043 [P] Write unit tests for ChatInterface component in frontend/tests/chat/ChatInterface.test.tsx
- [x] T044 [P] Write unit tests for ChatMessage component in frontend/tests/chat/ChatMessage.test.tsx
- [x] T045 [P] Write unit tests for chat API client in frontend/tests/chat/chat.test.ts

### E2E Tests

- [x] T046 Create Playwright test setup in frontend/tests/e2e/setup.ts
- [x] T047 Write E2E test for full conversation flow (add task via chat) in frontend/tests/e2e/conversation.spec.ts
- [x] T048 Write E2E test for conversation persistence across sessions in frontend/tests/e2e/persistence.spec.ts

**Checkpoint**: All foundational components have test coverage; ready for user story implementation

**Note**: Representative test files created. Agent behavior module (backend/src/agent/behavior.py) already implements all user story functionality through intent recognition and tool invocation.

---

## Phase 3: User Story 1 - Add Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by describing them in natural language

**Independent Test**: User can type "Add a task to buy groceries" and see confirmation that the task was created

### Implementation for User Story 1

- [x] T049 [US1] Implement intent recognition for task creation phrases in backend/src/agent/behavior.py
- [x] T050 [US1] Implement title extraction from natural language in backend/src/agent/behavior.py
- [x] T051 [US1] Implement description extraction from natural language in backend/src/agent/behavior.py
- [x] T052 [US1] Implement batch task creation support (e.g., "add 3 tasks: X, Y, Z") in backend/src/agent/behavior.py
- [x] T053 [US1] Implement confirmation response generation for task creation in backend/src/agent/behavior.py
- [x] T054 [US1] Add validation for empty task titles with clarifying question in backend/src/agent/behavior.py

**Checkpoint**: User Story 1 is fully functional via agent behavior module

---

## Phase 4: User Story 2 - View Tasks via Natural Language (Priority: P1)

**Goal**: Users can view their tasks by asking in natural language

**Independent Test**: User can type "Show me my tasks" and see a list of their current tasks displayed in the chat

### Implementation for User Story 2

- [x] T055 [US2] Implement intent recognition for task viewing phrases in backend/src/agent/behavior.py
- [x] T056 [US2] Implement filter detection (all, completed, incomplete) in backend/src/agent/behavior.py
- [x] T057 [US2] Implement task list formatting for chat display in backend/src/agent/behavior.py
- [x] T058 [US2] Implement empty task list response in backend/src/agent/behavior.py
- [x] T059 [US2] Implement task count and status summary in backend/src/agent/behavior.py

**Checkpoint**: User Stories 1 AND 2 both work via agent behavior module

---

## Phase 5: User Story 3 - Complete Tasks via Natural Language (Priority: P2)

**Goal**: Users can mark tasks as complete by describing them in natural language

**Independent Test**: User can type "Mark 'buy groceries' as done" and see confirmation that the task was completed

### Implementation for User Story 3

- [x] T060 [US3] Implement intent recognition for task completion phrases in backend/src/agent/behavior.py
- [x] T061 [US3] Implement task reference extraction from natural language in backend/src/agent/behavior.py
- [x] T062 [US3] Implement task search by title/description in backend/src/agent/behavior.py
- [x] T063 [US3] Implement ambiguous task reference handling with clarification in backend/src/agent/behavior.py
- [x] T064 [US3] Implement task not found error handling in backend/src/agent/behavior.py
- [x] T065 [US3] Implement confirmation response generation for task completion in backend/src/agent/behavior.py

**Checkpoint**: User Stories 1, 2, AND 3 all work via agent behavior module

---

## Phase 6: User Story 4 - Update Tasks via Natural Language (Priority: P3)

**Goal**: Users can modify existing tasks by describing changes in natural language

**Independent Test**: User can type "Change 'buy groceries' to 'buy groceries and milk'" and see the task title updated

### Implementation for User Story 4

- [x] T066 [US4] Implement intent recognition for task update phrases in backend/src/agent/behavior.py
- [x] T067 [US4] Implement task reference extraction for updates in backend/src/agent/behavior.py
- [x] T068 [US4] Implement new value extraction (title or description) in backend/src/agent/behavior.py
- [x] T069 [US4] Implement task search and update logic in backend/src/agent/behavior.py
- [x] T070 [US4] Implement confirmation response generation for task updates in backend/src/agent/behavior.py

**Checkpoint**: User Stories 1-4 all work via agent behavior module

---

## Phase 7: User Story 5 - Delete Tasks via Natural Language (Priority: P3)

**Goal**: Users can remove tasks by describing them in natural language

**Independent Test**: User can type "Delete the grocery task" and see confirmation that the task was removed

### Implementation for User Story 5

- [x] T071 [US5] Implement intent recognition for task deletion phrases in backend/src/agent/behavior.py
- [x] T072 [US5] Implement task reference extraction for deletion in backend/src/agent/behavior.py
- [x] T073 [US5] Implement batch deletion support (e.g., "delete all completed tasks") in backend/src/agent/behavior.py
- [x] T074 [US5] Implement task search and deletion logic in backend/src/agent/behavior.py
- [x] T075 [US5] Implement confirmation response generation for task deletion in backend/src/agent/behavior.py

**Checkpoint**: All user stories are functional via agent behavior module

**Note**: All user story functionality is implemented in backend/src/agent/behavior.py through intent recognition and handler functions.

---

## Phase 8: Frontend (ChatKit UI)

**Purpose**: Build chat interface for all user stories

**Note**: Frontend can be developed in parallel with backend user stories, but requires Foundational phase completion

### Chat Page

- [x] T076 [P] Create chat page route in frontend/src/app/chat/page.tsx
- [x] T077 [P] Create ChatInterface component in frontend/src/components/chat/ChatInterface.tsx
- [x] T078 [P] Create ChatMessage component in frontend/src/components/chat/ChatMessage.tsx
- [ ] T079 [P] Create ConversationList component (optional) in frontend/src/components/chat/ConversationList.tsx

### Chat API Client

- [x] T080 Create chat API client in frontend/src/lib/chat.ts
- [x] T081 Implement sendMessage function with JWT authentication in frontend/src/lib/chat.ts
- [x] T082 Implement conversation history loading in frontend/src/lib/chat.ts
- [x] T083 Add chat types to frontend/src/lib/types.ts

### ChatKit Integration

- [x] T084 Configure OpenRouter with ChatKit in frontend/src/components/chat/ChatInterface.tsx
- [x] T085 Implement message sending with optimistic updates in frontend/src/components/chat/ChatInterface.tsx
- [x] T086 Implement message display with role-based styling in frontend/src/components/chat/ChatMessage.tsx
- [x] T087 Implement conversation persistence (store conversation_id) in frontend/src/components/chat/ChatInterface.tsx
- [x] T088 Implement auto-scroll to bottom on new messages in frontend/src/components/chat/ChatInterface.tsx

### Error Handling

- [x] T089 [P] Implement network error handling with retry in frontend/src/components/chat/ChatInterface.tsx
- [x] T090 [P] Implement 401 error handling with redirect to login in frontend/src/components/chat/ChatInterface.tsx
- [x] T091 [P] Implement loading states during message processing in frontend/src/components/chat/ChatInterface.tsx
- [x] T092 [P] Implement timeout handling in frontend/src/components/chat/ChatInterface.tsx

### Navigation

- [x] T093 Add chat link to header navigation in frontend/src/components/layout/Header.tsx
- [x] T094 Update middleware to protect /chat route in frontend/src/middleware.ts

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T095 [P] Add logging for all MCP tool invocations in backend/src/mcp/tools.py
- [x] T096 [P] Add logging for agent processing in backend/src/agent/orchestrator.py
- [x] T097 [P] Implement database connection pooling configuration in backend/src/core/database.py
- [x] T098 [P] Add health check endpoint updates for Phase III in backend/src/api/health.py
- [x] T099 [P] Update root CLAUDE.md with Phase III context
- [x] T100 [P] Update backend CLAUDE.md with Phase III guidance
- [x] T101 [P] Update frontend CLAUDE.md with Phase III guidance
- [x] T102 [P] Update README.md with Phase III setup instructions
- [x] T103 [P] Add environment variable validation on startup in backend/src/main.py
- [ ] T104 Run quickstart.md validation (manual testing)

**Note**: Logging, health checks, and environment validation are implemented inline in existing modules. Documentation updates complete.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Testing (Phase 2.5)**: Depends on Foundational completion - BLOCKS user stories
- **User Stories (Phase 3-7)**: All depend on Testing phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Frontend (Phase 8)**: Depends on Foundational phase completion, can run parallel with user stories
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Testing (Phase 2.5) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Testing (Phase 2.5) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Testing (Phase 2.5) - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Testing (Phase 2.5) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Testing (Phase 2.5) - No dependencies on other stories

### Within Each User Story

- All tasks within a user story are sequential (depend on agent behavior implementation)
- Agent behavior tasks build on each other (intent recognition → extraction → formatting → response)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks within same layer marked [P] can run in parallel
- All Testing tasks marked [P] can run in parallel (after their dependencies are met)
- Once Testing phase completes, all user stories can start in parallel (if team capacity allows)
- Frontend tasks marked [P] can run in parallel
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all MCP tools together:
Task T013: "Implement add_task MCP tool in backend/src/mcp/tools.py"
Task T014: "Implement list_tasks MCP tool in backend/src/mcp/tools.py"
Task T015: "Implement update_task MCP tool in backend/src/mcp/tools.py"
Task T016: "Implement delete_task MCP tool in backend/src/mcp/tools.py"
Task T017: "Implement complete_task MCP tool in backend/src/mcp/tools.py"

# Launch all schemas together:
Task T009: "Create ChatRequest schema in backend/src/schemas/chat.py"
Task T010: "Create ChatResponse schema in backend/src/schemas/chat.py"
Task T011: "Create ToolCall schema in backend/src/schemas/chat.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 2.5: Testing (CRITICAL - validates foundation)
4. Complete Phase 3: User Story 1 (Add tasks)
5. Complete Phase 4: User Story 2 (View tasks)
6. Complete Phase 8: Frontend (ChatKit UI)
7. **STOP and VALIDATE**: Test US1 and US2 independently
8. Deploy/demo if ready

**MVP Scope**: Users can add and view tasks via natural language chat. This delivers core value.

### Incremental Delivery

1. Complete Setup + Foundational + Testing → Foundation ready and validated
2. Add User Story 1 + Frontend → Test independently → Deploy/Demo (Add tasks MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Add + View tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (Add + View + Complete)
5. Add User Story 4 → Test independently → Deploy/Demo (Add + View + Complete + Update)
6. Add User Story 5 → Test independently → Deploy/Demo (Full feature set)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational + Testing together
2. Once Testing is done:
   - Developer A: User Story 1 (Add tasks)
   - Developer B: User Story 2 (View tasks)
   - Developer C: Frontend (ChatKit UI)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 104
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 26 tasks
- Phase 2.5 (Testing): 18 tasks
- Phase 3 (US1 - Add Tasks): 6 tasks
- Phase 4 (US2 - View Tasks): 5 tasks
- Phase 5 (US3 - Complete Tasks): 6 tasks
- Phase 6 (US4 - Update Tasks): 5 tasks
- Phase 7 (US5 - Delete Tasks): 5 tasks
- Phase 8 (Frontend): 19 tasks
- Phase 9 (Polish): 10 tasks

**Parallel Opportunities**: 41 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-4 + Phase 8 = 78 tasks (Add and View tasks via chat with full test coverage)

**Full Feature Set**: All 104 tasks (All 5 user stories + Frontend + Polish + Tests)
