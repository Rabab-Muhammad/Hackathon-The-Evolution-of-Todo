# Phase III - AI-Powered Todo Chatbot

## Overview

Phase III transforms the todo application into an AI-powered chatbot interface where users can manage their tasks using natural language commands.

## Key Features

### 🤖 AI Chatbot Interface
- Natural language task management
- Conversational UI with beautiful chat interface
- Real-time AI responses
- Persistent conversation history

### ✨ Enhanced Capabilities
- **Add Tasks**: "Add a task to buy groceries"
- **View Tasks**: "Show my tasks" or "List all tasks"
- **Complete Tasks**: "Mark task as complete" or "Complete all tasks"
- **Update Tasks**: "Update task1 as task2"
- **Delete Tasks**: "Delete task" or "Delete all tasks"

### 🎨 Beautiful UI
- Modern gradient-based design
- Fully responsive (mobile, tablet, desktop)
- Beautiful task cards with animations
- Enhanced chatbot interface with avatars
- Smooth transitions and hover effects

### 🔒 Security
- JWT-based authentication
- User-scoped data access
- Secure API endpoints

## Technology Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom components with gradients
- **Chat Interface**: Custom ChatKit implementation

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: Neon PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth with JWT
- **AI Integration**: OpenRouter API

## Project Structure

```
phase-3/
├── backend/
│   ├── src/
│   │   ├── agent/          # AI agent orchestration
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database setup
│   │   ├── mcp/            # MCP tools
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Test files
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── app/            # Next.js pages
    │   ├── components/     # React components
    │   │   ├── auth/       # Authentication components
    │   │   ├── chat/       # Chat interface components
    │   │   ├── layout/     # Header, Footer
    │   │   ├── tasks/      # Task components
    │   │   └── ui/         # Base UI components
    │   └── lib/            # Utilities and API client
    └── package.json        # Node dependencies
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (Neon)
- OpenRouter API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd phase-3/backend
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
OPENROUTER_API_KEY=your-openrouter-api-key
```

5. Run the server:
```bash
uvicorn src.main:app --reload --port 8001
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd phase-3/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_OPENROUTER_KEY=your-openrouter-api-key
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000)

## Features Comparison

| Feature | Phase I | Phase II | Phase III |
|---------|---------|----------|-----------|
| Interface | Console | Web UI | AI Chatbot |
| Storage | In-memory | PostgreSQL | PostgreSQL |
| Authentication | None | JWT | JWT |
| Task Management | Manual | CRUD UI | Natural Language |
| Multi-user | No | Yes | Yes |
| Responsive | N/A | Yes | Yes |
| AI Integration | No | No | Yes |

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/signin` - Login
- `POST /api/auth/signout` - Logout

### Tasks (Traditional CRUD)
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/toggle` - Toggle completion

### Chat (AI Interface)
- `POST /api/{user_id}/chat` - Send message to AI chatbot

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT signing secret (32+ characters)
- `OPENROUTER_API_KEY` - OpenRouter API key for AI

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_OPENROUTER_KEY` - OpenRouter API key

## Development Notes

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- All components fully responsive

### Chat Scroll Fix
- Chat messages scroll within container only
- Page doesn't scroll when sending messages
- Smooth auto-scroll to latest message

### Color Scheme
- Primary: Blue gradient (AI Chatbot)
- Secondary: Gray (Tasks button)
- Success: Green gradient (Completed tasks)
- Danger: Red gradient (Delete actions)

## Testing

### Backend
```bash
cd phase-3/backend
pytest
```

### Frontend
```bash
cd phase-3/frontend
npm test
```

## Deployment

### Backend (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy from `phase-3/backend` directory

### Frontend (Vercel)
1. Connect GitHub repository
2. Set environment variables
3. Deploy from `phase-3/frontend` directory

## Success Criteria

- ✅ User can interact with chatbot via natural language
- ✅ AI agent correctly invokes MCP tools based on user intent
- ✅ Backend persists conversation and message history
- ✅ Server is stateless; conversation resumes after restarts
- ✅ MCP tools enforce user-scoped access
- ✅ ChatKit frontend connects to backend chat endpoint
- ✅ Website is fully responsive for all screen sizes
- ✅ Beautiful UI with modern design patterns

## License

MIT

## Contributors

Built with Claude Code (Anthropic)
