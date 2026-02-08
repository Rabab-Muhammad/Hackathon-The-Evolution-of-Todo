---
id: 0002
title: phase-iii-ai-chatbot-constitution
stage: constitution
date: 2026-02-08
surface: cli
model: claude-sonnet-4-5
feature: 003-ai-chatbot
branch: main
user: system
command: /sp.constitution
labels: [constitution, phase-iii, ai-chatbot, mcp, stateless-architecture]
links:
  spec: specs/003-ai-chatbot/
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    action: updated
    lines_changed: 350
tests:
  - type: validation
    status: pass
    description: Constitution template validation - no unresolved placeholders
---

## Prompt

Project: Evolution of Todo – Phase III: AI-Powered Todo Chatbot

Core Principles:
- Spec-Driven Development Only
  All chatbot and MCP features must be fully specified in Spec-Kit Plus before implementation. No manual coding allowed.

- Stateless Architecture
  Backend holds no conversation state. All chat history is persisted in Neon PostgreSQL. Any server instance can handle any request.

- AI-First Interaction
  Users manage todos via natural language. OpenRouter (not OpenAI API) is used as the AI model for ChatKit frontend.

- Standardized Tool Interface
  MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) define all task operations. AI agent uses only these tools.

- Traceability
  Every MCP tool, endpoint, and agent behavior must map to spec files in /specs. Frontend and backend implementations must reference these specs.

- Security & Authentication
  Better Auth with JWT ensures only authenticated users can access tasks. AI agents operate per user context.

- Conversation Management
  Conversation, message, and task state are persisted in database. Stateless server can resume any conversation without in-memory storage.

Key Standards:
- Frontend: OpenAI ChatKit using OpenRouter, connected to backend /api/{user_id}/chat
- Backend: FastAPI, OpenAI Agents SDK, MCP server (Official MCP SDK), SQLModel ORM, Neon PostgreSQL
- Authentication: Better Auth, JWT, user-scoped task access
- MCP Tools: Must expose exactly these operations: add_task, list_tasks, complete_task, delete_task, update_task
- Database Models:
    * Task: user_id, id, title, description, completed, created_at, updated_at
    * Conversation: user_id, id, created_at, updated_at
    * Message: user_id, id, conversation_id, role (user/assistant), content, created_at
- Chat API Endpoint:
    * POST /api/{user_id}/chat
    * Request: conversation_id (optional), message (required)
    * Response: conversation_id, response, tool_calls
- Natural Language Commands:
    * AI agent maps user commands to MCP tools using agent behavior specification
    * Always confirm actions, handle errors gracefully

Monorepo Layout:
- /frontend → ChatKit UI (OpenRouter key stored in env: NEXT_PUBLIC_OPENROUTER_KEY)
- /backend → FastAPI + Agents SDK + MCP server
- /specs → Specifications for chatbot, MCP tools, conversation flows
- Database migrations and models in /backend
- README.md with setup instructions

Constraints:
- Use OpenRouter key for AI, not OpenAI API key.
- Frontend and backend folders already exist; work inside these.
- No manual code outside of Claude Code generation.
- All MCP tool operations must be stateless; state persisted in DB only.
- ChatKit frontend must connect to stateless backend endpoint: /api/{user_id}/chat
- All responses must filter tasks by authenticated user_id.

Success Criteria:
- User can interact with chatbot via natural language to:
    * Add, view, update, delete, and complete tasks
    * Receive friendly confirmations
    * Retrieve correct task lists
- Backend persists conversation and task state in Neon DB
- MCP tools correctly invoked per agent logic
- Server is stateless; conversation resumes seamlessly after restarts
- All specs and CLAUDE.md files present and referenced
- Deployment-ready for local or cloud Kubernetes in next phases

## Response snapshot

Constitution updated from version 2.0.1 to 2.1.0 (MINOR version bump).

**Version Bump Rationale**: MINOR version increment because we added three new principles (VI, VII, VIII) and materially expanded guidance for Phase III AI-powered chatbot functionality without breaking Phase II requirements.

**Changes Made**:

1. **Modified Principles**:
   - Principle V (Scalability Ready): Expanded to include AI agent stateless architecture requirements

2. **Added Principles**:
   - Principle VI (Stateless Architecture): Backend must hold no conversation state in memory; all state persisted in database
   - Principle VII (AI-First Interaction): Users manage todos via natural language; OpenRouter as AI provider
   - Principle VIII (Standardized Tool Interface): MCP tools define all task operations; agent uses only these tools

3. **Expanded Key Standards**:
   - Conversation Management: Persistence, reconstruction, user-scoping requirements
   - MCP Tools: Official MCP SDK, stateless operations, exact tool list (add_task, list_tasks, complete_task, delete_task, update_task)
   - Natural Language Commands: Agent behavior specs, confirmation, error handling

4. **Technology Constraints Updated**:
   - Added: OpenRouter (AI model provider - NOT OpenAI API)
   - Added: OpenAI ChatKit (frontend chat UI)
   - Added: OpenAI Agents SDK (backend agent orchestration)
   - Added: Official MCP SDK (tool interface)

5. **Database Models Expanded**:
   - Added: Conversation (user_id, id, created_at, updated_at)
   - Added: Message (user_id, id, conversation_id, role, content, created_at)
   - Existing: Task (unchanged from Phase II)

6. **Success Criteria**:
   - Retained: SC-001 through SC-009 (Phase II criteria still required)
   - Added: SC-010 through SC-015 (Phase III chatbot functionality)

7. **Monorepo Structure**:
   - Added: specs/003-ai-chatbot/ with mcp/, agent/, conversation/ subdirectories
   - Added: backend/src/agent/ and backend/src/mcp/ directories
   - Added: frontend/src/components/chat/ directory

8. **Prohibited Actions Expanded**:
   - Direct database access from AI agent (must use MCP tools)
   - Using OpenAI API key instead of OpenRouter key
   - Storing conversation state in memory

**Template Compatibility**: All existing templates (plan-template.md, spec-template.md, tasks-template.md) remain compatible. The web app structure already supports AI backend extensions.

**Sync Impact Report**: Embedded at top of constitution file documenting all changes, validation status, and follow-up TODOs.

## Outcome

- ✅ Impact: Constitution successfully updated to v2.1.0 with Phase III AI-powered chatbot principles and standards
- 🧪 Tests: Validation passed - no unresolved placeholders, all principles documented with rationale
- 📁 Files: .specify/memory/constitution.md (350 lines)
- 🔁 Next prompts: Create Phase III specifications using /sp.specify, then /sp.plan, /sp.tasks
- 🧠 Reflection: MINOR version bump appropriate - added new principles without breaking Phase II. All Phase II criteria remain required. Stateless architecture principle critical for Kubernetes readiness.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): Template validation PASS, semantic versioning PASS, traceability PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.specify for Phase III feature specification
