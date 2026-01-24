# Todo Frontend - Next.js

## Overview

Modern, responsive web interface for the Todo Web Application, built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- **Task Management**: Create, read, update, delete tasks
- **Filtering**: Filter by status, priority, category
- **Search**: Search tasks by keyword
- **Sorting**: Sort by due date, priority, created date, title
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Accessible**: Keyboard navigation, screen reader support
- **Real-time Updates**: Optimistic UI updates

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **HTTP Client**: Fetch API
- **Date Picker**: react-datepicker
- **Icons**: Lucide React
- **Deployment**: Vercel

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main task list page
│   │   ├── layout.tsx            # Root layout
│   │   ├── tasks/
│   │   │   ├── new/
│   │   │   │   └── page.tsx      # Create task page
│   │   │   └── [id]/
│   │   │       └── edit/
│   │   │           └── page.tsx  # Edit task page
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   ├── TaskList.tsx          # Task list component
│   │   ├── TaskItem.tsx          # Single task component
│   │   ├── TaskForm.tsx          # Task form component
│   │   └── Filters.tsx           # Filter/sort controls
│   ├── lib/
│   │   ├── api.ts                # API client functions
│   │   └── utils.ts              # Utility functions
│   └── types/
│       └── index.ts              # TypeScript type definitions
├── public/                       # Static assets
├── .env.local.example            # Environment variables template
├── .env.local                    # Environment variables (not committed)
├── package.json                  # Dependencies
├── tsconfig.json                 # TypeScript configuration
├── tailwind.config.ts            # Tailwind configuration
├── next.config.js                # Next.js configuration
└── README.md                     # This file
```

## Setup

### Prerequisites

- Node.js 18 or higher
- npm or pnpm
- Backend API running (see `../backend/README.md`)

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local` and add your backend API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

4. **Start development server**:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

The application will be available at `http://localhost:3000`

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

### Code Style

- **TypeScript**: Strict mode enabled
- **ESLint**: Next.js configuration
- **Prettier**: Line length 100
- **Components**: Functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions

### Component Guidelines

**Good Component**:
```tsx
interface TaskItemProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  // Component logic
  return (
    // JSX
  );
}
```

**Component Checklist**:
- [ ] TypeScript interface for props
- [ ] Descriptive prop names
- [ ] Proper event handlers
- [ ] Accessibility attributes (ARIA labels)
- [ ] Responsive design (Tailwind classes)
- [ ] Error handling

### State Management

- **Server State**: Fetched from API, cached in component state
- **UI State**: Local component state (forms, modals, etc.)
- **URL State**: Filters and sort in URL query parameters

### API Integration

All API calls go through `lib/api.ts`:

```typescript
import { fetchTasks, createTask, updateTask, deleteTask } from '@/lib/api';

// Fetch tasks
const response = await fetchTasks(filters);
const tasks = response.data;

// Create task
const newTask = await createTask(formData);

// Update task
const updated = await updateTask(taskId, formData);

// Delete task
await deleteTask(taskId);
```

## Features

### Task List

**Location**: `src/app/page.tsx`

- Displays all tasks
- Supports filtering and sorting
- Shows loading and error states
- Empty state when no tasks
- Responsive grid/list layout

### Task Form

**Location**: `src/components/TaskForm.tsx`

- Create new tasks: `/tasks/new`
- Edit existing tasks: `/tasks/{id}/edit`
- Client-side validation
- Date picker for due dates
- Priority selection (high/medium/low)
- Category input

### Filters & Sorting

**Location**: `src/components/Filters.tsx`

- Filter by status (all/complete/incomplete)
- Filter by priority (all/high/medium/low)
- Filter by category
- Search by keyword (debounced)
- Sort by due date, priority, created date, title
- Sort order (ascending/descending)
- Clear all filters button

### Task Actions

- **Complete/Incomplete**: Toggle with checkbox
- **Edit**: Navigate to edit form
- **Delete**: Confirm and delete

## Styling

### Tailwind CSS

**Color Scheme**:
- Primary: Blue (`blue-600`)
- Success: Green (`green-500`)
- Warning: Yellow (`yellow-500`)
- Danger: Red (`red-600`)
- Neutral: Gray (`gray-*`)

**Common Classes**:
```tsx
// Button
className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"

// Input
className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"

// Card
className="bg-white rounded-lg shadow-sm border border-gray-200 p-4"
```

### Responsive Design

```tsx
// Mobile-first approach
className="
  w-full           // Mobile: full width
  md:w-1/2         // Tablet: half width
  lg:w-1/3         // Desktop: third width
"
```

## Accessibility

### Keyboard Navigation

- Tab through interactive elements
- Enter to submit forms
- Escape to close modals
- Arrow keys in dropdowns

### ARIA Labels

```tsx
<button aria-label="Mark task complete">
  <Check className="w-5 h-5" />
</button>

<input
  type="text"
  aria-label="Search tasks"
  aria-describedby="search-help"
/>
```

### Screen Reader Support

- Semantic HTML (`<main>`, `<nav>`, `<button>`)
- Alt text for images
- Form labels
- Error messages linked to inputs

## Testing

### Component Testing

```bash
npm test
```

### Manual Testing Checklist

- [ ] Create task with all fields
- [ ] Create task with only title
- [ ] Edit existing task
- [ ] Delete task (with confirmation)
- [ ] Mark task complete/incomplete
- [ ] Filter by status
- [ ] Filter by priority
- [ ] Search tasks
- [ ] Sort tasks
- [ ] Clear filters
- [ ] Test on mobile device
- [ ] Test with keyboard only
- [ ] Test with screen reader

## Deployment

### Vercel (Recommended)

1. **Push to GitHub**:
   ```bash
   git push origin main
   ```

2. **Import in Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select `frontend` as root directory

3. **Configure Environment Variables**:
   - Add `NEXT_PUBLIC_API_URL` with your backend URL
   - Example: `https://your-backend.railway.app/api/v1`

4. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy automatically

### Manual Deployment

```bash
# Build for production
npm run build

# Start production server
npm run start
```

## Environment Variables

### Development

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Production

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
```

**Note**: All environment variables must be prefixed with `NEXT_PUBLIC_` to be accessible in the browser.

## Troubleshooting

### API Connection Issues

**Error**: `Failed to fetch`
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` is correct
- Inspect Network tab in DevTools
- Check CORS configuration in backend

**Error**: `CORS policy`
- Verify backend `CORS_ORIGINS` includes frontend URL
- Ensure URLs match exactly (no trailing slash)

### Build Issues

**Error**: `Module not found`
- Delete `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Rebuild: `npm run build`

**Error**: `Type error`
- Check TypeScript types in `src/types/`
- Verify API response matches type definitions
- Run type check: `npx tsc --noEmit`

### Performance Issues

**Slow page load**:
- Check API response times
- Enable caching (React Query or SWR)
- Optimize images with Next.js Image component
- Use code splitting for large components

## Best Practices

### Performance

- Use `React.memo` for expensive components
- Debounce search inputs (300ms)
- Paginate large lists
- Lazy load routes with `next/dynamic`

### Security

- Sanitize user inputs (React does this by default)
- Validate on both client and server
- Use HTTPS in production
- Don't expose sensitive data in client code

### User Experience

- Show loading states
- Provide error messages
- Use optimistic updates
- Support keyboard navigation
- Test on mobile devices

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Vercel Documentation](https://vercel.com/docs)

## Support

For issues or questions:
1. Check specifications in `../specs/frontend/`
2. Review troubleshooting section above
3. Check browser console for errors
4. Verify backend API is working (test at `/docs`)
5. Review constitution in `../constitution.md`

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Ready for Implementation
