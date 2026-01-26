# Evolution of Todo

A multi-phase todo application demonstrating evolution from console app to full-stack web application.

## Current Phase: II - Full-Stack Web Application

Full-stack multi-user todo application with Next.js frontend, FastAPI backend, and PostgreSQL database.

## Project Structure

```
hackathon-todo/
├── frontend/           # Next.js 16+ with App Router
├── backend/            # FastAPI with SQLModel
├── phase-1/            # Phase I console app
│   └── console-todo/   # Console-based todo application
├── phase-2/            # Phase II full-stack app
│   └── fullstack-web-app/ # Next.js + FastAPI + PostgreSQL
└── README.md           # This file
```

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (Neon recommended) or Docker

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Create environment file
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit .env files with your configuration

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET

# Run migrations
python -m src.db.migrate

# Start server
uvicorn src.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key
```

**Important**: `BETTER_AUTH_SECRET` must be identical in both files.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/signup | No | Register user |
| POST | /api/auth/signin | No | Login user |
| POST | /api/auth/signout | Yes | Logout user |
| GET | /api/tasks | Yes | List tasks |
| POST | /api/tasks | Yes | Create task |
| GET | /api/tasks/{id} | Yes | Get task |
| PUT | /api/tasks/{id} | Yes | Update task |
| DELETE | /api/tasks/{id} | Yes | Delete task |
| PATCH | /api/tasks/{id}/toggle | Yes | Toggle completion |

## Testing

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

## Verification Steps

1. **Health Check**: `curl http://localhost:8000/api/health`
2. **Register**: Navigate to `http://localhost:3000/signup`
3. **Login**: Navigate to `http://localhost:3000/login`
4. **Create Task**: Click "New Task" on dashboard
5. **User Isolation**: Create second account, verify separate task lists

## Specifications

See `specs/002-fullstack-web-app/` for complete specifications:
- `overview.md` - Project scope
- `plan.md` - Implementation plan
- `contracts/api-contract.md` - API specification

---

## Phase I Reference (Legacy)

Phase I implemented a console-based todo application with in-memory storage.

### Running Phase I

```bash
# Navigate to Phase I directory
cd phase-1/console-todo

# Using UV (Recommended)
uv run main.py

# Direct Python
python main.py
```

### Phase I Features

1. **Add Task** - Create tasks with title and optional description
2. **Delete Task** - Remove tasks by ID
3. **Update Task** - Modify task title and/or description
4. **View Tasks** - Display all tasks with status indicators
5. **Mark Complete/Incomplete** - Toggle task completion status

### Phase I Limitations

- Data stored in memory only (no persistence)
- Single user only
- No authentication

---

## License

MIT
