"use client";

import { memo, useState } from "react";
import * as Checkbox from "@radix-ui/react-checkbox";
import { Check, Pencil, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { formatRelativeTime } from "@/lib/utils";
import { Task } from "@/types";
import { Button } from "@/components/ui/Button";

export interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
}

export const TaskCard = memo(function TaskCard({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
  isLoading = false,
}: TaskCardProps) {
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    if (isToggling || isLoading) return;
    setIsToggling(true);
    try {
      await onToggleComplete(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  return (
    <div
      className={cn(
        "group bg-card rounded-xl border border-border p-4 shadow-sm",
        "hover:shadow-md hover:border-border-hover transition-all duration-200",
        isLoading && "opacity-50 pointer-events-none"
      )}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <Checkbox.Root
          checked={task.completed}
          onCheckedChange={handleToggle}
          disabled={isToggling || isLoading}
          className={cn(
            "flex-shrink-0 w-5 h-5 mt-0.5 rounded border-2 transition-colors",
            "flex items-center justify-center",
            "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
            task.completed
              ? "bg-success border-success"
              : "border-border hover:border-primary"
          )}
        >
          <Checkbox.Indicator>
            <Check className="w-3 h-3 text-white" />
          </Checkbox.Indicator>
        </Checkbox.Root>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={cn(
              "font-medium text-foreground transition-all duration-200",
              task.completed && "line-through text-foreground-muted"
            )}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={cn(
                "text-sm text-foreground-secondary mt-1 line-clamp-2",
                task.completed && "text-foreground-muted"
              )}
            >
              {task.description}
            </p>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-3 pt-3 border-t border-border flex justify-between items-center">
        <span className="text-xs text-foreground-muted">
          {task.completed ? "Completed" : "Created"}{" "}
          {formatRelativeTime(task.updated_at)}
        </span>

        {/* Actions - visible on hover */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(task)}
            disabled={isLoading}
            className="text-foreground-secondary hover:text-primary"
          >
            <Pencil className="w-4 h-4" />
            <span className="sr-only">Edit</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(task.id)}
            disabled={isLoading}
            className="text-foreground-secondary hover:text-error"
          >
            <Trash2 className="w-4 h-4" />
            <span className="sr-only">Delete</span>
          </Button>
        </div>
      </div>
    </div>
  );
});
