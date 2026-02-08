"use client";

import { useState } from "react";
import { TaskReminder, ReminderType, ReminderChannel } from "@/types";

const PRESET_REMINDERS = [
  { label: "15 minutes before", minutes: 15 },
  { label: "30 minutes before", minutes: 30 },
  { label: "1 hour before", minutes: 60 },
  { label: "2 hours before", minutes: 120 },
  { label: "1 day before", minutes: 1440 },
  { label: "1 week before", minutes: 10080 },
];

interface ReminderConfig {
  type: ReminderType;
  relativeMinutes?: number;
  absoluteTime?: string;
  channels: ReminderChannel[];
}

interface ReminderPickerProps {
  value: ReminderConfig[];
  onChange: (reminders: ReminderConfig[]) => void;
  hasDueDate: boolean;
  disabled?: boolean;
}

export function ReminderPicker({
  value,
  onChange,
  hasDueDate,
  disabled = false,
}: ReminderPickerProps) {
  const [customMinutes, setCustomMinutes] = useState<number>(60);
  const [customTime, setCustomTime] = useState<string>("");

  const addPresetReminder = (minutes: number) => {
    if (value.some(r => r.type === "relative" && r.relativeMinutes === minutes)) {
      return; // Already exists
    }
    onChange([
      ...value,
      {
        type: "relative",
        relativeMinutes: minutes,
        channels: ["in_app"],
      },
    ]);
  };

  const addCustomReminder = () => {
    if (customMinutes <= 0) return;
    if (value.some(r => r.type === "relative" && r.relativeMinutes === customMinutes)) {
      return;
    }
    onChange([
      ...value,
      {
        type: "relative",
        relativeMinutes: customMinutes,
        channels: ["in_app"],
      },
    ]);
  };

  const addAbsoluteReminder = () => {
    if (!customTime) return;
    if (value.some(r => r.type === "absolute" && r.absoluteTime === customTime)) {
      return;
    }
    onChange([
      ...value,
      {
        type: "absolute",
        absoluteTime: customTime,
        channels: ["in_app"],
      },
    ]);
    setCustomTime("");
  };

  const removeReminder = (index: number) => {
    onChange(value.filter((_, i) => i !== index));
  };

  const formatReminder = (reminder: ReminderConfig) => {
    if (reminder.type === "absolute" && reminder.absoluteTime) {
      return new Date(reminder.absoluteTime).toLocaleString();
    }
    if (reminder.relativeMinutes) {
      const preset = PRESET_REMINDERS.find(p => p.minutes === reminder.relativeMinutes);
      if (preset) return preset.label;

      const minutes = reminder.relativeMinutes;
      if (minutes < 60) return `${minutes} minutes before`;
      if (minutes < 1440) return `${Math.floor(minutes / 60)} hours before`;
      return `${Math.floor(minutes / 1440)} days before`;
    }
    return "Unknown";
  };

  if (!hasDueDate) {
    return (
      <div className="text-sm text-gray-500 dark:text-gray-400 italic">
        Set a due date to add reminders
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Reminders
        </label>

        {/* Current reminders */}
        {value.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {value.map((reminder, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-1 px-2 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-md"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                {formatReminder(reminder)}
                <button
                  type="button"
                  onClick={() => removeReminder(index)}
                  disabled={disabled}
                  className="ml-1 text-blue-500 hover:text-blue-700 disabled:opacity-50"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
            ))}
          </div>
        )}

        {/* Quick add buttons */}
        <div className="flex flex-wrap gap-2">
          {PRESET_REMINDERS.slice(0, 4).map((preset) => {
            const exists = value.some(
              r => r.type === "relative" && r.relativeMinutes === preset.minutes
            );
            return (
              <button
                key={preset.minutes}
                type="button"
                onClick={() => addPresetReminder(preset.minutes)}
                disabled={disabled || exists}
                className={`
                  px-3 py-1 text-sm rounded-md border transition-all
                  ${exists
                    ? "bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed"
                    : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                  }
                  disabled:opacity-50
                `}
              >
                + {preset.label}
              </button>
            );
          })}
        </div>

        {/* Custom reminder */}
        <div className="flex items-center gap-2 mt-3">
          <input
            type="number"
            min="1"
            max="43200"
            value={customMinutes}
            onChange={(e) => setCustomMinutes(parseInt(e.target.value) || 60)}
            disabled={disabled}
            className="w-20 px-2 py-1 text-sm border rounded-md
              bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
              focus:ring-2 focus:ring-blue-500 focus:border-blue-500
              disabled:opacity-50"
          />
          <span className="text-sm text-gray-600 dark:text-gray-400">minutes before</span>
          <button
            type="button"
            onClick={addCustomReminder}
            disabled={disabled}
            className="px-2 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            Add
          </button>
        </div>

        {/* Absolute time reminder */}
        <div className="flex items-center gap-2 mt-2">
          <input
            type="datetime-local"
            value={customTime}
            onChange={(e) => setCustomTime(e.target.value)}
            disabled={disabled}
            className="px-2 py-1 text-sm border rounded-md
              bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
              focus:ring-2 focus:ring-blue-500 focus:border-blue-500
              disabled:opacity-50"
          />
          <button
            type="button"
            onClick={addAbsoluteReminder}
            disabled={disabled || !customTime}
            className="px-2 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            Add Exact Time
          </button>
        </div>
      </div>
    </div>
  );
}

export function ReminderBadge({ count }: { count: number }) {
  if (count === 0) return null;

  return (
    <span className="inline-flex items-center px-1.5 py-0.5 text-xs font-medium rounded bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300">
      <svg className="w-3 h-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      {count}
    </span>
  );
}
