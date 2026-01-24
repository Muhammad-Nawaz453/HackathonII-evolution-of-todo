
'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Plus } from 'lucide-react';
import TaskList from '@/components/TaskList';
import TaskFilters from '@/components/Filters';
import { fetchTasks } from '@/lib/api';
import { parseFiltersFromURL, buildQueryString } from '@/lib/utils';
import type { Task, FilterState } from '@/types';

export default function TaskListPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isLoadingRef = useRef(false);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>(() =>
    parseFiltersFromURL(searchParams)
  );

  // Sync filters with URL changes
  useEffect(() => {
    const newFilters = parseFiltersFromURL(searchParams);
    const filtersChanged = JSON.stringify(filters) !== JSON.stringify(newFilters);

    if (filtersChanged) {
      setFilters(newFilters);
    }
  }, [searchParams]);

  const loadTasks = useCallback(async () => {
    // Prevent concurrent requests
    if (isLoadingRef.current) return;

    isLoadingRef.current = true;
    setLoading(true);
    setError(null);

    try {
      const data = await fetchTasks(filters);
      setTasks(data.data || []);
    } catch (err) {
      setError('Failed to load tasks. Make sure the backend is running at http://localhost:8000');
      console.error('Error loading tasks:', err);
      setTasks([]);
    } finally {
      setLoading(false);
      isLoadingRef.current = false;
    }
  }, [filters]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleFilterChange = (newFilters: FilterState) => {
    // Only update if filters actually changed
    if (JSON.stringify(filters) === JSON.stringify(newFilters)) {
      return;
    }

    // Update URL without page reload
    const queryString = buildQueryString(newFilters);
    router.replace(`/?${queryString}`, { scroll: false });
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
  };

  const handleTaskDelete = (taskId: string) => {
    setTasks(tasks.filter(t => t.id !== taskId));
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <p className="text-gray-600 mt-1">
              {loading ? 'Loading...' : `${tasks.length} task${tasks.length !== 1 ? 's' : ''}`}
            </p>
          </div>
          <button
            onClick={() => router.push('/tasks/new')}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            New Task
          </button>
        </div>

        {/* Filters */}
        <TaskFilters filters={filters} onFilterChange={handleFilterChange} />

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading tasks...</p>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <p className="text-red-800 font-medium mb-2">⚠️ {error}</p>
            <p className="text-red-600 text-sm mb-4">
              The frontend is running, but it cannot connect to the backend API.
            </p>
            <div className="text-left bg-white rounded p-4 text-sm text-gray-700 max-w-2xl mx-auto">
              <p className="font-medium mb-2">To fix this:</p>
              <ol className="list-decimal list-inside space-y-1">
                <li>Make sure you have implemented the backend (see phase2/backend/)</li>
                <li>Start the backend: <code className="bg-gray-100 px-2 py-1 rounded">uvicorn src.main:app --reload</code></li>
                <li>Verify it's running at: <a href="http://localhost:8000/docs" target="_blank" className="text-blue-600 hover:underline">http://localhost:8000/docs</a></li>
                <li>Refresh this page</li>
              </ol>
            </div>
            <button
              onClick={loadTasks}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {/* Task List */}
        {!loading && !error && (
          <TaskList
            tasks={tasks}
            onTaskUpdate={handleTaskUpdate}
            onTaskDelete={handleTaskDelete}
          />
        )}
      </div>
    </main>
  );
}
