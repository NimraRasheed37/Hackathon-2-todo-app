"use client";

import { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { TaskForm } from "./TaskForm";
import { TaskCreate } from "@/types";

export interface AddTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskCreate) => Promise<void>;
}

export function AddTaskModal({ isOpen, onClose, onSubmit }: AddTaskModalProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: TaskCreate) => {
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
      title="Add New Task"
      description="Create a new task to add to your list."
    >
      <TaskForm
        mode="create"
        onSubmit={handleSubmit}
        onCancel={onClose}
        isLoading={isLoading}
      />
    </Modal>
  );
}
