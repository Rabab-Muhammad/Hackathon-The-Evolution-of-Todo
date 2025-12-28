# Research: Phase II Full-Stack Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-28 | **Spec**: [overview.md](./overview.md)

## Purpose

Document technology decisions and best practices research for Phase II implementation.

## Technology Stack Decisions

### Frontend: Next.js 16+ with App Router

**Decision**: Use Next.js 16+ with App Router, TypeScript, and Tailwind CSS

**Rationale**:
- Constitution mandates Next.js 16+ with App Router (@constitution, Technology Constraints)
- App Router provides server components, layouts, and improved data fetching
- TypeScript ensures type safety across frontend codebase
- Tailwind CSS enables rapid, consistent styling

**Alternatives Considered**:
- React + Vite: Rejected - Constitution requires Next.js
- Next.js Pages Router: Rejected - App Router is the modern standard

**Best Practices**:
- Use server components by default, client components only when needed
- Implement route groups for authentication layout separation
- Use middleware for route protection
- Store JWT in localStorage with HTTP-only cookie fallback

---

### Backend: FastAPI with SQLModel

**Decision**: Use FastAPI with SQLModel ORM for all backend services

**Rationale**:
- Constitution mandates FastAPI + SQLModel (@constitution, Technology Constraints)
- FastAPI provides automatic OpenAPI documentation
- SQLModel combines SQLAlchemy with Pydantic for type-safe database operations
- Async support enables efficient request handling

**Alternatives Considered**:
- Django + DRF: Rejected - Constitution requires FastAPI
- Flask: Rejected - Less modern, no built-in async support

**Best Practices**:
- Use dependency injection for database sessions
- Implement request validation with Pydantic models
- Create separate routers for auth and tasks domains
- Use middleware for JWT validation

---

### Database: Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL via `DATABASE_URL`

**Rationale**:
- Constitution mandates Neon PostgreSQL (@constitution, Technology Constraints)
- Serverless architecture matches application scalability needs
- PostgreSQL provides robust UUID and timestamp support
- Connection pooling handled by Neon

**Alternatives Considered**:
- Supabase: Rejected - Constitution requires Neon
- Local PostgreSQL: Development only, Neon for production

**Best Practices**:
- Use UUID primary keys for distributed ID generation
- Enable `uuid-ossp` extension for UUID generation
- Create indexes for foreign key columns and common queries
- Use cascading deletes for user-task relationship

---

### Authentication: Better Auth with JWT

**Decision**: Use Better Auth for JWT-based authentication

**Rationale**:
- Constitution mandates Better Auth with JWT (@constitution, Key Standards)
- JWT enables stateless authentication
- Shared `BETTER_AUTH_SECRET` allows cross-service token validation

**Alternatives Considered**:
- NextAuth.js: Could be used alongside Better Auth for frontend
- Custom JWT implementation: More complex, less secure

**Best Practices**:
- Sign tokens with HS256 algorithm using `BETTER_AUTH_SECRET`
- Set 24-hour token expiration (@specs/api/jwt-auth.md, FR-JWT-004)
- Include `sub` (user_id), `email`, `iat`, `exp` claims
- Validate tokens on every protected request
- Return 401 for all authentication failures

---

## Architecture Decisions

### Monorepo Structure

**Decision**: Follow mandatory monorepo structure from Constitution

```
hackathon-todo/
├── .specify/                    # Spec-Kit Plus configuration
├── specs/002-fullstack-web-app/ # Feature specifications
├── CLAUDE.md                    # Root project instructions
├── frontend/
│   ├── CLAUDE.md               # Frontend-specific instructions
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   ├── components/         # React components
│   │   └── lib/                # Utilities, API client
│   └── package.json
├── backend/
│   ├── CLAUDE.md               # Backend-specific instructions
│   ├── src/
│   │   ├── api/                # FastAPI routers
│   │   ├── models/             # SQLModel entities
│   │   ├── services/           # Business logic
│   │   └── core/               # Config, dependencies
│   └── pyproject.toml
├── docker-compose.yml
└── README.md
```

**Rationale**:
- Constitution mandates this structure (@constitution, Mandatory Monorepo Structure)
- Clear separation between frontend, backend, and specs
- Layered CLAUDE.md files enable context-specific AI guidance

---

### API Design Pattern

**Decision**: RESTful API with resource-based endpoints

**Endpoints** (from @specs/api/rest-endpoints.md):

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/auth/signup | No | User registration |
| POST | /api/auth/signin | No | User authentication |
| POST | /api/auth/signout | Yes | End session |
| GET | /api/tasks | Yes | List user tasks |
| POST | /api/tasks | Yes | Create task |
| GET | /api/tasks/{id} | Yes | Get single task |
| PUT | /api/tasks/{id} | Yes | Update task |
| DELETE | /api/tasks/{id} | Yes | Delete task |
| PATCH | /api/tasks/{id}/toggle | Yes | Toggle completion |

**Rationale**:
- RESTful design aligns with Constitution's REST API Conventions
- Resource-based URLs are intuitive and standard
- HTTP methods match CRUD operations semantically

---

### User Isolation Strategy

**Decision**: Filter all database queries by `user_id` from JWT claims

**Implementation Approach**:
1. JWT middleware extracts `user_id` from token
2. Dependency injection provides `current_user` to route handlers
3. All task queries include `WHERE user_id = :current_user_id`
4. Task ownership verified before update/delete operations

**Rationale**:
- Constitution requires user isolation (@constitution, Key Standards - User Isolation)
- Prevents data leakage between users
- Returns 404 (not 403) to hide task existence from other users

---

### Error Handling Strategy

**Decision**: Consistent error response format across all endpoints

**Error Response Format** (from @specs/api/rest-endpoints.md):
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [{"field": "name", "message": "specific error"}]
  }
}
```

**HTTP Status Code Mapping**:
- 200: Successful GET, PUT, PATCH
- 201: Successful POST (resource created)
- 401: Authentication required/failed
- 404: Resource not found
- 409: Conflict (duplicate email)
- 422: Validation error
- 500: Internal server error

**Rationale**:
- Consistent format enables frontend error parsing
- Field-level details support form validation display
- Generic auth errors prevent information leakage

---

## Security Decisions

### Password Hashing

**Decision**: Use bcrypt for password hashing

**Rationale**:
- Industry standard for password storage
- Built-in salt generation prevents rainbow table attacks
- Configurable work factor for future security improvements

---

### JWT Token Storage

**Decision**: Store JWT in localStorage (primary), HTTP-only cookie (fallback)

**Rationale**:
- localStorage enables easy access for API requests
- HTTP-only cookie provides XSS protection when server supports it
- Token cleared on logout (@specs/api/jwt-auth.md, FR-JWT-009)

---

### Rate Limiting

**Decision**: Implement rate limiting on authentication endpoints

**Limits** (from @specs/api/rest-endpoints.md):
- Authentication endpoints: 5 requests per minute per IP
- Task endpoints: 100 requests per minute per user

**Rationale**:
- Prevents brute force attacks on login
- Protects against API abuse

---

## Performance Decisions

### Database Indexing

**Indexes** (from @specs/database/schema.md):
- `idx_users_email`: Unique index on users.email (login lookup)
- `idx_tasks_user_created`: Composite index on tasks(user_id, created_at DESC)

**Rationale**:
- Email index enables fast login lookups (<10ms)
- Composite index optimizes user task listing queries

---

### Frontend Data Fetching

**Decision**: Use client-side fetching with loading states

**Rationale**:
- Dashboard requires authentication, so server components limited
- Client-side fetching enables optimistic updates
- Loading states provide immediate feedback

---

## Dependencies Summary

### Frontend Dependencies

| Package | Purpose |
|---------|---------|
| next | Framework (16+) |
| react | UI library |
| typescript | Type safety |
| tailwindcss | Styling |
| better-auth | Authentication client |

### Backend Dependencies

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| sqlmodel | ORM |
| pyjwt | JWT handling |
| bcrypt | Password hashing |
| asyncpg | PostgreSQL driver |
| python-dotenv | Environment config |

---

## Open Questions Resolved

| Question | Resolution | Reference |
|----------|------------|-----------|
| Password hashing algorithm? | bcrypt | Industry standard |
| Token expiration? | 24 hours | @specs/api/jwt-auth.md FR-JWT-004 |
| Primary key type? | UUID | @specs/database/schema.md |
| API prefix? | /api/ | @constitution, REST API Conventions |
| Frontend framework? | Next.js 16+ | @constitution, Technology Constraints |

---

## Checklist

- [x] All technology choices aligned with Constitution
- [x] All architectural decisions justified by specs
- [x] No NEEDS CLARIFICATION markers remain
- [x] Security requirements documented
- [x] Performance considerations addressed
