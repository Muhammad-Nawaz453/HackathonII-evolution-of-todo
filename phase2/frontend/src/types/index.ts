// TypeScript type definitions for the Todo application

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

export interface TaskFormData {
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: string;
  due_date: Date | null;
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

export interface ErrorResponse {
  detail: string;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}
