# Frontend Specification: Task List UI

## Feature Name
Task List Display and Management - Frontend Implementation

## Purpose
Implement the main task list interface that displays tasks, allows filtering/sorting, and provides quick actions (complete, delete). This is the primary view users interact with.

## User Stories

1. **As a user**, I want to see all my tasks in a list so I can review what needs to be done.
2. **As a user**, I want to see task details (title, description, priority, due date) at a glance.
3. **As a user**, I want to mark tasks complete/incomplete with a single click.
4. **As a user**, I want to delete tasks I no longer need.
5. **As a user**, I want to see visual indicators for priority levels and completion status.
6. **As a user**, I want to see when tasks are overdue.
7. **As a user**, I want the interface to be responsive and work on mobile devices.

## Acceptance Criteria

### Task List Display
- [ ] Displays all tasks fetched from API
- [ ] Shows loading state while fetching data
- [ ] Shows empty state when no tasks exist
- [ ] Shows error state if API call fails
- [ ] Each task shows: title, description (truncated), priority, due date, status
- [ ] Tasks are visually distinct (cards or list items with borders)
- [ ] Completed tasks have visual indication (strikethrough, opacity, checkmark)

### Task Actions
- [ ] Checkbox to toggle task completion status
- [ ] Delete button to remove task
- [ ] Edit button to open task form (links to edit mode)
- [ ] Actions trigger API calls with loading states
- [ ] Optimistic UI updates (update immediately, rollback on error)
- [ ] Success/error messages displayed to user

### Visual Design
- [ ] Priority indicators (color-coded: red=high, yellow=medium, blue=low)
- [ ] Due date formatting (relative: "Today", "Tomorrow", "Overdue")
- [ ] Overdue tasks highlighted in red
- [ ] Responsive layout (mobile, tablet, desktop)
- [ ] Accessible (keyboard navigation, ARIA labels)

### Performance
- [ ] Pagination or infinite scroll for large lists
- [ ] Debounced search input (300ms)
- [ ] Minimal re-renders (React.memo where appropriate)

## Component Architecture

### Component Hierarchy
```
TaskListPage (page.tsx)
├── TaskFilters (Filters.tsx)
├── TaskList (TaskList.tsx)
│   └── TaskItem (TaskItem.tsx) [repeated]
└── TaskForm (TaskForm.tsx) [modal or separate page]
```

### Component Specifications

#### TaskListPage (app/page.tsx)
**Purpose**: Main page component, orchestrates data fetching and state management.

**State**:
- `tasks`: Task[] - Array of tasks from API
- `loading`: boolean - Loading state
- `error`: string | null - Error message
- `filters`: FilterState - Current filter values

**Effects**:
- Fetch tasks on mount
- Refetch when filters change
- Handle URL query parameters for filters

**Props**: None (page component)

**Example**:
```tsx
'use client';

import { useState, useEffect } from 'react';
import TaskList from '@/components/TaskList';
import TaskFilters from '@/components/Filters';
import TaskForm from '@/components/TaskForm';
import { fetchTasks } from '@/lib/api';
import type { Task, FilterState } from '@/types';

export default function TaskListPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>({
    status: null,
    priority: null,
    category: null,
    search: '',
    sort: 'created_at',
    order: 'desc'
  });

  useEffect(() => {
    loadTasks();
  }, [filters]);

  const loadTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTasks(filters);
      setTasks(data.data);
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
  };

  const handleTaskDelete = (taskId: string) => {
    setTasks(tasks.filter(t => t.id !== taskId));
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">My Tasks</h1>

      <TaskFilters filters={filters} onFilterChange={setFilters} />

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={loadTasks} />}
      {!loading && !error && (
        <TaskList
          tasks={tasks}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      )}
    </main>
  );
}
```

---

#### TaskList (components/TaskList.tsx)
**Purpose**: Renders list of tasks, handles empty state.

**Props**:
- `tasks`: Task[] - Array of tasks to display
- `onTaskUpdate`: (task: Task) => void - Callback when task updated
- `onTaskDelete`: (taskId: string) => void - Callback when task deleted

**State**: None (presentational component)

**Example**:
```tsx
import TaskItem from './TaskItem';
import type { Task } from '@/types';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

export default function TaskList({ tasks, onTaskUpdate, onTaskDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No tasks found</p>
        <p className="text-gray-400 text-sm mt-2">
          Create your first task to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdate={onTaskUpdate}
          onDelete={onTaskDelete}
        />
      ))}
    </div>
  );
}
```

---

#### TaskItem (components/TaskItem.tsx)
**Purpose**: Displays single task with actions (complete, delete, edit).

**Props**:
- `task`: Task - Task data
- `onUpdate`: (task: Task) => void - Callback when task updated
- `onDelete`: (taskId: string) => void - Callback when task deleted

**State**:
- `loading`: boolean - Loading state for actions
- `error`: string | null - Error message

**Actions**:
- Toggle completion status
- Delete task
- Navigate to edit form

**Example**:
```tsx
'use client';

import { useState } from 'react';
import { Trash2, Edit, Check } from 'lucide-react';
import { toggleTaskStatus, deleteTask } from '@/lib/api';
import { formatDueDate, getPriorityColor } from '@/lib/utils';
import type { Task } from '@/types';

interface TaskItemProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [loading, setLoading] = useState(false);

  const handleToggleStatus = async () => {
    setLoading(true);
    try {
      const endpoint = task.status ? 'incomplete' : 'complete';
      const updated = await toggleTaskStatus(task.id, endpoint);
      onUpdate(updated.data);
    } catch (err) {
      alert('Failed to update task status');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setLoading(true);
    try {
      await deleteTask(task.id);
      onDelete(task.id);
    } catch (err) {
      alert('Failed to delete task');
      setLoading(false);
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.status;
  const priorityColor = getPriorityColor(task.priority);

  return (
    <div className={`
      bg-white rounded-lg shadow-sm border p-4
      ${task.status ? 'opacity-60' : ''}
      ${isOverdue ? 'border-red-300 bg-red-50' : 'border-gray-200'}
    `}>
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggleStatus}
          disabled={loading}
          className="mt-1 flex-shrink-0"
          aria-label={task.status ? 'Mark incomplete' : 'Mark complete'}
        >
          <div className={`
            w-5 h-5 rounded border-2 flex items-center justify-center
            ${task.status ? 'bg-green-500 border-green-500' : 'border-gray-300'}
          `}>
            {task.status && <Check className="w-4 h-4 text-white" />}
          </div>
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h3 className={`
              text-lg font-medium
              ${task.status ? 'line-through text-gray-500' : 'text-gray-900'}
            `}>
              {task.title}
            </h3>

            {/* Priority Badge */}
            <span className={`
              px-2 py-1 text-xs font-medium rounded-full flex-shrink-0
              ${priorityColor}
            `}>
              {task.priority}
            </span>
          </div>

          {task.description && (
            <p className="text-gray-600 text-sm mt-1 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
            {task.category && (
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                {task.category}
              </span>
            )}

            {task.due_date && (
              <span className={isOverdue ? 'text-red-600 font-medium' : ''}>
                {formatDueDate(task.due_date)}
              </span>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          <button
            onClick={() => window.location.href = `/tasks/${task.id}/edit`}
            className="p-2 text-gray-400 hover:text-blue-600 transition"
            aria-label="Edit task"
          >
            <Edit className="w-4 h-4" />
          </button>

          <button
            onClick={handleDelete}
            disabled={loading}
            className="p-2 text-gray-400 hover:text-red-600 transition"
            aria-label="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## TypeScript Types

```typescript
// types/index.ts

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: boolean;
  priority: 'high' | 'medium' | 'low';
  category: string | null;
  due_date: string | null; // ISO 8601 datetime
  created_at: string;
  updated_at: string;
}

export interface FilterState {
  status: 'complete' | 'incomplete' | null;
  priority: 'high' | 'medium' | 'low' | null;
  category: string | null;
  search: string;
  sort: 'due_date' | 'priority' | 'created_at' | 'title';
  order: 'asc' | 'desc';
}

export interface ApiResponse<T> {
  data: T;
  message: string;
}

export interface TaskListResponse {
  data: Task[];
  message: string;
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
}
```

---

## Utility Functions

```typescript
// lib/utils.ts

export function formatDueDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const taskDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

  const diffDays = Math.floor((taskDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  if (diffDays < 0) return 'Overdue';
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Tomorrow';
  if (diffDays <= 7) return `In ${diffDays} days`;

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function getPriorityColor(priority: string): string {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-800';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800';
    case 'low':
      return 'bg-blue-100 text-blue-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}
```

---

## API Client Functions

```typescript
// lib/api.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchTasks(filters: FilterState): Promise<TaskListResponse> {
  const params = new URLSearchParams();

  if (filters.status) params.append('status', filters.status);
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  params.append('sort', filters.sort);
  params.append('order', filters.order);

  const response = await fetch(`${API_URL}/tasks?${params}`);
  if (!response.ok) throw new Error('Failed to fetch tasks');

  return response.json();
}

export async function toggleTaskStatus(
  taskId: string,
  endpoint: 'complete' | 'incomplete'
): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}/${endpoint}`, {
    method: 'PATCH',
  });

  if (!response.ok) throw new Error('Failed to update task status');
  return response.json();
}

export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Failed to delete task');
}
```

---

## Styling (Tailwind CSS)

### Color Scheme
- **Primary**: Blue (actions, links)
- **Success**: Green (completed tasks)
- **Warning**: Yellow (medium priority)
- **Danger**: Red (high priority, overdue, delete)
- **Neutral**: Gray (text, borders)

### Responsive Breakpoints
- **Mobile**: < 640px (single column, compact)
- **Tablet**: 640px - 1024px (single column, spacious)
- **Desktop**: > 1024px (optional sidebar, wide layout)

---

## Accessibility

### Keyboard Navigation
- Tab through tasks
- Enter to toggle completion
- Delete key to delete (with confirmation)
- Arrow keys to navigate list

### ARIA Labels
- Checkbox: "Mark task complete" / "Mark task incomplete"
- Edit button: "Edit task: {title}"
- Delete button: "Delete task: {title}"
- Empty state: "No tasks found"

### Screen Reader Support
- Task status announced
- Priority level announced
- Due date announced
- Loading states announced

---

## Error Handling

### Network Errors
- Display error message with retry button
- Preserve user's filter state
- Log error to console (or error tracking service)

### Optimistic Updates
- Update UI immediately
- Rollback on error
- Show error toast notification

### Empty States
- No tasks: "No tasks found. Create your first task!"
- No results: "No tasks match your filters. Try adjusting your search."
- Error: "Failed to load tasks. Please try again."

---

## Performance Optimizations

### React Optimizations
- Use `React.memo` for TaskItem
- Use `useCallback` for event handlers
- Use `useMemo` for computed values (filtered/sorted tasks)

### Network Optimizations
- Debounce search input (300ms)
- Cache API responses (consider React Query or SWR)
- Pagination for large lists (20 items per page)

### Rendering Optimizations
- Virtual scrolling for 100+ tasks (react-window)
- Lazy load images if task descriptions include images
- Skeleton loading states

---

## Testing Strategy

### Component Tests
- TaskList renders empty state
- TaskList renders tasks correctly
- TaskItem displays task data
- TaskItem handles completion toggle
- TaskItem handles delete action

### Integration Tests
- Fetch tasks on mount
- Filter tasks updates list
- Sort tasks updates order
- Delete task removes from list
- Toggle status updates UI

### Manual Testing
- Test on mobile devices
- Test with screen reader
- Test keyboard navigation
- Test with slow network (throttling)

---

## Edge Cases

1. **Empty Task List**: Show helpful empty state
2. **Very Long Titles**: Truncate with ellipsis
3. **Very Long Descriptions**: Show first 2 lines, expand on click
4. **No Due Date**: Don't show due date section
5. **Past Due Date**: Highlight in red
6. **Network Offline**: Show offline message, queue actions
7. **Concurrent Updates**: Last write wins (no conflict resolution)

---

## Dependencies
- `architecture/00-system-architecture.md`
- `architecture/02-api-design.md`
- `backend/01-task-crud-api.md`

## Related Specifications
- `frontend/02-task-form.md` - Task creation/editing form
- `frontend/03-filters-sorting.md` - Filter and sort controls

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: Frontend Developer
