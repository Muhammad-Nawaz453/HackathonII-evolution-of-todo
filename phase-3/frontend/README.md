# Frontend - Phase 3 AI-Powered Todo Chatbot

This directory contains the Next.js frontend for Phase 3, which adds a conversational AI chat interface using OpenAI ChatKit.

## Overview

The frontend extends Phase 2 with:
- **ChatKit Integration**: Pre-built chat UI components from OpenAI
- **Split View Layout**: Chat on left, task list on right (desktop)
- **Real-Time Sync**: Task list updates when AI performs operations
- **Streaming Responses**: Token-by-token AI responses
- **Mobile Responsive**: Full-screen chat with task overlay

## Prerequisites

- Node.js 18 or higher
- npm or pnpm
- Phase 2 frontend code (this extends it)
- Backend running with chat endpoint

## Quick Start

### 1. Install Dependencies

```bash
# Install new dependencies
npm install @openai/chatkit lucide-react

# Or install all dependencies
npm install
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.local.example .env.local

# Edit .env.local and set:
# - NEXT_PUBLIC_CHAT_ENDPOINT (your backend chat URL)
```

### 3. Run Frontend

```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

### 4. Verify Installation

```bash
# Open chat interface
open http://localhost:3000/chat

# Send test message: "Show me my tasks"
# Verify AI responds and task list updates
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx               # Home page (from Phase 2)
│   │   ├── layout.tsx             # Root layout (from Phase 2)
│   │   └── chat/                  # NEW: Chat interface
│   │       └── page.tsx           # Chat page
│   ├── components/
│   │   ├── TaskList.tsx           # Task list (from Phase 2)
│   │   ├── TaskItem.tsx           # Task item (from Phase 2, enhanced)
│   │   ├── TaskForm.tsx           # Task form (from Phase 2)
│   │   └── chat/                  # NEW: Chat components
│   │       ├── ChatLayout.tsx     # Split view container
│   │       ├── ChatPanel.tsx      # Chat side
│   │       ├── TaskPanel.tsx      # Task list side
│   │       ├── ToolExecutionIndicator.tsx
│   │       ├── TaskHighlight.tsx  # Animation wrapper
│   │       └── MobileTaskOverlay.tsx
│   ├── hooks/                     # NEW: Custom hooks
│   │   ├── useTaskSync.ts         # Real-time task sync
│   │   ├── useChatEvents.ts       # Chat event handling
│   │   └── useTaskAnimations.ts   # Animation state
│   ├── lib/
│   │   ├── api.ts                 # API client (from Phase 2)
│   │   ├── chatkit.ts             # NEW: ChatKit configuration
│   │   └── taskSync.ts            # NEW: Sync logic
│   └── types/
│       └── index.ts               # TypeScript types (from Phase 2)
├── public/                        # Static assets
├── package.json                   # Dependencies
├── .env.local.example             # Environment variables template
├── .env.local                     # Environment variables (not committed)
├── next.config.js                 # Next.js configuration
├── tailwind.config.js             # Tailwind CSS configuration
└── README.md                      # This file
```

## Features

### Chat Interface

- Natural language task management
- Streaming AI responses
- Typing indicators
- Tool execution status
- Error handling with retry

### Split View (Desktop)

- Chat panel (60%) on left
- Task list (40%) on right
- Resizable divider
- Toggle split view on/off

### Mobile Layout

- Full-screen chat
- Floating action button for tasks
- Slide-in task overlay
- Swipe to dismiss

### Real-Time Sync

- Task list updates when AI creates tasks
- Visual highlights for changes (green/blue borders)
- Smooth animations
- Optimistic UI updates

## Routes

- `/` - Home page with task list (Phase 2)
- `/chat` - Chat interface (Phase 3)
- `/tasks/new` - Create task form (Phase 2)
- `/tasks/[id]/edit` - Edit task form (Phase 2)

## Components

### ChatLayout

Main container for split view layout. Handles responsive design and mobile overlay.

```tsx
import { ChatLayout } from '@/components/chat/ChatLayout';

<ChatLayout conversationId="conv-123" />
```

### ChatPanel

Left side of split view. Contains ChatKit components and tool execution indicators.

### TaskPanel

Right side of split view. Shows task list with real-time updates and highlights.

### ToolExecutionIndicator

Shows status of AI tool execution:
- "Creating task..." (with spinner)
- "✓ Task created" (with checkmark)
- "✗ Failed" (with error icon)

### TaskHighlight

Wrapper component that adds highlight animations to tasks:
- Green border for newly created tasks
- Blue border for updated tasks
- Fade-out for deleted tasks

## Hooks

### useTaskSync

Manages task fetching and real-time synchronization.

```tsx
const { tasks, loading, refreshTasks, highlightedTaskIds, highlightTask } = useTaskSync();
```

### useChatEvents

Handles chat events and triggers task updates.

```tsx
const { toolExecutions, onToolExecution } = useChatEvents({
  onTaskCreated: (task) => { /* ... */ },
  onTaskUpdated: (taskId) => { /* ... */ },
  onTaskDeleted: (taskId) => { /* ... */ }
});
```

### useTaskAnimations

Manages animation state for task highlights.

```tsx
const { highlightedTasks, highlightTask, clearHighlight } = useTaskAnimations();
```

## Configuration

### ChatKit Configuration

Edit `src/lib/chatkit.ts`:

```typescript
export const chatKitConfig: ChatKitConfig = {
  apiEndpoint: process.env.NEXT_PUBLIC_CHAT_ENDPOINT,
  streaming: true,
  maxMessageLength: 1000,
  theme: {
    primaryColor: '#3b82f6',
    // ... more theme options
  }
};
```

### Tailwind CSS

Chat components use Tailwind CSS classes. Customize in `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'chat-primary': '#3b82f6',
        'chat-secondary': '#f3f4f6',
      }
    }
  }
}
```

## Testing

### Run Tests

```bash
# Run all tests
npm test

# Run specific test
npm test -- ChatLayout

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e
```

### Manual Testing

1. Open http://localhost:3000/chat
2. Test conversation patterns:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark the grocery task as done"
   - "Delete completed tasks"
3. Verify task list updates in real-time
4. Test on mobile device or responsive mode

## Development

### Code Style

```bash
# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check
```

### Adding New Components

1. Create component in `src/components/chat/`
2. Add TypeScript types
3. Add tests
4. Import and use in chat page

### Debugging

Enable debug mode in `.env.local`:

```bash
NEXT_PUBLIC_DEBUG=true
```

This will log:
- Chat events
- Tool executions
- Task updates
- API calls

## Build and Deploy

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Environment Variables in Vercel

Set these in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_CHAT_ENDPOINT`

## Performance

### Optimization Tips

1. **Code Splitting**: Use dynamic imports for heavy components
2. **Image Optimization**: Use Next.js Image component
3. **Caching**: Enable SWR or React Query for API calls
4. **Bundle Size**: Analyze with `npm run analyze`

### Performance Targets

- Chat page load: < 2 seconds
- First token: < 1 second
- Task list update: < 200ms
- Smooth animations: 60fps

## Troubleshooting

### "ChatKit components not rendering"

**Solution**: Verify `@openai/chatkit` is installed:
```bash
npm list @openai/chatkit
```

### "Streaming not working"

**Solution**:
- Check `NEXT_PUBLIC_CHAT_ENDPOINT` is correct
- Verify backend CORS allows your frontend origin
- Check browser console for errors

### "Task list not updating"

**Solution**:
- Verify `useTaskSync` hook is called
- Check chat events are emitted
- Inspect browser console for errors

### "Mobile layout broken"

**Solution**:
- Test at different breakpoints (320px, 768px, 1024px)
- Check Tailwind responsive classes
- Verify viewport meta tag in layout

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile Safari: iOS 14+
- Chrome Mobile: Latest

## Accessibility

- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ ARIA labels
- ✅ Focus management
- ✅ Color contrast (WCAG AA)

## Security

- ✅ No API keys in frontend code
- ✅ Input sanitization
- ✅ Output sanitization (XSS prevention)
- ✅ HTTPS in production
- ✅ Secure environment variables

## Support

For issues or questions:
1. Check `../../docs/TROUBLESHOOTING.md`
2. Review specifications in `../../specs/`
3. Check Next.js documentation: https://nextjs.org/docs

## License

MIT License - See LICENSE file for details
