# Quickstart: AI-Powered Todo Chatbot (Phase 3)

**Feature**: `003-ai-chatbot`
**Date**: 2026-02-02

## Prerequisites

- Phase 2 application running (backend + frontend)
- OpenAI API key
- Node.js 18+ and Python 3.11+

## Setup Steps

### 1. Backend Setup

```bash
# Navigate to backend
cd phase-2/backend

# Add OpenAI dependency
pip install openai>=1.0.0

# Create/update .env with OpenAI settings
cat >> .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
MAX_CONVERSATION_MESSAGES=50
EOF

# Run database migrations (creates conversations and messages tables)
python -c "from src.database import create_db_and_tables; create_db_and_tables()"

# Start backend
uvicorn src.main:app --reload
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd phase-2/frontend

# No additional dependencies needed - using existing fetch API
# Start frontend
npm run dev
```

### 3. Verify Installation

```bash
# Test backend health
curl http://localhost:8000/

# Test chat endpoint (requires auth token)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?"}'
```

## New File Structure

```
phase-2/
├── backend/src/
│   ├── models/
│   │   ├── task.py           # Existing
│   │   ├── conversation.py   # NEW: Conversation model
│   │   └── message.py        # NEW: Message model
│   ├── agents/
│   │   ├── __init__.py       # NEW
│   │   ├── tools.py          # NEW: Tool implementations
│   │   └── task_agent.py     # NEW: OpenAI agent config
│   ├── repositories/
│   │   ├── task_repository.py          # Existing
│   │   └── conversation_repository.py  # NEW
│   ├── api/routes/
│   │   ├── tasks.py          # Existing
│   │   └── chat.py           # NEW: Chat endpoint
│   └── schemas/
│       └── chat.py           # NEW: Chat request/response schemas
│
└── frontend/src/
    ├── app/(protected)/
    │   ├── layout.tsx        # MODIFIED: Add tab navigation
    │   ├── dashboard/page.tsx # Existing
    │   └── chat/page.tsx     # NEW: Chat page
    ├── components/
    │   ├── chat/
    │   │   ├── ChatInterface.tsx   # NEW
    │   │   ├── MessageList.tsx     # NEW
    │   │   └── MessageInput.tsx    # NEW
    │   └── layout/
    │       └── TabNavigation.tsx   # NEW
    └── lib/
        └── chat-api.ts       # NEW: Chat API client
```

## Environment Variables

### Backend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | OpenAI API key |
| OPENAI_MODEL | No | gpt-4o-mini | Model to use |
| MAX_CONVERSATION_MESSAGES | No | 50 | Max messages per request |

### Frontend (.env.local)

No new environment variables required.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/chat` | JWT | Send message to AI |
| GET | `/api/conversations` | JWT | List conversations |
| GET | `/api/conversations/{id}` | JWT | Get conversation |
| DELETE | `/api/conversations/{id}` | JWT | Delete conversation |

## Testing the Feature

### Manual Testing

1. Log in to the application
2. Click "Chat" tab in navigation
3. Send a message: "Add buy milk to my tasks"
4. Verify response confirms task creation
5. Switch to "Dashboard" tab
6. Verify task appears in list

### API Testing

```bash
# Get auth token (use existing login flow)

# Create a task via chat
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add call mom to my tasks"}'

# List tasks via chat
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my tasks?", "conversation_id": 1}'

# Complete a task via chat
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Mark call mom as done", "conversation_id": 1}'
```

## Troubleshooting

### "OpenAI API error"
- Check OPENAI_API_KEY is set correctly
- Verify API key has credits
- Check network connectivity to api.openai.com

### "Conversation not found"
- Ensure conversation_id is valid
- Ensure conversation belongs to authenticated user

### "Task not found"
- Task may have been deleted
- Use exact title or task ID for matching

### Slow responses
- OpenAI API can take 2-4 seconds
- Check for network latency
- Consider using streaming (future enhancement)

## Next Steps

After completing this quickstart:

1. Review the full API contract in `contracts/chat-api.yaml`
2. Review tool contracts in `contracts/tools.md`
3. Run the automated tests: `pytest tests/`
4. Deploy to staging environment
