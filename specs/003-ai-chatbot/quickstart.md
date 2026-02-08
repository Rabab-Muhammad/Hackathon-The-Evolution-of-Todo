# Quickstart Guide: Phase III AI Chatbot

**Feature**: Phase III AI-Powered Todo Chatbot
**Date**: 2026-02-08
**Prerequisites**: Phase II implementation complete

## Purpose

Step-by-step guide to set up and run the Phase III AI-powered chatbot locally. This guide assumes Phase II (authentication, tasks, database) is already working.

## Prerequisites

### Phase II Requirements (Must Be Complete)

- ✅ Phase II backend running (FastAPI + SQLModel)
- ✅ Phase II frontend running (Next.js 16+)
- ✅ Neon PostgreSQL database accessible
- ✅ Better Auth authentication working
- ✅ Users can sign up, log in, and manage tasks via CRUD UI

### System Requirements

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager
- Git
- PostgreSQL client (for database verification)

### Required API Keys

- **OpenRouter API Key**: Sign up at https://openrouter.ai/ and create API key
- **Neon Database URL**: From Phase II setup
- **Better Auth Secret**: From Phase II setup (32+ characters)

## Environment Variables

### Backend (.env or environment)

```bash
# Phase II (Existing)
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-32-character-secret-from-phase-ii

# Phase III (New)
# Note: OpenRouter key is frontend-only
# Backend uses Agents SDK with MCP tools
```

### Frontend (.env.local)

```bash
# Phase II (Existing)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-from-phase-ii

# Phase III (New)
NEXT_PUBLIC_OPENROUTER_KEY=sk-or-v1-your-openrouter-api-key
```

## Installation Steps

### Step 1: Verify Phase II is Working

```bash
# Test backend health
curl http://localhost:8000/api/health

# Test authentication
# Sign up and log in via frontend at http://localhost:3000

# Test task CRUD
# Create, view, update, delete tasks via dashboard
```

**Expected**: All Phase II functionality works correctly.

### Step 2: Install Backend Dependencies

```bash
cd backend

# Install new Phase III dependencies
pip install openai  # OpenAI SDK (for OpenRouter compatibility)
pip install mcp     # Official MCP SDK

# Or update requirements.txt and install all
pip install -r requirements.txt
```

**New Dependencies**:
- `openai>=1.0.0` - OpenAI SDK (OpenRouter compatible)
- `mcp>=0.1.0` - Official MCP SDK for Python
- `pydantic>=2.0.0` - Already installed (Phase II)
- `sqlmodel>=0.0.14` - Already installed (Phase II)

### Step 3: Run Database Migrations

```bash
cd backend

# Run Phase III migration (creates conversations and messages tables)
python -m src.db.migrate

# Verify tables created
psql $DATABASE_URL -c "\dt"
# Should show: users, tasks, conversations, messages
```

**Expected Output**:
```
                List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+---------
 public | users           | table | user
 public | tasks           | table | user
 public | conversations   | table | user
 public | messages        | table | user
```

### Step 4: Install Frontend Dependencies

```bash
cd frontend

# Install new Phase III dependencies
npm install @openai/chatkit  # OpenAI ChatKit library

# Or update package.json and install all
npm install
```

**New Dependencies**:
- `@openai/chatkit` - Chat UI library
- `react>=18.0.0` - Already installed (Phase II)
- `next>=16.0.0` - Already installed (Phase II)

### Step 5: Configure OpenRouter

```bash
# Add OpenRouter API key to frontend/.env.local
echo "NEXT_PUBLIC_OPENROUTER_KEY=sk-or-v1-your-key-here" >> frontend/.env.local

# Verify environment variable is set
cd frontend
npm run dev
# Check browser console for OpenRouter configuration
```

**Verify**: OpenRouter key is loaded (check browser dev tools → Application → Local Storage)

### Step 6: Start Backend

```bash
cd backend

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Endpoints**:
```bash
# Health check
curl http://localhost:8000/api/health

# Chat endpoint (requires authentication)
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### Step 7: Start Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev
```

**Expected Output**:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Ready in 2.1s
```

**Verify Pages**:
- Landing: http://localhost:3000
- Login: http://localhost:3000/login
- Dashboard: http://localhost:3000/dashboard (Phase II CRUD UI)
- Chat: http://localhost:3000/chat (Phase III chatbot UI)

## Testing the Chatbot

### Test 1: Add Task via Chat

1. Navigate to http://localhost:3000/chat
2. Type: "Add a task to buy groceries"
3. Press Enter or click Send

**Expected Response**:
```
I've added the task 'Buy groceries' to your list.
```

**Verify**: Task appears in database and in dashboard (http://localhost:3000/dashboard)

### Test 2: View Tasks via Chat

1. In chat, type: "Show me my tasks"
2. Press Enter

**Expected Response**:
```
You have 1 task:
1. Buy groceries (not completed)
```

### Test 3: Complete Task via Chat

1. In chat, type: "Mark buy groceries as done"
2. Press Enter

**Expected Response**:
```
Great! I've marked 'Buy groceries' as complete.
```

**Verify**: Task is marked complete in database and dashboard

### Test 4: Conversation Persistence

1. Refresh the page (F5)
2. Verify conversation history is still visible
3. Send another message
4. Verify conversation continues seamlessly

**Expected**: All previous messages are loaded, new messages are added to same conversation

### Test 5: Server Restart (Stateless Test)

1. Stop backend server (Ctrl+C)
2. Restart backend server
3. Refresh frontend
4. Verify conversation history is still visible
5. Send a new message

**Expected**: Conversation resumes without data loss (proves stateless architecture)

## Troubleshooting

### Issue: "OpenRouter API key not found"

**Solution**:
```bash
# Verify environment variable is set
echo $NEXT_PUBLIC_OPENROUTER_KEY

# If empty, add to frontend/.env.local
echo "NEXT_PUBLIC_OPENROUTER_KEY=sk-or-v1-your-key" >> frontend/.env.local

# Restart frontend
cd frontend
npm run dev
```

### Issue: "Conversation not found" error

**Solution**:
```bash
# Check database for conversations table
psql $DATABASE_URL -c "SELECT * FROM conversations;"

# If table doesn't exist, run migrations
cd backend
python -m src.db.migrate
```

### Issue: "Unable to process your message"

**Possible Causes**:
1. OpenRouter API key invalid or expired
2. OpenRouter rate limit exceeded
3. Network connectivity issues
4. MCP tools not registered correctly

**Solution**:
```bash
# Check backend logs for detailed error
# Look for "OpenRouter API error" or "MCP tool error"

# Verify OpenRouter key is valid
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $NEXT_PUBLIC_OPENROUTER_KEY"

# Should return list of available models
```

### Issue: "Task not found" when completing/deleting

**Possible Causes**:
1. Task belongs to different user (user isolation working correctly)
2. Task was already deleted
3. Ambiguous task reference

**Solution**:
- Use more specific task description
- List tasks first to see exact titles
- Use task ID if available

### Issue: Chat UI not loading

**Solution**:
```bash
# Verify ChatKit is installed
cd frontend
npm list @openai/chatkit

# If not installed
npm install @openai/chatkit

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Issue: Database connection errors

**Solution**:
```bash
# Verify DATABASE_URL is correct
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Check Neon dashboard for database status
```

## Verification Checklist

Before proceeding to implementation, verify:

- [ ] Phase II backend and frontend are running
- [ ] Database migrations completed successfully
- [ ] All 4 tables exist (users, tasks, conversations, messages)
- [ ] OpenRouter API key is configured
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can add task via chat
- [ ] Can view tasks via chat
- [ ] Can complete task via chat
- [ ] Conversation persists across page refreshes
- [ ] Conversation persists across server restarts
- [ ] Traditional CRUD UI (dashboard) still works

## Next Steps

Once quickstart verification is complete:

1. **Run `/sp.tasks`**: Generate detailed task breakdown
2. **Run `/sp.implement`**: Execute implementation tasks
3. **Run Tests**: Execute unit, integration, and E2E tests
4. **Deploy**: Follow deployment guide for production

## Additional Resources

- **OpenRouter Documentation**: https://openrouter.ai/docs
- **OpenAI Agents SDK**: https://platform.openai.com/docs/guides/agents
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **ChatKit Documentation**: https://platform.openai.com/docs/chatkit
- **Phase III Specifications**: `/specs/003-ai-chatbot/`

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review backend logs for detailed errors
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Ensure Phase II is working before debugging Phase III

---

**Quickstart Status**: ✅ Complete
**Next Step**: Update agent context and prepare for task generation
