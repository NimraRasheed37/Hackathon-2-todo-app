"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { Task, Tag, TaskPriority, FilterStatus, SearchResults } from "@/types";

interface SearchFilters {
  text: string;
  status: FilterStatus[];
  priority: TaskPriority[];
  tags: number[];
  dueDateFrom: string;
  dueDateTo: string;
  hasRecurrence: boolean | null;
}

interface UseSearchOptions {
  userId: string;
  token: string;
  apiUrl?: string;
  debounceMs?: number;
  defaultLimit?: number;
}

interface UseSearchResult {
  results: Task[];
  total: number;
  hasMore: boolean;
  isLoading: boolean;
  error: Error | null;
  search: (filters: SearchFilters) => void;
  loadMore: () => Promise<void>;
  reset: () => void;
}

export function useSearch({
  userId,
  token,
  apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  debounceMs = 300,
  defaultLimit = 20,
}: UseSearchOptions): UseSearchResult {
  const [results, setResults] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const currentFilters = useRef<SearchFilters | null>(null);
  const currentOffset = useRef(0);
  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  const executeSearch = useCallback(
    async (filters: SearchFilters, offset: number = 0) => {
      try {
        setIsLoading(true);
        setError(null);

        const requestBody: Record<string, unknown> = {
          limit: defaultLimit,
          offset,
        };

        if (filters.text) {
          requestBody.text = filters.text;
        }

        if (filters.status.length > 0) {
          requestBody.status = filters.status;
        }

        if (filters.priority.length > 0) {
          requestBody.priority = filters.priority;
        }

        if (filters.tags.length > 0) {
          requestBody.tags = filters.tags;
        }

        if (filters.dueDateFrom) {
          requestBody.due_date_from = filters.dueDateFrom;
        }

        if (filters.dueDateTo) {
          requestBody.due_date_to = filters.dueDateTo;
        }

        if (filters.hasRecurrence !== null) {
          requestBody.has_recurrence = filters.hasRecurrence;
        }

        const response = await fetch(
          `${apiUrl}/api/${userId}/tasks/search`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
          }
        );

        if (!response.ok) {
          throw new Error(`Search failed: ${response.status}`);
        }

        const data: SearchResults = await response.json();

        if (offset === 0) {
          setResults(data.results);
        } else {
          setResults((prev) => [...prev, ...data.results]);
        }

        setTotal(data.total);
        setHasMore(data.hasMore);
        currentOffset.current = offset + data.results.length;
      } catch (err) {
        setError(err instanceof Error ? err : new Error("Search failed"));
      } finally {
        setIsLoading(false);
      }
    },
    [userId, token, apiUrl, defaultLimit]
  );

  const search = useCallback(
    (filters: SearchFilters) => {
      // Cancel previous debounce
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }

      // Store current filters
      currentFilters.current = filters;
      currentOffset.current = 0;

      // Debounce the search
      debounceTimer.current = setTimeout(() => {
        executeSearch(filters, 0);
      }, debounceMs);
    },
    [executeSearch, debounceMs]
  );

  const loadMore = useCallback(async () => {
    if (!currentFilters.current || isLoading || !hasMore) {
      return;
    }

    await executeSearch(currentFilters.current, currentOffset.current);
  }, [executeSearch, isLoading, hasMore]);

  const reset = useCallback(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }
    setResults([]);
    setTotal(0);
    setHasMore(false);
    setError(null);
    currentFilters.current = null;
    currentOffset.current = 0;
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  return {
    results,
    total,
    hasMore,
    isLoading,
    error,
    search,
    loadMore,
    reset,
  };
}

// Quick search hook for autocomplete
interface UseQuickSearchResult {
  tasks: { id: number; title: string; completed: boolean }[];
  tags: { id: number; name: string; color: string }[];
  isLoading: boolean;
  search: (query: string) => void;
  clear: () => void;
}

export function useQuickSearch({
  userId,
  token,
  apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  debounceMs = 150,
}: Omit<UseSearchOptions, "defaultLimit">): UseQuickSearchResult {
  const [tasks, setTasks] = useState<{ id: number; title: string; completed: boolean }[]>([]);
  const [tags, setTags] = useState<{ id: number; name: string; color: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  const search = useCallback(
    (query: string) => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }

      if (!query.trim()) {
        setTasks([]);
        setTags([]);
        return;
      }

      debounceTimer.current = setTimeout(async () => {
        setIsLoading(true);
        try {
          const response = await fetch(
            `${apiUrl}/api/${userId}/tasks/quick-search?q=${encodeURIComponent(query)}&limit=5`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (response.ok) {
            const data = await response.json();
            setTasks(data.tasks || []);
            setTags(data.tags || []);
          }
        } catch (err) {
          console.error("Quick search failed:", err);
        } finally {
          setIsLoading(false);
        }
      }, debounceMs);
    },
    [userId, token, apiUrl, debounceMs]
  );

  const clear = useCallback(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }
    setTasks([]);
    setTags([]);
  }, []);

  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  return {
    tasks,
    tags,
    isLoading,
    search,
    clear,
  };
}
