# Phase 3: AI-Powered Todo Chatbot

**Status**: Specification Complete, Ready for Implementation
**Version**: 3.0.0
**Created**: 2026-02-03

## Overview

Phase 3 transforms the todo application into an intelligent, conversational AI-powered system using **Google Gemini API (100% FREE)**, modern chat UI components, and the official MCP (Model Context Protocol) SDK. Users can manage tasks through natural language conversation while seeing real-time updates in a split-screen interface.

**🎉 COMPLETELY FREE - No credit card required!**
- Google Gemini API: 1500 requests/day FREE tier
- No OpenAI subscription needed
- Production-ready AI capabilities at zero cost

## Key Features

### 🤖 Conversational AI Interface
- Natural language task management ("Add a high priority task to review the report by Friday")
- Intelligent intent recognition and entity extraction
- Multi-turn conversations with context retention
- Ambiguity resolution and clarification questions

### 🛠️ Google Gemini Integration
- Gemini 1.5 Flash powered agent with custom system prompts (FREE)
- Function calling via MCP protocol
- Streaming responses for better UX
- Conversation history management
- 1500 free requests per day (no credit card needed)

### 🔧 MCP Tool Integration
- 12+ specialized tools for task management
- Structured tool schemas following MCP standard
- Robust error handling and validation
- Integration with existing Phase 2 CRUD operations

### 💬 Modern Chat UI
- Production-ready chat interface
- Real-time message streaming
- Typing indicators and tool execution status
- Mobile-responsive design
- Custom-built components (no paid dependencies)

### 🔄 Real-Time Task Synchronization
- Split-screen view (chat + task list)
- Instant task list updates when AI performs operations
- Visual highlights and animations for changes
- Optimistic UI updates

## Technology Stack

### Backend (Extends Phase 2)
- **Google Gemini API**: Gemini 1.5 Flash for agent (FREE - 1500 req/day)
- **google-generativeai**: Official Gemini Python SDK
- **Official MCP SDK**: Tool protocol implementation
- **FastAPI**: Chat endpoint with SSE streaming
- **Existing**: SQLModel, PostgreSQL (Neon), Pydantic

**Cost: $0/month** 🎉

### Frontend (Extends Phase 2)
- **Custom Chat UI**: Built with React components (no paid dependencies)
- **Next.js 14+**: App Router, React Server Components
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Styling and animations
- **Existing**: React, Fetch API

**Cost: $0/month** 🎉

## Project Structure

```
phase-3/
├── constitution.md                    # Phase 3 principles and guidelines
├── README.md                          # This file
├── IMPLEMENTATION_GUIDE.md            # Step-by-step implementation
├── specs/                             # Detailed specifications
│   ├── 01-chat-ui-integration.md      # Chat UI setup and configuration
│   ├── 02-gemini-agent-setup.md       # Google Gemini Agent configuration
│   ├── 03-mcp-tools.md                # MCP tool definitions
│   ├── 04-chatbot-ui.md               # UI components and real-time sync
│   └── 05-natural-language-flows.md   # Conversation patterns
├── backend/                           # Backend implementation
│   ├── src/
│   │   ├── ai_agent.py                # Gemini client initialization and management
│   │   ├── mcp_server.py              # MCP server and tool registry
│   │   ├── tools/                     # MCP tool implementations
│   │   │   ├── __init__.py
│   │   │   ├── task_tools.py          # CRUD tools
│   │   │   ├── search_tools.py        # Search and filter tools
│   │   │   └── utility_tools.py       # Helper tools
│   │   ├── routers/
│   │   │   └── chat.py                # Chat endpoint with streaming
│   │   ├── main.py                    # FastAPI app (existing, extended)
│   │   ├── models.py                  # DB models (existing)
│   │   └── crud.py                    # CRUD operations (existing)
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment variables template
│   └── README.md                      # Backend setup instructions
├── frontend/                          # Frontend implementation
│   ├── src/
│   │   ├── app/
│   │   │   └── chat/
│   │   │       └── page.tsx           # Chat page route
│   │   ├── components/
│   │   │   ├── chat/                  # Chat-specific components
│   │   │   │   ├── ChatLayout.tsx     # Split view container
│   │   │   │   ├── ChatPanel.tsx      # Chat side
│   │   │   │   ├── TaskPanel.tsx      # Task list side
│   │   │   │   ├── ToolExecutionIndicator.tsx
│   │   │   │   ├── TaskHighlight.tsx  # Animation wrapper
│   │   │   │   └── MobileTaskOverlay.tsx
│   │   │   ├── TaskList.tsx           # Existing, reused
│   │   │   └── TaskItem.tsx           # Existing, enhanced
│   │   ├── hooks/
│   │   │   ├── useTaskSync.ts         # Real-time task sync
│   │   │   ├── useChatEvents.ts       # Chat event handling
│   │   │   └── useTaskAnimations.ts   # Animation state
│   │   ├── lib/
│   │   │   ├── chat-client.ts         # Chat client configuration
│   │   │   ├── api.ts                 # API client (existing)
│   │   │   └── taskSync.ts            # Sync logic
│   │   └── types/
│   │       └── index.ts               # TypeScript types (existing)
│   ├── package.json                   # Node dependencies
│   ├── .env.local.example             # Environment variables template
│   └── README.md                      # Frontend setup instructions
└── docs/                              # Additional documentation
    ├── CONVERSATION_EXAMPLES.md       # Example conversations
    ├── TOOL_REFERENCE.md              # MCP tool documentation
    └── TROUBLESHOOTING.md             # Common issues and solutions
```

## Quick Start

### Prerequisites

- Phase 2 completed and deployed
- **Google Gemini API key** (FREE - get from https://makersuite.google.com/app/apikey)
  - No credit card required
  - 1500 requests per day free tier
- Node.js 18+ and Python 3.11+
- Existing Phase 2 infrastructure (Neon DB, Vercel)

### Installation

#### 1. Backend Setup

```bash
cd phase-3/backend

# Install dependencies
pip install google-generativeai mcp sse-starlette python-dateutil

# Or use requirements.txt
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
# Get FREE key from: https://makersuite.google.com/app/apikey

# Run backend
uvicorn src.main:app --reload --port 8000
```

#### 2. Frontend Setup

```bash
cd phase-3/frontend

# Install dependencies (no paid packages needed!)
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_CHAT_ENDPOINT

# Run frontend
npm run dev
```

#### 3. Verify Installation

1. Open http://localhost:3000/chat
2. Send a test message: "Add a task to test the chatbot"
3. Verify task appears in the task list (split view)
4. Check that AI responds with confirmation

## Implementation Order

Follow this order for systematic implementation:

### Phase 1: Backend Foundation (Week 1)
1. **MCP Tools** (Spec 03)
   - Implement tool schemas
   - Create tool execution functions
   - Test tools independently
   - Estimated: 2-3 days

2. **Gemini Agent Setup** (Spec 02)
   - Configure Google Gemini client
   - Write system prompt
   - Register MCP tools with function calling
   - Test agent behavior
   - Estimated: 2-3 days

3. **Chat Endpoint** (Spec 02)
   - Create streaming endpoint
   - Integrate Gemini agent and tools
   - Test end-to-end
   - Estimated: 1-2 days

### Phase 2: Frontend Integration (Week 2)
4. **Chat UI Integration** (Spec 01)
   - Build custom chat components
   - Create chat page
   - Implement streaming
   - Test chat UI
   - Estimated: 2-3 days

5. **Chatbot UI** (Spec 04)
   - Build split view layout
   - Implement real-time sync
   - Add animations
   - Test mobile layout
   - Estimated: 2-3 days

### Phase 3: Natural Language & Polish (Week 3)
6. **Natural Language Flows** (Spec 05)
   - Test all conversation patterns
   - Refine system prompt
   - Handle edge cases
   - Improve error messages
   - Estimated: 3-4 days

7. **Testing & Documentation**
   - End-to-end testing
   - Performance optimization
   - Documentation
   - Demo preparation
   - Estimated: 2-3 days

**Total Estimated Time**: 3 weeks (15-20 days)

## Key Capabilities

### Natural Language Commands

Users can interact naturally:

```
✅ "Add a high priority task to review the quarterly report by Friday"
✅ "Show me all my work tasks that are incomplete"
✅ "Reschedule my morning meetings to 2 PM"
✅ "Mark the grocery shopping task as complete"
✅ "What are my high priority tasks for this week?"
✅ "Delete all completed tasks from last month"
✅ "Create a personal task for doctor appointment on Monday at 10 AM"
```

### Intelligent Features

- **Context Retention**: Remembers previous messages in conversation
- **Ambiguity Resolution**: Asks clarifying questions when needed
- **Multi-Step Operations**: Handles complex requests across multiple turns
- **Error Recovery**: Gracefully handles failures with helpful suggestions
- **Confirmation**: Asks before destructive operations (bulk deletes)

## Environment Variables

### Backend (.env)

```bash
# Google Gemini Configuration (FREE - No credit card needed!)
GEMINI_API_KEY=your-api-key-here
# Get FREE key from: https://makersuite.google.com/app/apikey
# Free tier: 1500 requests per day

GEMINI_MODEL=gemini-1.5-flash  # Recommended: fast and free

# Database (from Phase 2)
DATABASE_URL=postgresql://...

# MCP Server (optional)
MCP_SERVER_PORT=3001
```

### Frontend (.env.local)

```bash
# API Endpoints
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENDPOINT=http://localhost:8000/api/chat

# Chat UI Configuration (optional)
NEXT_PUBLIC_CHAT_THEME=default
```

## Testing

### Backend Tests

```bash
cd phase-3/backend

# Run all tests
pytest

# Run specific test suites
pytest tests/test_mcp_tools.py
pytest tests/test_agent.py
pytest tests/test_chat_endpoint.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Frontend Tests

```bash
cd phase-3/frontend

# Run all tests
npm test

# Run specific test suites
npm test -- ChatLayout
npm test -- useTaskSync

# Run E2E tests
npm run test:e2e
```

### Manual Testing

Use the conversation examples in `docs/CONVERSATION_EXAMPLES.md` to manually test all natural language patterns.

## Performance Targets

- **First Token**: < 1 second after user message
- **Tool Execution**: < 500ms per tool
- **Task List Update**: < 200ms after tool completion
- **Full Response**: < 5 seconds (including tool execution)
- **Chat Page Load**: < 2 seconds

## Security Considerations

- ✅ Gemini API key stored in environment variables (never committed)
- ✅ Input validation on all user messages
- ✅ Output sanitization before rendering
- ✅ Rate limiting on chat endpoint
- ✅ CORS configured for frontend domain
- ✅ Conversation isolation (users can't access others' chats)
- ✅ **No credit card required** - completely free tier

## Deployment

### Backend Deployment

Deploy to Railway, Render, or keep local:

```bash
# Railway
railway up

# Render
# Connect GitHub repo and configure environment variables

# Local (for development)
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment

Deploy to Vercel (same as Phase 2):

```bash
# Vercel
vercel --prod

# Set environment variables in Vercel dashboard:
# - NEXT_PUBLIC_CHAT_ENDPOINT
```

## Troubleshooting

### Common Issues

**Issue**: "Gemini API key not found"
- **Solution**: Set `GEMINI_API_KEY` in backend `.env` file
- Get FREE key from: https://makersuite.google.com/app/apikey

**Issue**: "Chat components not rendering"
- **Solution**: Verify all dependencies installed: `npm install`

**Issue**: "Streaming not working"
- **Solution**: Check CORS configuration in FastAPI, ensure SSE headers are set

**Issue**: "Task list not updating"
- **Solution**: Verify chat events are being emitted, check browser console for errors

**Issue**: "Agent not calling tools"
- **Solution**: Check system prompt, verify function declarations are registered correctly with Gemini

See `docs/TROUBLESHOOTING.md` for more details.

## Documentation

- **Constitution**: `constitution.md` - Phase 3 principles and guidelines
- **Specifications**: `specs/` - Detailed feature specifications
- **Implementation Guide**: `IMPLEMENTATION_GUIDE.md` - Step-by-step instructions
- **Conversation Examples**: `docs/CONVERSATION_EXAMPLES.md` - Test conversations
- **Tool Reference**: `docs/TOOL_REFERENCE.md` - MCP tool documentation
- **Troubleshooting**: `docs/TROUBLESHOOTING.md` - Common issues

## Success Criteria

Phase 3 is complete when:

- ✅ All 5 specifications are implemented
- ✅ Users can create, read, update, delete tasks via natural language
- ✅ Agent correctly interprets >90% of user intents
- ✅ Task list updates in real-time when AI performs operations
- ✅ Chat interface works on desktop and mobile
- ✅ All conversation patterns from Spec 05 work correctly
- ✅ Performance targets are met
- ✅ No critical bugs or security issues
- ✅ Documentation is complete
- ✅ Demo video is recorded

## Bonus Features (Optional)

If time permits, implement these bonus features for extra points:

### Multi-Language Support (Urdu) - +100 points
- Detect user language
- Translate prompts and responses
- Support Urdu natural language commands

### Voice Commands - +200 points
- Voice input via Web Speech API
- Voice output via Text-to-Speech
- Hands-free task management

## Contributing

This is a hackathon project. Follow the constitution and specifications strictly. All code must be traceable to a specification.

## License

MIT License - See LICENSE file for details

## Contact

For questions or issues, refer to the specifications or create an issue in the project repository.

---

**Phase 3 Status**: Specification Complete ✅
**Next Step**: Begin implementation following `IMPLEMENTATION_GUIDE.md`
**Estimated Completion**: 3 weeks (15-20 days)
