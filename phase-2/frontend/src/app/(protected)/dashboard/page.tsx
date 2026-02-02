
"use client";

import { useState, useEffect } from "react";
import { useSession } from "@/lib/auth-client";
import { useSearchParams, useRouter } from "next/navigation";
import { useTasks } from "@/lib/hooks/useTasks";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskFilters } from "@/components/tasks/TaskFilters";
import { AddTaskModal } from "@/components/tasks/AddTaskModal";
import { EditTaskModal } from "@/components/tasks/EditTaskModal";
import { DeleteConfirmDialog } from "@/components/tasks/DeleteConfirmDialog";
import { Button } from "@/components/ui/Button";
import { Plus, ListTodo, CheckCircle2, Clock } from "lucide-react";
import { Task, FilterStatus, SortOption } from "@/types";

export default function DashboardPage() {
  const { data: session } = useSession();
  const userId = session?.user?.id || "";
  const searchParams = useSearchParams();
  const router = useRouter();

  // Get filter from URL query parameter
  const urlFilter = searchParams.get("filter") as FilterStatus | null;

  // UI State
  const [filter, setFilter] = useState<FilterStatus>(urlFilter || "all");
  const [sort, setSort] = useState<SortOption>("created");

  // Sync filter with URL
  useEffect(() => {
    if (urlFilter && urlFilter !== filter) {
      setFilter(urlFilter);
    }
  }, [urlFilter]);

  // Update URL when filter changes (optional - for sharing/bookmarking)
  const handleFilterChange = (newFilter: FilterStatus) => {
    setFilter(newFilter);
    // Only update URL if filter is not "all"
    if (newFilter === "all") {
      router.push("/dashboard", { scroll: false });
    } else {
      router.push(`/dashboard?filter=${newFilter}`, { scroll: false });
    }
  };
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);

  // Data
  const {
    tasks,
    isLoading,
    error,
    createTask,
    updateTask,
    toggleComplete,
    deleteTask,
    taskCounts,
  } = useTasks({ userId, filter, sort });

  const deletingTask = deletingTaskId
    ? tasks.find((t) => t.id === deletingTaskId) || null
    : null;

  const handleCreateTask = async (data: {
    title: string;
    description?: string;
  }) => {
    await createTask(data);
    setIsCreateModalOpen(false);
  };

  const handleUpdateTask = async (data: {
    title?: string;
    description?: string;
  }) => {
    if (!editingTask) return;
    await updateTask(editingTask.id, data);
    setEditingTask(null);
  };

  const handleDeleteTask = async () => {
    if (!deletingTaskId) return;
    await deleteTask(deletingTaskId);
    setDeletingTaskId(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">My Tasks</h1>
          <p className="text-foreground-secondary mt-1">
            Manage and track your daily tasks
          </p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)} size="lg">
          <Plus className="w-5 h-5" />
          <span>Add Task</span>
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-card rounded-xl border border-border p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary-light flex items-center justify-center">
              <ListTodo className="w-5 h-5 text-primary" />
            </div>
            <div>
              <p className="text-sm text-foreground-muted">Total</p>
              <p className="text-2xl font-bold text-foreground">
                {taskCounts.all}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-card rounded-xl border border-border p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-warning-light flex items-center justify-center">
              <Clock className="w-5 h-5 text-warning" />
            </div>
            <div>
              <p className="text-sm text-foreground-muted">Pending</p>
              <p className="text-2xl font-bold text-foreground">
                {taskCounts.pending}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-card rounded-xl border border-border p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-success-light flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-success" />
            </div>
            <div>
              <p className="text-sm text-foreground-muted">Completed</p>
              <p className="text-2xl font-bold text-foreground">
                {taskCounts.completed}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <TaskFilters
        currentFilter={filter}
        currentSort={sort}
        taskCounts={taskCounts}
        onFilterChange={handleFilterChange}
        onSortChange={setSort}
      />

      {/* Task List */}
      <TaskList
        tasks={tasks}
        isLoading={isLoading}
        error={error}
        filter={filter}
        onToggleComplete={toggleComplete}
        onEdit={setEditingTask}
        onDelete={setDeletingTaskId}
        onCreateTask={() => setIsCreateModalOpen(true)}
      />

      {/* Modals */}
      <AddTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateTask}
      />

      <EditTaskModal
        isOpen={!!editingTask}
        task={editingTask}
        onClose={() => setEditingTask(null)}
        onSubmit={handleUpdateTask}
      />

      <DeleteConfirmDialog
        isOpen={!!deletingTaskId}
        taskTitle={deletingTask?.title || ""}
        onConfirm={handleDeleteTask}
        onCancel={() => setDeletingTaskId(null)}
      />
    </div>
  );
}
