# Backend CLAUDE.md - FastAPI Application

## Overview

FastAPI backend with SQLModel ORM for Phase II todo application.

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI app entry
│   ├── core/
│   │   ├── config.py           # Environment config
│   │   ├── database.py         # Database connection
│   │   ├── security.py         # Password hashing, JWT
│   │   └── dependencies.py     # DI (current_user, db)
│   ├── models/
│   │   ├── user.py             # User SQLModel
│   │   └── task.py             # Task SQLModel
│   ├── schemas/
│   │   ├── auth.py             # Auth request/response
│   │   ├── task.py             # Task request/response
│   │   └── error.py            # Error response
│   ├── api/
│   │   ├── router.py           # Main router
│   │   ├── auth.py             # Auth endpoints
│   │   └── tasks.py            # Task endpoints
│   ├── services/
│   │   ├── auth.py             # Auth business logic
│   │   └── task.py             # Task business logic
│   └── db/
│       └── migrate.py          # Migration runner
└── tests/
```

## Key Specifications

- **Database Schema**: `@specs/database/schema.md`
- **REST Endpoints**: `@specs/api/rest-endpoints.md`
- **JWT Flow**: `@specs/api/jwt-auth.md`
- **API Contract**: `@specs/contracts/api-contract.md`

## Implementation Rules

### Authentication
- Hash passwords with bcrypt
- Sign JWTs with HS256 using `BETTER_AUTH_SECRET`
- Token claims: `sub` (user_id), `email`, `iat`, `exp`
- 24-hour token expiration

### User Isolation
- ALL task queries MUST filter by `user_id`
- Return 404 for tasks not owned by user (not 403)
- Extract user_id from JWT in middleware

### Error Handling
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [{"field": "name", "message": "error"}]
  }
}
```

### Status Codes
- 200: Successful GET, PUT, PATCH, DELETE
- 201: Successful POST (resource created)
- 401: Authentication required/failed
- 404: Resource not found
- 409: Conflict (duplicate email)
- 422: Validation error

## Database Models

### User
- `id`: UUID (PK)
- `email`: str (unique)
- `password_hash`: str
- `created_at`: datetime

### Task
- `id`: UUID (PK)
- `user_id`: UUID (FK → users.id)
- `title`: str (max 100)
- `description`: str (max 500, nullable)
- `completed`: bool (default false)
- `created_at`, `updated_at`: datetime

## Environment Variables

```env
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=<32+ character secret>
```

## Testing

- pytest for all tests
- TestClient for API tests
- Test user isolation explicitly
