# Phase 3 Backend - Quick Start Guide

## 🚀 Running the Backend

### Option 1: Using the Startup Script (Recommended)
```bash
cd phase-3/backend
start.bat
```

### Option 2: Manual Start
```bash
cd phase-3/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

## 📋 Prerequisites

1. **Python 3.11+** installed
2. **Gemini API Key** (FREE - no credit card required)
   - Get it from: https://makersuite.google.com/app/apikey
3. **Dependencies** installed:
   ```bash
   pip install google-generativeai fastapi uvicorn python-dotenv
   ```

## 🔑 Environment Setup

The `.env` file should contain:
```bash
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-1.5-flash
API_HOST=0.0.0.0
API_PORT=8001
```

## 🧪 Testing the API

### 1. Health Check
```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "gemini_api": "configured",
  "tasks_count": 0
}
```

### 2. Test Gemini API Connection
```bash
curl http://localhost:8001/api/test-gemini
```

Expected response:
```json
{
  "status": "success",
  "message": "Gemini API is working!",
  "response": "Hello! Gemini API is working! ..."
}
```

### 3. Chat with AI
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Add a task to buy groceries\"}"
```

### 4. Create a Task
```bash
curl -X POST http://localhost:8001/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Buy groceries\", \"priority\": \"high\"}"
```

### 5. Get All Tasks
```bash
curl http://localhost:8001/api/tasks
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🔧 Available Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /api/test-gemini` - Test Gemini API connection

### Task Management
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

### AI Chat
- `POST /api/chat` - Chat with AI assistant

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not configured"
**Solution**:
1. Create `.env` file in `phase-3/backend/`
2. Add: `GEMINI_API_KEY=your-api-key-here`
3. Get free key from: https://makersuite.google.com/app/apikey

### Error: "No module named 'google.generativeai'"
**Solution**:
```bash
pip install google-generativeai
```

### Error: "Port 8001 already in use"
**Solution**: Change port in command:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8002
```

### Error: "ModuleNotFoundError: No module named 'todo_manager'"
**Solution**: You're running from the wrong directory. Make sure you're in `phase-3/backend/`:
```bash
cd phase-3/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

## 💡 Features

### Current Implementation
✅ Google Gemini API integration (FREE)
✅ Basic task CRUD operations
✅ AI chat endpoint
✅ In-memory storage (for demo)
✅ CORS enabled
✅ API documentation

### Coming Soon
- Database integration (PostgreSQL/Neon)
- MCP tools for advanced task management
- Conversation history
- Function calling for task operations
- Frontend integration

## 🎯 Next Steps

1. **Test the backend**: Run `start.bat` and test endpoints
2. **Try the chat**: Send messages to `/api/chat`
3. **Build frontend**: Create a simple chat UI
4. **Add database**: Integrate with Neon PostgreSQL
5. **Implement MCP tools**: Add advanced task management

## 📖 Documentation

- **Phase 3 README**: `phase-3/README.md`
- **Gemini API Docs**: https://ai.google.dev/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Status**: ✅ Minimal implementation ready for testing
**Cost**: $0/month (Google Gemini free tier)
**Setup Time**: 5 minutes
