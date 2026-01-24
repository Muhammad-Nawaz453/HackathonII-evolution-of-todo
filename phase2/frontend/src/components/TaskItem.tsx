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
      alert('Failed to update task status. Make sure the backend is running.');
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
      alert('Failed to delete task. Make sure the backend is running.');
      setLoading(false);
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.status;
  const priorityColor = getPriorityColor(task.priority);

  return (
    <div className={`
      bg-white rounded-lg shadow-sm border p-4 transition-all
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
            w-5 h-5 rounded border-2 flex items-center justify-center transition-colors
            ${task.status ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-gray-400'}
            ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
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
              px-2 py-1 text-xs font-medium rounded-full flex-shrink-0 capitalize
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
            disabled={loading}
          >
            <Edit className="w-4 h-4" />
          </button>

          <button
            onClick={handleDelete}
            disabled={loading}
            className="p-2 text-gray-400 hover:text-red-600 transition disabled:opacity-50"
            aria-label="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
