"use client";

import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  maxLength?: number;
  showCount?: boolean;
  currentLength?: number;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
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
    const inputId = id || label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-foreground-secondary mb-1"
          >
            {label}
            {props.required && <span className="text-error ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            ref={ref}
            id={inputId}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg border",
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
            aria-describedby={error ? `${inputId}-error` : undefined}
            maxLength={maxLength}
            {...props}
          />
        </div>
        <div className="flex justify-between mt-1">
          {error && (
            <p
              id={`${inputId}-error`}
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
                currentLength > maxLength
                  ? "text-error"
                  : "text-foreground-muted"
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

Input.displayName = "Input";

export { Input };
