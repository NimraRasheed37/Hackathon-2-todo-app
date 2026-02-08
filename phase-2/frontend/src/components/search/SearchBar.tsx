"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Task, Tag, TaskPriority, FilterStatus } from "@/types";

interface SearchFilters {
  text?: string;
  status?: FilterStatus[];
  priority?: TaskPriority[];
  tags?: string[];
  dueDateFrom?: string;
  dueDateTo?: string;
  hasRecurrence?: boolean;
}

interface SearchBarProps {
  onSearch: (filters: SearchFilters) => void;
  availableTags?: Tag[];
  placeholder?: string;
  showAdvanced?: boolean;
  debounceMs?: number;
}

export function SearchBar({
  onSearch,
  availableTags = [],
  placeholder = "Search tasks...",
  showAdvanced = true,
  debounceMs = 300,
}: SearchBarProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [filters, setFilters] = useState<SearchFilters>({
    text: "",
    status: [],
    priority: [],
    tags: [],
    dueDateFrom: "",
    dueDateTo: "",
    hasRecurrence: undefined,
  });

  const debounceTimer = useRef<NodeJS.Timeout | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Debounced search
  const debouncedSearch = useCallback((newFilters: SearchFilters) => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }
    debounceTimer.current = setTimeout(() => {
      onSearch(newFilters);
    }, debounceMs);
  }, [onSearch, debounceMs]);

  // Update filters and trigger search
  const updateFilters = (updates: Partial<SearchFilters>) => {
    const newFilters = { ...filters, ...updates };
    setFilters(newFilters);
    debouncedSearch(newFilters);
  };

  // Clear all filters
  const clearFilters = () => {
    const emptyFilters: SearchFilters = {
      text: "",
      status: [],
      priority: [],
      tags: [],
      dueDateFrom: "",
      dueDateTo: "",
      hasRecurrence: undefined,
    };
    setFilters(emptyFilters);
    onSearch(emptyFilters);
  };

  // Toggle array filter value
  const toggleArrayFilter = <T extends string | number>(
    key: keyof Pick<SearchFilters, "status" | "priority" | "tags">,
    value: T
  ) => {
    const current = (filters[key] || []) as T[];
    const updated = current.includes(value)
      ? current.filter((v) => v !== value)
      : [...current, value];
    updateFilters({ [key]: updated });
  };

  // Check if any filters are active
  const hasActiveFilters =
    filters.text ||
    (filters.status && filters.status.length > 0) ||
    (filters.priority && filters.priority.length > 0) ||
    (filters.tags && filters.tags.length > 0) ||
    filters.dueDateFrom ||
    filters.dueDateTo ||
    filters.hasRecurrence !== undefined;

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  return (
    <div className="w-full space-y-3">
      {/* Main search input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg
            className="h-5 w-5 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <input
          ref={inputRef}
          type="text"
          value={filters.text}
          onChange={(e) => updateFilters({ text: e.target.value })}
          placeholder={placeholder}
          className="block w-full pl-10 pr-20 py-2.5 text-sm
            bg-white dark:bg-gray-800
            border border-gray-200 dark:border-gray-700 rounded-lg
            focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            placeholder-gray-400 dark:placeholder-gray-500
            text-gray-900 dark:text-white"
        />
        <div className="absolute inset-y-0 right-0 flex items-center gap-1 pr-2">
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              title="Clear all filters"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
          {showAdvanced && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className={`p-1.5 rounded-md transition-colors ${
                isExpanded
                  ? "bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400"
                  : "text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              }`}
              title="Advanced filters"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Advanced filters */}
      {showAdvanced && isExpanded && (
        <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700 space-y-4">
          {/* Status filter */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Status
            </label>
            <div className="flex flex-wrap gap-2">
              {(["pending", "completed"] as FilterStatus[]).map((status) => (
                <button
                  key={status}
                  onClick={() => toggleArrayFilter("status", status)}
                  className={`px-3 py-1 text-sm rounded-md border transition-all ${
                    (filters.status || []).includes(status)
                      ? "bg-blue-100 border-blue-300 text-blue-700 dark:bg-blue-900/30 dark:border-blue-700 dark:text-blue-300"
                      : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }`}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Priority filter */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Priority
            </label>
            <div className="flex flex-wrap gap-2">
              {(["critical", "high", "medium", "low", "none"] as TaskPriority[]).map((priority) => (
                <button
                  key={priority}
                  onClick={() => toggleArrayFilter("priority", priority)}
                  className={`px-3 py-1 text-sm rounded-md border transition-all ${
                    (filters.priority || []).includes(priority)
                      ? "bg-blue-100 border-blue-300 text-blue-700 dark:bg-blue-900/30 dark:border-blue-700 dark:text-blue-300"
                      : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }`}
                >
                  {priority.charAt(0).toUpperCase() + priority.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Tags filter */}
          {availableTags.length > 0 && (
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Tags
              </label>
              <div className="flex flex-wrap gap-2">
                {availableTags.map((tag) => (
                  <button
                    key={tag.id}
                    onClick={() => toggleArrayFilter("tags", tag.id)}
                    className={`inline-flex items-center gap-1 px-2.5 py-1 text-sm rounded-full border transition-all ${
                      (filters.tags || []).includes(tag.id)
                        ? "border-current"
                        : "border-transparent hover:border-gray-300 dark:hover:border-gray-600"
                    }`}
                    style={{
                      backgroundColor: (filters.tags || []).includes(tag.id) ? `${tag.color}20` : "transparent",
                      color: tag.color,
                    }}
                  >
                    <span className="w-2 h-2 rounded-full" style={{ backgroundColor: tag.color }} />
                    {tag.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Date range filter */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Due from
              </label>
              <input
                type="date"
                value={filters.dueDateFrom}
                onChange={(e) => updateFilters({ dueDateFrom: e.target.value })}
                className="w-full px-3 py-1.5 text-sm border rounded-md
                  bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                  focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Due to
              </label>
              <input
                type="date"
                value={filters.dueDateTo}
                onChange={(e) => updateFilters({ dueDateTo: e.target.value })}
                className="w-full px-3 py-1.5 text-sm border rounded-md
                  bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                  focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Recurrence filter */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Recurrence
            </label>
            <div className="flex gap-2">
              {[
                { value: undefined as boolean | undefined, label: "Any" },
                { value: true as boolean | undefined, label: "Recurring" },
                { value: false as boolean | undefined, label: "Non-recurring" },
              ].map((option) => (
                <button
                  key={String(option.value)}
                  onClick={() => updateFilters({ hasRecurrence: option.value })}
                  className={`px-3 py-1 text-sm rounded-md border transition-all ${
                    filters.hasRecurrence === option.value
                      ? "bg-blue-100 border-blue-300 text-blue-700 dark:bg-blue-900/30 dark:border-blue-700 dark:text-blue-300"
                      : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Active filters summary */}
      {hasActiveFilters && !isExpanded && (
        <div className="flex flex-wrap gap-2 text-sm">
          {(filters.status || []).length > 0 && (
            <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-gray-600 dark:text-gray-400">
              Status: {(filters.status || []).join(", ")}
            </span>
          )}
          {(filters.priority || []).length > 0 && (
            <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-gray-600 dark:text-gray-400">
              Priority: {(filters.priority || []).join(", ")}
            </span>
          )}
          {(filters.tags || []).length > 0 && (
            <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-gray-600 dark:text-gray-400">
              {(filters.tags || []).length} tag{(filters.tags || []).length !== 1 ? "s" : ""}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
