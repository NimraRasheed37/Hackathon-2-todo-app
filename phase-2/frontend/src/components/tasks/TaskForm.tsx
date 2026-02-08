"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Button } from "@/components/ui/Button";
import { PrioritySelector } from "./PrioritySelector";
import { RecurrenceSelector } from "./RecurrenceSelector";
import { ReminderPicker } from "./ReminderPicker";
import { TagManager } from "./TagManager";
import { Task, TaskPriority, RecurrencePattern, Tag, ReminderType, ReminderChannel } from "@/types";

const MAX_TITLE_LENGTH = 200;
const MAX_DESCRIPTION_LENGTH = 1000;

interface ReminderConfig {
  type: ReminderType;
  relativeMinutes?: number;
  absoluteTime?: string;
  channels: ReminderChannel[];
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority: TaskPriority;
  due_date?: string;
  recurrence_pattern?: RecurrencePattern;
  tag_ids?: string[];
  reminders?: ReminderConfig[];
}

export interface TaskFormProps {
  mode: "create" | "edit";
  initialData?: Task | null;
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  availableTags?: Tag[];
  onCreateTag?: (name: string, color: string) => Promise<Tag>;
}

export function TaskForm({
  mode,
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
  availableTags = [],
  onCreateTag,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [priority, setPriority] = useState<TaskPriority>(initialData?.priority || "none");
  const [dueDate, setDueDate] = useState<string>(
    initialData?.due_date ? initialData.due_date.split("T")[0] : ""
  );
  const [dueTime, setDueTime] = useState<string>(
    initialData?.due_date ? initialData.due_date.split("T")[1]?.substring(0, 5) || "" : ""
  );
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern | null>(
    initialData?.recurrence_pattern || null
  );
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>(
    initialData?.tags?.map(t => Number(t.id)) || []
  );
  const [reminders, setReminders] = useState<ReminderConfig[]>([]);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
  }>({});

  // Reset form when initialData changes
  useEffect(() => {
    setTitle(initialData?.title || "");
    setDescription(initialData?.description || "");
    setPriority(initialData?.priority || "none");
    setDueDate(initialData?.due_date ? initialData.due_date.split("T")[0] : "");
    setDueTime(initialData?.due_date ? initialData.due_date.split("T")[1]?.substring(0, 5) || "" : "");
    setRecurrencePattern(initialData?.recurrence_pattern || null);
    setSelectedTagIds(initialData?.tags?.map(t => Number(t.id)) || []);
    setReminders([]);
    setErrors({});
  }, [initialData]);

  const validate = () => {
    const newErrors: { title?: string; description?: string } = {};

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      newErrors.title = "Title is required";
    } else if (trimmedTitle.length > MAX_TITLE_LENGTH) {
      newErrors.title = `Title must be ${MAX_TITLE_LENGTH} characters or less`;
    }

    if (description.length > MAX_DESCRIPTION_LENGTH) {
      newErrors.description = `Description must be ${MAX_DESCRIPTION_LENGTH} characters or less`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    const trimmedTitle = title.trim();
    const trimmedDescription = description.trim();

    // Combine date and time
    let fullDueDate: string | undefined;
    if (dueDate) {
      fullDueDate = dueTime ? `${dueDate}T${dueTime}:00` : `${dueDate}T23:59:00`;
    }

    await onSubmit({
      title: trimmedTitle,
      description: trimmedDescription || undefined,
      priority,
      due_date: fullDueDate,
      recurrence_pattern: recurrencePattern || undefined,
      tag_ids: selectedTagIds.length > 0 ? selectedTagIds.map(String) : undefined,
      reminders: reminders.length > 0 ? reminders : undefined,
    });
  };

  const isValid = title.trim().length > 0 && title.trim().length <= MAX_TITLE_LENGTH;
  const hasDueDate = !!dueDate;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title */}
      <Input
        label="Title"
        placeholder="What needs to be done?"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        error={errors.title}
        maxLength={MAX_TITLE_LENGTH}
        showCount
        currentLength={title.length}
        required
        disabled={isLoading}
        autoFocus
      />

      {/* Description */}
      <Textarea
        label="Description"
        placeholder="Add more details... (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        error={errors.description}
        maxLength={MAX_DESCRIPTION_LENGTH}
        showCount
        currentLength={description.length}
        disabled={isLoading}
      />

      {/* Priority */}
      <PrioritySelector
        value={priority}
        onChange={setPriority}
        disabled={isLoading}
      />

      {/* Due Date & Time */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-foreground-secondary">
          Due Date
        </label>
        <div className="flex gap-2">
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={isLoading}
            className="flex-1 px-3 py-2.5 text-sm border rounded-xl
              bg-card text-foreground border-border
              focus:ring-2 focus:ring-primary focus:border-primary
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-all duration-200"
          />
          <input
            type="time"
            value={dueTime}
            onChange={(e) => setDueTime(e.target.value)}
            disabled={isLoading || !dueDate}
            className="w-32 px-3 py-2.5 text-sm border rounded-xl
              bg-card text-foreground border-border
              focus:ring-2 focus:ring-primary focus:border-primary
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-all duration-200"
          />
          {dueDate && (
            <button
              type="button"
              onClick={() => {
                setDueDate("");
                setDueTime("");
              }}
              disabled={isLoading}
              className="px-3 py-1 text-sm text-foreground-muted hover:text-foreground rounded-lg hover:bg-secondary transition-colors"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Advanced Options Toggle */}
      <button
        type="button"
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="flex items-center gap-1.5 text-sm text-primary hover:text-primary-hover font-medium transition-colors"
      >
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${showAdvanced ? "rotate-90" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
        {showAdvanced ? "Hide" : "Show"} advanced options
      </button>

      {/* Advanced Options */}
      {showAdvanced && (
        <div className="space-y-4 pt-4 border-t border-border">
          {/* Recurrence */}
          <RecurrenceSelector
            value={recurrencePattern}
            onChange={setRecurrencePattern}
            disabled={isLoading}
          />

          {/* Reminders */}
          <ReminderPicker
            value={reminders}
            onChange={setReminders}
            hasDueDate={hasDueDate}
            disabled={isLoading}
          />

          {/* Tags */}
          <TagManager
            availableTags={availableTags}
            selectedTagIds={selectedTagIds}
            onChange={setSelectedTagIds}
            onCreateTag={onCreateTag}
            disabled={isLoading}
          />
        </div>
      )}

      {/* Form Actions */}
      <div className="flex justify-end gap-3 pt-2">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={!isValid} isLoading={isLoading}>
          {mode === "create" ? "Create Task" : "Save Changes"}
        </Button>
      </div>
    </form>
  );
}
