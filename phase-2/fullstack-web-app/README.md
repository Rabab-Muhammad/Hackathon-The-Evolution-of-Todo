# Phase 2: Full-Stack Web Application

This is the Phase 2 implementation of the Todo application as part of the Evolution of Todo project. This is a full-stack web application built with Next.js frontend and FastAPI backend with PostgreSQL database.

## Architecture

The application follows a modern full-stack architecture:
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon recommended)
- **Authentication**: Better Auth with JWT tokens

## Features

- Multi-user support with authentication
- Persistent storage with PostgreSQL
- Full CRUD operations for tasks
- Responsive web interface
- JWT-based authentication
- User isolation (users only see their own tasks)

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+, TypeScript, Tailwind CSS |
| Backend | FastAPI, SQLModel, Python 3.11+ |
| Database | PostgreSQL (Neon) |
| Auth | Better Auth, JWT (HS256) |
| Deployment | Docker, Railway/Vercel |

## Project Structure

```
fullstack-web-app/
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and API clients
│   │   └── ...
│   ├── package.json
│   └── ...
├── backend/                # FastAPI application
│   ├── src/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── ...
│   ├── requirements.txt
│   └── ...
├── specs/                  # Feature specifications
│   └── 002-fullstack-web-app/
├── docker-compose.yml      # Docker configuration
└── README.md              # This file
```

## Running the Application

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or Docker for containerized setup)
- pnpm (recommended) or npm

### Option 1: Docker (Recommended)

```bash
# Create environment files
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

This represents the Phase 2 evolution of the Todo application from a console application to a full-stack web application with persistent storage and multi-user support.