'use client';

import { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';
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
      onSubmit(formData);
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
          <input
            type="date"
            id="due_date"
            value={formData.due_date ? formData.due_date.toISOString().split('T')[0] : ''}
            onChange={(e) => handleChange('due_date', e.target.value ? new Date(e.target.value) : null)}
            onBlur={() => handleBlur('due_date')}
            min={new Date().toISOString().split('T')[0]}
            className={`
              w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2
              ${errors.due_date && touched.due_date
                ? 'border-red-300 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
              }
            `}
            disabled={loading}
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
