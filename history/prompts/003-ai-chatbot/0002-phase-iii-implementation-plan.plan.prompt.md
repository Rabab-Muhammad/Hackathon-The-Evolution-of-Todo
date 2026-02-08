---
id: 0002
title: phase-iii-implementation-plan
stage: plan
date: 2026-02-08
surface: cli
model: claude-sonnet-4-5
feature: 003-ai-chatbot
branch: 003-ai-chatbot
user: system
command: /sp.plan
labels: [plan, phase-iii, ai-chatbot, implementation, architecture]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: specs/003-ai-chatbot/plan.md
    action: created
    lines_changed: 400
  - path: specs/003-ai-chatbot/research.md
    action: created
    lines_changed: 450
  - path: specs/003-ai-chatbot/data-model.md
    action: created
    lines_changed: 500
  - path: specs/003-ai-chatbot/contracts/chat-api.yaml
    action: created
    lines_changed: 350
  - path: specs/003-ai-chatbot/contracts/mcp-tools.md
    action: created
    lines_changed: 400
  - path: specs/003-ai-chatbot/quickstart.md
    action: created
    lines_changed: 350
tests:
  - type: validation
    status: pass
    description: Constitution check - all gates passed
---

## Prompt

/sp.plan

Title: Evolution of Todo – Phase III: AI Chatbot Implementation Plan

Objective:
Generate a complete step-by-step implementation plan for Phase III of the Evolution of Todo project, based on the existing Spec-Kit Plus specification files generated from `/sp.specify`. The plan should cover all required tasks to implement the AI-powered Todo Chatbot without any manual coding.

System Role:
You are Claude Code acting as a Product Architect and Implementation Planner. You MUST:
- Produce a clear, sequenced plan of implementation tasks.
- Reference the spec files from `/specs/` explicitly.
- Break down tasks by layer (frontend, backend, agent, MCP, database, UI).
- Include dependencies, sequencing, and testing steps.
- Ensure all tasks are implementable strictly via Claude Code.

Plan Structure:
I. Database Setup
II. MCP Server and Tools
III. Agent Behavior
IV. Chat API Endpoint
V. Frontend (ChatKit UI)
VI. AI Provider Configuration
VII. Integration Testing
VIII. Documentation & Readiness

Constraints:
- No direct database manipulation outside MCP tools.
- No in-memory state on server.
- All chatbot logic must go through the agent → MCP tools.
- No features may be implemented without a corresponding spec file.

## Response snapshot

Created comprehensive implementation plan for Phase III AI Chatbot with complete Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts:

**Phase 0: Research & Technology Decisions** (research.md)
- OpenAI Agents SDK integration patterns
- Official MCP SDK usage with SQLModel
- OpenRouter integration (OpenAI-compatible API)
- ChatKit frontend integration
- Conversation persistence strategy
- Stateless backend design patterns

**Phase 1: Design & Contracts** (data-model.md, contracts/, quickstart.md)
- Data model with 4 entities (User, Task, Conversation, Message)
- Entity relationships and validation rules
- SQLModel definitions and database schema
- OpenAPI 3.0 spec for chat endpoint (chat-api.yaml)
- JSON schemas for 5 MCP tools (mcp-tools.md)
- Quickstart guide with setup instructions

**Implementation Plan** (plan.md)
- Technical context and constitution check (all gates passed)
- Project structure (web application, existing frontend/backend)
- Phase 2 implementation sequence (6 layers)
- Risk assessment and mitigation strategies
- Success criteria (28 Phase III + 9 Phase II)

**Key Decisions**:
- OpenRouter for AI inference (provider-agnostic)
- OpenAI Agents SDK for agent orchestration
- Official MCP SDK for tool interface
- Stateless backend with database persistence
- ChatKit for polished chat UI
- Context window limited to 50 messages

**Architecture Highlights**:
- Stateless request cycle (any instance handles any request)
- Conversation context reconstructed from database
- MCP tools as exclusive interface for task operations
- User isolation enforced at all layers
- Horizontal scaling ready

**Files Created**: 6 planning documents (plan, research, data-model, 2 contracts, quickstart)

## Outcome

- ✅ Impact: Complete implementation plan with research, design, and contracts ready for task generation
- 🧪 Tests: Constitution check passed (all 8 principles satisfied)
- 📁 Files: 6 planning documents created (plan.md, research.md, data-model.md, chat-api.yaml, mcp-tools.md, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed task breakdown for implementation
- 🧠 Reflection: Comprehensive planning phase complete. All technology decisions documented with rationale. Data model and API contracts provide clear implementation guidance. Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning phase completed successfully
- Graders run and results (PASS/FAIL): Constitution check PASS, technical context PASS, design artifacts PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to `/sp.tasks` for task breakdown generation
