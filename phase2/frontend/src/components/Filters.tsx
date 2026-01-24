'use client';

import { useState, useEffect, useCallback } from 'react';
import { Search, X, ArrowUpDown } from 'lucide-react';
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
