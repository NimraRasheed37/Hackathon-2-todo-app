"use client";

import { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { TaskForm } from "./TaskForm";
import { Task, TaskUpdate } from "@/types";

export interface EditTaskModalProps {
  isOpen: boolean;
  task: Task | null;
  onClose: () => void;
  onSubmit: (data: TaskUpdate) => Promise<void>;
}

export function EditTaskModal({
  isOpen,
  task,
  onClose,
  onSubmit,
}: EditTaskModalProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: TaskUpdate) => {
    setIsLoading(true);
    try {
      await onSubmit(data);
      onClose();
    } catch {
      // Error is already handled by the hook with toast
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Edit Task"
      description="Update your task details."
    >
      <TaskForm
        mode="edit"
        initialData={task}
        onSubmit={handleSubmit}
        onCancel={onClose}
        isLoading={isLoading}
      />
    </Modal>
  );
}
