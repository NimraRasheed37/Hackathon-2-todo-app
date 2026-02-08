"use client";

import { forwardRef, TextareaHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface TextareaProps
  extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  maxLength?: number;
  showCount?: boolean;
  currentLength?: number;
}

const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      className,
      label,
      error,
      maxLength,
      showCount = false,
      currentLength = 0,
      id,
      ...props
    },
    ref
  ) => {
    const textareaId = id || label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={textareaId}
            className="block text-sm font-medium text-foreground-secondary mb-1"
          >
            {label}
            {props.required && <span className="text-error ml-1">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={cn(
            "w-full px-4 py-2.5 rounded-xl border min-h-[100px] resize-none",
            "bg-card text-foreground placeholder-foreground-muted",
            "transition-all duration-200",
            "focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent",
            error
              ? "border-error focus:ring-error"
              : "border-border hover:border-border-hover",
            "disabled:bg-background-tertiary disabled:cursor-not-allowed disabled:opacity-60",
            className
          )}
          aria-invalid={error ? "true" : "false"}
          aria-describedby={error ? `${textareaId}-error` : undefined}
          maxLength={maxLength}
          {...props}
        />
        <div className="flex justify-between mt-1">
          {error && (
            <p
              id={`${textareaId}-error`}
              className="text-sm text-error"
              role="alert"
            >
              {error}
            </p>
          )}
          {showCount && maxLength && (
            <p
              className={cn(
                "text-sm ml-auto",
                currentLength > maxLength ? "text-error" : "text-foreground-muted"
              )}
            >
              {currentLength}/{maxLength}
            </p>
          )}
        </div>
      </div>
    );
  }
);

Textarea.displayName = "Textarea";

export { Textarea };
