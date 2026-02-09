<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 2.1.0 → 2.2.0

  Status: Phase IV expansion - Cloud-Native Kubernetes Deployment

  Modified principles:
    - V. Scalability Ready: Expanded to include Kubernetes and cloud-native deployment

  Added sections:
    - IX. Cloud-Native Infrastructure (NEW)
    - Deployment Standards (NEW)
    - AI-Assisted DevOps (NEW)
    - Container Standards (NEW)
    - Helm Chart Standards (NEW)

  Removed sections: None

  Technology Constraints updated:
    - Added: Minikube (local Kubernetes)
    - Added: Helm (package manager)
    - Added: Docker Desktop (container runtime)
    - Added: AI DevOps tools (Gordon, kubectl-ai, Kagent)

  Monorepo Structure expanded:
    - Added: deployment/ directory for Helm charts and K8s manifests
    - Added: specs/004-k8s-deployment/ for Phase IV specifications

  Success Criteria updated:
    - Added SC-016 through SC-021 for Phase IV deployment functionality

  Templates validation:
    - .specify/templates/plan-template.md: ✅ Compatible (supports infrastructure planning)
    - .specify/templates/spec-template.md: ✅ Compatible (user stories work for deployment)
    - .specify/templates/tasks-template.md: ✅ Compatible (supports deployment tasks)

  Follow-up TODOs:
    - Create Phase IV specifications in specs/004-k8s-deployment/
    - Update root CLAUDE.md to reference Phase IV
    - Create deployment/CLAUDE.md for infrastructure guidance
    - Document AI DevOps tool usage patterns
-->

# Evolution of Todo – Phase IV Constitution

## Core Principles

### I. Spec-Driven Development

All features MUST be defined in Spec-Kit Plus spec files before implementation.

- No manual coding is permitted; all implementation code MUST be generated from specifications
- Each feature, API endpoint, database schema, UI component, MCP tool, agent behavior, and infrastructure component requires a complete spec before implementation
- Specifications serve as the single source of truth for all behavior across frontend, backend, database, AI agents, and infrastructure
- Changes to behavior MUST first be reflected in updated specifications
- Infrastructure as Code MUST follow the same spec-driven approach as application code

**Rationale**: Ensures traceability, consistency, and that all code across the full stack (including infrastructure and deployment) derives from explicit, documented requirements.

### II. End-to-End Traceability

Every frontend, backend, API, database, auth, MCP tool, agent behavior, and infrastructure change MUST be traceable to a spec file.

- Each UI component MUST reference its spec in `specs/ui/`
- Each API endpoint MUST reference its spec in `specs/api/`
- Each database entity MUST reference its spec in `specs/database/`
- Each feature MUST reference its spec in `specs/features/`
- Each MCP tool MUST reference its spec in `specs/mcp/`
- Each agent behavior MUST reference its spec in `specs/agent/`
- Each Dockerfile, Helm chart, and Kubernetes manifest MUST reference its spec in `specs/deployment/`
- All PRs MUST include references to the specs that define the changes

**Rationale**: In a multi-layer architecture with AI agents and cloud-native deployment, traceability ensures that changes can be audited, debugged, and validated across all tiers including infrastructure.

### III. Security by Design

JWT-based authentication MUST be enforced using Better Auth for all protected operations.

- All API requests (except auth endpoints) MUST include `Authorization: Bearer <token>` header
- Backend MUST verify JWT tokens using `BETTER_AUTH_SECRET` environment variable
- Tokens MUST be validated on every request before processing
- Authentication failures MUST return HTTP 401 status code
- Invalid or expired tokens MUST be rejected with clear error messages
- AI agents MUST operate within authenticated user context only
- MCP tools MUST enforce user-scoped access to tasks
- Kubernetes secrets MUST be used for sensitive configuration
- Container images MUST NOT contain hardcoded secrets

**Rationale**: A multi-user AI-powered application requires robust authentication; AI agents must never access data outside user scope; cloud-native deployments require secure secret management.

### IV. Separation of Concerns

Frontend (Next.js), Backend (FastAPI), Database (Neon PostgreSQL), AI Agent Layer, MCP Tools, Infrastructure, and Specs MUST be clearly separated.

- Frontend MUST only contain UI logic, state management, and API client code
- Backend MUST only contain business logic, data access, API endpoints, and agent orchestration
- AI Agent Layer MUST only contain agent behavior, tool invocation, and conversation management
- MCP Tools MUST only contain stateless task operations with database persistence
- Infrastructure MUST only contain deployment configurations, Helm charts, and Kubernetes manifests
- Database migrations MUST be version-controlled and separate from application code
- Specs MUST be organized by domain: features/, api/, database/, ui/, mcp/, agent/, deployment/
- Cross-cutting concerns MUST be documented in shared contracts

**Rationale**: Clear separation enables independent development, testing, and deployment of each tier, including infrastructure as a distinct concern.

### V. Scalability Ready

Monorepo architecture MUST support current Phase IV (Kubernetes Deployment) and future Phases (Dapr, Kafka, Service Mesh).

- Project structure MUST follow the mandatory monorepo layout
- Dependencies MUST be isolated to their respective packages (frontend, backend, deployment)
- Environment configuration MUST use environment variables, not hardcoded values
- API contracts MUST be versioned and backward-compatible where possible
- Database schema MUST support future extensions without breaking changes
- AI agent architecture MUST be stateless and horizontally scalable
- Kubernetes deployments MUST support horizontal pod autoscaling
- Helm charts MUST be parameterized for different environments

**Rationale**: Phase IV establishes cloud-native deployment; architectural decisions now enable future service mesh, event-driven architectures, and multi-cloud deployments.

### VI. Stateless Architecture

Backend MUST hold no conversation state in memory; all state MUST be persisted in database.

- Conversation history MUST be stored in Conversation and Message tables
- Any server instance MUST be able to handle any request without in-memory session state
- Agent context MUST be reconstructed from database on each request
- Server restarts MUST NOT lose conversation continuity
- Horizontal scaling MUST be possible without sticky sessions
- Kubernetes pods MUST be ephemeral and replaceable without data loss

**Rationale**: Stateless architecture is essential for cloud deployment, horizontal scaling, and resilience in Kubernetes environments.

### VII. AI-First Interaction

Users MUST manage todos via natural language; AI agent MUST map commands to MCP tools.

- Primary user interface is conversational chat, not traditional CRUD forms
- AI agent MUST interpret user intent and invoke appropriate MCP tools
- OpenRouter (not OpenAI API) MUST be used as the AI model provider
- Agent behavior MUST be specified in agent behavior specifications
- Agent responses MUST be friendly, confirmatory, and handle errors gracefully
- Traditional CRUD UI (Phase II) remains available as fallback

**Rationale**: AI-first interaction is the core value proposition of Phase III; natural language interface must be the primary interaction model.

### VIII. Standardized Tool Interface

MCP tools MUST define all task operations; AI agent MUST use only these tools.

- MCP tools MUST expose exactly: add_task, list_tasks, complete_task, delete_task, update_task
- All task operations MUST go through MCP tool interface (no direct database access from agent)
- MCP tools MUST be stateless; all state persisted in database
- MCP tools MUST enforce user-scoped access (filter by authenticated user_id)
- Tool schemas MUST be versioned and documented in specs/mcp/

**Rationale**: Standardized tool interface ensures consistent behavior, testability, and enables future tool extensions without agent logic changes.

### IX. Cloud-Native Infrastructure

All deployment artifacts MUST be containerized, orchestrated via Kubernetes, and managed through AI-assisted DevOps tools.

- Frontend and backend MUST be containerized separately with optimized Dockerfiles
- Containers MUST be deployable on Kubernetes (local Minikube and future cloud providers)
- Helm charts MUST define all Kubernetes resources (Deployments, Services, ConfigMaps, Secrets)
- Infrastructure as Code MUST be generated via AI agents (no manual YAML editing)
- AI DevOps tools (Gordon, kubectl-ai, Kagent) MUST be preferred over manual CLI commands
- Deployment specifications MUST be documented before implementation
- All infrastructure changes MUST be reproducible and explainable
- Local development MUST use Minikube; production-ready for cloud migration

**Rationale**: Phase IV establishes cloud-native deployment patterns; AI-assisted infrastructure generation ensures consistency, best practices, and prepares for future multi-cloud deployments.

## Key Standards

### Authentication

- Better Auth MUST issue JWT tokens upon successful authentication
- Frontend MUST attach `Authorization: Bearer <token>` header to every API call
- Backend MUST verify JWT using `BETTER_AUTH_SECRET` environment variable
- Token refresh and expiration MUST be handled gracefully
- AI agent requests MUST include user context derived from JWT
- Kubernetes secrets MUST store `BETTER_AUTH_SECRET` and `DATABASE_URL`

### User Isolation

- All tasks MUST be linked to a `user_id` foreign key
- API MUST only return tasks belonging to the authenticated user
- Users MUST NOT be able to access, modify, or delete other users' tasks
- Database queries MUST always include user scope filtering
- MCP tools MUST enforce user_id filtering on all operations
- AI agents MUST operate only within authenticated user's data scope

### REST API Conventions

- All routes MUST be under `/api/` prefix
- HTTP status codes MUST follow conventions:
  - 200: Successful GET, PUT, PATCH
  - 201: Successful POST (resource created)
  - 401: Unauthorized (missing or invalid token)
  - 404: Resource not found
  - 422: Validation error (invalid input)
- Error responses MUST include descriptive messages
- Chat endpoint: `POST /api/{user_id}/chat` with conversation_id (optional) and message (required)

### Database

- SQLModel ORM MUST be used for all database operations
- Neon PostgreSQL connection MUST use `DATABASE_URL` environment variable
- Migrations MUST be version-controlled and reversible
- Schema changes MUST be documented in specs/database/
- Database models MUST include:
  - Task: user_id, id, title, description, completed, created_at, updated_at
  - Conversation: user_id, id, created_at, updated_at
  - Message: user_id, id, conversation_id, role (user/assistant), content, created_at

### Conversation Management

- All conversation history MUST be persisted in database
- Conversation state MUST be reconstructable from database on any server instance
- Messages MUST be stored with role (user/assistant), content, and timestamps
- Conversations MUST be user-scoped (filter by user_id)
- Backend MUST NOT hold conversation state in memory
- Server restarts MUST NOT lose conversation continuity

### MCP Tools

- MCP server MUST use Official MCP SDK
- Tools MUST be stateless; all state in database
- Tool operations MUST be atomic and idempotent where possible
- Tools MUST expose exactly these operations:
  - add_task: Create new task for user
  - list_tasks: Retrieve user's tasks (with optional filters)
  - complete_task: Mark task as completed
  - delete_task: Remove task
  - update_task: Modify task title/description
- All tools MUST enforce user_id scoping
- Tool schemas MUST be documented in specs/mcp/

### Natural Language Commands

- AI agent MUST map user natural language to MCP tool invocations
- Agent behavior MUST be specified in specs/agent/
- Agent MUST confirm actions before execution where appropriate
- Agent MUST handle errors gracefully with user-friendly messages
- Agent MUST provide context-aware responses
- Agent responses MUST reference specific tasks by title or ID when relevant

### Deployment Standards

- All deployment artifacts MUST be version-controlled in `deployment/` directory
- Helm charts MUST be the primary deployment mechanism
- Kubernetes manifests MUST be generated via Helm templates (no raw YAML)
- Environment-specific values MUST be externalized in `values.yaml` files
- Deployment specifications MUST be documented in `specs/004-k8s-deployment/`

### AI-Assisted DevOps

- Docker AI Agent (Gordon) MUST be used for Dockerfile generation and optimization
- kubectl-ai MUST be used for Kubernetes operations (deployments, scaling, debugging)
- Kagent MUST be used for cluster health analysis and resource optimization
- If AI tools unavailable, Claude Code MUST generate equivalent CLI commands
- All AI-generated commands MUST be documented and reproducible
- Manual infrastructure edits are prohibited; regenerate via AI agents

### Container Standards

- Frontend and backend MUST have separate container images
- Dockerfiles MUST use multi-stage builds for optimization
- Base images MUST be official and minimal (e.g., node:alpine, python:slim)
- Container images MUST NOT contain secrets or sensitive data
- Images MUST be tagged with semantic versions
- Health checks MUST be defined in Dockerfiles
- Non-root users MUST be used for running containers

### Helm Chart Standards

- Helm charts MUST define:
  - Deployments (with replica counts, resource limits, health checks)
  - Services (ClusterIP for backend, NodePort/LoadBalancer for frontend)
  - ConfigMaps (for non-sensitive configuration)
  - Secrets (for sensitive data like DATABASE_URL, BETTER_AUTH_SECRET)
  - Ingress (optional, for production)
- Values.yaml MUST support:
  - Replica counts (default: 2 for backend, 1 for frontend)
  - Image tags (default: latest)
  - Resource limits (CPU, memory)
  - Environment variables
- Charts MUST be reusable across environments (dev, staging, prod)
- Chart versions MUST follow semantic versioning

## Mandatory Monorepo Structure

```
hackathon-todo/
├── .specify/
│   ├── memory/constitution.md
│   ├── templates/
│   └── scripts/
├── specs/
│   ├── 001-todo-console-app/      # Phase I (legacy)
│   ├── 002-fullstack-web-app/     # Phase II
│   ├── 003-ai-chatbot/            # Phase III
│   ├── 004-k8s-deployment/        # Phase IV (NEW)
│   │   ├── overview.md
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── docker/                # Dockerfile specs
│   │   ├── helm/                  # Helm chart specs
│   │   └── verification/          # Deployment verification specs
│   └── ...
├── deployment/                     # Deployment artifacts (NEW)
│   ├── CLAUDE.md                   # Deployment guidance
│   ├── docker/
│   │   ├── frontend.Dockerfile
│   │   └── backend.Dockerfile
│   ├── helm/
│   │   └── todo-chatbot/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── values-dev.yaml
│   │       ├── values-prod.yaml
│   │       └── templates/
│   │           ├── frontend-deployment.yaml
│   │           ├── frontend-service.yaml
│   │           ├── backend-deployment.yaml
│   │           ├── backend-service.yaml
│   │           ├── configmap.yaml
│   │           ├── secrets.yaml
│   │           └── ingress.yaml
│   └── k8s/                        # Raw manifests (if needed)
├── CLAUDE.md                       # Root project guidance
├── frontend/
│   ├── CLAUDE.md                   # Frontend-specific guidance
│   ├── src/
│   │   ├── components/
│   │   │   └── chat/              # ChatKit integration
│   │   ├── pages/
│   │   └── services/
│   └── ...
├── backend/
│   ├── CLAUDE.md                   # Backend-specific guidance
│   ├── src/
│   │   ├── models/                # Task, Conversation, Message
│   │   ├── services/
│   │   ├── api/
│   │   ├── agent/                 # Agent orchestration
│   │   └── mcp/                   # MCP server
│   └── ...
├── docker-compose.yml
└── README.md
```

## Technology Constraints

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend | Next.js | 16+ with App Router, TypeScript, Tailwind CSS |
| Frontend Chat UI | OpenAI ChatKit | Using OpenRouter as model provider |
| Backend | FastAPI | With SQLModel ORM |
| Backend Agent | OpenAI Agents SDK | Agent orchestration and tool invocation |
| Backend Tools | Official MCP SDK | Stateless tool interface |
| Database | Neon PostgreSQL | Serverless, connection via DATABASE_URL |
| Auth | Better Auth | JWT tokens, shared BETTER_AUTH_SECRET |
| AI Model Provider | OpenRouter | NOT OpenAI API - use NEXT_PUBLIC_OPENROUTER_KEY |
| Container Runtime | Docker Desktop | Local development and image building |
| Orchestration | Kubernetes | Minikube for local, cloud-ready for production |
| Package Manager | Helm | Version 3+ for Kubernetes deployments |
| AI DevOps Tools | Gordon, kubectl-ai, Kagent | AI-assisted infrastructure operations |
| Specs | Spec-Kit Plus | All features, APIs, DB, MCP tools, agent behavior, infrastructure documented |

## Success Criteria

Measurable outcomes that define project completion:

### Phase II Criteria (Still Required)

- **SC-001**: Logged-in user can sign up, sign in, and manage only their own tasks
- **SC-002**: Backend rejects unauthenticated requests with HTTP 401
- **SC-003**: JWT token is required for every API call (except auth endpoints)
- **SC-004**: Repository contains organized Spec-Kit specs with full traceability
- **SC-005**: Layered CLAUDE.md files exist for root, frontend/, backend/, and deployment/
- **SC-006**: Working Next.js frontend with authentication UI
- **SC-007**: Working FastAPI backend with JWT validation
- **SC-008**: Neon PostgreSQL integration with user-scoped task storage
- **SC-009**: Architecture is ready to extend into future phases

### Phase III Criteria (Still Required)

- **SC-010**: User can interact with chatbot via natural language to add, view, update, delete, and complete tasks
- **SC-011**: AI agent correctly invokes MCP tools based on user intent
- **SC-012**: Backend persists conversation and message history in database
- **SC-013**: Server is stateless; conversation resumes seamlessly after restarts
- **SC-014**: MCP tools enforce user-scoped access; users cannot access other users' tasks via chatbot
- **SC-015**: ChatKit frontend connects to backend `/api/{user_id}/chat` endpoint using OpenRouter

### Phase IV Criteria (New)

- **SC-016**: Frontend and backend are containerized with optimized Dockerfiles generated via AI agents
- **SC-017**: Helm chart deploys both frontend and backend to Minikube successfully
- **SC-018**: Kubernetes pods are running and healthy (verified via kubectl-ai or Kagent)
- **SC-019**: Frontend is accessible via Minikube service or ingress
- **SC-020**: Backend API responds correctly and AI chatbot works end-to-end in Kubernetes
- **SC-021**: Horizontal scaling works (replica count can be changed via Helm values)
- **SC-022**: All deployment artifacts are AI-generated with no manual edits
- **SC-023**: Deployment is reproducible from specifications and AI commands

## Development Workflow

The following workflow MUST be followed for all feature development:

1. **Specify**: Define feature requirements in spec.md before any implementation
2. **Plan**: Create implementation plan documenting technical approach for all layers (including infrastructure)
3. **Generate**: Use Claude Code to generate all implementation code (frontend, backend, database, MCP tools, agent behavior, infrastructure)
4. **Validate**: Verify generated code meets specification requirements across all tiers
5. **Document**: Record all significant decisions and prompt history

**Prohibited Actions**:
- Manual code edits outside of generated output
- Implementation without prior specification
- Skipping validation against acceptance criteria
- Hardcoding secrets or configuration values
- Bypassing authentication for protected endpoints
- Direct database access from AI agent (must use MCP tools)
- Using OpenAI API key instead of OpenRouter key
- Storing conversation state in memory (must persist in database)
- Manual editing of Dockerfiles, Helm charts, or Kubernetes manifests (must regenerate via AI)
- Committing secrets to version control

## Governance

This constitution supersedes all other practices for the Evolution of Todo project.

**Amendment Process**:
1. Proposed changes MUST be documented with rationale
2. Changes MUST be reviewed for impact on existing specifications
3. Version MUST be incremented according to semantic versioning:
   - MAJOR: Principle removals or incompatible redefinitions
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording, or non-semantic refinements

**Compliance**:
- All specifications MUST reference applicable principles
- All PRs/reviews MUST verify compliance with this constitution
- Security additions MUST be justified against Security by Design principle
- Architectural changes MUST be justified against Scalability Ready and Stateless Architecture principles
- AI agent behavior MUST be justified against AI-First Interaction and Standardized Tool Interface principles
- Infrastructure changes MUST be justified against Cloud-Native Infrastructure principle

**Version**: 2.2.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-02-09
