<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 2.0.0 → 2.0.1

  Status: Validation pass - confirmed alignment with Phase II requirements

  Validated principles (all 5 required by user):
    - I. Spec-Driven Development: ✅ Aligned
    - II. End-to-End Traceability: ✅ Aligned
    - III. Security by Design (JWT/Better Auth): ✅ Aligned
    - IV. Separation of Concerns: ✅ Aligned
    - V. Scalability Ready: ✅ Aligned

  Key Standards validated:
    - Authentication (Better Auth, JWT): ✅ Present
    - User Isolation (user_id scoping): ✅ Present
    - REST API Conventions (/api/, status codes): ✅ Present
    - Database (SQLModel, Neon PostgreSQL): ✅ Present

  Mandatory Monorepo Structure: ✅ Matches user specification exactly

  Technology Constraints: ✅ All technologies documented
    - Next.js 16+ (App Router, TypeScript, Tailwind)
    - FastAPI + SQLModel
    - Neon Serverless PostgreSQL
    - Better Auth with JWT

  Templates validation:
    - .specify/templates/plan-template.md: ✅ Compatible (Constitution Check is dynamic, web app structure supported)
    - .specify/templates/spec-template.md: ✅ Compatible (requirements/scenarios align with principles)
    - .specify/templates/tasks-template.md: ✅ Compatible (web app structure already supported)

  Follow-up TODOs:
    - Create layered CLAUDE.md files for frontend/ and backend/ during implementation
-->

# Evolution of Todo – Phase II Constitution

## Core Principles

### I. Spec-Driven Development

All features MUST be defined in Spec-Kit Plus spec files before implementation.

- No manual coding is permitted; all implementation code MUST be generated from specifications
- Each feature, API endpoint, database schema, and UI component requires a complete spec before implementation
- Specifications serve as the single source of truth for all behavior across frontend, backend, and database
- Changes to behavior MUST first be reflected in updated specifications

**Rationale**: Ensures traceability, consistency, and that all code across the full stack derives from explicit, documented requirements.

### II. End-to-End Traceability

Every frontend, backend, API, database, and auth change MUST be traceable to a spec file.

- Each UI component MUST reference its spec in `specs/ui/`
- Each API endpoint MUST reference its spec in `specs/api/`
- Each database entity MUST reference its spec in `specs/database/`
- Each feature MUST reference its spec in `specs/features/`
- All PRs MUST include references to the specs that define the changes

**Rationale**: In a multi-layer architecture, traceability ensures that changes can be audited, debugged, and validated across all tiers.

### III. Security by Design

JWT-based authentication MUST be enforced using Better Auth for all protected operations.

- All API requests (except auth endpoints) MUST include `Authorization: Bearer <token>` header
- Backend MUST verify JWT tokens using `BETTER_AUTH_SECRET` environment variable
- Tokens MUST be validated on every request before processing
- Authentication failures MUST return HTTP 401 status code
- Invalid or expired tokens MUST be rejected with clear error messages

**Rationale**: A multi-user application requires robust authentication; security cannot be an afterthought.

### IV. Separation of Concerns

Frontend (Next.js), Backend (FastAPI), Database (Neon PostgreSQL), and Specs MUST be clearly separated.

- Frontend MUST only contain UI logic, state management, and API client code
- Backend MUST only contain business logic, data access, and API endpoints
- Database migrations MUST be version-controlled and separate from application code
- Specs MUST be organized by domain: features/, api/, database/, ui/
- Cross-cutting concerns MUST be documented in shared contracts

**Rationale**: Clear separation enables independent development, testing, and deployment of each tier, supporting team scalability.

### V. Scalability Ready

Monorepo architecture MUST support future Phases (AI Chatbot, Kubernetes, Dapr, Kafka).

- Project structure MUST follow the mandatory monorepo layout
- Dependencies MUST be isolated to their respective packages (frontend, backend)
- Environment configuration MUST use environment variables, not hardcoded values
- API contracts MUST be versioned and backward-compatible where possible
- Database schema MUST support future extensions without breaking changes

**Rationale**: Phase II establishes the foundation for Phase III (AI Chatbot) and beyond; architectural decisions now prevent costly refactoring later.

## Key Standards

### Authentication

- Better Auth MUST issue JWT tokens upon successful authentication
- Frontend MUST attach `Authorization: Bearer <token>` header to every API call
- Backend MUST verify JWT using `BETTER_AUTH_SECRET` environment variable
- Token refresh and expiration MUST be handled gracefully

### User Isolation

- All tasks MUST be linked to a `user_id` foreign key
- API MUST only return tasks belonging to the authenticated user
- Users MUST NOT be able to access, modify, or delete other users' tasks
- Database queries MUST always include user scope filtering

### REST API Conventions

- All routes MUST be under `/api/` prefix
- HTTP status codes MUST follow conventions:
  - 200: Successful GET, PUT, PATCH
  - 201: Successful POST (resource created)
  - 401: Unauthorized (missing or invalid token)
  - 404: Resource not found
  - 422: Validation error (invalid input)
- Error responses MUST include descriptive messages

### Database

- SQLModel ORM MUST be used for all database operations
- Neon PostgreSQL connection MUST use `DATABASE_URL` environment variable
- Migrations MUST be version-controlled and reversible
- Schema changes MUST be documented in specs/database/

## Mandatory Monorepo Structure

```
hackathon-todo/
├── .spec-kit/config.yaml
├── specs/
│   ├── overview.md
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
├── CLAUDE.md
├── frontend/
│   └── CLAUDE.md
├── backend/
│   └── CLAUDE.md
├── docker-compose.yml
└── README.md
```

## Technology Constraints

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend | Next.js | 16+ with App Router, TypeScript, Tailwind CSS |
| Backend | FastAPI | With SQLModel ORM |
| Database | Neon PostgreSQL | Serverless, connection via DATABASE_URL |
| Auth | Better Auth | JWT tokens, shared BETTER_AUTH_SECRET |
| Specs | Spec-Kit Plus | All features, APIs, DB changes documented |

## Success Criteria

Measurable outcomes that define Phase II completion:

- **SC-001**: Logged-in user can sign up, sign in, and manage only their own tasks
- **SC-002**: Backend rejects unauthenticated requests with HTTP 401
- **SC-003**: JWT token is required for every API call (except auth endpoints)
- **SC-004**: Repository contains organized Spec-Kit specs with full traceability
- **SC-005**: Layered CLAUDE.md files exist for root, frontend/, and backend/
- **SC-006**: Working Next.js frontend with authentication UI
- **SC-007**: Working FastAPI backend with JWT validation
- **SC-008**: Neon PostgreSQL integration with user-scoped task storage
- **SC-009**: Phase II output is architecturally ready to extend into Phase III AI Chatbot

## Development Workflow

The following workflow MUST be followed for all feature development:

1. **Specify**: Define feature requirements in spec.md before any implementation
2. **Plan**: Create implementation plan documenting technical approach for all layers
3. **Generate**: Use Claude Code to generate all implementation code (frontend, backend, database)
4. **Validate**: Verify generated code meets specification requirements across all tiers
5. **Document**: Record all significant decisions and prompt history

**Prohibited Actions**:
- Manual code edits outside of generated output
- Implementation without prior specification
- Skipping validation against acceptance criteria
- Hardcoding secrets or configuration values
- Bypassing authentication for protected endpoints

## Governance

This constitution supersedes all other practices for the Evolution of Todo – Phase II project.

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
- Architectural changes MUST be justified against Scalability Ready principle

**Version**: 2.0.1 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-28
