# Frontend Specification: Filters and Sorting

## Feature Name
Task Filtering and Sorting Controls - Frontend Implementation

## Purpose
Implement filter and sort controls that allow users to narrow down their task list by status, priority, category, and search keywords, as well as sort tasks by different criteria.

## User Stories

1. **As a user**, I want to filter tasks by completion status so I can focus on incomplete tasks.
2. **As a user**, I want to filter tasks by priority so I can see high-priority items first.
3. **As a user**, I want to filter tasks by category so I can view work or personal tasks separately.
4. **As a user**, I want to search tasks by keyword so I can quickly find specific tasks.
5. **As a user**, I want to sort tasks by due date, priority, or creation date.
6. **As a user**, I want my filter and sort preferences to persist in the URL so I can bookmark or share filtered views.
7. **As a user**, I want to clear all filters with one click.

## Acceptance Criteria

### Filter Controls
- [ ] Status filter: All, Complete, Incomplete (radio buttons or tabs)
- [ ] Priority filter: All, High, Medium, Low (dropdown or checkboxes)
- [ ] Category filter: All, or specific category (dropdown with dynamic categories)
- [ ] Search input: Text field with debounced search (300ms)
- [ ] Clear filters button: Resets all filters to defaults

### Sort Controls
- [ ] Sort by: Due Date, Priority, Created Date, Title (dropdown)
- [ ] Sort order: Ascending, Descending (toggle button)
- [ ] Default sort: Created Date, Descending (newest first)

### URL Synchronization
- [ ] Filters reflected in URL query parameters
- [ ] URL changes update filters
- [ ] Shareable URLs with filters applied
- [ ] Browser back/forward buttons work correctly

### Visual Feedback
- [ ] Active filters highlighted
- [ ] Filter count badge (e.g., "3 filters active")
- [ ] Loading state while fetching filtered results
- [ ] Empty state when no results match filters

### Performance
- [ ] Search input debounced (300ms)
- [ ] Filters applied without page reload
- [ ] Smooth transitions between filter states

## Component Architecture

### Component Hierarchy
```
TaskFilters (components/Filters.tsx)
├── StatusFilter (tabs or radio buttons)
├── PriorityFilter (dropdown)
├── CategoryFilter (dropdown)
├── SearchInput (text input with debounce)
├── SortControls (dropdown + toggle)
└── ClearFiltersButton
```

### Component Specifications

#### TaskFilters (components/Filters.tsx)
**Purpose**: Main filter component containing all filter controls.

**Props**:
- `filters`: FilterState - Current filter values
- `onFilterChange`: (filters: FilterState) => void - Callback when filters change

**State**:
- `searchInput`: string - Local search input (before debounce)
- `categories`: string[] - Available categories (fetched from API or derived from tasks)

**Example**:
```tsx
'use client';

import { useState, useEffect, useCallback } from 'react';
import { Search, X, ChevronDown, ArrowUpDown } from 'lucide-react';
import { debounce } from '@/lib/utils';
import type { FilterState } from '@/types';

interface TaskFiltersProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
}

export default function TaskFilters({ filters, onFilterChange }: TaskFiltersProps) {
  const [searchInput, setSearchInput] = useState(filters.search);

  // Debounced search handler
  const debouncedSearch = useCallback(
    debounce((value: string) => {
      onFilterChange({ ...filters, search: value });
    }, 300),
    [filters, onFilterChange]
  );

  useEffect(() => {
    debouncedSearch(searchInput);
  }, [searchInput, debouncedSearch]);

  const handleFilterChange = (key: keyof FilterState, value: any) => {
    onFilterChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    setSearchInput('');
    onFilterChange({
      status: null,
      priority: null,
      category: null,
      search: '',
      sort: 'created_at',
      order: 'desc',
    });
  };

  const activeFilterCount = [
    filters.status,
    filters.priority,
    filters.category,
    filters.search,
  ].filter(Boolean).length;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
      {/* Search Bar */}
      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search tasks..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {searchInput && (
            <button
              onClick={() => setSearchInput('')}
              className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
              aria-label="Clear search"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Filter Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <div className="flex gap-2">
            {[
              { value: null, label: 'All' },
              { value: 'incomplete', label: 'Active' },
              { value: 'complete', label: 'Done' },
            ].map(option => (
              <button
                key={option.label}
                onClick={() => handleFilterChange('status', option.value)}
                className={`
                  flex-1 px-3 py-2 text-sm font-medium rounded-lg transition-colors
                  ${filters.status === option.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* Priority Filter */}
        <div>
          <label htmlFor="priority-filter" className="block text-sm font-medium text-gray-700 mb-2">
            Priority
          </label>
          <select
            id="priority-filter"
            value={filters.priority || ''}
            onChange={(e) => handleFilterChange('priority', e.target.value || null)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Category Filter */}
        <div>
          <label htmlFor="category-filter" className="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <input
            type="text"
            id="category-filter"
            value={filters.category || ''}
            onChange={(e) => handleFilterChange('category', e.target.value || null)}
            placeholder="Filter by category..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Sort Controls */}
      <div className="flex flex-wrap items-center gap-4 pb-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <label htmlFor="sort-by" className="text-sm font-medium text-gray-700">
            Sort by:
          </label>
          <select
            id="sort-by"
            value={filters.sort}
            onChange={(e) => handleFilterChange('sort', e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="created_at">Created Date</option>
            <option value="due_date">Due Date</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
          </select>
        </div>

        <button
          onClick={() => handleFilterChange('order', filters.order === 'asc' ? 'desc' : 'asc')}
          className="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          aria-label={`Sort ${filters.order === 'asc' ? 'descending' : 'ascending'}`}
        >
          <ArrowUpDown className="w-4 h-4" />
          {filters.order === 'asc' ? 'Ascending' : 'Descending'}
        </button>
      </div>

      {/* Active Filters & Clear Button */}
      {activeFilterCount > 0 && (
        <div className="flex items-center justify-between pt-4">
          <span className="text-sm text-gray-600">
            {activeFilterCount} filter{activeFilterCount !== 1 ? 's' : ''} active
          </span>
          <button
            onClick={clearFilters}
            className="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
            Clear Filters
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## URL Synchronization

### Using Next.js Router
```tsx
// In TaskListPage component

import { useRouter, useSearchParams } from 'next/navigation';

export default function TaskListPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Initialize filters from URL
  const [filters, setFilters] = useState<FilterState>({
    status: searchParams.get('status') as any || null,
    priority: searchParams.get('priority') as any || null,
    category: searchParams.get('category') || null,
    search: searchParams.get('search') || '',
    sort: searchParams.get('sort') as any || 'created_at',
    order: searchParams.get('order') as any || 'desc',
  });

  // Update URL when filters change
  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters);

    // Build query string
    const params = new URLSearchParams();
    if (newFilters.status) params.set('status', newFilters.status);
    if (newFilters.priority) params.set('priority', newFilters.priority);
    if (newFilters.category) params.set('category', newFilters.category);
    if (newFilters.search) params.set('search', newFilters.search);
    params.set('sort', newFilters.sort);
    params.set('order', newFilters.order);

    // Update URL without page reload
    router.push(`/?${params.toString()}`, { scroll: false });
  };

  // ... rest of component
}
```

---

## Utility Functions

```typescript
// lib/utils.ts (additions)

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

export function buildQueryString(filters: FilterState): string {
  const params = new URLSearchParams();

  if (filters.status) params.append('status', filters.status);
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  params.append('sort', filters.sort);
  params.append('order', filters.order);

  return params.toString();
}

export function parseFiltersFromURL(searchParams: URLSearchParams): FilterState {
  return {
    status: searchParams.get('status') as any || null,
    priority: searchParams.get('priority') as any || null,
    category: searchParams.get('category') || null,
    search: searchParams.get('search') || '',
    sort: (searchParams.get('sort') as any) || 'created_at',
    order: (searchParams.get('order') as any) || 'desc',
  };
}
```

---

## Filter Presets (Optional Enhancement)

```tsx
// Predefined filter combinations

const FILTER_PRESETS = [
  {
    name: 'Today',
    filters: {
      status: 'incomplete',
      sort: 'due_date',
      order: 'asc',
    },
  },
  {
    name: 'High Priority',
    filters: {
      status: 'incomplete',
      priority: 'high',
      sort: 'due_date',
      order: 'asc',
    },
  },
  {
    name: 'Overdue',
    filters: {
      status: 'incomplete',
      sort: 'due_date',
      order: 'asc',
      // Note: Backend would need to support overdue filter
    },
  },
];

// Preset buttons component
function FilterPresets({ onApplyPreset }: { onApplyPreset: (filters: Partial<FilterState>) => void }) {
  return (
    <div className="flex gap-2 mb-4">
      {FILTER_PRESETS.map(preset => (
        <button
          key={preset.name}
          onClick={() => onApplyPreset(preset.filters)}
          className="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          {preset.name}
        </button>
      ))}
    </div>
  );
}
```

---

## Mobile Responsive Design

```tsx
// Mobile-optimized filter component

export default function TaskFiltersMobile({ filters, onFilterChange }: TaskFiltersProps) {
  const [showFilters, setShowFilters] = useState(false);

  return (
    <>
      {/* Mobile Filter Toggle Button */}
      <button
        onClick={() => setShowFilters(!showFilters)}
        className="md:hidden w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-200 rounded-lg mb-4"
      >
        <span className="font-medium">Filters & Sort</span>
        <ChevronDown className={`w-5 h-5 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
      </button>

      {/* Filter Panel (collapsible on mobile) */}
      <div className={`
        md:block
        ${showFilters ? 'block' : 'hidden'}
      `}>
        {/* Filter controls here */}
      </div>
    </>
  );
}
```

---

## Accessibility

### Keyboard Navigation
- Tab through all filter controls
- Enter to apply filter
- Escape to close dropdowns
- Arrow keys in dropdowns

### ARIA Labels
- Search input: aria-label="Search tasks"
- Status filter: aria-label="Filter by status"
- Priority filter: aria-label="Filter by priority"
- Category filter: aria-label="Filter by category"
- Sort dropdown: aria-label="Sort tasks by"
- Clear button: aria-label="Clear all filters"

### Screen Reader Support
- Announce filter changes
- Announce result count after filtering
- Announce loading state
- Announce empty state

---

## Performance Optimizations

### Debouncing
```typescript
// Debounce search input to reduce API calls
const debouncedSearch = useCallback(
  debounce((value: string) => {
    onFilterChange({ ...filters, search: value });
  }, 300),
  [filters, onFilterChange]
);
```

### Memoization
```typescript
// Memoize filter options to prevent recalculation
const filterOptions = useMemo(() => {
  return {
    categories: [...new Set(tasks.map(t => t.category).filter(Boolean))],
  };
}, [tasks]);
```

### URL Updates
```typescript
// Use shallow routing to avoid full page reload
router.push(`/?${params.toString()}`, { scroll: false });
```

---

## Testing Strategy

### Component Tests
- Filters render correctly
- Status filter updates state
- Priority filter updates state
- Category filter updates state
- Search input debounces correctly
- Sort controls update state
- Clear filters resets all values

### Integration Tests
- Filters update URL parameters
- URL parameters initialize filters
- Filtered results display correctly
- Empty state shows when no results
- Loading state shows during fetch

### Manual Testing
- Test on mobile devices
- Test with screen reader
- Test keyboard navigation
- Test browser back/forward buttons
- Test shareable URLs

---

## Edge Cases

1. **No Results**: Show empty state with clear filters button
2. **Invalid URL Parameters**: Ignore invalid values, use defaults
3. **Special Characters in Search**: Properly encode in URL
4. **Very Long Category Names**: Truncate in dropdown
5. **Rapid Filter Changes**: Debounce to prevent excessive API calls
6. **Browser Back Button**: Restore previous filter state
7. **Bookmark with Filters**: Filters applied on page load

---

## Visual Design

### Filter States
- **Default**: Gray background, dark text
- **Active**: Blue background, white text
- **Hover**: Slightly darker background
- **Disabled**: Reduced opacity, no hover effect

### Sort Indicators
- Ascending: ↑ arrow icon
- Descending: ↓ arrow icon
- Active sort field highlighted

### Filter Badge
- Show count of active filters
- Red badge with white text
- Position: Top-right of filter button (mobile)

---

## API Integration

### Query Parameters
```typescript
// Build query string from filters
const queryString = buildQueryString(filters);

// Fetch tasks with filters
const response = await fetch(`${API_URL}/tasks?${queryString}`);
```

### Example API Call
```
GET /api/v1/tasks?status=incomplete&priority=high&sort=due_date&order=asc&search=groceries
```

---

## Future Enhancements

1. **Saved Filters**: Allow users to save filter combinations
2. **Filter History**: Recent filter combinations
3. **Advanced Filters**: Date ranges, multiple categories
4. **Filter Suggestions**: Auto-suggest categories as user types
5. **Bulk Actions**: Select multiple tasks, apply actions
6. **Export Filtered Results**: Download as CSV/JSON

---

## Dependencies
- `architecture/00-system-architecture.md`
- `architecture/02-api-design.md`
- `backend/01-task-crud-api.md`
- `frontend/01-task-list-ui.md`

## Related Specifications
- `frontend/02-task-form.md` - Task creation/editing form

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: Frontend Developer
