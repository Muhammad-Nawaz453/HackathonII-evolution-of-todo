# Phase 3 Implementation Guide

**Version**: 2.0.0
**Last Updated**: 2026-02-08 (Updated for Google Gemini - FREE)

This guide provides step-by-step instructions for implementing Phase 3: AI-Powered Todo Chatbot using Google Gemini API (completely free). Follow these steps in order for systematic, testable progress.

## Prerequisites

Before starting Phase 3 implementation:

- ✅ Phase 2 is complete and deployed
- ✅ Backend running on FastAPI with PostgreSQL (Neon)
- ✅ Frontend running on Next.js 14+ with Tailwind CSS
- ✅ **Google Gemini API key obtained** (FREE - get from https://makersuite.google.com/app/apikey)
  - No credit card required
  - 1500 requests per day free tier
- ✅ All Phase 3 specifications reviewed and understood
- ✅ Development environment set up (Python 3.11+, Node.js 18+)

## Implementation Timeline

**Total Estimated Time**: 15-20 days (3 weeks)

- **Week 1**: Backend (MCP Tools + Agent SDK + Chat Endpoint)
- **Week 2**: Frontend (ChatKit + UI Components + Real-time Sync)
- **Week 3**: Natural Language Flows + Testing + Polish

## Phase 1: Backend Foundation (Days 1-7)

### Day 1-2: MCP Tools Implementation

**Goal**: Create all MCP tool definitions and execution logic

#### Step 1.1: Install Dependencies

```bash
cd phase2/backend  # Work in existing Phase 2 backend

# Install new dependencies
pip install google-generativeai mcp sse-starlette python-dateutil jsonschema

# Or add to requirements.txt and install
pip install -r requirements.txt
```

#### Step 1.2: Create Tool Directory Structure

```bash
mkdir -p src/tools
touch src/tools/__init__.py
touch src/tools/task_tools.py
touch src/tools/search_tools.py
touch src/tools/utility_tools.py
```

#### Step 1.3: Implement Task Tools

**File**: `src/tools/task_tools.py`

Implement these tools (refer to Spec 03 for full schemas):
- `add_task` - Create new task
- `get_task` - Get single task by ID
- `get_tasks` - Get multiple tasks with filters
- `update_task` - Update existing task
- `delete_task` - Delete single task
- `bulk_delete_tasks` - Delete multiple tasks

**Testing**:
```bash
# Create test file
touch tests/test_task_tools.py

# Run tests
pytest tests/test_task_tools.py -v
```

#### Step 1.4: Implement Search Tools

**File**: `src/tools/search_tools.py`

Implement:
- `search_tasks` - Full-text search
- `filter_tasks` - Filter by criteria
- `get_tasks_by_date` - Get tasks by date range

**Testing**:
```bash
pytest tests/test_search_tools.py -v
```

#### Step 1.5: Implement Utility Tools

**File**: `src/tools/utility_tools.py`

Implement:
- `parse_date` - Natural language date parsing
- `get_task_statistics` - Task statistics
- `validate_task_data` - Input validation

**Testing**:
```bash
pytest tests/test_utility_tools.py -v
```

#### Step 1.6: Create MCP Server

**File**: `src/mcp_server.py`

Implement:
- `TodoMCPServer` class
- Tool registration
- Tool execution with validation
- Error handling

**Testing**:
```bash
pytest tests/test_mcp_server.py -v
```

**Checkpoint**: All MCP tools implemented and tested independently

---

### Day 3-4: OpenAI Agent SDK Setup

**Goal**: Configure OpenAI Agent with system prompt and tool registration

#### Step 2.1: Create Agent Setup Module

**File**: `src/agent_setup.py`

Implement:
- `AgentManager` class
- `ConversationManager` class
- `StreamingHandler` class
- System prompt (from Spec 02)

#### Step 2.2: Configure Environment Variables

**File**: `.env`

```bash
# Add to existing .env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

#### Step 2.3: Initialize Agent at Startup

**File**: `src/main.py` (modify existing)

```python
from .mcp_server import initialize_mcp_server, get_mcp_server
from .agent_setup import initialize_agent

@app.on_event("startup")
async def startup_event():
    # Initialize MCP server
    initialize_mcp_server()

    # Get tool schemas for OpenAI
    mcp_server = get_mcp_server()
    tool_schemas = mcp_server.get_tool_schemas_for_openai()

    # Initialize agent with tools
    initialize_agent(tool_schemas)

    print("✓ MCP server and agent initialized")
```

#### Step 2.4: Test Agent Behavior

Create test script:

```python
# tests/test_agent_behavior.py
import pytest
from src.agent_setup import get_agent_manager, get_conversation_manager

def test_agent_initialization():
    agent = get_agent_manager()
    assert agent.client is not None

def test_simple_conversation():
    agent = get_agent_manager()
    conv_manager = get_conversation_manager()

    messages = conv_manager.get_context("test-conv-1")
    messages.append({"role": "user", "content": "Add a task to buy groceries"})

    response = agent.generate_response(messages, stream=False)
    assert response is not None
    # Verify agent calls add_task tool
```

**Testing**:
```bash
pytest tests/test_agent_behavior.py -v
```

**Checkpoint**: Agent initialized, system prompt loaded, tools registered

---

### Day 5-6: Chat Endpoint with Streaming

**Goal**: Create FastAPI endpoint for chat with SSE streaming

#### Step 3.1: Create Chat Router

**File**: `src/routers/chat.py`

Implement:
- `POST /api/chat` endpoint
- Request/response models
- Streaming response handler
- Tool execution integration

#### Step 3.2: Register Chat Router

**File**: `src/main.py` (modify)

```python
from .routers import tasks, chat

app.include_router(tasks.router)
app.include_router(chat.router)  # Add this
```

#### Step 3.3: Test Chat Endpoint

**Manual Test with curl**:

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test the chatbot", "conversation_id": "test-1"}'
```

**Automated Test**:

```python
# tests/test_chat_endpoint.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post(
        "/api/chat",
        json={"message": "Show me my tasks"}
    )
    assert response.status_code == 200
```

#### Step 3.4: Test Streaming

```python
def test_chat_streaming():
    with client.stream("POST", "/api/chat", json={"message": "Add a task"}) as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"

        # Read stream
        for line in response.iter_lines():
            if line.startswith(b"data:"):
                print(line.decode())
```

**Checkpoint**: Chat endpoint working with streaming, tools executing correctly

---

### Day 7: Backend Integration Testing

**Goal**: Test full backend flow end-to-end

#### Step 4.1: End-to-End Tests

```python
# tests/test_e2e_backend.py

def test_create_task_via_chat():
    # Send chat message
    response = client.post("/api/chat", json={
        "message": "Add a high priority task to review report by Friday"
    })

    # Verify task was created
    tasks = client.get("/api/tasks").json()
    assert any(t["title"] == "Review report" for t in tasks)

def test_search_task_via_chat():
    # Create task first
    client.post("/api/tasks", json={"title": "Test task"})

    # Search via chat
    response = client.post("/api/chat", json={
        "message": "Find tasks about test"
    })

    # Verify search results in response
    # (parse streaming response)
```

#### Step 4.2: Performance Testing

```python
import time

def test_response_time():
    start = time.time()
    response = client.post("/api/chat", json={"message": "Show my tasks"})
    duration = time.time() - start

    assert duration < 3.0  # Should respond within 3 seconds
```

**Checkpoint**: Backend fully functional, all tests passing

---

## Phase 2: Frontend Integration (Days 8-14)

### Day 8-9: ChatKit Integration

**Goal**: Install ChatKit and create basic chat interface

#### Step 5.1: Install Dependencies

```bash
cd phase2/frontend  # Work in existing Phase 2 frontend

# Install ChatKit
npm install @openai/chatkit

# Install additional dependencies
npm install lucide-react  # For icons
```

#### Step 5.2: Create ChatKit Configuration

**File**: `src/lib/chatkit.ts`

Implement ChatKit configuration (refer to Spec 01)

#### Step 5.3: Create Chat Page

**File**: `src/app/chat/page.tsx`

Create basic chat page with ChatKit components

#### Step 5.4: Test Chat Page

```bash
npm run dev

# Open http://localhost:3000/chat
# Send test message: "Hello"
# Verify response appears
```

#### Step 5.5: Implement Streaming

Update `chatkit.ts` to handle SSE streaming from backend

**Testing**:
- Send message
- Verify tokens stream in real-time
- Check typing indicator appears

**Checkpoint**: Chat interface working, messages sending/receiving

---

### Day 10-11: Split View Layout

**Goal**: Create split-screen layout with chat and task list

#### Step 6.1: Create Layout Components

Create these components (refer to Spec 04):
- `ChatLayout.tsx` - Main container
- `ChatPanel.tsx` - Left side (chat)
- `TaskPanel.tsx` - Right side (tasks)

#### Step 6.2: Implement Responsive Design

Test at different breakpoints:
- Desktop (>1024px): Split view
- Tablet (768-1024px): Split view with smaller task panel
- Mobile (<768px): Full-screen chat with FAB for tasks

#### Step 6.3: Add Mobile Task Overlay

**File**: `src/components/chat/MobileTaskOverlay.tsx`

Implement slide-in task list for mobile

**Checkpoint**: Split view working on all screen sizes

---

### Day 12-13: Real-Time Task Synchronization

**Goal**: Update task list when AI performs operations

#### Step 7.1: Create Sync Hooks

**File**: `src/hooks/useTaskSync.ts`

Implement task fetching and refresh logic

**File**: `src/hooks/useChatEvents.ts`

Implement chat event handling

#### Step 7.2: Connect Chat Events to Task Updates

In `ChatLayout.tsx`:
- Listen for tool execution events
- Refresh task list when tools complete
- Highlight affected tasks

#### Step 7.3: Add Animations

**File**: `src/components/chat/TaskHighlight.tsx`

Implement highlight animations:
- Green border for created tasks
- Blue border for updated tasks
- Fade-out for deleted tasks

#### Step 7.4: Test Real-Time Sync

Manual test:
1. Open chat in split view
2. Say "Add a task to test sync"
3. Verify task appears in right panel immediately
4. Verify task is highlighted (green border)
5. Verify highlight fades after 3 seconds

**Checkpoint**: Real-time sync working, animations smooth

---

### Day 14: Tool Execution Indicators

**Goal**: Show visual feedback for tool execution

#### Step 8.1: Create Tool Execution Indicator

**File**: `src/components/chat/ToolExecutionIndicator.tsx`

Show status badges:
- "Creating task..." (with spinner)
- "✓ Task created" (with checkmark)
- "✗ Failed to create task" (with error icon)

#### Step 8.2: Integrate with Chat Panel

Display indicators above message input

#### Step 8.3: Test Tool Indicators

Send messages that trigger tools:
- "Add a task" → See "Creating task..."
- "Show my tasks" → See "Retrieving tasks..."
- "Delete task 999" → See "✗ Task not found"

**Checkpoint**: Tool execution feedback working

---

## Phase 3: Natural Language & Polish (Days 15-20)

### Day 15-17: Natural Language Testing

**Goal**: Test all conversation patterns from Spec 05

#### Step 9.1: Create Test Conversation Scripts

**File**: `tests/conversation_tests.json`

```json
[
  {
    "name": "Simple task creation",
    "messages": [
      {"user": "Add a task to buy groceries", "expected_tool": "add_task"}
    ]
  },
  {
    "name": "Task with details",
    "messages": [
      {"user": "Create a high priority work task to review report by Friday", "expected_tool": "add_task"}
    ]
  }
  // ... more test cases
]
```

#### Step 9.2: Run Conversation Tests

Test each pattern from Spec 05:
- ✅ Simple creation
- ✅ Creation with details
- ✅ Task retrieval
- ✅ Search
- ✅ Update
- ✅ Completion
- ✅ Deletion
- ✅ Multi-turn conversations
- ✅ Ambiguity resolution
- ✅ Error handling

#### Step 9.3: Refine System Prompt

Based on test results, improve system prompt:
- Add examples for failing patterns
- Clarify tool usage instructions
- Improve error handling guidance

#### Step 9.4: Test Date Parsing

Test all date formats:
- "tomorrow", "next Friday", "in 3 days"
- "at 2 PM", "in the morning"
- "this week", "by Monday"

**Checkpoint**: >90% intent recognition accuracy

---

### Day 18: Error Handling & Edge Cases

**Goal**: Handle all error scenarios gracefully

#### Step 10.1: Test Error Scenarios

- Task not found
- Invalid dates
- Missing required information
- Database errors
- Network failures
- OpenAI API errors

#### Step 10.2: Improve Error Messages

Make error messages:
- User-friendly (no technical jargon)
- Actionable (suggest next steps)
- Specific (explain what went wrong)

#### Step 10.3: Add Retry Mechanisms

- Automatic retry for transient failures
- Manual retry button for permanent failures
- Exponential backoff for rate limits

**Checkpoint**: All error scenarios handled gracefully

---

### Day 19: Performance Optimization

**Goal**: Meet all performance targets

#### Step 11.1: Measure Performance

```bash
# Backend
pytest tests/test_performance.py -v

# Frontend
npm run test:performance
```

#### Step 11.2: Optimize Slow Operations

- Add database indexes for frequent queries
- Cache conversation context
- Optimize task list rendering
- Reduce bundle size

#### Step 11.3: Verify Targets Met

- ✅ First token < 1 second
- ✅ Tool execution < 500ms
- ✅ Task list update < 200ms
- ✅ Full response < 5 seconds
- ✅ Chat page load < 2 seconds

**Checkpoint**: All performance targets met

---

### Day 20: Documentation & Demo

**Goal**: Complete documentation and prepare demo

#### Step 12.1: Update Documentation

- README with setup instructions
- API documentation (tool schemas)
- Conversation examples
- Troubleshooting guide

#### Step 12.2: Create Demo Video

Record demo showing:
1. Simple task creation
2. Task with details (priority, date, category)
3. Search and filter
4. Update task
5. Mark complete
6. Delete task
7. Multi-turn conversation
8. Error handling
9. Mobile view
10. Real-time sync

#### Step 12.3: Final Testing

- Run all test suites
- Manual testing of all features
- Cross-browser testing
- Mobile device testing

**Checkpoint**: Phase 3 complete and ready for submission

---

## Testing Checklist

### Backend Tests

- [ ] All MCP tools execute correctly
- [ ] Tool schemas are valid
- [ ] Agent initializes successfully
- [ ] System prompt loads correctly
- [ ] Chat endpoint responds
- [ ] Streaming works
- [ ] Tool execution integrates with agent
- [ ] Error handling works
- [ ] Performance targets met

### Frontend Tests

- [ ] ChatKit components render
- [ ] Chat page loads
- [ ] Messages send and receive
- [ ] Streaming displays correctly
- [ ] Split view works on desktop
- [ ] Mobile layout works
- [ ] Task list updates in real-time
- [ ] Animations are smooth
- [ ] Tool indicators display
- [ ] Error messages show

### Integration Tests

- [ ] Create task via chat → appears in list
- [ ] Update task via chat → list updates
- [ ] Delete task via chat → removed from list
- [ ] Search via chat → results display
- [ ] Multi-turn conversation works
- [ ] Context retained across messages
- [ ] Ambiguity resolution works
- [ ] Error recovery works

### Natural Language Tests

- [ ] All patterns from Spec 05 work
- [ ] Intent recognition >90% accurate
- [ ] Entity extraction >85% accurate
- [ ] Date parsing >95% accurate
- [ ] Clarification questions work
- [ ] Confirmation for destructive actions

## Deployment Checklist

### Backend Deployment

- [ ] Environment variables set
- [ ] OpenAI API key configured
- [ ] Database connection working
- [ ] CORS configured for frontend
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Health check endpoint working

### Frontend Deployment

- [ ] Environment variables set
- [ ] Chat endpoint URL configured
- [ ] Build succeeds
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Performance optimized

## Troubleshooting

### Common Issues

**"Agent not calling tools"**
- Check system prompt includes tool usage instructions
- Verify tool schemas are registered
- Check OpenAI API logs for errors

**"Streaming not working"**
- Verify SSE headers are set
- Check CORS configuration
- Test with curl first

**"Task list not updating"**
- Check chat events are emitted
- Verify useTaskSync hook is called
- Check browser console for errors

**"Performance is slow"**
- Check database indexes
- Verify caching is enabled
- Profile slow operations

## Success Criteria

Phase 3 is complete when:

- ✅ All 5 specifications implemented
- ✅ All tests passing (backend + frontend)
- ✅ Natural language accuracy >90%
- ✅ Performance targets met
- ✅ No critical bugs
- ✅ Documentation complete
- ✅ Demo video recorded
- ✅ Ready for submission

## Next Steps

After Phase 3 completion:

1. **Submit to Hackathon**: Prepare submission with demo video
2. **Bonus Features**: Implement multi-language or voice commands
3. **User Testing**: Get feedback from real users
4. **Iterate**: Improve based on feedback

---

**Good luck with implementation!** Follow this guide systematically, test frequently, and refer to the specifications for detailed requirements.
