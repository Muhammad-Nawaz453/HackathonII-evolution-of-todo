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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTask();
  }, [taskId]);

  const loadTask = async () => {
    try {
      const response = await fetchTask(taskId);
      setTask(response.data);
    } catch (err) {
      setError('Failed to load task. Make sure the backend is running.');
      console.error('Error loading task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: TaskFormData) => {
    setSubmitting(true);
    setError(null);

    try {
      await updateTask(taskId, data);
      router.push('/?success=Task updated successfully');
    } catch (err) {
      setError('Failed to update task. Make sure the backend is running.');
      console.error('Error updating task:', err);
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.push('/');
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8 max-w-2xl">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading task...</p>
          </div>
        </div>
      </main>
    );
  }

  if (error && !task) {
    return (
      <main className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8 max-w-2xl">
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
            <p className="font-medium">⚠️ {error}</p>
            <p className="text-sm mt-1">
              Make sure the backend is running at <code className="bg-red-100 px-1 rounded">http://localhost:8000</code>
            </p>
            <button
              onClick={() => router.push('/')}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Back to Tasks
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <h1 className="text-3xl font-bold mb-8">Edit Task</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-6">
            <p className="font-medium">⚠️ {error}</p>
            <p className="text-sm mt-1">
              Make sure the backend is running at <code className="bg-red-100 px-1 rounded">http://localhost:8000</code>
            </p>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <TaskForm
            initialData={task!}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            loading={submitting}
          />
        </div>
      </div>
    </main>
  );
}
