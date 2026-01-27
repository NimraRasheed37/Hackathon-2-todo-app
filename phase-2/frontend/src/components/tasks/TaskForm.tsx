"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Button } from "@/components/ui/Button";
import { Task } from "@/types";

const MAX_TITLE_LENGTH = 200;
const MAX_DESCRIPTION_LENGTH = 1000;

export interface TaskFormProps {
  mode: "create" | "edit";
  initialData?: Task | null;
  onSubmit: (data: { title: string; description?: string }) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

export function TaskForm({
  mode,
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(
    initialData?.description || ""
  );
  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
  }>({});

  // Reset form when initialData changes
  useEffect(() => {
    setTitle(initialData?.title || "");
    setDescription(initialData?.description || "");
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

    await onSubmit({
      title: trimmedTitle,
      description: trimmedDescription || undefined,
    });
  };

  const isValid = title.trim().length > 0 && title.trim().length <= MAX_TITLE_LENGTH;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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
