"use client";

import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { cn } from "@/lib/utils";
import { FilterStatus, SortOption } from "@/types";
import { ChevronDown, Check } from "lucide-react";

export interface TaskFiltersProps {
  currentFilter: FilterStatus;
  currentSort: SortOption;
  taskCounts: {
    all: number;
    pending: number;
    completed: number;
  };
  onFilterChange: (filter: FilterStatus) => void;
  onSortChange: (sort: SortOption) => void;
}

const filterOptions: { value: FilterStatus; label: string }[] = [
  { value: "all", label: "All" },
  { value: "pending", label: "Pending" },
  { value: "completed", label: "Completed" },
];

const sortOptions: { value: SortOption; label: string }[] = [
  { value: "created", label: "Newest first" },
  { value: "updated", label: "Recently updated" },
  { value: "title", label: "A-Z" },
];

export function TaskFilters({
  currentFilter,
  currentSort,
  taskCounts,
  onFilterChange,
  onSortChange,
}: TaskFiltersProps) {
  const getSortLabel = () => {
    const option = sortOptions.find((o) => o.value === currentSort);
    return option?.label || "Sort by";
  };

  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 py-4 border-b border-border">
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2">
        {filterOptions.map((option) => {
          const count =
            option.value === "all"
              ? taskCounts.all
              : option.value === "pending"
              ? taskCounts.pending
              : taskCounts.completed;

          return (
            <button
              key={option.value}
              onClick={() => onFilterChange(option.value)}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
                currentFilter === option.value
                  ? "bg-primary-light text-primary"
                  : "bg-secondary text-foreground-secondary hover:bg-secondary-hover"
              )}
            >
              {option.label}: {count}
            </button>
          );
        })}
      </div>

      {/* Sort dropdown */}
      <DropdownMenu.Root>
        <DropdownMenu.Trigger asChild>
          <button
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium",
              "bg-card border border-border text-foreground-secondary",
              "hover:bg-card-hover transition-colors",
              "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            )}
          >
            <span>Sort: {getSortLabel()}</span>
            <ChevronDown className="w-4 h-4" />
          </button>
        </DropdownMenu.Trigger>

        <DropdownMenu.Portal>
          <DropdownMenu.Content
            className="bg-card rounded-lg shadow-lg border border-border py-1 min-w-[180px] z-50"
            sideOffset={8}
            align="end"
          >
            {sortOptions.map((option) => (
              <DropdownMenu.Item
                key={option.value}
                onClick={() => onSortChange(option.value)}
                className={cn(
                  "flex items-center justify-between px-4 py-2 text-sm cursor-pointer",
                  "outline-none transition-colors",
                  currentSort === option.value
                    ? "bg-primary-light text-primary"
                    : "text-foreground-secondary hover:bg-secondary"
                )}
              >
                <span>{option.label}</span>
                {currentSort === option.value && (
                  <Check className="w-4 h-4" />
                )}
              </DropdownMenu.Item>
            ))}
          </DropdownMenu.Content>
        </DropdownMenu.Portal>
      </DropdownMenu.Root>
    </div>
  );
}
