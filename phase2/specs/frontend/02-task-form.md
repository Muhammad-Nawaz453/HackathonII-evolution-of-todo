# Frontend Specification: Task Form

## Feature Name
Task Creation and Editing Form - Frontend Implementation

## Purpose
Implement a form component for creating new tasks and editing existing tasks. The form includes validation, date picker, priority selection, and category input.

## User Stories

1. **As a user**, I want to create new tasks with a simple form so I can quickly add items to my todo list.
2. **As a user**, I want to edit existing tasks to update details or fix mistakes.
3. **As a user**, I want to set a due date using a date picker so I don't have to type dates manually.
4. **As a user**, I want to select priority levels (high/medium/low) so I can organize my tasks.
5. **As a user**, I want to add categories/tags to organize my tasks.
6. **As a user**, I want immediate feedback if I make validation errors.
7. **As a user**, I want the form to be accessible on mobile devices.

## Acceptance Criteria

### Form Display
- [ ] Form displays all task fields (title, description, priority, category, due date)
- [ ] Form can be used for both creating and editing tasks
- [ ] Edit mode pre-fills form with existing task data
- [ ] Form is responsive (mobile, tablet, desktop)
- [ ] Form is accessible (keyboard navigation, ARIA labels)

### Form Validation
- [ ] Title is required (1-200 characters)
- [ ] Description is optional (max 1000 characters)
- [ ] Priority defaults to "medium"
- [ ] Category is optional (max 50 characters)
- [ ] Due date is optional, must be future date
- [ ] Validation errors shown inline next to fields
- [ ] Submit button disabled until form is valid

### Form Submission
- [ ] Submit button shows loading state during API call
- [ ] Success: Redirect to task list with success message
- [ ] Error: Display error message, keep form data
- [ ] Cancel button returns to task list without saving

### Date Picker
- [ ] Calendar widget for selecting due date
- [ ] Can clear due date (set to null)
- [ ] Prevents selecting past dates
- [ ] Shows current date highlighted
- [ ] Mobile-friendly date picker

### Priority Selection
- [ ] Radio buttons or dropdown for priority
- [ ] Visual indicators (colors) for each priority
- [ ] Default selection is "medium"

## Component Architecture

### Component Hierarchy
```
TaskFormPage (app/tasks/new/page.tsx or app/tasks/[id]/edit/page.tsx)
└── TaskForm (components/TaskForm.tsx)
    ├── Input fields
    ├── Textarea
    ├── PrioritySelector
    ├── DatePicker
    └── Submit/Cancel buttons
```

### Component Specifications

#### TaskFormPage (app/tasks/new/page.tsx)
**Purpose**: Page component for creating new tasks.

**State**:
- `loading`: boolean - Submission loading state
- `error`: string | null - Error message

**Example**:
```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import TaskForm from '@/components/TaskForm';
import { createTask } from '@/lib/api';
import type { TaskFormData } from '@/types';

export default function NewTaskPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: TaskFormData) => {
    setLoading(true);
    setError(null);

    try {
      await createTask(data);
      router.push('/?success=Task created successfully');
    } catch (err) {
      setError('Failed to create task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/');
  };

  return (
    <main className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Create New Task</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      <TaskForm
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        loading={loading}
      />
    </main>
  );
}
```

#### TaskFormPage - Edit Mode (app/tasks/[id]/edit/page.tsx)
**Purpose**: Page component for editing existing tasks.

**State**:
- `task`: Task | null - Task being edited
- `loading`: boolean - Loading/submission state
- `error`: string | null - Error message

**Example**:
```tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import TaskForm from '@/components/TaskForm';
import { fetchTask, updateTask } from '@/lib/api';
import type { Task, TaskFormData } from '@/types';

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTask();
  }, [taskId]);

  const loadTask = async () => {
    try {
      const response = await fetchTask(taskId);
      setTask(response.data);
    } catch (err) {
      setError('Failed to load task');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: TaskFormData) => {
    setLoading(true);
    setError(null);

    try {
      await updateTask(taskId, data);
      router.push('/?success=Task updated successfully');
    } catch (err) {
      setError('Failed to update task. Please try again.');
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/');
  };

  if (loading && !task) {
    return <div className="container mx-auto px-4 py-8">Loading...</div>;
  }

  if (error && !task) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Edit Task</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      <TaskForm
        initialData={task}
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        loading={loading}
      />
    </main>
  );
}
```

---

#### TaskForm (components/TaskForm.tsx)
**Purpose**: Reusable form component for creating/editing tasks.

**Props**:
- `initialData?`: Task - Initial values for edit mode
- `onSubmit`: (data: TaskFormData) => void - Submit callback
- `onCancel`: () => void - Cancel callback
- `loading`: boolean - Loading state

**State**:
- `formData`: TaskFormData - Form field values
- `errors`: Record<string, string> - Validation errors
- `touched`: Record<string, boolean> - Touched fields

**Example**:
```tsx
'use client';

import { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import type { Task, TaskFormData } from '@/types';

interface TaskFormProps {
  initialData?: Task;
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
  loading: boolean;
}

export default function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  loading
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    priority: initialData?.priority || 'medium',
    category: initialData?.category || '',
    due_date: initialData?.due_date ? new Date(initialData.due_date) : null,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = (name: string, value: any): string | null => {
    switch (name) {
      case 'title':
        if (!value || !value.trim()) {
          return 'Title is required';
        }
        if (value.length > 200) {
          return 'Title must be 200 characters or less';
        }
        return null;

      case 'description':
        if (value && value.length > 1000) {
          return 'Description must be 1000 characters or less';
        }
        return null;

      case 'category':
        if (value && value.length > 50) {
          return 'Category must be 50 characters or less';
        }
        return null;

      case 'due_date':
        if (value && value < new Date()) {
          return 'Due date must be in the future';
        }
        return null;

      default:
        return null;
    }
  };

  const handleChange = (name: string, value: any) => {
    setFormData(prev => ({ ...prev, [name]: value }));

    // Validate on change if field was touched
    if (touched[name]) {
      const error = validateField(name, value);
      setErrors(prev => ({
        ...prev,
        [name]: error || ''
      }));
    }
  };

  const handleBlur = (name: string) => {
    setTouched(prev => ({ ...prev, [name]: true }));

    const error = validateField(name, formData[name as keyof TaskFormData]);
    setErrors(prev => ({
      ...prev,
      [name]: error || ''
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate all fields
    const newErrors: Record<string, string> = {};
    Object.keys(formData).forEach(key => {
      const error = validateField(key, formData[key as keyof TaskFormData]);
      if (error) newErrors[key] = error;
    });

    setErrors(newErrors);
    setTouched({
      title: true,
      description: true,
      category: true,
      due_date: true,
    });

    // Submit if no errors
    if (Object.keys(newErrors).length === 0) {
      onSubmit({
        ...formData,
        due_date: formData.due_date?.toISOString() || null,
      });
    }
  };

  const isValid = !errors.title && formData.title.trim().length > 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Title Field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={formData.title}
          onChange={(e) => handleChange('title', e.target.value)}
          onBlur={() => handleBlur('title')}
          className={`
            w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2
            ${errors.title && touched.title
              ? 'border-red-300 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
            }
          `}
          placeholder="e.g., Buy groceries"
          maxLength={200}
          disabled={loading}
        />
        {errors.title && touched.title && (
          <p className="text-red-600 text-sm mt-1">{errors.title}</p>
        )}
        <p className="text-gray-500 text-xs mt-1">
          {formData.title.length}/200 characters
        </p>
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) => handleChange('description', e.target.value)}
          onBlur={() => handleBlur('description')}
          rows={4}
          className={`
            w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2
            ${errors.description && touched.description
              ? 'border-red-300 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
            }
          `}
          placeholder="Add more details about this task..."
          maxLength={1000}
          disabled={loading}
        />
        {errors.description && touched.description && (
          <p className="text-red-600 text-sm mt-1">{errors.description}</p>
        )}
        <p className="text-gray-500 text-xs mt-1">
          {formData.description.length}/1000 characters
        </p>
      </div>

      {/* Priority Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Priority
        </label>
        <div className="flex gap-4">
          {(['high', 'medium', 'low'] as const).map(priority => (
            <label
              key={priority}
              className={`
                flex-1 flex items-center justify-center px-4 py-3 border-2 rounded-lg cursor-pointer
                transition-all
                ${formData.priority === priority
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
                }
              `}
            >
              <input
                type="radio"
                name="priority"
                value={priority}
                checked={formData.priority === priority}
                onChange={(e) => handleChange('priority', e.target.value)}
                className="sr-only"
                disabled={loading}
              />
              <span className={`
                font-medium capitalize
                ${priority === 'high' ? 'text-red-600' : ''}
                ${priority === 'medium' ? 'text-yellow-600' : ''}
                ${priority === 'low' ? 'text-blue-600' : ''}
              `}>
                {priority}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Category Field */}
      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
          Category
        </label>
        <input
          type="text"
          id="category"
          value={formData.category}
          onChange={(e) => handleChange('category', e.target.value)}
          onBlur={() => handleBlur('category')}
          className={`
            w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2
            ${errors.category && touched.category
              ? 'border-red-300 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
            }
          `}
          placeholder="e.g., work, personal, home"
          maxLength={50}
          disabled={loading}
        />
        {errors.category && touched.category && (
          <p className="text-red-600 text-sm mt-1">{errors.category}</p>
        )}
      </div>

      {/* Due Date Field */}
      <div>
        <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
          Due Date
        </label>
        <div className="relative">
          <DatePicker
            selected={formData.due_date}
            onChange={(date) => handleChange('due_date', date)}
            onBlur={() => handleBlur('due_date')}
            minDate={new Date()}
            dateFormat="MMM d, yyyy"
            placeholderText="Select a due date"
            className={`
              w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2
              ${errors.due_date && touched.due_date
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
              }
            `}
            disabled={loading}
            isClearable
          />
          <Calendar className="absolute right-3 top-2.5 w-5 h-5 text-gray-400 pointer-events-none" />
        </div>
        {errors.due_date && touched.due_date && (
          <p className="text-red-600 text-sm mt-1">{errors.due_date}</p>
        )}
      </div>

      {/* Form Actions */}
      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={!isValid || loading}
          className={`
            flex-1 px-6 py-3 rounded-lg font-medium transition-colors
            ${isValid && !loading
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }
          `}
        >
          {loading ? 'Saving...' : initialData ? 'Update Task' : 'Create Task'}
        </button>

        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
```

---

## TypeScript Types

```typescript
// types/index.ts (additions)

export interface TaskFormData {
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: string;
  due_date: Date | null;
}
```

---

## API Client Functions

```typescript
// lib/api.ts (additions)

export async function createTask(data: TaskFormData): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      due_date: data.due_date?.toISOString() || null,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create task');
  }

  return response.json();
}

export async function fetchTask(taskId: string): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch task');
  }

  return response.json();
}

export async function updateTask(
  taskId: string,
  data: TaskFormData
): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      due_date: data.due_date?.toISOString() || null,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update task');
  }

  return response.json();
}
```

---

## Validation Rules

### Client-Side Validation
1. **Title**: Required, 1-200 characters, non-empty after trim
2. **Description**: Optional, max 1000 characters
3. **Priority**: Required, one of: high, medium, low
4. **Category**: Optional, max 50 characters
5. **Due Date**: Optional, must be future date

### Validation Timing
- **On Change**: Validate if field was previously touched
- **On Blur**: Mark field as touched, validate
- **On Submit**: Validate all fields, prevent submission if errors

### Error Messages
- Title empty: "Title is required"
- Title too long: "Title must be 200 characters or less"
- Description too long: "Description must be 1000 characters or less"
- Category too long: "Category must be 50 characters or less"
- Due date past: "Due date must be in the future"

---

## Accessibility

### Keyboard Navigation
- Tab through all form fields
- Enter to submit form
- Escape to cancel (close modal if applicable)
- Arrow keys in date picker

### ARIA Labels
- Required fields marked with asterisk and aria-required
- Error messages linked with aria-describedby
- Form has aria-label="Task form"
- Submit button has aria-busy during loading

### Screen Reader Support
- Field labels read before inputs
- Validation errors announced
- Loading state announced
- Success/error messages announced

---

## Error Handling

### Validation Errors
- Show inline next to field
- Red border on invalid fields
- Disable submit until valid

### API Errors
- Display error message above form
- Keep form data (don't clear)
- Allow user to retry
- Log error to console

### Network Errors
- Show "Network error" message
- Provide retry button
- Consider offline mode (future)

---

## Mobile Considerations

### Responsive Design
- Full-width inputs on mobile
- Larger touch targets (min 44x44px)
- Stack priority buttons vertically on small screens
- Native date picker on mobile devices

### Input Types
- `type="text"` for title and category
- `type="textarea"` for description
- Native date input fallback for mobile

---

## Testing Strategy

### Component Tests
- Form renders with empty fields (create mode)
- Form renders with initial data (edit mode)
- Validation errors display correctly
- Submit button disabled when invalid
- Form submission calls onSubmit with correct data

### Integration Tests
- Create task flow (fill form, submit, redirect)
- Edit task flow (load task, update, submit, redirect)
- Cancel returns to task list
- Validation prevents invalid submission

### Manual Testing
- Test on mobile devices
- Test with screen reader
- Test keyboard navigation
- Test date picker on different browsers

---

## Edge Cases

1. **Very Long Title**: Truncate at 200 characters, show counter
2. **Past Due Date**: Prevent selection in date picker
3. **Empty Description**: Allow (optional field)
4. **Special Characters**: Allow in all text fields
5. **Network Timeout**: Show error, allow retry
6. **Concurrent Edit**: Last write wins (no conflict resolution)

---

## Dependencies
- `architecture/00-system-architecture.md`
- `architecture/02-api-design.md`
- `backend/01-task-crud-api.md`
- `frontend/01-task-list-ui.md`

## Related Specifications
- `frontend/03-filters-sorting.md` - Filter and sort controls

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: Frontend Developer
