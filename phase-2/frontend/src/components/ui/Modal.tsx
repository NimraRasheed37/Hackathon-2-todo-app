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
            "bg-card rounded-2xl shadow-2xl border border-border",
            "w-[90vw] max-w-md max-h-[85vh]",
            "flex flex-col overflow-hidden",
            "animate-in fade-in-0 zoom-in-95 slide-in-from-left-1/2 slide-in-from-top-[48%]",
            "focus:outline-none z-50",
            className
          )}
        >
          {/* Fixed Header */}
          <div className="flex-shrink-0 px-6 pt-6 pb-4">
            <Dialog.Title className="text-xl font-semibold text-foreground pr-8">
              {title}
            </Dialog.Title>
            {description && (
              <Dialog.Description className="text-sm text-foreground-muted mt-1">
                {description}
              </Dialog.Description>
            )}
            <Dialog.Close asChild>
              <button
                className={cn(
                  "absolute top-5 right-5",
                  "p-1.5 rounded-xl",
                  "text-foreground-muted hover:text-foreground hover:bg-secondary",
                  "transition-all duration-200",
                  "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                )}
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </Dialog.Close>
          </div>

          {/* Scrollable Content with styled scrollbar */}
          <div className="flex-1 overflow-y-auto px-6 pb-6 modal-scrollbar">
            {children}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
