"use client";

import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  className,
}: ModalProps) {
  return (
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm animate-in fade-in-0 z-50" />
        <Dialog.Content
          className={cn(
            "fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2",
            "bg-white rounded-xl shadow-xl",
            "w-[90vw] max-w-md max-h-[85vh] overflow-y-auto",
            "p-6",
            "animate-in fade-in-0 zoom-in-95 slide-in-from-left-1/2 slide-in-from-top-[48%]",
            "focus:outline-none z-50",
            className
          )}
        >
          <Dialog.Title className="text-xl font-semibold text-gray-900">
            {title}
          </Dialog.Title>
          {description && (
            <Dialog.Description className="text-sm text-gray-500 mt-1">
              {description}
            </Dialog.Description>
          )}
          <Dialog.Close asChild>
            <button
              className={cn(
                "absolute top-4 right-4",
                "p-1 rounded-full",
                "text-gray-400 hover:text-gray-600 hover:bg-gray-100",
                "transition-colors duration-200",
                "focus:outline-none focus:ring-2 focus:ring-blue-500"
              )}
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </Dialog.Close>
          <div className="mt-4">{children}</div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
