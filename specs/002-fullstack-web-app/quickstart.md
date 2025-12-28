# Quickstart Guide: Phase II Full-Stack Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-28

## Overview

This guide provides step-by-step instructions to set up and run the Phase II full-stack todo application locally.

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- Git
- A Neon PostgreSQL account (or local PostgreSQL for development)

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon-todo
git checkout 002-fullstack-web-app
```

### 2. Environment Variables

Create `.env` files for both frontend and backend:

**Backend (`backend/.env`)**:
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key
```

**Frontend (`frontend/.env.local`)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key
```

> **Important**: `BETTER_AUTH_SECRET` MUST be identical in both files for JWT validation to work.

### 3. Database Setup

**Option A: Neon PostgreSQL (Recommended)**
1. Create account at neon.tech
2. Create new project
3. Copy connection string to `DATABASE_URL`

**Option B: Local PostgreSQL**
1. Install PostgreSQL
2. Create database: `createdb hackathon_todo`
3. Set `DATABASE_URL=postgresql://localhost/hackathon_todo`

---

## Backend Setup

### 1. Navigate to Backend

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python -m src.db.migrate
```

### 5. Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

**Verify**: Visit `http://localhost:8000/docs` for API documentation.

---

## Frontend Setup

### 1. Navigate to Frontend

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

---

## Verification Steps

### 1. Health Check

**Backend**:
```bash
curl http://localhost:8000/api/health
# Expected: {"status": "ok"}
```

**Frontend**:
- Open `http://localhost:3000`
- Should see the landing page

### 2. User Registration

1. Navigate to `http://localhost:3000/signup`
2. Enter email and password (8+ characters)
3. Click "Sign Up"
4. Should redirect to dashboard

### 3. Task Operations

1. On dashboard, click "New Task"
2. Enter title: "Test Task"
3. Click "Save"
4. Task should appear in list
5. Click checkbox to mark complete
6. Click "Edit" to modify
7. Click "Delete" to remove

### 4. User Isolation Test

1. Log out
2. Create a new account with different email
3. Verify no tasks visible (empty dashboard)
4. Create a task
5. Log out and log back in with first account
6. Verify you only see first account's tasks

---

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Common Issues

### JWT Validation Fails (401 errors)

**Cause**: `BETTER_AUTH_SECRET` mismatch between frontend and backend

**Solution**: Ensure both `.env` files have identical `BETTER_AUTH_SECRET` values

### Database Connection Error

**Cause**: Invalid `DATABASE_URL` or database not running

**Solution**:
1. Verify PostgreSQL is running
2. Check connection string format
3. Ensure database exists

### CORS Errors

**Cause**: Frontend making requests to wrong backend URL

**Solution**: Verify `NEXT_PUBLIC_API_URL` points to correct backend address

### Port Already in Use

**Cause**: Another process using port 3000 or 8000

**Solution**:
```bash
# Find process
lsof -i :3000  # or :8000

# Kill process
kill -9 <PID>
```

---

## Development Workflow

### Daily Development

1. Start backend: `cd backend && uvicorn src.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Make changes - both servers auto-reload

### Before Committing

1. Run backend tests: `cd backend && pytest`
2. Run frontend tests: `cd frontend && npm test`
3. Verify lint passes: `npm run lint`

---

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Next Steps

After verifying the quickstart:

1. Review [api-contract.md](./contracts/api-contract.md) for API details
2. Review [data-model.md](./data-model.md) for entity definitions
3. Run `/sp.tasks` to generate implementation tasks

---

## Success Criteria Validation

| Criterion | Verification |
|-----------|--------------|
| SC-001: Registration < 2 min | Time the signup flow |
| SC-002: Login < 5 sec | Measure login to dashboard |
| SC-003: Task creation < 3 clicks | Count clicks to create task |
| SC-004: User isolation | Multi-account test above |
| SC-005: 401 on unauthorized | Test API without token |
| SC-006: Mobile usable | Resize browser to 320px |
| SC-007: Data persists | Refresh page after creating task |
