"use client";

import { TaskPriority } from "@/types";

const PRIORITY_CONFIG: Record<
  TaskPriority,
  { label: string; color: string; bgColor: string; icon: string }
> = {
  critical: {
    label: "Critical",
    color: "text-red-600 dark:text-red-400",
    bgColor: "bg-red-100 dark:bg-red-900/30 border-red-200 dark:border-red-800",
    icon: "!!",
  },
  high: {
    label: "High",
    color: "text-orange-600 dark:text-orange-400",
    bgColor: "bg-orange-100 dark:bg-orange-900/30 border-orange-200 dark:border-orange-800",
    icon: "!",
  },
  medium: {
    label: "Medium",
    color: "text-yellow-600 dark:text-yellow-400",
    bgColor: "bg-yellow-100 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800",
    icon: "-",
  },
  low: {
    label: "Low",
    color: "text-blue-600 dark:text-blue-400",
    bgColor: "bg-blue-100 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800",
    icon: "v",
  },
  none: {
    label: "None",
    color: "text-gray-500 dark:text-gray-400",
    bgColor: "bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700",
    icon: "",
  },
};

const PRIORITY_ORDER: TaskPriority[] = ["none", "low", "medium", "high", "critical"];

interface PrioritySelectorProps {
  value: TaskPriority;
  onChange: (priority: TaskPriority) => void;
  disabled?: boolean;
  compact?: boolean;
}

export function PrioritySelector({
  value,
  onChange,
  disabled = false,
  compact = false,
}: PrioritySelectorProps) {
  const config = PRIORITY_CONFIG[value];

  if (compact) {
    return (
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as TaskPriority)}
        disabled={disabled}
        className={`
          px-2 py-1 text-sm rounded border font-medium
          ${config.bgColor} ${config.color}
          focus:outline-none focus:ring-2 focus:ring-blue-500
          disabled:opacity-50 disabled:cursor-not-allowed
        `}
      >
        {PRIORITY_ORDER.map((priority) => (
          <option key={priority} value={priority}>
            {PRIORITY_CONFIG[priority].label}
          </option>
        ))}
      </select>
    );
  }

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Priority
      </label>
      <div className="flex flex-wrap gap-2">
        {PRIORITY_ORDER.map((priority) => {
          const priorityConfig = PRIORITY_CONFIG[priority];
          const isSelected = value === priority;

          return (
            <button
              key={priority}
              type="button"
              onClick={() => onChange(priority)}
              disabled={disabled}
              className={`
                px-3 py-1.5 text-sm font-medium rounded-md border transition-all
                ${isSelected
                  ? `${priorityConfig.bgColor} ${priorityConfig.color} ring-2 ring-offset-1 ring-blue-500`
                  : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                }
                disabled:opacity-50 disabled:cursor-not-allowed
              `}
            >
              {priorityConfig.icon && (
                <span className="mr-1 font-bold">{priorityConfig.icon}</span>
              )}
              {priorityConfig.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function PriorityBadge({ priority }: { priority: TaskPriority }) {
  const config = PRIORITY_CONFIG[priority];

  if (priority === "none") {
    return null;
  }

  return (
    <span
      className={`
        inline-flex items-center px-2 py-0.5 text-xs font-medium rounded
        ${config.bgColor} ${config.color} border
      `}
    >
      {config.icon && <span className="mr-0.5 font-bold">{config.icon}</span>}
      {config.label}
    </span>
  );
}
