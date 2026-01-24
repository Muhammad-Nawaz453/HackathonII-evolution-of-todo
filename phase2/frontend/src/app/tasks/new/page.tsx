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
      setError('Failed to create task. Make sure the backend is running.');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/');
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <h1 className="text-3xl font-bold mb-8">Create New Task</h1>

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
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            loading={loading}
          />
        </div>
      </div>
    </main>
  );
}
