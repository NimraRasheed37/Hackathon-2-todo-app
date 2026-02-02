"use client";

import { useState } from "react";
import { useTasks } from "@/lib/hooks/useTasks";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskFilters } from "@/components/tasks/TaskFilters";
import { AddTaskModal } from "@/components/tasks/AddTaskModal";
import { EditTaskModal } from "@/components/tasks/EditTaskModal";
import { DeleteConfirmDialog } from "@/components/tasks/DeleteConfirmDialog";
import { Button } from "@/components/ui/Button";
import { Plus, ListTodo, CheckCircle2, Clock } from "lucide-react";
import { Task, FilterStatus, SortOption } from "@/types";

export default function DashboardContent({ userId }: { userId: string }) {
  const [filter, setFilter] = useState<FilterStatus>("all");
  const [sort, setSort] = useState<SortOption>("created");
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);

  // ✅ Now runs ONLY when userId is valid
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">My Tasks</h1>
          <p className="text-muted-foreground mt-1">
            Manage and track your daily tasks
          </p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)} size="lg">
          <Plus className="w-5 h-5" />
          <span>Add Task</span>
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <StatCard icon={<ListTodo />} label="Total" value={taskCounts.all} />
        <StatCard icon={<Clock />} label="Pending" value={taskCounts.pending} />
        <StatCard icon={<CheckCircle2 />} label="Completed" value={taskCounts.completed} />
      </div>

      <TaskFilters
        currentFilter={filter}
        currentSort={sort}
        taskCounts={taskCounts}
        onFilterChange={setFilter}
        onSortChange={setSort}
      />

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

      <AddTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={async (data) => {
          await createTask(data);
          setIsCreateModalOpen(false);
        }}
      />

      <EditTaskModal
        isOpen={!!editingTask}
        task={editingTask}
        onClose={() => setEditingTask(null)}
        onSubmit={async (data) => {
          if (!editingTask) return;
          await updateTask(editingTask.id, data);
          setEditingTask(null);
        }}
      />

      <DeleteConfirmDialog
        isOpen={!!deletingTaskId}
        taskTitle={deletingTask?.title || ""}
        onConfirm={async () => {
          if (!deletingTaskId) return;
          await deleteTask(deletingTaskId);
          setDeletingTaskId(null);
        }}
        onCancel={() => setDeletingTaskId(null)}
      />
    </div>
  );
}

function StatCard({ icon, label, value }: any) {
  return (
    <div className="bg-card rounded-xl border p-4 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
          {icon}
        </div>
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
      </div>
    </div>
  );
}
