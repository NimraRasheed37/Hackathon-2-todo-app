"use client";

import useSWR, { mutate } from "swr";
import { api } from "@/lib/api";
import { Task, TaskCreate, TaskUpdate, FilterStatus, SortOption } from "@/types";
import { toast } from "sonner";

interface UseTasksOptions {
  userId: string;
  filter?: FilterStatus;
  sort?: SortOption;
}

interface UseTasksReturn {
  tasks: Task[];
  allTasks: Task[];
  isLoading: boolean;
  error: Error | null;
  createTask: (data: TaskCreate) => Promise<void>;
  updateTask: (taskId: number, data: TaskUpdate) => Promise<void>;
  toggleComplete: (taskId: number) => Promise<void>;
  deleteTask: (taskId: number) => Promise<void>;
  taskCounts: {
    all: number;
    pending: number;
    completed: number;
  };
}

export function useTasks({
  userId,
  filter = "all",
  sort = "created",
}: UseTasksOptions): UseTasksReturn {
  const cacheKey = userId ? `/api/${userId}/tasks` : null;

  const { data: allTasks = [], error, isLoading } = useSWR<Task[]>(
    cacheKey,
    () => api.getTasks(userId, undefined, sort),
    {
      revalidateOnFocus: false,
      dedupingInterval: 5000,
    }
  );

  // Filter tasks client-side for instant filtering
  const filteredTasks = allTasks.filter((task) => {
    if (filter === "pending") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  // Sort tasks client-side
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    switch (sort) {
      case "title":
        return a.title.localeCompare(b.title);
      case "updated":
        return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
      case "created":
      default:
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    }
  });

  // Calculate task counts
  const taskCounts = {
    all: allTasks.length,
    pending: allTasks.filter((t) => !t.completed).length,
    completed: allTasks.filter((t) => t.completed).length,
  };

  const createTask = async (data: TaskCreate) => {
    const optimisticTask: Task = {
      id: Date.now(),
      user_id: userId,
      title: data.title,
      description: data.description || null,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    try {
      await mutate(
        cacheKey,
        async (current: Task[] = []) => {
          const newTask = await api.createTask(userId, data);
          return [newTask, ...current];
        },
        {
          optimisticData: (current: Task[] = []) => [optimisticTask, ...current],
          rollbackOnError: true,
          revalidate: false,
        }
      );
      toast.success("Task created successfully!");
    } catch (err) {
      toast.error("Failed to create task");
      throw err;
    }
  };

  const updateTask = async (taskId: number, data: TaskUpdate) => {
    try {
      await mutate(
        cacheKey,
        async (current: Task[] = []) => {
          const updatedTask = await api.updateTask(userId, taskId, data);
          return current.map((t) => (t.id === taskId ? updatedTask : t));
        },
        {
          optimisticData: (current: Task[] = []) =>
            current.map((t) =>
              t.id === taskId
                ? { ...t, ...data, updated_at: new Date().toISOString() }
                : t
            ),
          rollbackOnError: true,
          revalidate: false,
        }
      );
      toast.success("Task updated successfully!");
    } catch (err) {
      toast.error("Failed to update task");
      throw err;
    }
  };

  const toggleComplete = async (taskId: number) => {
    try {
      await mutate(
        cacheKey,
        async (current: Task[] = []) => {
          const updatedTask = await api.toggleComplete(userId, taskId);
          return current.map((t) => (t.id === taskId ? updatedTask : t));
        },
        {
          optimisticData: (current: Task[] = []) =>
            current.map((t) =>
              t.id === taskId
                ? {
                    ...t,
                    completed: !t.completed,
                    updated_at: new Date().toISOString(),
                  }
                : t
            ),
          rollbackOnError: true,
          revalidate: false,
        }
      );
    } catch (err) {
      toast.error("Failed to update task");
      throw err;
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      await mutate(
        cacheKey,
        async (current: Task[] = []) => {
          await api.deleteTask(userId, taskId);
          return current.filter((t) => t.id !== taskId);
        },
        {
          optimisticData: (current: Task[] = []) =>
            current.filter((t) => t.id !== taskId),
          rollbackOnError: true,
          revalidate: false,
        }
      );
      toast.success("Task deleted successfully!");
    } catch (err) {
      toast.error("Failed to delete task");
      throw err;
    }
  };

  return {
    tasks: sortedTasks,
    allTasks,
    isLoading,
    error: error || null,
    createTask,
    updateTask,
    toggleComplete,
    deleteTask,
    taskCounts,
  };
}
