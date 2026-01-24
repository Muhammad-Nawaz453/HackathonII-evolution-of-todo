// API client for communicating with the backend

import type { Task, TaskFormData, FilterState, TaskListResponse, ApiResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Fetch all tasks with optional filters
 */
export async function fetchTasks(filters: FilterState): Promise<TaskListResponse> {
  const params = new URLSearchParams();

  if (filters.status) params.append('status', filters.status);
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  params.append('sort', filters.sort);
  params.append('order', filters.order);

  const response = await fetch(`${API_URL}/tasks?${params}`);

  if (!response.ok) {
    throw new Error('Failed to fetch tasks');
  }

  return response.json();
}

/**
 * Fetch a single task by ID
 */
export async function fetchTask(taskId: string): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch task');
  }

  return response.json();
}

/**
 * Create a new task
 */
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

/**
 * Update an existing task (partial update)
 */
export async function updateTask(
  taskId: string,
  data: Partial<TaskFormData>
): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      due_date: data.due_date ? data.due_date.toISOString() : undefined,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update task');
  }

  return response.json();
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: string): Promise<void> {
  const response = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Failed to delete task');
  }
}

/**
 * Toggle task completion status
 */
export async function toggleTaskStatus(
  taskId: string,
  endpoint: 'complete' | 'incomplete'
): Promise<ApiResponse<Task>> {
  const response = await fetch(`${API_URL}/tasks/${taskId}/${endpoint}`, {
    method: 'PATCH',
  });

  if (!response.ok) {
    throw new Error('Failed to update task status');
  }

  return response.json();
}
