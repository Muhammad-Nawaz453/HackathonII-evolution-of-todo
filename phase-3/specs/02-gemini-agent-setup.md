# Specification: Google Gemini Agent Setup

**Feature ID**: PHASE3-02
**Status**: Draft
**Created**: 2026-02-03
**Updated**: 2026-02-08 (Migrated to Google Gemini - FREE)
**Dependencies**: Phase 2 (FastAPI backend), Phase 3 Spec 03 (MCP Tools)

## Purpose

Configure and initialize the Google Gemini API to create an intelligent AI agent that can understand natural language todo management commands, orchestrate tool calls via MCP function calling, and generate helpful conversational responses. The agent serves as the brain of the chatbot, interpreting user intent and coordinating actions.

**🎉 100% FREE Solution:**
- Google Gemini API: 1500 requests/day free tier
- No credit card required
- Production-ready AI capabilities at zero cost

## User Stories

**As a user**, I want to:
1. Communicate with an AI that understands my todo management needs in natural language
2. Have the AI correctly interpret my intent (create, read, update, delete tasks)
3. Receive clear, conversational responses that confirm what the AI did
4. Get helpful suggestions when my request is ambiguous
5. Trust that the AI will ask for confirmation before destructive operations

**As a developer**, I want to:
1. Configure the Google Gemini client with appropriate system prompts
2. Register MCP tools with Gemini using function calling
3. Handle conversation context and message history
4. Stream agent responses to the frontend
5. Monitor agent behavior and function calling accuracy
6. Debug agent decisions and tool selections
7. Use a completely free solution with no credit card required

## Acceptance Criteria

### AC1: Gemini Client Initialization
- [ ] Google Generative AI SDK installed (`google-generativeai` package)
- [ ] Gemini client initialized with gemini-1.5-flash model (FREE)
- [ ] Client configuration includes system instruction
- [ ] Client configuration includes temperature and other parameters
- [ ] Client initialization happens at application startup
- [ ] Client initialization errors are caught and logged
- [ ] API key validation on startup

### AC2: System Prompt Design
- [ ] System prompt defines agent role (todo management assistant)
- [ ] System prompt includes instructions for tool usage
- [ ] System prompt defines response format guidelines
- [ ] System prompt includes examples of good responses
- [ ] System prompt instructs agent to ask for clarification when needed
- [ ] System prompt instructs agent to confirm destructive operations
- [ ] System prompt is version-controlled and documented

### AC3: Function Declaration Registration
- [ ] All MCP tools registered as Gemini function declarations
- [ ] Function schemas properly formatted for Gemini function calling
- [ ] Function descriptions are clear and accurate
- [ ] Agent can discover available functions
- [ ] Agent can call functions with correct parameters
- [ ] Function call results are properly returned to agent
- [ ] Function declarations follow Gemini's schema format

### AC4: Conversation Context Management
- [ ] Agent maintains conversation history (last 10 messages)
- [ ] Context includes user messages and agent responses
- [ ] Context includes tool calls and results
- [ ] Context is stored per conversation ID
- [ ] Old conversations are cleaned up (after 24 hours)
- [ ] Context size is limited to prevent token overflow

### AC5: Response Generation
- [ ] Agent generates natural, conversational responses
- [ ] Responses confirm actions taken
- [ ] Responses include relevant details (task titles, counts, etc.)
- [ ] Responses are concise but informative
- [ ] Responses use markdown formatting when appropriate
- [ ] Responses stream token-by-token to frontend

### AC6: Error Handling
- [ ] Gemini API errors are caught and handled gracefully
- [ ] Function execution errors are communicated to user
- [ ] Invalid function calls are logged and recovered from
- [ ] Rate limit errors trigger exponential backoff (1500 req/day limit)
- [ ] Timeout errors show helpful message to user
- [ ] All errors are logged with context for debugging
- [ ] Free tier quota exceeded errors handled gracefully

### AC7: Streaming Support
- [ ] Agent responses stream via Server-Sent Events (SSE)
- [ ] Streaming starts within 1 second of request
- [ ] Streaming handles interruptions gracefully
- [ ] Streaming includes tool execution status updates
- [ ] Streaming completes with [DONE] signal

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
├─────────────────────────────────────────────────────────┤
│  /src/agent_setup.py                                    │
│  ├── AgentManager                                       │
│  │   ├── initialize_agent()                             │
│  │   ├── get_agent()                                    │
│  │   └── cleanup()                                      │
│  ├── ConversationManager                                │
│  │   ├── get_context(conversation_id)                   │
│  │   ├── add_message(conversation_id, message)          │
│  │   └── cleanup_old_conversations()                    │
│  └── StreamingHandler                                   │
│      ├── stream_response(agent, message, context)       │
│      └── format_sse_event(data)                         │
├─────────────────────────────────────────────────────────┤
│  /src/routers/chat.py                                   │
│  └── POST /api/chat                                     │
│      ├── Validate request                               │
│      ├── Get conversation context                       │
│      ├── Call agent with message + context              │
│      ├── Stream response via SSE                        │
│      └── Update conversation history                    │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Google Gemini API (FREE)                    │
│  ├── Model: gemini-1.5-flash                           │
│  ├── System Instruction                                 │
│  ├── Function Declarations (MCP Tools)                  │
│  ├── Function Calling                                   │
│  └── Response Streaming                                 │
│  └── Free Tier: 1500 requests/day                      │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Calls
                          ▼
┌────────────────────────────────────────────────────────┐
│              MCP Server (Phase 3 Spec 03)               │
│  └── Task Management Tools                              │
└─────────────────────────────────────────────────────────┘
```

### Gemini Client Configuration

**File**: `backend/src/ai_agent.py`

```python
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import os
from datetime import datetime, timedelta

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System instruction for the todo management agent
SYSTEM_INSTRUCTION = """You are an intelligent todo management assistant. Your role is to help users manage their tasks through natural conversation.

**Your Capabilities:**
- Create new tasks with details (title, priority, category, due date)
- Search and retrieve tasks based on various criteria
- Update existing tasks (change title, priority, due date, etc.)
- Mark tasks as complete or incomplete
- Delete tasks (with user confirmation for bulk operations)
- Provide task statistics and summaries

**Guidelines:**
1. **Be Conversational**: Use natural, friendly language. Avoid robotic responses.
2. **Be Specific**: When confirming actions, include task details (title, due date, priority).
3. **Ask for Clarification**: If the user's request is ambiguous, ask clarifying questions.
4. **Confirm Destructive Actions**: Before deleting multiple tasks, confirm with the user.
5. **Use Tools Appropriately**: Call the right tool for each task. Don't guess - use search tools when needed.
6. **Handle Errors Gracefully**: If a tool fails, explain the issue and suggest alternatives.
7. **Be Concise**: Keep responses brief but informative. Use bullet points for lists.
8. **Use Formatting**: Use markdown for better readability (bold, lists, etc.).

**Response Format:**
- Start with action confirmation: ✓ for success, ✗ for failure
- Include specific details: task titles, counts, dates
- Offer next steps or related actions when appropriate
- Use lists for multiple items

**Examples:**

User: "Add a task to buy groceries"
You: "✓ I've added 'Buy groceries' to your task list."

User: "Show me my high priority tasks"
You: [Call filter_tasks with priority=high]
You: "You have 3 high priority tasks:
1. Review Q1 report (due Friday)
2. Team standup (due today)
3. Client presentation (due Monday)"

User: "Reschedule the meeting to 2 PM"
You: [Call search_tasks with query="meeting"]
You: "I found 2 tasks with 'meeting': 1) Team standup, 2) Client call. Which one would you like to reschedule?"

**Important:**
- Always use tools to interact with tasks (never make up data)
- Parse natural language dates correctly (use parse_date tool if needed)
- When multiple tasks match, present options to the user
- Never execute bulk deletes without explicit confirmation
"""

class AgentManager:
    """Manages the OpenAI Agent instance and configuration."""

    def __init__(self):
        self.client: Optional[OpenAI] = None
        self.model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.temperature: float = 0.7
        self.max_tokens: int = 500
        self.tools: List[Dict[str, Any]] = []

    def initialize(self, tools: List[Dict[str, Any]]):
        """Initialize the OpenAI client and register tools.

        Args:
            tools: List of MCP tool schemas in OpenAI function format
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.tools = tools

        print(f"✓ Agent initialized with model: {self.model}")
        print(f"✓ Registered {len(self.tools)} tools")

    def get_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        if not self.client:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        return self.client

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = True
    ):
        """Generate a response from the agent.

        Args:
            messages: Conversation history (system + user messages)
            stream: Whether to stream the response

        Yields:
            Response chunks if streaming, else returns full response
        """
        client = self.get_client()

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=stream
            )

            if stream:
                async for chunk in response:
                    yield chunk
            else:
                return response

        except Exception as e:
            print(f"Error generating response: {e}")
            raise


class ConversationManager:
    """Manages conversation history and context."""

    def __init__(self, max_history: int = 10, cleanup_hours: int = 24):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.max_history = max_history
        self.cleanup_hours = cleanup_hours
        self.last_cleanup = datetime.now()

    def get_context(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get conversation context for a given conversation ID.

        Args:
            conversation_id: Unique conversation identifier

        Returns:
            List of messages (system prompt + history)
        """
        # Always start with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history if exists
        if conversation_id in self.conversations:
            history = self.conversations[conversation_id]
            # Limit to last N messages
            messages.extend(history[-self.max_history:])

        return messages

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict]] = None
    ):
        """Add a message to conversation history.

        Args:
            conversation_id: Unique conversation identifier
            role: Message role (user, assistant, tool)
            content: Message content
            tool_calls: Optional tool calls made by assistant
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        if tool_calls:
            message["tool_calls"] = tool_calls

        self.conversations[conversation_id].append(message)

        # Trigger cleanup if needed
        self._maybe_cleanup()

    def _maybe_cleanup(self):
        """Clean up old conversations periodically."""
        now = datetime.now()
        if (now - self.last_cleanup).total_seconds() > 3600:  # Every hour
            self.cleanup_old_conversations()
            self.last_cleanup = now

    def cleanup_old_conversations(self):
        """Remove conversations older than cleanup_hours."""
        cutoff = datetime.now() - timedelta(hours=self.cleanup_hours)

        to_remove = []
        for conv_id, messages in self.conversations.items():
            if not messages:
                to_remove.append(conv_id)
                continue

            last_message = messages[-1]
            last_time = datetime.fromisoformat(last_message["timestamp"])

            if last_time < cutoff:
                to_remove.append(conv_id)

        for conv_id in to_remove:
            del self.conversations[conv_id]

        if to_remove:
            print(f"Cleaned up {len(to_remove)} old conversations")


# Global instances
agent_manager = AgentManager()
conversation_manager = ConversationManager()


def initialize_agent(tools: List[Dict[str, Any]]):
    """Initialize the agent with MCP tools.

    This should be called at application startup.

    Args:
        tools: List of MCP tool schemas
    """
    agent_manager.initialize(tools)


def get_agent_manager() -> AgentManager:
    """Get the global agent manager instance."""
    return agent_manager


def get_conversation_manager() -> ConversationManager:
    """Get the global conversation manager instance."""
    return conversation_manager
```

### Streaming Handler

**File**: `backend/src/agent_setup.py` (continued)

```python
from typing import AsyncGenerator
import json

class StreamingHandler:
    """Handles streaming responses from the agent."""

    @staticmethod
    def format_sse_event(event_type: str, data: Any) -> str:
        """Format data as Server-Sent Event.

        Args:
            event_type: Type of event (token, tool_call, done, error)
            data: Event data

        Returns:
            Formatted SSE string
        """
        return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

    @staticmethod
    async def stream_agent_response(
        agent: AgentManager,
        messages: List[Dict[str, str]],
        tool_executor: Any  # MCP tool executor
    ) -> AsyncGenerator[str, None]:
        """Stream agent response with tool execution.

        Args:
            agent: Agent manager instance
            messages: Conversation messages
            tool_executor: MCP tool executor for function calls

        Yields:
            SSE-formatted events
        """
        try:
            # Start streaming from agent
            response_text = ""
            tool_calls = []

            async for chunk in agent.generate_response(messages, stream=True):
                delta = chunk.choices[0].delta

                # Handle text content
                if delta.content:
                    response_text += delta.content
                    yield StreamingHandler.format_sse_event(
                        "token",
                        {"token": delta.content}
                    )

                # Handle tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        tool_calls.append(tool_call)

                        # Notify frontend about tool execution
                        yield StreamingHandler.format_sse_event(
                            "tool_call",
                            {
                                "tool": tool_call.function.name,
                                "status": "executing"
                            }
                        )

                        # Execute tool
                        try:
                            tool_result = await tool_executor.execute(
                                tool_call.function.name,
                                json.loads(tool_call.function.arguments)
                            )

                            # Notify success
                            yield StreamingHandler.format_sse_event(
                                "tool_call",
                                {
                                    "tool": tool_call.function.name,
                                    "status": "completed",
                                    "result": tool_result
                                }
                            )

                            # Add tool result to messages and continue
                            messages.append({
                                "role": "assistant",
                                "content": None,
                                "tool_calls": [tool_call]
                            })
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result)
                            })

                            # Get agent's response to tool result
                            async for follow_up_chunk in agent.generate_response(
                                messages,
                                stream=True
                            ):
                                follow_up_delta = follow_up_chunk.choices[0].delta
                                if follow_up_delta.content:
                                    response_text += follow_up_delta.content
                                    yield StreamingHandler.format_sse_event(
                                        "token",
                                        {"token": follow_up_delta.content}
                                    )

                        except Exception as tool_error:
                            # Notify tool execution failure
                            yield StreamingHandler.format_sse_event(
                                "tool_call",
                                {
                                    "tool": tool_call.function.name,
                                    "status": "failed",
                                    "error": str(tool_error)
                                }
                            )

            # Send completion signal
            yield StreamingHandler.format_sse_event("done", {"message": "complete"})

        except Exception as e:
            # Send error event
            yield StreamingHandler.format_sse_event(
                "error",
                {"error": str(e), "type": type(e).__name__}
            )


# Export streaming handler
streaming_handler = StreamingHandler()
```

### Chat Router Integration

**File**: `backend/src/routers/chat.py`

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import logging

from ..agent_setup import (
    get_agent_manager,
    get_conversation_manager,
    streaming_handler
)
from ..mcp_server import get_tool_executor

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: list = []


@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with streaming support.

    Args:
        request: Chat request with message and optional conversation ID

    Returns:
        StreamingResponse with SSE events
    """
    try:
        # Get managers
        agent = get_agent_manager()
        conv_manager = get_conversation_manager()
        tool_executor = get_tool_executor()

        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{int(time.time())}"

        # Get conversation context
        messages = conv_manager.get_context(conversation_id)

        # Add user message
        messages.append({"role": "user", "content": request.message})
        conv_manager.add_message(conversation_id, "user", request.message)

        # Stream response
        async def event_generator():
            async for event in streaming_handler.stream_agent_response(
                agent,
                messages,
                tool_executor
            ):
                yield event

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

## System Prompt Design Principles

### 1. Role Definition
- Clearly state the agent's role and purpose
- Define boundaries (what it can and cannot do)
- Set expectations for behavior

### 2. Capability Description
- List all available tools and their purposes
- Explain when to use each tool
- Provide examples of tool usage

### 3. Response Guidelines
- Define response format and style
- Specify when to ask for clarification
- Set rules for confirmation (destructive operations)

### 4. Examples
- Include example conversations
- Show good and bad responses
- Demonstrate tool calling patterns

### 5. Error Handling
- Instruct how to handle tool failures
- Define fallback behaviors
- Specify error message format

## Edge Cases and Error Handling

### Edge Case 1: OpenAI API Rate Limit
**Scenario**: Too many requests to OpenAI API
**Handling**:
- Catch rate limit error (429 status)
- Implement exponential backoff (1s, 2s, 4s)
- Return friendly error message to user
- Log rate limit events for monitoring

### Edge Case 2: Invalid Tool Call
**Scenario**: Agent calls tool with invalid parameters
**Handling**:
- Validate tool parameters before execution
- Return structured error to agent
- Agent reformulates request or asks user for clarification
- Log invalid tool calls for prompt improvement

### Edge Case 3: Context Overflow
**Scenario**: Conversation history exceeds token limit
**Handling**:
- Summarize older messages
- Keep only last 10 messages
- Preserve system prompt always
- Warn user if context is truncated

### Edge Case 4: Tool Execution Timeout
**Scenario**: Tool takes > 10 seconds to execute
**Handling**:
- Set timeout on tool execution
- Return timeout error to agent
- Agent informs user and suggests retry
- Log slow tool executions

### Edge Case 5: Ambiguous User Intent
**Scenario**: User message is unclear or has multiple interpretations
**Handling**:
- Agent asks clarifying questions
- Provide options for user to choose
- Don't guess or assume intent
- Example: "Did you mean X or Y?"

### Edge Case 6: No Tools Available
**Scenario**: MCP server is down or tools not registered
**Handling**:
- Agent initialization fails gracefully
- Return error to user explaining issue
- Provide fallback (basic chat without tools)
- Alert developers via logging

## Dependencies

### External Dependencies
- `openai` (latest version) - OpenAI Python SDK
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

### Internal Dependencies
- Phase 3 Spec 03: MCP Tools (tool schemas and executor)
- Phase 2: FastAPI backend (existing infrastructure)

## Testing Requirements

### Unit Tests
- [ ] Agent initialization with valid/invalid API key
- [ ] System prompt loading and formatting
- [ ] Conversation context management (add, retrieve, cleanup)
- [ ] Message history limiting (max 10 messages)
- [ ] SSE event formatting

### Integration Tests
- [ ] Agent generates response for simple query
- [ ] Agent calls tools correctly
- [ ] Agent handles tool execution errors
- [ ] Streaming works end-to-end
- [ ] Conversation context persists across messages

### Behavior Tests
- [ ] Agent interprets "add task" intent correctly
- [ ] Agent interprets "show tasks" intent correctly
- [ ] Agent asks for clarification when needed
- [ ] Agent confirms before bulk delete
- [ ] Agent handles ambiguous dates correctly

### Error Tests
- [ ] OpenAI API error handling (rate limit, timeout, invalid key)
- [ ] Tool execution error handling
- [ ] Invalid tool call recovery
- [ ] Context overflow handling
- [ ] Network error handling

## Performance Requirements

- **Agent Initialization**: < 1 second at startup
- **First Token**: < 1 second after user message
- **Tool Execution**: < 500ms per tool call
- **Context Retrieval**: < 50ms
- **Memory Usage**: < 100MB per conversation
- **Conversation Cleanup**: Runs every hour, < 1 second

## Security Considerations

- **API Key Security**: Store in environment variable, never commit
- **Input Validation**: Validate user messages before sending to agent
- **Output Sanitization**: Sanitize agent responses before sending to frontend
- **Rate Limiting**: Implement per-user rate limits
- **Conversation Isolation**: Ensure users can't access others' conversations
- **Logging**: Log agent decisions but not sensitive user data

## Documentation Requirements

- [ ] README with agent setup instructions
- [ ] System prompt documentation and versioning
- [ ] Tool registration guide
- [ ] Conversation management guide
- [ ] Troubleshooting guide for common issues
- [ ] Example conversations for testing

## Success Metrics

- Agent initializes successfully at startup
- Agent generates responses within 1 second (first token)
- Agent calls tools with >90% accuracy
- Agent handles errors gracefully (no crashes)
- Conversation context persists correctly
- Streaming works without interruptions
- System prompt produces helpful, conversational responses

## Future Enhancements (Out of Scope for Phase 3)

- Multi-agent orchestration (specialized agents for different tasks)
- Agent memory (long-term user preferences)
- Agent learning (fine-tuning on user interactions)
- Multi-modal support (images, voice)
- Agent analytics dashboard
- A/B testing different system prompts

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: High
**Implementation Order**: 2 of 5 (implement after MCP tools are defined)
