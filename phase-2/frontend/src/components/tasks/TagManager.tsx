"use client";

import { useState } from "react";
import { Tag } from "@/types";

const PRESET_COLORS = [
  "#EF4444", // Red
  "#F97316", // Orange
  "#EAB308", // Yellow
  "#22C55E", // Green
  "#06B6D4", // Cyan
  "#3B82F6", // Blue
  "#8B5CF6", // Purple
  "#EC4899", // Pink
  "#6B7280", // Gray
];

interface TagManagerProps {
  availableTags: Tag[];
  selectedTagIds: number[];
  onChange: (tagIds: number[]) => void;
  onCreateTag?: (name: string, color: string) => Promise<Tag>;
  disabled?: boolean;
}

export function TagManager({
  availableTags,
  selectedTagIds,
  onChange,
  onCreateTag,
  disabled = false,
}: TagManagerProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [newTagName, setNewTagName] = useState("");
  const [newTagColor, setNewTagColor] = useState(PRESET_COLORS[0]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const toggleTag = (tagId: number) => {
    if (selectedTagIds.includes(tagId)) {
      onChange(selectedTagIds.filter(id => id !== tagId));
    } else {
      onChange([...selectedTagIds, tagId]);
    }
  };

  const handleCreateTag = async () => {
    if (!onCreateTag || !newTagName.trim()) return;

    setIsSubmitting(true);
    try {
      const newTag = await onCreateTag(newTagName.trim(), newTagColor);
      onChange([...selectedTagIds, newTag.id as unknown as number]);
      setNewTagName("");
      setIsCreating(false);
    } catch (error) {
      console.error("Failed to create tag:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Tags
        </label>
        {onCreateTag && !isCreating && (
          <button
            type="button"
            onClick={() => setIsCreating(true)}
            disabled={disabled}
            className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 disabled:opacity-50"
          >
            + New tag
          </button>
        )}
      </div>

      {/* Create new tag form */}
      {isCreating && (
        <div className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800/50 space-y-3">
          <input
            type="text"
            value={newTagName}
            onChange={(e) => setNewTagName(e.target.value)}
            placeholder="Tag name"
            maxLength={50}
            disabled={isSubmitting}
            className="w-full px-3 py-1.5 text-sm border rounded-md
              bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
              focus:ring-2 focus:ring-blue-500 focus:border-blue-500
              disabled:opacity-50"
          />
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600 dark:text-gray-400">Color:</span>
            <div className="flex gap-1">
              {PRESET_COLORS.map((color) => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setNewTagColor(color)}
                  disabled={isSubmitting}
                  className={`w-6 h-6 rounded-full border-2 transition-all ${
                    newTagColor === color
                      ? "border-gray-800 dark:border-white scale-110"
                      : "border-transparent hover:scale-105"
                  }`}
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleCreateTag}
              disabled={!newTagName.trim() || isSubmitting}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {isSubmitting ? "Creating..." : "Create"}
            </button>
            <button
              type="button"
              onClick={() => {
                setIsCreating(false);
                setNewTagName("");
              }}
              disabled={isSubmitting}
              className="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Available tags */}
      <div className="flex flex-wrap gap-2">
        {availableTags.length === 0 ? (
          <p className="text-sm text-gray-500 dark:text-gray-400 italic">
            No tags yet. Create your first tag!
          </p>
        ) : (
          availableTags.map((tag) => {
            const isSelected = selectedTagIds.includes(tag.id as unknown as number);
            return (
              <button
                key={tag.id}
                type="button"
                onClick={() => toggleTag(tag.id as unknown as number)}
                disabled={disabled}
                className={`
                  inline-flex items-center gap-1.5 px-2.5 py-1 text-sm rounded-full
                  border-2 transition-all
                  ${isSelected
                    ? "border-current shadow-sm"
                    : "border-transparent hover:border-gray-300 dark:hover:border-gray-600"
                  }
                  disabled:opacity-50 disabled:cursor-not-allowed
                `}
                style={{
                  backgroundColor: isSelected ? `${tag.color}20` : "transparent",
                  color: tag.color,
                }}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: tag.color }}
                />
                {tag.name}
                {isSelected && (
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}

export function TagBadge({ tag }: { tag: Tag }) {
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full"
      style={{
        backgroundColor: `${tag.color}20`,
        color: tag.color,
      }}
    >
      <span
        className="w-1.5 h-1.5 rounded-full"
        style={{ backgroundColor: tag.color }}
      />
      {tag.name}
    </span>
  );
}

export function TagList({ tags }: { tags: Tag[] }) {
  if (tags.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-1">
      {tags.map((tag) => (
        <TagBadge key={tag.id} tag={tag} />
      ))}
    </div>
  );
}
