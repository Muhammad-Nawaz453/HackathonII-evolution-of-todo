# Todo AI Chatbot Constitution - Phase III

## Project Vision

Build an intelligent, conversational AI-powered todo management system that demonstrates excellence in AI agent orchestration, natural language understanding, and seamless integration of modern AI technologies. Transform the Phase II web application into an intuitive chatbot interface where users can manage tasks through natural conversation.

**Phase III Goals:**
- Deliver a conversational AI interface using modern chat UI components
- Implement intelligent agent orchestration with Google Gemini API (FREE - 1500 requests/day)
- Create robust tool integration using Official MCP SDK
- Enable natural language task management (create, update, delete, search)
- Maintain production-ready quality with proper error handling
- Demonstrate clean separation between AI layer, API layer, and data layer
- Support complex multi-step operations through conversation
- Provide real-time feedback and streaming responses
- **Zero cost AI solution** - No credit card required, completely free tier

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**All code is generated from specifications - now including AI agent behavior.**

- Every feature begins with a complete specification document
- Specifications must include: purpose, user stories, acceptance criteria, conversation flows, tool schemas, agent prompts, and error scenarios
- AI Agent specs define system prompts, tool definitions, conversation patterns, and decision logic
- MCP Tool specs define tool schemas, input/output contracts, error handling, and integration points
- ChatKit specs define UI components, message handling, streaming behavior, and state management
- No code is written until the specification is reviewed and approved
- Implementation must match the specification exactly
- Changes to behavior require specification updates first

**Rationale**: In AI-powered systems, specifications serve as contracts between user intent, agent behavior, and tool execution, ensuring predictable AI responses, reliable tool calling, and maintainable conversation flows.

### II. AI-First Architecture & Separation of Concerns

**Each layer has a single, well-defined responsibility with clear AI boundaries.**

#### AI Agent Layer (Google Gemini API)
- **Agent Configuration** (`ai_agent.py`): Gemini client initialization, system prompts, model selection
- **Conversation Management**: Context handling, message history, session state
- **Tool Orchestration**: Function calling with Gemini, parameter extraction, result processing
- **Response Generation**: Natural language responses, streaming, formatting

#### MCP Tool Layer (Official MCP SDK)
- **MCP Server** (`mcp_server.py`): Server initialization, tool registration, request handling
- **Tool Definitions** (`tools/`): Tool schemas, input validation, execution logic
- **Tool Execution**: CRUD operation calls, error handling, result formatting
- **Tool Registry**: Tool discovery, capability advertisement, version management

#### Backend Integration Layer (FastAPI)
- **Chat Router** (`routers/chat.py`): Chat endpoints, request/response handling, streaming
- **Existing CRUD Layer** (`crud.py`): Database operations (unchanged from Phase 2)
- **Existing Models** (`models.py`): Database models (unchanged from Phase 2)
- **Session Management**: Conversation persistence, user context

#### Frontend Chat Layer (Next.js + ChatKit)
- **Chat Interface** (`app/chat/page.tsx`): ChatKit integration, layout, routing
- **Chat Components** (`components/`): Message display, input handling, typing indicators
- **ChatKit Client** (`lib/chatkit.ts`): Backend communication, streaming, state management
- **Task Sync**: Real-time task list updates, optimistic UI updates

#### Architectural Rules
- AI Agent never directly accesses database (uses MCP tools only)
- MCP Tools never contain business logic (delegate to CRUD layer)
- Frontend never calls CRUD endpoints directly for chat operations (uses chat endpoint)
- All AI responses stream to frontend for better UX
- Conversation context maintained server-side, not client-side
- Tool execution results always validated before returning to agent

**Rationale**: Clean AI architecture enables independent testing of agent behavior, tool reliability, and UI responsiveness while maintaining security and data integrity.

### III. Natural Language Understanding Standards

**Agent must accurately interpret user intent and execute appropriate actions.**

#### Intent Recognition Patterns
- **Create Intent**: "add", "create", "new", "make", "schedule"
- **Read Intent**: "show", "list", "get", "what", "find", "search"
- **Update Intent**: "change", "update", "modify", "reschedule", "move"
- **Delete Intent**: "remove", "delete", "cancel", "clear"
- **Complete Intent**: "done", "complete", "finish", "mark"

#### Entity Extraction
- **Task Title**: Main subject of the task (e.g., "review quarterly report")
- **Priority**: "high", "medium", "low", "urgent", "important"
- **Category**: "work", "personal", "shopping", "health", etc.
- **Due Date**: Natural language dates ("Friday", "next Monday", "tomorrow at 2 PM")
- **Time**: Specific times ("10 AM", "2:30 PM", "morning", "afternoon")
- **Status**: "complete", "incomplete", "done", "pending"

#### Ambiguity Handling
- When intent is unclear, ask clarifying questions
- When multiple tasks match, present options to user
- When parameters are missing, prompt for required information
- When dates are ambiguous, confirm interpretation
- When operations affect multiple tasks, confirm before executing

#### Conversation Context
- Remember previous messages in conversation (last 10 messages)
- Reference tasks mentioned earlier ("that task", "the meeting")
- Maintain user preferences within session
- Track multi-step operations across messages

**Rationale**: Accurate natural language understanding is critical for user trust and adoption. The agent must be helpful, not frustrating.

### IV. MCP Tool Design Standards

**Tools must be atomic, reliable, and well-documented.**

#### Tool Schema Requirements
- **Name**: Clear, verb-based naming (e.g., `add_task`, `search_tasks`)
- **Description**: Concise explanation of what the tool does
- **Input Schema**: JSON Schema with all parameters, types, required fields
- **Output Schema**: Structured response format with success/error indicators
- **Examples**: Sample inputs and expected outputs

#### Tool Categories
1. **Task CRUD Tools**
   - `add_task`: Create new task with all parameters
   - `get_task`: Retrieve single task by ID
   - `get_tasks`: Retrieve multiple tasks with filters
   - `update_task`: Modify existing task fields
   - `delete_task`: Remove single task
   - `bulk_delete_tasks`: Remove multiple tasks by filter

2. **Task Status Tools**
   - `mark_task_complete`: Set task status to complete
   - `mark_task_incomplete`: Set task status to incomplete
   - `bulk_mark_complete`: Mark multiple tasks complete

3. **Search & Filter Tools**
   - `search_tasks`: Full-text search across title and description
   - `filter_tasks`: Filter by priority, category, status, date range
   - `get_tasks_by_date`: Get tasks for specific date or date range

4. **Utility Tools**
   - `parse_date`: Convert natural language date to ISO format
   - `get_task_statistics`: Get counts and summaries
   - `validate_task_data`: Validate task parameters before creation

#### Tool Execution Principles
- Each tool does one thing well (single responsibility)
- Tools are idempotent where possible (safe to retry)
- Tools validate inputs before execution
- Tools return structured errors with actionable messages
- Tools log execution for debugging and monitoring
- Tools handle database errors gracefully

#### Tool Response Format
```json
{
  "success": true,
  "data": { /* tool-specific result */ },
  "message": "Human-readable success message",
  "affected_count": 1
}
```

#### Tool Error Format
```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "TASK_NOT_FOUND",
  "details": { /* additional context */ }
}
```

**Rationale**: Well-designed tools enable reliable agent behavior, easier debugging, and maintainable code.

### V. Conversation Flow Design

**Conversations must feel natural, helpful, and efficient.**

#### Conversation Patterns

**Pattern 1: Simple Command**
```
User: "Add a task to buy groceries"
Agent: [Calls add_task]
Agent: "✓ I've added 'Buy groceries' to your task list."
```

**Pattern 2: Command with Details**
```
User: "Create a high priority work task to review the Q1 report by Friday"
Agent: [Calls add_task with priority=high, category=work, due_date=Friday]
Agent: "✓ I've created a high priority work task: 'Review the Q1 report' due Friday."
```

**Pattern 3: Clarification Required**
```
User: "Reschedule the meeting"
Agent: [Calls search_tasks with query="meeting"]
Agent: "I found 3 tasks with 'meeting': 1) Team standup, 2) Client call, 3) Project review. Which one would you like to reschedule?"
User: "The client call"
Agent: "What time should I reschedule the client call to?"
User: "2 PM tomorrow"
Agent: [Calls update_task]
Agent: "✓ I've rescheduled 'Client call' to tomorrow at 2 PM."
```

**Pattern 4: Bulk Operations**
```
User: "Show me all my high priority tasks"
Agent: [Calls filter_tasks with priority=high]
Agent: "You have 4 high priority tasks: 1) Review Q1 report (due Friday), 2) Team standup (due today), 3) Client presentation (due Monday), 4) Budget approval (due next week)."
```

**Pattern 5: Error Handling**
```
User: "Delete task 999"
Agent: [Calls delete_task, receives error]
Agent: "I couldn't find a task with ID 999. Would you like me to show you your current tasks?"
```

#### Response Guidelines
- Start with action confirmation (✓ for success, ✗ for failure)
- Use natural, conversational language (not robotic)
- Provide specific details (task titles, dates, counts)
- Offer next steps or related actions
- Keep responses concise but informative
- Use formatting for readability (lists, bold, etc.)

#### Streaming Behavior
- Stream responses token-by-token for better UX
- Show typing indicator while agent is thinking
- Show tool execution status ("Searching tasks...", "Creating task...")
- Update UI immediately when tools complete
- Handle stream interruptions gracefully

**Rationale**: Natural conversation flows make the AI feel intelligent and helpful, not mechanical.

### VI. ChatKit Integration Standards

**Frontend must provide seamless, responsive chat experience.**

#### ChatKit Components
- **ChatContainer**: Main chat layout, message scrolling, auto-scroll
- **MessageList**: Display conversation history, message bubbles
- **MessageInput**: Text input, send button, keyboard shortcuts
- **TypingIndicator**: Show when agent is processing
- **ToolExecutionIndicator**: Show when tools are running
- **ErrorDisplay**: Show errors inline with retry options

#### Message Types
- **User Message**: User input, right-aligned, distinct styling
- **Agent Message**: AI response, left-aligned, streaming support
- **System Message**: Status updates, tool execution, errors
- **Tool Result**: Structured display of tool outputs (optional)

#### State Management
- **Conversation State**: Message history, current input, loading state
- **Task Sync State**: Real-time task list updates from chat actions
- **Error State**: Error messages, retry mechanisms
- **Session State**: Conversation ID, user context

#### Real-Time Updates
- When agent creates task → update task list immediately
- When agent updates task → highlight changed task
- When agent deletes task → remove from list with animation
- When agent searches → optionally highlight matching tasks

#### Responsive Design
- Mobile-first chat interface
- Split view on desktop (chat left, tasks right)
- Full-screen chat on mobile
- Keyboard shortcuts (Enter to send, Shift+Enter for newline)
- Accessibility (ARIA labels, keyboard navigation)

**Rationale**: ChatKit provides production-ready chat UI, but proper integration is critical for great UX.

### VII. Security & Privacy Standards

**AI systems require additional security considerations.**

#### API Security
- Rate limiting on chat endpoint (prevent abuse)
- Input sanitization before sending to AI
- Output sanitization before rendering (prevent injection)
- API key security (never expose OpenAI key to frontend)
- CORS configured for chat endpoint
- Request size limits (prevent large payloads)

#### AI Safety
- System prompt injection prevention
- User input validation before agent processing
- Tool execution authorization (verify user owns tasks)
- Conversation history limits (prevent context overflow)
- Sensitive data filtering (don't log personal info)
- Graceful degradation when AI service is down

#### Data Privacy
- Conversation history stored server-side only
- Automatic conversation cleanup after session ends
- No conversation data sent to third parties (except OpenAI)
- User consent for AI features (if required)
- Clear data retention policies

#### Tool Security
- Tools validate all inputs before execution
- Tools check user authorization before database operations
- Tools prevent SQL injection (use ORM)
- Tools log execution for audit trail
- Tools rate-limited to prevent abuse

**Rationale**: AI systems introduce new attack vectors. Security must be built-in from the start.

### VIII. Error Handling & Resilience

**AI systems must handle failures gracefully.**

#### Agent Error Handling
- OpenAI API failures → retry with exponential backoff
- Tool execution failures → inform user, suggest alternatives
- Invalid tool calls → log error, ask user to rephrase
- Context overflow → summarize conversation, continue
- Timeout errors → inform user, offer to retry

#### Tool Error Handling
- Database errors → return structured error to agent
- Validation errors → return field-specific errors
- Not found errors → suggest search or list alternatives
- Permission errors → inform user, don't expose details
- Network errors → retry transient failures

#### Frontend Error Handling
- Chat endpoint errors → show error message, retry button
- Streaming errors → reconnect, resume conversation
- Network offline → queue messages, send when online
- Invalid responses → show generic error, log details

#### Error Recovery Patterns
- Automatic retry for transient failures (3 attempts)
- User-initiated retry for permanent failures
- Fallback to simpler operations when complex ones fail
- Clear error messages with actionable next steps
- Graceful degradation (disable chat if AI unavailable)

**Rationale**: Users must trust the AI to handle errors gracefully, not crash or lose data.

### IX. Testing Strategy

**Test AI behavior, tool reliability, and conversation flows.**

#### Agent Testing
- **Unit Tests**: Test tool calling logic, parameter extraction
- **Integration Tests**: Test agent + tools end-to-end
- **Conversation Tests**: Test multi-turn conversations
- **Intent Tests**: Test natural language understanding accuracy
- **Error Tests**: Test error handling and recovery

#### Tool Testing
- **Unit Tests**: Test each tool in isolation with mock database
- **Integration Tests**: Test tools with real database
- **Schema Tests**: Verify tool schemas are valid MCP format
- **Error Tests**: Test all error paths and edge cases
- **Performance Tests**: Test tool execution speed

#### Frontend Testing
- **Component Tests**: Test ChatKit components
- **Integration Tests**: Test chat flow with mock backend
- **Streaming Tests**: Test message streaming behavior
- **Error Tests**: Test error display and retry mechanisms
- **Accessibility Tests**: Test keyboard navigation, screen readers

#### End-to-End Testing
- Test complete user flows (create task via chat → see in list)
- Test complex conversations (multi-step operations)
- Test error scenarios (network failures, invalid inputs)
- Test edge cases (empty lists, bulk operations, ambiguous queries)

#### Test Coverage Goals
- Agent logic: 80%+ coverage
- MCP tools: 90%+ coverage (critical path)
- Frontend components: 70%+ coverage
- All conversation patterns tested
- All error paths tested

**Rationale**: AI systems are non-deterministic, making testing even more critical.

### X. Performance & Scalability

**AI operations must be fast and efficient.**

#### Response Time Targets
- Agent response start (first token): < 1 second
- Tool execution: < 500ms per tool
- Full response completion: < 5 seconds
- Chat endpoint latency: < 200ms (excluding AI processing)

#### Optimization Strategies
- Stream responses token-by-token (don't wait for completion)
- Cache conversation context (avoid re-processing)
- Batch tool calls when possible (bulk operations)
- Use database indexes for tool queries
- Implement connection pooling for database
- Use async operations for I/O-bound tasks

#### Scalability Considerations
- Stateless chat endpoint (enable horizontal scaling)
- Conversation state in Redis or database (not in-memory)
- Rate limiting per user (prevent abuse)
- Queue long-running operations (if needed)
- Monitor OpenAI API usage and costs
- Implement circuit breakers for external services

#### Cost Management
- Use appropriate OpenAI model (GPT-4 vs GPT-3.5)
- Limit conversation context length (last 10 messages)
- Cache common queries and responses
- Monitor token usage per conversation
- Set budget alerts for OpenAI API
- Implement usage quotas per user (if needed)

**Rationale**: AI operations are expensive and slow. Optimization is critical for good UX and cost control.

## Technology Stack

### AI & Agent Layer
- **AI Platform**: OpenAI API (GPT-4 or GPT-3.5-turbo)
- **Agent Framework**: OpenAI Agents SDK (latest)
- **Tool Protocol**: Official MCP SDK (Model Context Protocol)
- **Streaming**: Server-Sent Events (SSE) or WebSocket

### Backend (Extends Phase 2)
- **Framework**: FastAPI 0.109+ (existing)
- **ORM**: SQLModel 0.0.14+ (existing)
- **Database**: PostgreSQL via Neon (existing)
- **New Dependencies**:
  - `openai` (latest) - OpenAI API client
  - `mcp` (latest) - Official MCP SDK
  - `sse-starlette` - Server-Sent Events for streaming

### Frontend (Extends Phase 2)
- **Framework**: Next.js 14+ (existing)
- **Language**: TypeScript 5+ (existing)
- **Styling**: Tailwind CSS 3+ (existing)
- **New Dependencies**:
  - `@openai/chatkit` - OpenAI ChatKit components
  - `eventsource` or `fetch` - SSE client for streaming

### Infrastructure (Same as Phase 2)
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway, Render, or local
- **Database**: Neon Serverless PostgreSQL

## Non-Negotiable Constraints

### Technical Constraints
1. **OpenAI ChatKit Required**: Must use official ChatKit (not custom chat UI)
2. **OpenAI Agents SDK Required**: Must use Agents SDK (not just completion API)
3. **Official MCP SDK Required**: Must use MCP for tool integration
4. **Streaming Required**: All AI responses must stream
5. **Real-Time Sync**: Task list must update when chat modifies tasks
6. **Natural Language**: Must support complex natural language commands

### Development Constraints
1. **Specification First**: No code without a spec (agent, tools, UI)
2. **Tool Schema First**: Define MCP tool schemas before implementation
3. **Conversation Flow First**: Design conversation patterns before coding
4. **One Feature at a Time**: Complete each spec fully before starting next
5. **Version Control**: Commit after each completed feature

### AI Behavior Constraints
1. **Accuracy**: Agent must correctly interpret user intent (>90% accuracy)
2. **Reliability**: Tools must execute successfully (>95% success rate)
3. **Clarity**: Agent responses must be clear and actionable
4. **Safety**: Agent must not execute destructive operations without confirmation
5. **Transparency**: Agent must explain what it's doing (tool execution feedback)

## Development Workflow

### Feature Development Cycle

1. **Specify**: Write complete specification in `specs/` directory
   - Agent behavior specs (system prompts, conversation patterns)
   - MCP tool specs (schemas, execution logic, error handling)
   - ChatKit integration specs (UI components, streaming, state management)

2. **Tool Schema First**: Define MCP tool schemas
   - Document in tool spec
   - Review and approve before implementation
   - Validate against MCP SDK requirements

3. **Backend First**: Implement MCP server and tools
   - Create MCP server with tool registration
   - Implement tool execution logic
   - Test tools independently with mock agent
   - Verify all tool schemas are valid

4. **Agent Second**: Configure OpenAI Agent
   - Write system prompt
   - Register MCP tools with agent
   - Test agent behavior with sample conversations
   - Verify tool calling accuracy

5. **Chat Endpoint Third**: Implement FastAPI chat router
   - Create streaming endpoint
   - Integrate agent and tools
   - Handle conversation state
   - Test end-to-end with API client

6. **Frontend Last**: Implement ChatKit UI
   - Integrate ChatKit components
   - Connect to chat endpoint
   - Implement streaming and state management
   - Test user interactions

7. **Integration**: Test full stack together
   - Test all conversation patterns
   - Verify task list sync
   - Test error handling end-to-end
   - Check edge cases and ambiguous queries

8. **Document**: Update README files
   - Agent configuration documentation
   - MCP tool documentation
   - ChatKit integration guide
   - Conversation examples

9. **Commit**: Create atomic commits with clear messages
   - Separate commits for tools, agent, chat endpoint, frontend
   - Reference specification in commit message

### Specification Template

Each specification must include:

- **Feature Name**: Clear, descriptive title
- **Purpose**: Why this feature exists
- **User Stories**: Who needs this and why
- **Acceptance Criteria**: Testable conditions for success
- **Conversation Flows**: Example conversations with expected behavior
- **Tool Schemas** (Tool specs): MCP schema, input/output, error handling
- **Agent Prompts** (Agent specs): System prompt, instructions, examples
- **UI Components** (Frontend specs): ChatKit integration, message handling
- **Edge Cases**: Ambiguous queries, error scenarios, multi-step operations
- **Dependencies**: What other features/specs this relies on

## Success Metrics

A feature is successful when:

1. Specification is complete and unambiguous
2. Tool schemas are valid and documented
3. Agent correctly interprets natural language (>90% accuracy)
4. Tools execute reliably (>95% success rate)
5. All acceptance criteria pass
6. All conversation patterns work as expected
7. All edge cases are handled gracefully
8. Code is clean, typed, and documented
9. User experience is natural and helpful
10. No regressions in existing features (Phase 2 still works)
11. Feature is deployed and accessible

## Project Constraints Summary

**DO:**
- Write specifications before code (agent, tools, UI)
- Define tool schemas first (MCP format)
- Design conversation flows before implementation
- Use OpenAI ChatKit, Agents SDK, and MCP SDK
- Stream all AI responses for better UX
- Validate inputs at every layer
- Handle errors gracefully with clear messages
- Test agent behavior thoroughly
- Document conversation patterns
- Sync task list in real-time
- Monitor AI costs and performance

**DON'T:**
- Write code without a specification
- Use custom chat UI instead of ChatKit
- Use completion API instead of Agents SDK
- Skip tool schema validation
- Block on AI responses (always stream)
- Expose OpenAI API key to frontend
- Execute destructive operations without confirmation
- Ignore ambiguous user queries
- Skip error handling for AI failures
- Hardcode conversation patterns
- Ignore AI costs and token usage

## Governance

### Constitution Authority
- This constitution supersedes all other development practices for Phase III
- When in doubt, refer to this document
- Deviations require explicit justification and documentation
- All code reviews must verify constitutional compliance
- Phase II constitution still applies to non-AI features

### Amendment Process
1. Propose amendment with rationale
2. Document impact on existing code
3. Update constitution with version increment
4. Update all affected specifications
5. Refactor code to comply with new rules

### Enforcement
- Every pull request must pass constitutional review
- Violations must be fixed before merge
- Repeated violations indicate specification gaps
- Constitution is living document - update as needed

---

**Version**: 3.0.0
**Ratified**: 2026-02-03
**Last Amended**: 2026-02-03
**Next Review**: After Phase III completion
**Supersedes**: Constitution v2.0.0 (Phase II)
**Extends**: Phase II architecture and principles
