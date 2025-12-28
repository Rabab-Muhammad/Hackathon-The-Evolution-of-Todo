# Architecture Specification: Phase II Full-Stack Application

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the high-level system architecture for the Phase II full-stack web application, establishing clear boundaries between frontend, backend, and database layers to support multi-user task management with secure authentication.

## System Overview

The application follows a three-tier architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Next.js Frontend                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │  │
│  │  │   Pages     │  │ Components  │  │   Auth Client   │    │  │
│  │  │ (App Router)│  │  (React)    │  │  (Better Auth)  │    │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS (JWT in Authorization header)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Service Layer                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Backend                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │  │
│  │  │ API Routes  │  │   Services  │  │  JWT Validator  │    │  │
│  │  │  (/api/*)   │  │   (CRUD)    │  │ (BETTER_AUTH_   │    │  │
│  │  │             │  │             │  │     SECRET)     │    │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL (SQLModel ORM)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Data Layer                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               Neon PostgreSQL (Serverless)                 │  │
│  │  ┌─────────────┐  ┌─────────────────────────────────────┐ │  │
│  │  │    Users    │  │              Tasks                   │ │  │
│  │  │   Table     │──│  (user_id foreign key)               │ │  │
│  │  └─────────────┘  └─────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### Client Layer (Frontend)

| Component | Responsibility |
|-----------|----------------|
| Pages | Route handling, page composition, data fetching |
| Components | Reusable UI elements, user interaction handling |
| Auth Client | Token management, authentication state, session handling |

**Constraints**:
- MUST NOT contain business logic
- MUST NOT directly access database
- MUST attach JWT token to all API requests
- MUST handle authentication redirects

### Service Layer (Backend)

| Component | Responsibility |
|-----------|----------------|
| API Routes | HTTP endpoint handling, request/response formatting |
| Services | Business logic, data validation, CRUD operations |
| JWT Validator | Token verification, user context extraction |

**Constraints**:
- MUST verify JWT on every protected request
- MUST enforce user isolation (only return user's own data)
- MUST return appropriate HTTP status codes
- MUST NOT expose internal implementation details in errors

### Data Layer (Database)

| Component | Responsibility |
|-----------|----------------|
| Users Table | User account storage and authentication data |
| Tasks Table | Task data with user ownership |

**Constraints**:
- MUST use foreign key relationships for data integrity
- MUST support concurrent access from multiple users
- MUST be accessible only through the Service Layer

## Data Flow

### Authentication Flow

```
1. User submits credentials (email/password) via Login page
2. Frontend sends credentials to Backend auth endpoint
3. Backend validates credentials against database
4. Backend issues JWT token (signed with BETTER_AUTH_SECRET)
5. Frontend stores token and includes in subsequent requests
6. Backend validates token on each protected request
7. Backend extracts user_id from token for data scoping
```

### Task Operation Flow

```
1. User performs action in UI (create/read/update/delete)
2. Frontend sends request with JWT in Authorization header
3. Backend validates JWT token
4. Backend extracts user_id from validated token
5. Backend performs database operation scoped to user_id
6. Backend returns result with appropriate status code
7. Frontend updates UI based on response
```

## Security Boundaries

| Boundary | Protection |
|----------|------------|
| Frontend ↔ Backend | JWT token validation on every request |
| Backend ↔ Database | User scoping in all queries |
| User ↔ User | Complete data isolation via user_id filtering |

## Integration Points

### Environment Variables

| Variable | Layer | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | Backend | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Both | JWT signing/verification key |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL |

### API Contract

- All API endpoints under `/api/` prefix
- Protected endpoints require `Authorization: Bearer <token>` header
- Responses use standard HTTP status codes (200, 201, 401, 404, 422)
- Error responses include descriptive messages

## Scalability Considerations

- Stateless backend allows horizontal scaling
- Database connection pooling for concurrent requests
- JWT tokens eliminate server-side session storage
- Serverless PostgreSQL auto-scales with demand

## Phase III Readiness

The architecture supports future AI integration by:
- Clear API boundaries for new endpoints
- User context available in all requests
- Database schema extensible for AI-related data
- Service layer pattern allows new service injection
