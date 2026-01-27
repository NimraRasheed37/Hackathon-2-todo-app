"use client";

import { Task } from "@/types";
import { TaskCard } from "./TaskCard";
import { TaskListSkeleton } from "@/components/ui/Skeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { ClipboardList, CheckCircle } from "lucide-react";

export interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  error?: Error | null;
  filter: "all" | "pending" | "completed";
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onCreateTask: () => void;
}

export function TaskList({
  tasks,
  isLoading,
  error,
  filter,
  onToggleComplete,
  onEdit,
  onDelete,
  onCreateTask,
}: TaskListProps) {
  if (isLoading) {
    return <TaskListSkeleton count={4} />;
  }

  if (error) {
    return (
      <EmptyState
        title="Failed to load tasks"
        description={error.message || "Please try again later."}
      />
    );
  }

  if (tasks.length === 0) {
    // Different empty states based on filter
    if (filter === "completed") {
      return (
        <EmptyState
          icon={CheckCircle}
          title="No completed tasks"
          description="Tasks you complete will appear here."
        />
      );
    }

    if (filter === "pending") {
      return (
        <EmptyState
          icon={CheckCircle}
          title="All caught up!"
          description="You have no pending tasks. Great job!"
        />
      );
    }

    // No tasks at all
    return (
      <EmptyState
        icon={ClipboardList}
        title="No tasks yet"
        description="Create your first task to get started."
        actionLabel="Add Your First Task"
        onAction={onCreateTask}
      />
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
