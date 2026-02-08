# Troubleshooting Guide - Phase 3

This guide helps you diagnose and fix common issues when implementing Phase 3: AI-Powered Todo Chatbot.

## Table of Contents

- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Integration Issues](#integration-issues)
- [Performance Issues](#performance-issues)
- [Deployment Issues](#deployment-issues)

---

## Backend Issues

### Issue: "OpenAI API key not found"

**Symptoms**:
- Backend fails to start
- Error: `ValueError: OPENAI_API_KEY environment variable not set`

**Solution**:
```bash
# 1. Check .env file exists
ls -la .env

# 2. Verify OPENAI_API_KEY is set
cat .env | grep OPENAI_API_KEY

# 3. If missing, add it
echo "OPENAI_API_KEY=sk-proj-your-key-here" >> .env

# 4. Restart backend
uvicorn src.main:app --reload
```

**Prevention**: Always copy `.env.example` to `.env` before starting

---

### Issue: "Agent not calling tools"

**Symptoms**:
- Agent responds but doesn't execute tools
- No tool execution indicators in chat
- Tasks not being created/updated

**Diagnosis**:
```bash
# 1. Check if tools are registered
curl http://localhost:8000/api/tools

# 2. Check agent initialization logs
# Look for: "✓ Registered N MCP tools"
```

**Solutions**:

**A. Tools not registered**:
```python
# In src/main.py, verify startup event:
@app.on_event("startup")
async def startup_event():
    initialize_mcp_server()  # Must be called
    mcp_server = get_mcp_server()
    tool_schemas = mcp_server.get_tool_schemas_for_openai()
    initialize_agent(tool_schemas)  # Must pass tools
```

**B. System prompt missing tool instructions**:
```python
# In src/agent_setup.py, verify SYSTEM_PROMPT includes:
# - List of available tools
# - Instructions on when to use each tool
# - Examples of tool usage
```

**C. OpenAI model doesn't support function calling**:
```bash
# Use gpt-4-turbo-preview or gpt-3.5-turbo
# NOT gpt-3.5-turbo-instruct (doesn't support functions)
OPENAI_MODEL=gpt-4-turbo-preview
```

---

### Issue: "Database connection failed"

**Symptoms**:
- Error: `sqlalchemy.exc.OperationalError`
- Backend crashes on startup

**Solution**:
```bash
# 1. Verify DATABASE_URL format
# Correct: postgresql://user:pass@host:port/db?sslmode=require
# Incorrect: postgres:// (should be postgresql://)

# 2. Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('YOUR_DATABASE_URL'); engine.connect()"

# 3. Check Neon database is running
# Visit: https://console.neon.tech/

# 4. Verify SSL mode for Neon
DATABASE_URL=postgresql://...?sslmode=require
```

---

### Issue: "Streaming not working"

**Symptoms**:
- Chat endpoint returns 200 but no data streams
- Frontend shows loading forever
- No tokens appear in chat

**Diagnosis**:
```bash
# Test streaming with curl
curl -N -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' \
  --no-buffer

# Should see: event: token\ndata: {"token": "..."}\n\n
```

**Solutions**:

**A. Missing SSE headers**:
```python
# In src/routers/chat.py
return StreamingResponse(
    event_generator(),
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"  # Important for nginx
    }
)
```

**B. CORS blocking streaming**:
```python
# In src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**C. Buffering enabled**:
```bash
# If using nginx, disable buffering
proxy_buffering off;
```

---

### Issue: "Rate limit exceeded"

**Symptoms**:
- Error: `openai.error.RateLimitError`
- Agent stops responding after several requests

**Solution**:
```python
# Implement exponential backoff (already in agent_setup.py)
# Or upgrade OpenAI plan for higher limits

# Temporary workaround: Use gpt-3.5-turbo (higher limits)
OPENAI_MODEL=gpt-3.5-turbo
```

---

### Issue: "Tool execution timeout"

**Symptoms**:
- Tool execution takes > 10 seconds
- Frontend shows "Executing..." forever

**Diagnosis**:
```bash
# Check database query performance
# Add logging to tool execution
```

**Solution**:
```python
# Add database indexes
# In src/models.py
class Task(SQLModel, table=True):
    # ...
    __table_args__ = (
        Index('idx_priority', 'priority'),
        Index('idx_category', 'category'),
        Index('idx_due_date', 'due_date'),
        Index('idx_complete', 'complete'),
    )
```

---

## Frontend Issues

### Issue: "ChatKit components not rendering"

**Symptoms**:
- Blank chat page
- Error: `Cannot find module '@openai/chatkit'`

**Solution**:
```bash
# 1. Verify installation
npm list @openai/chatkit

# 2. If not installed
npm install @openai/chatkit

# 3. Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# 4. Restart dev server
npm run dev
```

---

### Issue: "Task list not updating"

**Symptoms**:
- Agent creates task but it doesn't appear in list
- No real-time sync

**Diagnosis**:
```javascript
// Check browser console for errors
// Look for: "Failed to fetch tasks" or similar
```

**Solutions**:

**A. useTaskSync hook not called**:
```typescript
// In ChatLayout.tsx, verify:
const { tasks, refreshTasks } = useTaskSync();

// And in useChatEvents:
onTaskCreated: (task) => {
  refreshTasks();  // Must call this
}
```

**B. Chat events not emitted**:
```typescript
// In ChatPanel.tsx, verify onToolExecution is called:
<ChatKitProvider
  onToolExecution={onToolExecution}  // Must pass this
>
```

**C. API endpoint incorrect**:
```bash
# Check .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000  # Must match backend
```

---

### Issue: "Streaming not displaying"

**Symptoms**:
- Full response appears at once (not token-by-token)
- No typing indicator

**Solution**:
```typescript
// In src/lib/chatkit.ts, verify streaming is enabled:
export const chatKitConfig: ChatKitConfig = {
  streaming: true,  // Must be true
  streamingProtocol: 'sse',
  // ...
};
```

---

### Issue: "Mobile layout broken"

**Symptoms**:
- Layout doesn't adapt to mobile
- Elements overflow screen

**Diagnosis**:
```bash
# Test at different breakpoints
# Chrome DevTools > Toggle device toolbar
# Test: 320px, 375px, 768px, 1024px
```

**Solution**:
```typescript
// Verify responsive classes in ChatLayout.tsx
<div className="flex flex-col md:flex-row">
  <div className="w-full md:w-3/5">  {/* Chat */}
  <div className="w-full md:w-2/5">  {/* Tasks */}
</div>

// Check viewport meta tag in layout.tsx
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

---

### Issue: "Animations not smooth"

**Symptoms**:
- Janky animations
- Low frame rate
- Browser lag

**Solution**:
```typescript
// Use CSS transforms (GPU accelerated)
// Instead of: left, top, width, height
// Use: transform, opacity

// Example in TaskHighlight.tsx
.task-highlight {
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity;
}

// Avoid animating many elements at once
// Batch updates with requestAnimationFrame
```

---

## Integration Issues

### Issue: "CORS errors"

**Symptoms**:
- Error: `Access to fetch at 'http://localhost:8000' has been blocked by CORS policy`
- Network requests fail in browser

**Solution**:
```python
# Backend: src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue: "Chat endpoint returns 404"

**Symptoms**:
- Error: `404 Not Found` when sending message
- Chat endpoint not accessible

**Diagnosis**:
```bash
# Check if endpoint exists
curl http://localhost:8000/api/chat

# Check API docs
open http://localhost:8000/docs
```

**Solution**:
```python
# Verify chat router is registered in src/main.py
from .routers import chat

app.include_router(chat.router)  # Must include this
```

---

### Issue: "Environment variables not loading"

**Symptoms**:
- `process.env.NEXT_PUBLIC_CHAT_ENDPOINT` is undefined
- Backend can't find `OPENAI_API_KEY`

**Solution**:

**Frontend**:
```bash
# 1. Verify .env.local exists
ls -la .env.local

# 2. Verify variables start with NEXT_PUBLIC_
NEXT_PUBLIC_CHAT_ENDPOINT=http://localhost:8000/api/chat

# 3. Restart dev server (required after .env changes)
npm run dev
```

**Backend**:
```bash
# 1. Verify .env exists
ls -la .env

# 2. Load with python-dotenv
from dotenv import load_dotenv
load_dotenv()  # Must call this

# 3. Restart backend
uvicorn src.main:app --reload
```

---

## Performance Issues

### Issue: "Slow response times"

**Symptoms**:
- First token takes > 3 seconds
- Tool execution takes > 1 second

**Diagnosis**:
```bash
# Add timing logs
import time

start = time.time()
result = await tool_executor.execute(...)
duration = time.time() - start
print(f"Tool execution: {duration}s")
```

**Solutions**:

**A. Database queries slow**:
```python
# Add indexes (see above)
# Use query profiling
# EXPLAIN ANALYZE SELECT ...
```

**B. OpenAI API slow**:
```bash
# Use faster model
OPENAI_MODEL=gpt-3.5-turbo  # Faster than gpt-4

# Reduce max_tokens
AGENT_MAX_TOKENS=300  # Lower = faster
```

**C. Too much conversation context**:
```bash
# Reduce history length
AGENT_MAX_HISTORY=5  # Lower = faster
```

---

### Issue: "High memory usage"

**Symptoms**:
- Backend uses > 500MB RAM
- Frontend uses > 200MB RAM

**Solution**:

**Backend**:
```python
# Clean up old conversations more frequently
CONVERSATION_CLEANUP_HOURS=12  # Instead of 24

# Limit conversation history
AGENT_MAX_HISTORY=5  # Instead of 10
```

**Frontend**:
```typescript
// Clear old messages
const MAX_MESSAGES = 50;
if (messages.length > MAX_MESSAGES) {
  messages = messages.slice(-MAX_MESSAGES);
}
```

---

## Deployment Issues

### Issue: "Build fails on Vercel"

**Symptoms**:
- Vercel build error
- TypeScript errors in production

**Solution**:
```bash
# 1. Test build locally
npm run build

# 2. Fix TypeScript errors
npm run type-check

# 3. Check environment variables in Vercel dashboard
# Must set: NEXT_PUBLIC_CHAT_ENDPOINT

# 4. Verify Node.js version
# package.json:
"engines": {
  "node": ">=18.0.0"
}
```

---

### Issue: "Backend crashes in production"

**Symptoms**:
- Backend works locally but crashes on Railway/Render
- Error logs show import errors

**Solution**:
```bash
# 1. Verify all dependencies in requirements.txt
pip freeze > requirements.txt

# 2. Check Python version
# Railway/Render: Use Python 3.11+

# 3. Set environment variables in dashboard
# Required: OPENAI_API_KEY, DATABASE_URL

# 4. Check logs
railway logs  # or render logs
```

---

### Issue: "Database connection fails in production"

**Symptoms**:
- Works locally but not in production
- SSL/TLS errors

**Solution**:
```bash
# Neon requires SSL
DATABASE_URL=postgresql://...?sslmode=require

# Verify connection pooling
# In src/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True  # Important for serverless
)
```

---

## Debugging Tips

### Enable Debug Logging

**Backend**:
```python
# In .env
LOG_LEVEL=DEBUG

# In code
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend**:
```bash
# In .env.local
NEXT_PUBLIC_DEBUG=true
```

### Check API Responses

```bash
# Use curl with verbose output
curl -v -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Monitor Network Requests

```javascript
// In browser console
// Network tab > Filter: Fetch/XHR
// Check request/response for each API call
```

### Test Components Independently

```typescript
// Test useTaskSync hook
const TestComponent = () => {
  const { tasks, loading, error } = useTaskSync();
  console.log({ tasks, loading, error });
  return <div>Check console</div>;
};
```

---

## Getting Help

If you're still stuck:

1. **Check Specifications**: Review `specs/` for detailed requirements
2. **Check Examples**: See `docs/CONVERSATION_EXAMPLES.md` for test cases
3. **Check Logs**: Backend and frontend logs often reveal the issue
4. **Test Independently**: Test backend and frontend separately
5. **Simplify**: Remove complexity until it works, then add back

## Common Mistakes

- ❌ Forgetting to restart dev server after .env changes
- ❌ Not calling `refreshTasks()` after tool execution
- ❌ Using wrong OpenAI model (must support function calling)
- ❌ Missing CORS configuration
- ❌ Not handling streaming correctly
- ❌ Forgetting to register tools with agent
- ❌ Not validating environment variables on startup

## Quick Fixes Checklist

- [ ] Environment variables set correctly
- [ ] Dependencies installed (npm install, pip install)
- [ ] Backend running on correct port (8000)
- [ ] Frontend running on correct port (3000)
- [ ] CORS configured for frontend origin
- [ ] OpenAI API key valid and has credits
- [ ] Database accessible and migrations run
- [ ] Tools registered with agent
- [ ] System prompt includes tool instructions
- [ ] Streaming headers set correctly
- [ ] Chat events emitted and handled
- [ ] Task list refresh called after operations

---

**Last Updated**: 2026-02-03
**Version**: 3.0.0

For additional support, refer to:
- Phase 3 README: `../README.md`
- Implementation Guide: `../IMPLEMENTATION_GUIDE.md`
- Tool Reference: `TOOL_REFERENCE.md`
