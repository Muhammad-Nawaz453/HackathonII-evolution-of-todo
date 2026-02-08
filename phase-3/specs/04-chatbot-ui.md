# Specification: Chatbot UI with Real-Time Task Sync

**Feature ID**: PHASE3-04
**Status**: Draft
**Created**: 2026-02-03
**Dependencies**: Phase 3 Spec 01 (ChatKit Integration), Phase 2 (Task List UI)

## Purpose

Create a comprehensive chatbot user interface that combines the conversational AI interface with real-time task list updates. Users should see their tasks update immediately when the AI agent performs operations, providing visual confirmation and maintaining context between chat and traditional task management views.

## User Stories

**As a user**, I want to:
1. See a split-screen view with chat on the left and my task list on the right (desktop)
2. See my task list update in real-time when I create/update/delete tasks via chat
3. See visual indicators (highlights, animations) when tasks are modified by the AI
4. Switch between chat-only view and split view based on my preference
5. Use the chat interface on mobile with easy access to my task list
6. See typing indicators and tool execution status while the AI is working
7. Navigate seamlessly between chat and traditional task management

**As a developer**, I want to:
1. Implement real-time synchronization between chat actions and task list UI
2. Use React state management to coordinate updates across components
3. Provide visual feedback for all AI operations
4. Ensure the UI is responsive and performant
5. Handle edge cases like concurrent updates and network delays

## Acceptance Criteria

### AC1: Split View Layout (Desktop)
- [ ] Desktop view (>768px) shows split screen: chat left (60%), tasks right (40%)
- [ ] Split view is resizable with draggable divider
- [ ] Both panels scroll independently
- [ ] Layout is responsive and adapts to window size
- [ ] Split view can be toggled to full-screen chat

### AC2: Mobile Layout
- [ ] Mobile view (<768px) shows chat full-screen by default
- [ ] Floating action button (FAB) to access task list
- [ ] Task list slides in from right as overlay
- [ ] Swipe gesture to dismiss task list overlay
- [ ] Easy navigation between chat and task list

### AC3: Real-Time Task Updates
- [ ] When AI creates task → task appears in list immediately
- [ ] When AI updates task → task updates in list with highlight animation
- [ ] When AI deletes task → task removes from list with fade-out animation
- [ ] When AI marks complete → task checkbox updates with animation
- [ ] Updates happen during streaming (not after full response)

### AC4: Visual Feedback
- [ ] Newly created tasks highlighted with green border (3 seconds)
- [ ] Updated tasks highlighted with blue border (3 seconds)
- [ ] Deleted tasks fade out with animation (500ms)
- [ ] Completed tasks show checkmark animation
- [ ] Tool execution shows status badge in chat ("Creating task...", "Searching...")

### AC5: Tool Execution Indicators
- [ ] Show "Thinking..." indicator when AI is processing
- [ ] Show specific tool status: "Creating task...", "Searching tasks...", "Updating task..."
- [ ] Show success/failure icons after tool execution
- [ ] Tool execution time displayed (optional)
- [ ] Multiple tool calls shown sequentially

### AC6: Task List Filtering in Split View
- [ ] Task list shows all tasks by default
- [ ] Filter buttons: All, Incomplete, Complete, High Priority
- [ ] Search box to filter tasks by title
- [ ] Filters persist when switching views
- [ ] Filter state syncs with chat context (optional)

### AC7: Navigation and Routing
- [ ] `/chat` route shows chat interface
- [ ] `/` route shows traditional task list
- [ ] Header navigation between routes
- [ ] Back button works correctly
- [ ] Deep linking to specific conversations (future)

### AC8: Error Handling in UI
- [ ] Network errors show inline error message in chat
- [ ] Failed tool executions show error badge
- [ ] Retry button for failed operations
- [ ] Offline indicator when network is down
- [ ] Graceful degradation (chat disabled, task list still works)

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                              │
├─────────────────────────────────────────────────────────────────┤
│  /app/chat/page.tsx (Main Chat Page)                            │
│  ├── ChatLayout (Split View Container)                          │
│  │   ├── ChatPanel (Left - 60%)                                 │
│  │   │   ├── ChatContainer (ChatKit)                            │
│  │   │   ├── MessageList (ChatKit)                              │
│  │   │   ├── ToolExecutionIndicator (Custom)                    │
│  │   │   └── MessageInput (ChatKit)                             │
│  │   └── TaskPanel (Right - 40%)                                │
│  │       ├── TaskListHeader (Filters, Search)                   │
│  │       ├── TaskList (Reused from Phase 2)                     │
│  │       └── TaskItem (Enhanced with animations)                │
│  └── TaskSyncManager (State Management)                         │
│      ├── useTaskSync() hook                                     │
│      ├── useChatEvents() hook                                   │
│      └── useTaskAnimations() hook                               │
├─────────────────────────────────────────────────────────────────┤
│  /components/chat/                                              │
│  ├── ChatLayout.tsx (Split view container)                      │
│  ├── ChatPanel.tsx (Chat side)                                  │
│  ├── TaskPanel.tsx (Task list side)                             │
│  ├── ToolExecutionIndicator.tsx (Tool status)                   │
│  ├── TaskHighlight.tsx (Animation wrapper)                      │
│  └── MobileTaskOverlay.tsx (Mobile task list)                   │
├─────────────────────────────────────────────────────────────────┤
│  /lib/taskSync.ts (Task synchronization logic)                  │
│  └── /hooks/                                                    │
│      ├── useTaskSync.ts (Real-time sync)                        │
│      ├── useChatEvents.ts (Chat event handling)                 │
│      └── useTaskAnimations.ts (Animation state)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Structure

#### ChatLayout Component

**File**: `frontend/src/components/chat/ChatLayout.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import { ChatPanel } from './ChatPanel';
import { TaskPanel } from './TaskPanel';
import { useTaskSync } from '@/hooks/useTaskSync';
import { useChatEvents } from '@/hooks/useChatEvents';

interface ChatLayoutProps {
  conversationId: string;
}

export function ChatLayout({ conversationId }: ChatLayoutProps) {
  const [splitViewEnabled, setSplitViewEnabled] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const [showTaskOverlay, setShowTaskOverlay] = useState(false);

  // Task synchronization
  const { tasks, refreshTasks, highlightedTaskIds } = useTaskSync();

  // Chat event handling
  const { toolExecutions, onToolExecution } = useChatEvents({
    onTaskCreated: (task) => {
      refreshTasks();
    },
    onTaskUpdated: (taskId) => {
      refreshTasks();
    },
    onTaskDeleted: (taskId) => {
      refreshTasks();
    }
  });

  // Detect mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  if (isMobile) {
    return (
      <div className="flex flex-col h-screen">
        <ChatPanel
          conversationId={conversationId}
          onToolExecution={onToolExecution}
          toolExecutions={toolExecutions}
        />

        {/* Floating Action Button */}
        <button
          onClick={() => setShowTaskOverlay(true)}
          className="fixed bottom-20 right-4 bg-blue-600 text-white rounded-full p-4 shadow-lg"
        >
          <TaskIcon />
        </button>

        {/* Task Overlay */}
        {showTaskOverlay && (
          <MobileTaskOverlay
            tasks={tasks}
            highlightedTaskIds={highlightedTaskIds}
            onClose={() => setShowTaskOverlay(false)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      {/* Chat Panel - Left Side */}
      <div className={splitViewEnabled ? 'w-3/5 border-r' : 'w-full'}>
        <ChatPanel
          conversationId={conversationId}
          onToolExecution={onToolExecution}
          toolExecutions={toolExecutions}
        />
      </div>

      {/* Task Panel - Right Side */}
      {splitViewEnabled && (
        <div className="w-2/5">
          <TaskPanel
            tasks={tasks}
            highlightedTaskIds={highlightedTaskIds}
            onRefresh={refreshTasks}
          />
        </div>
      )}

      {/* Toggle Split View Button */}
      <button
        onClick={() => setSplitViewEnabled(!splitViewEnabled)}
        className="fixed top-4 right-4 bg-white border rounded-lg px-3 py-2 shadow-sm"
      >
        {splitViewEnabled ? 'Hide Tasks' : 'Show Tasks'}
      </button>
    </div>
  );
}
```

#### useTaskSync Hook

**File**: `frontend/src/hooks/useTaskSync.ts`

```typescript
import { useState, useEffect, useCallback } from 'react';
import { Task } from '@/types';
import { getTasks } from '@/lib/api';

interface UseTaskSyncReturn {
  tasks: Task[];
  loading: boolean;
  error: Error | null;
  refreshTasks: () => Promise<void>;
  highlightedTaskIds: Set<string>;
  highlightTask: (taskId: string, duration?: number) => void;
}

export function useTaskSync(): UseTaskSyncReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [highlightedTaskIds, setHighlightedTaskIds] = useState<Set<string>>(new Set());

  // Fetch tasks
  const refreshTasks = useCallback(async () => {
    try {
      setLoading(true);
      const fetchedTasks = await getTasks();
      setTasks(fetchedTasks);
      setError(null);
    } catch (err) {
      setError(err as Error);
      console.error('Failed to fetch tasks:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    refreshTasks();
  }, [refreshTasks]);

  // Highlight task temporarily
  const highlightTask = useCallback((taskId: string, duration = 3000) => {
    setHighlightedTaskIds((prev) => new Set(prev).add(taskId));

    setTimeout(() => {
      setHighlightedTaskIds((prev) => {
        const next = new Set(prev);
        next.delete(taskId);
        return next;
      });
    }, duration);
  }, []);

  return {
    tasks,
    loading,
    error,
    refreshTasks,
    highlightedTaskIds,
    highlightTask
  };
}
```

#### useChatEvents Hook

**File**: `frontend/src/hooks/useChatEvents.ts`

```typescript
import { useState, useCallback } from 'react';

interface ToolExecution {
  id: string;
  tool: string;
  status: 'executing' | 'completed' | 'failed';
  result?: any;
  error?: string;
  timestamp: number;
}

interface ChatEventHandlers {
  onTaskCreated?: (task: any) => void;
  onTaskUpdated?: (taskId: string) => void;
  onTaskDeleted?: (taskId: string) => void;
}

interface UseChatEventsReturn {
  toolExecutions: ToolExecution[];
  onToolExecution: (event: any) => void;
  clearToolExecutions: () => void;
}

export function useChatEvents(handlers: ChatEventHandlers): UseChatEventsReturn {
  const [toolExecutions, setToolExecutions] = useState<ToolExecution[]>([]);

  const onToolExecution = useCallback((event: any) => {
    const { tool, status, result, error } = event;

    // Update tool execution state
    setToolExecutions((prev) => {
      const existing = prev.find((t) => t.tool === tool && t.status === 'executing');

      if (existing) {
        // Update existing execution
        return prev.map((t) =>
          t.id === existing.id
            ? { ...t, status, result, error, timestamp: Date.now() }
            : t
        );
      } else {
        // Add new execution
        return [
          ...prev,
          {
            id: `${tool}-${Date.now()}`,
            tool,
            status,
            result,
            error,
            timestamp: Date.now()
          }
        ];
      }
    });

    // Call appropriate handler
    if (status === 'completed' && result) {
      if (tool === 'add_task' && handlers.onTaskCreated) {
        handlers.onTaskCreated(result.data);
      } else if (tool === 'update_task' && handlers.onTaskUpdated) {
        handlers.onTaskUpdated(result.data.id);
      } else if (tool === 'delete_task' && handlers.onTaskDeleted) {
        handlers.onTaskDeleted(result.data.id);
      }
    }

    // Auto-clear completed/failed executions after 5 seconds
    if (status === 'completed' || status === 'failed') {
      setTimeout(() => {
        setToolExecutions((prev) =>
          prev.filter((t) => t.tool !== tool || t.status === 'executing')
        );
      }, 5000);
    }
  }, [handlers]);

  const clearToolExecutions = useCallback(() => {
    setToolExecutions([]);
  }, []);

  return {
    toolExecutions,
    onToolExecution,
    clearToolExecutions
  };
}
```

#### ToolExecutionIndicator Component

**File**: `frontend/src/components/chat/ToolExecutionIndicator.tsx`

```typescript
import { CheckCircle, XCircle, Loader2 } from 'lucide-react';

interface ToolExecution {
  id: string;
  tool: string;
  status: 'executing' | 'completed' | 'failed';
  error?: string;
}

interface ToolExecutionIndicatorProps {
  executions: ToolExecution[];
}

export function ToolExecutionIndicator({ executions }: ToolExecutionIndicatorProps) {
  if (executions.length === 0) return null;

  return (
    <div className="space-y-2 mb-4">
      {executions.map((execution) => (
        <div
          key={execution.id}
          className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg text-sm"
        >
          {execution.status === 'executing' && (
            <>
              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
              <span className="text-gray-700">
                {getToolLabel(execution.tool)}...
              </span>
            </>
          )}

          {execution.status === 'completed' && (
            <>
              <CheckCircle className="w-4 h-4 text-green-600" />
              <span className="text-gray-700">
                {getToolLabel(execution.tool)} completed
              </span>
            </>
          )}

          {execution.status === 'failed' && (
            <>
              <XCircle className="w-4 h-4 text-red-600" />
              <span className="text-gray-700">
                {getToolLabel(execution.tool)} failed
                {execution.error && `: ${execution.error}`}
              </span>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

function getToolLabel(tool: string): string {
  const labels: Record<string, string> = {
    add_task: 'Creating task',
    get_tasks: 'Retrieving tasks',
    update_task: 'Updating task',
    delete_task: 'Deleting task',
    search_tasks: 'Searching tasks',
    mark_task_complete: 'Marking task complete',
    get_task_statistics: 'Getting statistics'
  };
  return labels[tool] || tool;
}
```

#### TaskHighlight Component

**File**: `frontend/src/components/chat/TaskHighlight.tsx`

```typescript
import { ReactNode } from 'react';

interface TaskHighlightProps {
  children: ReactNode;
  isHighlighted: boolean;
  type?: 'created' | 'updated' | 'deleted';
}

export function TaskHighlight({ children, isHighlighted, type = 'updated' }: TaskHighlightProps) {
  const highlightColors = {
    created: 'ring-2 ring-green-400 bg-green-50',
    updated: 'ring-2 ring-blue-400 bg-blue-50',
    deleted: 'ring-2 ring-red-400 bg-red-50'
  };

  return (
    <div
      className={`
        transition-all duration-300
        ${isHighlighted ? highlightColors[type] : ''}
      `}
    >
      {children}
    </div>
  );
}
```

## UI/UX Design

### Desktop Split View

```
┌─────────────────────────────────────────────────────────────────┐
│  Header: AI Todo Assistant          [Hide Tasks] [View Tasks]   │
├──────────────────────────────┬──────────────────────────────────┤
│                              │                                  │
│  Chat Panel (60%)            │  Task Panel (40%)                │
│  ┌────────────────────────┐  │  ┌────────────────────────────┐ │
│  │ User: Add high priority│  │  │ [All] [Incomplete] [High]  │ │
│  │ task to review report  │  │  │ [Search tasks...]          │ │
│  └────────────────────────┘  │  ├────────────────────────────┤ │
│                              │  │ ☐ Buy groceries            │ │
│  [Creating task...]          │  │ ☐ Review report ← NEW!     │ │
│                              │  │ ☑ Team standup             │ │
│  ┌────────────────────────┐  │  └────────────────────────────┘ │
│  │ AI: ✓ I've created a   │  │                                  │
│  │ high priority task...  │  │  3 tasks total                   │
│  └────────────────────────┘  │  1 complete, 2 incomplete        │
│                              │                                  │
├──────────────────────────────┴──────────────────────────────────┤
│  [Type your message...]                          [Send]         │
└─────────────────────────────────────────────────────────────────┘
```

### Mobile View

```
┌─────────────────────────┐
│  ← AI Todo Assistant    │
├─────────────────────────┤
│                         │
│  Chat Messages          │
│  ┌───────────────────┐  │
│  │ User: Add task    │  │
│  └───────────────────┘  │
│                         │
│  [Creating task...]     │
│                         │
│  ┌───────────────────┐  │
│  │ AI: ✓ Task added  │  │
│  └───────────────────┘  │
│                         │
│                         │
├─────────────────────────┤
│ [Type message...] [Send]│
└─────────────────────────┘
         [📋] ← FAB
```

## Edge Cases and Error Handling

### Edge Case 1: Concurrent Updates
**Scenario**: User updates task in task list while AI is updating same task
**Handling**:
- Last write wins (AI update takes precedence)
- Show warning message if conflict detected
- Refresh task list after AI operation completes

### Edge Case 2: Network Delay
**Scenario**: Task list update delayed due to slow network
**Handling**:
- Show loading indicator in task panel
- Optimistic update (show change immediately, rollback if fails)
- Retry failed updates automatically (3 attempts)

### Edge Case 3: Task Not Found After Creation
**Scenario**: AI creates task but it doesn't appear in list
**Handling**:
- Force refresh task list
- Show error message if still not found
- Log error for debugging

### Edge Case 4: Multiple Tool Executions
**Scenario**: AI executes multiple tools in sequence
**Handling**:
- Show all tool executions in order
- Update task list after each tool completes
- Batch animations if multiple tasks affected

### Edge Case 5: Mobile Overlay Interaction
**Scenario**: User opens task overlay while AI is responding
**Handling**:
- Allow overlay to open
- Continue showing tool execution indicators
- Update task list in overlay in real-time

## Dependencies

### External Dependencies
- `@openai/chatkit` (ChatKit components)
- `lucide-react` (Icons)
- `framer-motion` (Animations - optional)
- Phase 2 Task List components (reused)

### Internal Dependencies
- Phase 3 Spec 01: ChatKit Integration
- Phase 3 Spec 02: Agent SDK (for tool execution events)
- Phase 2: Task List UI components

## Testing Requirements

### Unit Tests
- [ ] useTaskSync hook fetches and updates tasks
- [ ] useChatEvents hook handles tool execution events
- [ ] useTaskAnimations hook manages highlight state
- [ ] ToolExecutionIndicator renders correctly
- [ ] TaskHighlight applies correct styles

### Integration Tests
- [ ] Chat panel and task panel communicate correctly
- [ ] Task list updates when AI creates task
- [ ] Task list updates when AI updates task
- [ ] Task list updates when AI deletes task
- [ ] Highlights appear and disappear correctly

### E2E Tests
- [ ] User sends message → task created → appears in list
- [ ] User sends message → task updated → list updates
- [ ] User sends message → task deleted → removed from list
- [ ] Split view toggle works correctly
- [ ] Mobile overlay works correctly

### Visual Tests
- [ ] Animations are smooth (60fps)
- [ ] Highlights are visible and clear
- [ ] Tool execution indicators are readable
- [ ] Layout is responsive at all breakpoints
- [ ] No layout shift during updates

## Performance Requirements

- **Task List Refresh**: < 200ms
- **Highlight Animation**: 60fps, no jank
- **Tool Execution Indicator**: Updates within 100ms
- **Split View Resize**: Smooth, no lag
- **Mobile Overlay**: Opens/closes in < 300ms
- **Memory Usage**: < 50MB for chat + task list

## Accessibility Requirements

- [ ] Keyboard navigation works in both panels
- [ ] Screen reader announces task updates
- [ ] Focus management when switching panels
- [ ] ARIA labels for all interactive elements
- [ ] Color contrast meets WCAG AA standards
- [ ] Animations respect prefers-reduced-motion

## Documentation Requirements

- [ ] Component documentation with examples
- [ ] Hook usage guide
- [ ] State management explanation
- [ ] Animation customization guide
- [ ] Mobile layout guide

## Success Metrics

- Split view renders correctly on desktop
- Mobile view works on all screen sizes
- Task list updates in real-time (<500ms delay)
- Animations are smooth (60fps)
- No console errors or warnings
- Accessibility standards met (WCAG AA)
- Performance targets met

## Future Enhancements (Out of Scope for Phase 3)

- Drag-and-drop tasks from list to chat
- Task preview on hover in chat
- Inline task editing in split view
- Customizable split view ratio
- Multiple task list views (kanban, calendar)
- Task filtering based on chat context

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: Medium-High
**Implementation Order**: 4 of 5 (implement after ChatKit and Agent SDK)
