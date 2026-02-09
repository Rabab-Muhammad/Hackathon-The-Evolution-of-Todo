# Evolution of Todo

A multi-phase todo application demonstrating progressive evolution from console app to AI-powered chatbot, showcasing modern software development practices and architectural patterns.

---

## 📚 Project Evolution Overview

This project demonstrates the evolution of a simple todo application through three distinct phases, each building upon the previous one:

### **Phase I: Console Application** ✅ Complete
**Goal**: Basic task management via command-line interface

**Technology Stack**:
- Python 3.11+
- In-memory storage (dictionary)
- Console-based UI with colored output

**Key Features**:
- ✅ Add, view, update, delete, and complete tasks
- ✅ Sequential ID generation (never recycled)
- ✅ Input validation and error handling
- ✅ Modular architecture (models, services, CLI, validators)

**Limitations**:
- ❌ No data persistence (memory only)
- ❌ Single user only
- ❌ No authentication
- ❌ No network access

**Location**: `phase-1/console-todo/`

---

### **Phase II: Full-Stack Web Application** ✅ Complete
**Goal**: Multi-user web application with persistent storage

**Technology Stack**:
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel ORM
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: Better Auth with JWT (HS256)

**Key Features**:
- ✅ User authentication (signup, signin, signout)
- ✅ JWT-based authorization
- ✅ User isolation (each user sees only their tasks)
- ✅ RESTful API with OpenAPI documentation
- ✅ Persistent storage in PostgreSQL
- ✅ Responsive web UI
- ✅ Traditional CRUD operations

**Architecture**:
- Frontend: Next.js with App Router
- Backend: FastAPI with dependency injection
- Database: SQLModel with Neon PostgreSQL
- Auth: JWT tokens with 24-hour expiration

**API Endpoints**:
- `POST /api/auth/signup` - Register user
- `POST /api/auth/signin` - Login user
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion

**Location**: `phase-2/fullstack-web-app/` (archived)

**Active Implementation**: `frontend/` and `backend/` (root level)

---

### **Phase III: AI-Powered Chatbot** ✅ Complete
**Goal**: Natural language task management via AI chatbot

**Technology Stack**:
- **Frontend**: Next.js 16+, OpenAI ChatKit, TypeScript
- **Backend**: FastAPI, OpenAI Agents SDK, Official MCP SDK
- **AI Provider**: OpenRouter (OpenAI-compatible API)
- **Database**: Neon PostgreSQL (with conversation persistence)
- **Authentication**: Better Auth with JWT (inherited from Phase II)

**Key Features**:
- 🤖 **Natural Language Interface**: Manage tasks via conversational AI
- 💬 **ChatKit UI**: Modern chat interface with OpenAI ChatKit
- 🔧 **MCP Tools**: 5 standardized tools (add, list, update, delete, complete)
- 🧠 **AI Agent**: Intent recognition and tool orchestration
- 🔄 **Stateless Backend**: All conversation state in database
- 💾 **Conversation Persistence**: Full chat history stored
- 🔐 **User Isolation**: Enforced at all layers (DB, MCP, Agent, API)
- 📱 **Responsive Design**: Works on mobile and desktop

**Architecture Highlights**:

1. **Stateless Backend**
   - No in-memory conversation state
   - Context reconstructed from database on each request
   - Enables horizontal scaling without sticky sessions

2. **MCP (Model Context Protocol) Tools**
   - Standardized interface for task operations
   - User-scoped access enforcement
   - Stateless design with database persistence

3. **AI Agent Behavior**
   - Pattern-based intent recognition
   - Natural language processing (title extraction, task search)
   - Tool selection and chaining
   - User-friendly error handling

4. **Conversation Management**
   - Conversations stored in database
   - Messages linked to conversations
   - Support for multiple concurrent conversations
   - Conversation history retrieval

**Natural Language Examples**:
- "Add a task to buy groceries"
- "Show me my tasks"
- "Mark buy groceries as done"
- "Change buy groceries to buy groceries and milk"
- "Delete the grocery task"

**API Endpoints** (Phase III additions):
- `POST /api/{user_id}/chat` - Send chat message, get AI response

**Location**: `frontend/` and `backend/` (root level) + `specs/003-ai-chatbot/`

---

### **Phase IV: Cloud-Native Kubernetes Deployment** 🚀 Current Phase
**Goal**: Deploy AI-powered chatbot to local Kubernetes cluster (Minikube)

**Technology Stack**:
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (Minikube for local)
- **Package Manager**: Helm 3+
- **Base Images**: node:20-alpine (frontend), python:3.11-slim (backend)
- **Service Exposure**: NodePort (30080 frontend, 30081 backend)

**Key Features**:
- 🐳 **Multi-stage Docker Builds**: Optimized images (150-220MB)
- ☸️ **Helm Charts**: Parameterized Kubernetes deployment
- 🔧 **Configuration Management**: ConfigMaps and Secrets
- 📊 **Health Checks**: Liveness and readiness probes
- 🔄 **Horizontal Scaling**: Configurable replica counts
- 🔐 **Security**: Non-root containers, no hardcoded secrets
- 📦 **Stateless Architecture**: External database, ephemeral pods

**Architecture Highlights**:

1. **Container Images**
   - Frontend: Next.js standalone output (~150-200MB)
   - Backend: FastAPI with minimal dependencies (~180-220MB)
   - Non-root users (UID 1001) for security
   - Multi-stage builds for optimal size

2. **Kubernetes Resources**
   - Deployments: Frontend (1 replica), Backend (2 replicas)
   - Services: NodePort for local access
   - ConfigMaps: Non-sensitive configuration
   - Secrets: DATABASE_URL, BETTER_AUTH_SECRET, API keys

3. **Helm Chart Structure**
   - Single chart for both applications
   - Environment-specific values files (dev, prod)
   - Template helpers for consistency
   - Post-install instructions

4. **Deployment Scripts**
   - `build-images.sh`: Build container images
   - `deploy.sh`: Deploy to Minikube with Helm
   - `verify.sh`: Verify deployment health
   - `scale.sh`: Scale replicas dynamically

**Quick Start (Minikube)**:
```bash
# Prerequisites: Docker, Minikube, Helm, kubectl

# Start Minikube
minikube start --cpus=2 --memory=4096

# Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# Build images
cd deployment/scripts
./build-images.sh

# Create values-dev.yaml with your secrets
cp ../helm/todo-chatbot/values-dev.yaml.example ../helm/todo-chatbot/values-dev.yaml
# Edit values-dev.yaml with DATABASE_URL, BETTER_AUTH_SECRET, OPENROUTER_KEY

# Deploy to Minikube
./deploy.sh

# Verify deployment
./verify.sh

# Access application
# Frontend: http://localhost:30080
# Backend: http://localhost:30081
```

**Location**: `deployment/` + `specs/004-k8s-deployment/`

---

## 🎯 Current Phase: IV - Cloud-Native Kubernetes Deployment

AI-powered todo application with natural language interface using OpenAI ChatKit, OpenRouter, and MCP tools.

**Key Features:**
- 🤖 Natural language task management via AI chatbot
- 💬 Conversational interface with OpenAI ChatKit
- 🔧 MCP (Model Context Protocol) tools for standardized operations
- 🔄 Stateless backend architecture for horizontal scaling
- 💾 Conversation persistence in PostgreSQL
- 🔐 JWT authentication with user isolation
- 📱 Responsive design for mobile and desktop

## Project Structure

```
hackathon-todo/
├── frontend/           # Next.js 16+ with ChatKit UI
├── backend/            # FastAPI with AI Agent + MCP Tools
├── phase-1/            # Phase I console app (archived)
├── phase-2/            # Phase II full-stack app (archived)
├── specs/              # Spec-Kit Plus specifications
│   ├── 001-todo-console-app/
│   ├── 002-fullstack-web-app/
│   └── 003-ai-chatbot/  # Current phase specs
└── README.md           # This file
```

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (Neon recommended)
- OpenRouter API key (sign up at https://openrouter.ai/)

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit backend/.env
# - Set DATABASE_URL to your Neon PostgreSQL connection string
# - Set BETTER_AUTH_SECRET (32+ characters)

# Edit frontend/.env.local
# - Set NEXT_PUBLIC_API_URL=http://localhost:8000
# - Set BETTER_AUTH_SECRET (same as backend)
# - Set NEXT_PUBLIC_OPENROUTER_KEY (your OpenRouter API key)

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend python -m src.db.migrate

# Access the application
# Frontend: http://localhost:3000
# AI Chat: http://localhost:3000/chat
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
# Phase II & III: Database & Authentication
DATABASE_URL=postgresql://user:password@host.neon.tech/database
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key

# Phase III: Optional settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend (`frontend/.env.local`)

```env
# Phase II & III: Backend API & Authentication
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-minimum-secret-key

# Phase III: OpenRouter AI Provider
NEXT_PUBLIC_OPENROUTER_KEY=sk-or-v1-your-openrouter-api-key-here
```

**Important**:
- `BETTER_AUTH_SECRET` must be identical in both files
- Get OpenRouter API key from https://openrouter.ai/
- OpenRouter key is required for Phase III AI chat functionality

---

## 🚀 Usage Guide

### Phase III: AI Chat Interface (Primary)

1. **Sign up** at http://localhost:3000/signup
2. **Navigate to AI Chat** at http://localhost:3000/chat
3. **Start chatting** with natural language:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark buy groceries as complete"
   - "Change buy groceries to buy groceries and milk"
   - "Delete the grocery task"

### Phase II: Traditional CRUD UI (Fallback)

1. **Login** at http://localhost:3000/login
2. **Go to Dashboard** at http://localhost:3000/dashboard
3. **Use traditional UI** to manage tasks with buttons and forms

### Phase I: Console Application (Legacy)

```bash
cd phase-1/console-todo
uv run main.py
# or
python main.py
```

---

## 🧪 Testing

### Backend Tests (Phase III)

```bash
cd backend

# Run all tests
pytest

# Run specific test files
pytest tests/test_mcp_tools.py      # MCP tools tests
pytest tests/test_chat_api.py       # Chat API tests
pytest tests/test_agent.py          # Agent behavior tests

# Run with coverage
pytest --cov=src --cov-report=html
```

### Frontend Tests (Phase III)

```bash
cd frontend

# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Run with coverage
npm test -- --coverage
```

---

## 📊 API Documentation

### Interactive API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Phase II & III API Endpoints

| Method | Endpoint | Auth | Description | Phase |
|--------|----------|------|-------------|-------|
| POST | /api/auth/signup | No | Register user | II |
| POST | /api/auth/signin | No | Login user | II |
| POST | /api/auth/signout | Yes | Logout user | II |
| GET | /api/tasks | Yes | List tasks | II |
| POST | /api/tasks | Yes | Create task | II |
| GET | /api/tasks/{id} | Yes | Get task | II |
| PUT | /api/tasks/{id} | Yes | Update task | II |
| DELETE | /api/tasks/{id} | Yes | Delete task | II |
| PATCH | /api/tasks/{id}/toggle | Yes | Toggle completion | II |
| **POST** | **/api/{user_id}/chat** | **Yes** | **AI chat message** | **III** |

---

## 📁 Project Structure (Detailed)

```
hackathon-todo/
├── frontend/                    # Next.js 16+ Application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── login/          # Login page
│   │   │   ├── signup/         # Signup page
│   │   │   ├── dashboard/      # Traditional CRUD UI (Phase II)
│   │   │   └── chat/           # AI Chat UI (Phase III) 🆕
│   │   ├── components/
│   │   │   ├── ui/             # Base components
│   │   │   ├── layout/         # Header, Footer
│   │   │   ├── auth/           # Auth forms
│   │   │   ├── tasks/          # Task components (Phase II)
│   │   │   └── chat/           # Chat components (Phase III) 🆕
│   │   │       ├── ChatInterface.tsx
│   │   │       └── ChatMessage.tsx
│   │   └── lib/
│   │       ├── api.ts          # REST API client
│   │       ├── auth.ts         # Auth utilities
│   │       ├── chat.ts         # Chat API client (Phase III) 🆕
│   │       └── types.ts        # TypeScript types
│   └── package.json
│
├── backend/                     # FastAPI Application
│   ├── src/
│   │   ├── api/                # API endpoints
│   │   │   ├── auth.py         # Auth endpoints
│   │   │   ├── tasks.py        # Task endpoints (Phase II)
│   │   │   ├── chat.py         # Chat endpoint (Phase III) 🆕
│   │   │   └── router.py       # Main router
│   │   ├── models/             # Database models
│   │   │   ├── user.py         # User model
│   │   │   ├── task.py         # Task model
│   │   │   ├── conversation.py # Conversation model (Phase III) 🆕
│   │   │   └── message.py      # Message model (Phase III) 🆕
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── auth.py         # Auth schemas
│   │   │   ├── task.py         # Task schemas
│   │   │   └── chat.py         # Chat schemas (Phase III) 🆕
│   │   ├── services/           # Business logic
│   │   ├── core/               # Core utilities
│   │   ├── mcp/                # MCP Tools (Phase III) 🆕
│   │   │   ├── server.py       # MCP server
│   │   │   └── tools.py        # 5 MCP tools
│   │   ├── agent/              # AI Agent (Phase III) 🆕
│   │   │   ├── orchestrator.py # Agent orchestrator
│   │   │   └── behavior.py     # Intent recognition
│   │   └── db/
│   │       ├── migrate.py      # Migration runner
│   │       └── migrations/     # Migration scripts
│   ├── tests/                  # Test suite
│   │   ├── conftest.py         # Test fixtures 🆕
│   │   ├── test_mcp_tools.py   # MCP tools tests 🆕
│   │   └── test_chat_api.py    # Chat API tests 🆕
│   └── requirements.txt
│
├── phase-1/                     # Phase I (Archived)
│   └── console-todo/           # Console application
│
├── phase-2/                     # Phase II (Archived)
│   └── fullstack-web-app/      # Full-stack web app
│
├── specs/                       # Spec-Kit Plus Specifications
│   ├── 001-todo-console-app/   # Phase I specs
│   ├── 002-fullstack-web-app/  # Phase II specs
│   └── 003-ai-chatbot/         # Phase III specs 🆕
│       ├── overview.md
│       ├── architecture.md
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── mcp/                # MCP tool specs
│       ├── agent/              # Agent behavior specs
│       └── api/                # API specs
│
├── .specify/                    # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md     # Project constitution (v2.1.0)
│   ├── templates/              # Spec templates
│   └── scripts/                # Automation scripts
│
├── CLAUDE.md                    # Root project guidance
├── README.md                    # This file
└── docker-compose.yml          # Docker configuration
```

---

## 🔍 Verification Steps

### Phase III Verification

1. **Health Check**:
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Register User**:
   - Navigate to http://localhost:3000/signup
   - Create account with email and password

3. **Test AI Chat**:
   - Navigate to http://localhost:3000/chat
   - Try: "Add a task to buy groceries"
   - Try: "Show me my tasks"
   - Try: "Mark buy groceries as done"

4. **Verify Conversation Persistence**:
   - Refresh the page
   - Conversation history should remain

5. **Test User Isolation**:
   - Create second account
   - Verify separate task lists and conversations

### Phase II Verification

1. **Traditional CRUD UI**:
   - Navigate to http://localhost:3000/dashboard
   - Create, update, delete tasks using buttons
   - Verify tasks sync with AI chat interface

---

## 📖 Documentation

### Phase-Specific Documentation

- **Phase I**: `phase-1/console-todo/README.md`
- **Phase II**: `specs/002-fullstack-web-app/`
- **Phase III**: `specs/003-ai-chatbot/`

### Key Documents

- **Constitution**: `.specify/memory/constitution.md` (v2.1.0)
- **Root Guidance**: `CLAUDE.md`
- **Backend Guidance**: `backend/CLAUDE.md`
- **Frontend Guidance**: `frontend/CLAUDE.md`

### Specifications (Phase III)

- `specs/003-ai-chatbot/overview.md` - Project scope
- `specs/003-ai-chatbot/architecture.md` - System design
- `specs/003-ai-chatbot/spec.md` - Requirements
- `specs/003-ai-chatbot/plan.md` - Implementation plan
- `specs/003-ai-chatbot/tasks.md` - Task breakdown (104 tasks)
- `specs/003-ai-chatbot/mcp/tools.md` - MCP tool specifications
- `specs/003-ai-chatbot/agent/behavior.md` - Agent behavior
- `specs/003-ai-chatbot/api/chat-endpoint.md` - Chat API spec

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Progressive Enhancement**: Evolution from simple to complex
2. **Spec-Driven Development**: All features defined before implementation
3. **Stateless Architecture**: Horizontal scaling readiness
4. **AI Integration**: Natural language interfaces with MCP tools
5. **User Isolation**: Multi-tenant security patterns
6. **Modern Stack**: Next.js 16+, FastAPI, PostgreSQL, OpenRouter
7. **Testing**: Unit, integration, and E2E test coverage
8. **Documentation**: Comprehensive specs and traceability

---

## 🚧 Known Limitations

### Phase III
- OpenRouter API key required (not free tier)
- Agent uses pattern matching (not LLM-based intent recognition)
- Conversation history not paginated (loads all messages)
- No conversation archival/deletion UI

### Phase II
- JWT stored in localStorage (consider httpOnly cookies for production)
- No password reset functionality
- No email verification

### Phase I
- No data persistence
- Single user only
- Console-only interface

---

## 🤝 Contributing

This project follows Spec-Driven Development (SDD) principles:

1. All features must be specified in `specs/` before implementation
2. No manual code edits - all code generated via Claude Code
3. Constitution compliance required (`.specify/memory/constitution.md`)
4. Full traceability from specs to code

---

## 📜 License

MIT

---

## 🙏 Acknowledgments

- **Spec-Kit Plus**: Specification-driven development framework
- **OpenRouter**: AI model provider (OpenAI-compatible API)
- **OpenAI ChatKit**: Chat UI components
- **Neon**: Serverless PostgreSQL database
- **FastAPI**: Modern Python web framework
- **Next.js**: React framework for production

---

## 📞 Support

For issues or questions:
- Check `specs/` directory for detailed specifications
- Review `CLAUDE.md` files for implementation guidance
- See API documentation at http://localhost:8000/docs

---

**Built with ❤️ using Spec-Driven Development and Claude Code**

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
