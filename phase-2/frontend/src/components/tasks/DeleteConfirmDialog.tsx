"use client";

import { useState } from "react";
import * as AlertDialog from "@radix-ui/react-alert-dialog";
import { Button } from "@/components/ui/Button";
import { AlertTriangle } from "lucide-react";

export interface DeleteConfirmDialogProps {
  isOpen: boolean;
  taskTitle: string;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
}

export function DeleteConfirmDialog({
  isOpen,
  taskTitle,
  onConfirm,
  onCancel,
}: DeleteConfirmDialogProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleConfirm = async () => {
    setIsLoading(true);
    try {
      await onConfirm();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AlertDialog.Root open={isOpen} onOpenChange={(open) => !open && onCancel()}>
      <AlertDialog.Portal>
        <AlertDialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm animate-in fade-in-0 z-50" />
        <AlertDialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl w-[90vw] max-w-md p-6 animate-in fade-in-0 zoom-in-95 z-50">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 p-2 bg-red-100 rounded-full">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <AlertDialog.Title className="text-lg font-semibold text-gray-900">
                Delete Task
              </AlertDialog.Title>
              <AlertDialog.Description className="mt-2 text-sm text-gray-600">
                Are you sure you want to delete &quot;{taskTitle}&quot;? This
                action cannot be undone.
              </AlertDialog.Description>
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <AlertDialog.Cancel asChild>
              <Button variant="secondary" disabled={isLoading}>
                Cancel
              </Button>
            </AlertDialog.Cancel>
            <AlertDialog.Action asChild>
              <Button
                variant="danger"
                onClick={handleConfirm}
                isLoading={isLoading}
              >
                Delete
              </Button>
            </AlertDialog.Action>
          </div>
        </AlertDialog.Content>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  );
}
