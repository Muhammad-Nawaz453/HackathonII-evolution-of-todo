# Specification: Custom Chat UI Integration

**Feature ID**: PHASE3-01
**Status**: Draft
**Created**: 2026-02-03
**Updated**: 2026-02-08 (Migrated to free alternatives)
**Dependencies**: Phase 2 (Next.js frontend)

## Purpose

Build a custom chat UI in the Next.js frontend to provide a production-ready, conversational interface for todo management. Using custom React components with Tailwind CSS, we create a clean chat interface without paid dependencies, integrating seamlessly with the Google Gemini-powered backend.

## User Stories

**As a user**, I want to:
1. Access a chat interface where I can type natural language commands
2. See my messages and the AI's responses in a clean, familiar chat layout
3. See typing indicators when the AI is processing my request
4. See real-time streaming of AI responses (not wait for full response)
5. Navigate between the chat interface and traditional task list view
6. Use the chat on both desktop and mobile devices

**As a developer**, I want to:
1. Build custom chat components using React and Tailwind CSS (no paid dependencies)
2. Configure chat client to connect to our FastAPI chat endpoint
3. Handle streaming responses from the backend
4. Manage conversation state and message history
5. Integrate chat actions with the existing task list UI
6. Keep the solution 100% free with no external paid services

## Acceptance Criteria

### AC1: Custom Chat Components Setup
- [ ] Custom chat components built with React and Tailwind CSS
- [ ] Chat client configured with backend chat endpoint URL
- [ ] Chat UI styled to match app design (consistent with Phase 2)
- [ ] Chat components render without errors
- [ ] No console errors or warnings
- [ ] No paid dependencies required

### AC2: Chat Page Route
- [ ] New route created at `/chat` in Next.js App Router
- [ ] Chat page accessible via navigation from main task list
- [ ] Chat page has proper layout (header, chat container, footer)
- [ ] Chat page is responsive (mobile and desktop)
- [ ] Chat page loads quickly (< 2 seconds)

### AC3: Message Display
- [ ] User messages display on the right side with distinct styling
- [ ] AI messages display on the left side with distinct styling
- [ ] Messages show timestamps
- [ ] Messages support markdown formatting (bold, lists, etc.)
- [ ] Long messages wrap properly and don't overflow
- [ ] Message list auto-scrolls to bottom when new message arrives
- [ ] User can manually scroll up to view history

### AC4: Message Input
- [ ] Text input field at bottom of chat
- [ ] Send button next to input field
- [ ] Enter key sends message
- [ ] Shift+Enter creates new line in message
- [ ] Input field clears after sending message
- [ ] Input field disabled while AI is responding
- [ ] Input field shows placeholder text ("Ask me to manage your tasks...")
- [ ] Input field has character limit (1000 characters)

### AC5: Streaming Responses
- [ ] AI responses stream token-by-token (not all at once)
- [ ] Typing indicator shows while AI is thinking
- [ ] Streaming starts within 1 second of sending message
- [ ] Streaming handles network interruptions gracefully
- [ ] Streaming can be cancelled by user (optional)

### AC6: Loading and Error States
- [ ] Loading spinner shows while waiting for first token
- [ ] Error messages display inline in chat when requests fail
- [ ] Retry button available for failed messages
- [ ] Network offline state handled gracefully
- [ ] Timeout errors show helpful message

### AC7: Conversation History
- [ ] Conversation persists during session (page refresh clears)
- [ ] Up to 50 messages displayed in history
- [ ] Older messages can be scrolled to view
- [ ] Conversation history loads on page load (if session exists)

### AC8: Mobile Responsiveness
- [ ] Chat interface works on mobile devices (320px width minimum)
- [ ] Touch scrolling works smoothly
- [ ] Virtual keyboard doesn't cover input field
- [ ] Messages are readable on small screens
- [ ] Send button is easily tappable (44px minimum)

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                      │
├─────────────────────────────────────────────────────────┤
│  /app/chat/page.tsx                                     │
│  ├── ChatContainer (ChatKit)                            │
│  │   ├── MessageList (ChatKit)                          │
│  │   │   ├── UserMessage (ChatKit)                      │
│  │   │   └── AgentMessage (ChatKit)                     │
│  │   ├── TypingIndicator (ChatKit)                      │
│  │   └── MessageInput (ChatKit)                         │
│  └── ChatKitProvider (ChatKit)                          │
├─────────────────────────────────────────────────────────┤
│  /lib/chatkit.ts                                        │
│  ├── ChatKit Configuration                              │
│  ├── Backend API Integration                            │
│  ├── Streaming Handler                                  │
│  └── Error Handler                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTP POST /api/chat
                          │ Server-Sent Events (SSE)
                          ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Phase 3)                   │
│              /api/chat endpoint                          │
└─────────────────────────────────────────────────────────┘
```

### ChatKit Configuration

**File**: `frontend/src/lib/chatkit.ts`

```typescript
import { ChatKitProvider, ChatKitConfig } from '@openai/chatkit';

export const chatKitConfig: ChatKitConfig = {
  // Backend endpoint for chat
  apiEndpoint: process.env.NEXT_PUBLIC_CHAT_ENDPOINT || 'http://localhost:8000/api/chat',

  // Streaming configuration
  streaming: true,
  streamingProtocol: 'sse', // Server-Sent Events

  // Message configuration
  maxMessageLength: 1000,
  maxHistoryLength: 50,

  // UI configuration
  theme: {
    primaryColor: '#3b82f6', // Tailwind blue-500
    userMessageBg: '#3b82f6',
    agentMessageBg: '#f3f4f6', // Tailwind gray-100
    fontFamily: 'Inter, system-ui, sans-serif',
  },

  // Error handling
  retryAttempts: 3,
  retryDelay: 1000, // ms

  // Accessibility
  ariaLabels: {
    messageInput: 'Type your message',
    sendButton: 'Send message',
    messageList: 'Conversation history',
  },
};

export function createChatKitClient() {
  return new ChatKitProvider(chatKitConfig);
}
```

### Chat Page Component

**File**: `frontend/src/app/chat/page.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import { ChatKitProvider, ChatContainer, MessageList, MessageInput } from '@openai/chatkit';
import { chatKitConfig } from '@/lib/chatkit';
import Link from 'next/link';

export default function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null);

  useEffect(() => {
    // Generate or retrieve conversation ID
    const sessionId = sessionStorage.getItem('conversationId') || generateId();
    sessionStorage.setItem('conversationId', sessionId);
    setConversationId(sessionId);
  }, []);

  if (!conversationId) {
    return <div>Loading chat...</div>;
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <h1 className="text-xl font-semibold">AI Todo Assistant</h1>
          <Link
            href="/"
            className="text-blue-600 hover:text-blue-700 text-sm"
          >
            View Tasks
          </Link>
        </div>
      </header>

      {/* Chat Container */}
      <main className="flex-1 overflow-hidden">
        <ChatKitProvider config={chatKitConfig}>
          <ChatContainer
            conversationId={conversationId}
            className="h-full max-w-4xl mx-auto"
          >
            <MessageList
              className="flex-1 overflow-y-auto px-4 py-6"
              emptyStateMessage="👋 Hi! I'm your AI todo assistant. Ask me to add, update, or find tasks."
            />
            <MessageInput
              className="border-t border-gray-200 px-4 py-3"
              placeholder="Ask me to manage your tasks..."
              onSend={handleSendMessage}
            />
          </ChatContainer>
        </ChatKitProvider>
      </main>
    </div>
  );
}

function handleSendMessage(message: string) {
  // ChatKit handles sending to backend
  console.log('User sent:', message);
}

function generateId(): string {
  return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
```

### Streaming Handler

**File**: `frontend/src/lib/chatkit.ts` (extended)

```typescript
export class StreamingHandler {
  private eventSource: EventSource | null = null;

  async streamResponse(
    message: string,
    conversationId: string,
    onToken: (token: string) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ) {
    const endpoint = `${chatKitConfig.apiEndpoint}?conversation_id=${conversationId}`;

    try {
      // Send message via POST
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      // Read streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          onComplete();
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              onComplete();
              return;
            }
            try {
              const parsed = JSON.parse(data);
              if (parsed.token) {
                onToken(parsed.token);
              }
            } catch (e) {
              console.error('Failed to parse SSE data:', e);
            }
          }
        }
      }
    } catch (error) {
      onError(error as Error);
    }
  }

  cancel() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
```

## UI/UX Design

### Desktop Layout (Split View - Optional Enhancement)

```
┌─────────────────────────────────────────────────────────────┐
│  Header: AI Todo Assistant              [View Tasks]        │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                  │
│  Chat Messages           │  Task List (Live Updates)        │
│  ┌────────────────────┐  │  ┌────────────────────────────┐ │
│  │ User: Add task     │  │  │ ☐ Buy groceries            │ │
│  └────────────────────┘  │  │ ☐ Review Q1 report         │ │
│  ┌────────────────────┐  │  │ ☑ Team standup             │ │
│  │ AI: ✓ Added task   │  │  └────────────────────────────┘ │
│  └────────────────────┘  │                                  │
│                          │                                  │
├──────────────────────────┴──────────────────────────────────┤
│  [Type your message...]                          [Send]     │
└─────────────────────────────────────────────────────────────┘
```

### Mobile Layout (Full Screen Chat)

```
┌─────────────────────────┐
│  ← AI Todo Assistant    │
├─────────────────────────┤
│                         │
│  Chat Messages          │
│  ┌───────────────────┐  │
│  │ User: Add task    │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ AI: ✓ Added task  │  │
│  └───────────────────┘  │
│                         │
│                         │
│                         │
├─────────────────────────┤
│ [Type message...] [Send]│
└─────────────────────────┘
```

## Edge Cases and Error Handling

### Edge Case 1: Network Offline
**Scenario**: User sends message while offline
**Handling**:
- Show "You're offline" message
- Queue message locally
- Retry when connection restored
- Show retry button

### Edge Case 2: Streaming Interrupted
**Scenario**: Network drops during streaming response
**Handling**:
- Show partial response received so far
- Show "Connection lost" indicator
- Provide retry button
- Resume conversation on retry

### Edge Case 3: Backend Timeout
**Scenario**: Backend takes > 30 seconds to respond
**Handling**:
- Show timeout error message
- Suggest trying simpler query
- Provide retry button
- Log timeout for monitoring

### Edge Case 4: Invalid Response Format
**Scenario**: Backend returns malformed JSON
**Handling**:
- Show generic error message
- Log error details for debugging
- Don't crash the UI
- Allow user to continue conversation

### Edge Case 5: Very Long Messages
**Scenario**: User types > 1000 characters
**Handling**:
- Show character count (e.g., "950/1000")
- Disable send button when over limit
- Show warning message
- Suggest breaking into multiple messages

### Edge Case 6: Rapid Message Sending
**Scenario**: User sends multiple messages quickly
**Handling**:
- Queue messages on client side
- Send one at a time
- Show "Waiting for previous response..." indicator
- Prevent UI from becoming unresponsive

## Dependencies

### External Dependencies
- `@openai/chatkit` (npm package)
- `eventsource` or native `fetch` for SSE
- Phase 2 Next.js frontend (existing)

### Internal Dependencies
- Backend chat endpoint (Phase 3 Spec 02, 03)
- Task list component (Phase 2, for split view)

## Testing Requirements

### Unit Tests
- [ ] ChatKit configuration loads correctly
- [ ] Streaming handler parses SSE data correctly
- [ ] Error handler catches and formats errors
- [ ] Message validation works (length, format)

### Integration Tests
- [ ] Chat page renders without errors
- [ ] Messages send to backend successfully
- [ ] Streaming responses display correctly
- [ ] Error states display correctly
- [ ] Navigation between chat and task list works

### E2E Tests
- [ ] User can send message and receive response
- [ ] Streaming works end-to-end
- [ ] Error recovery works (retry button)
- [ ] Mobile layout works on real devices
- [ ] Keyboard shortcuts work (Enter, Shift+Enter)

### Accessibility Tests
- [ ] Screen reader announces messages
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] ARIA labels are present and correct
- [ ] Focus management works properly
- [ ] Color contrast meets WCAG AA standards

## Performance Requirements

- **Initial Load**: Chat page loads in < 2 seconds
- **Message Send**: Message appears in UI immediately (optimistic update)
- **First Token**: First token of AI response arrives in < 1 second
- **Streaming Rate**: Tokens stream at readable pace (not too fast/slow)
- **Scroll Performance**: Smooth scrolling even with 50+ messages
- **Memory Usage**: No memory leaks from streaming connections

## Security Considerations

- **Input Sanitization**: Sanitize user input before sending to backend
- **Output Sanitization**: Sanitize AI responses before rendering (XSS prevention)
- **API Key Security**: Never expose OpenAI API key in frontend code
- **CORS**: Backend must allow frontend origin
- **Rate Limiting**: Respect backend rate limits (show friendly message if hit)
- **Session Security**: Conversation IDs are not guessable (use UUIDs)

## Documentation Requirements

- [ ] README in `frontend/` with ChatKit setup instructions
- [ ] Code comments explaining ChatKit configuration
- [ ] Example conversation flows in documentation
- [ ] Troubleshooting guide for common issues
- [ ] Screenshots of chat interface (desktop and mobile)

## Success Metrics

- ChatKit components render without errors
- Users can send messages and receive streaming responses
- Chat interface is responsive on mobile and desktop
- Error handling works gracefully
- No console errors or warnings
- Performance targets met (< 2s load, < 1s first token)
- Accessibility standards met (WCAG AA)

## Future Enhancements (Out of Scope for Phase 3)

- Voice input/output
- Multi-language support
- Message editing/deletion
- Conversation export
- Rich media in messages (images, files)
- Message reactions (thumbs up/down)
- Conversation search
- Multiple conversation threads

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: Medium
**Implementation Order**: 1 of 5 (implement first)
