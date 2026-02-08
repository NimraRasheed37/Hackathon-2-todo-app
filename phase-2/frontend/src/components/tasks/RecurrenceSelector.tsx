"use client";

import { useState } from "react";
import { RecurrencePattern, RecurrenceFrequency } from "@/types";

const FREQUENCY_OPTIONS: { value: RecurrenceFrequency; label: string }[] = [
  { value: "daily", label: "Daily" },
  { value: "weekly", label: "Weekly" },
  { value: "monthly", label: "Monthly" },
  { value: "yearly", label: "Yearly" },
  { value: "custom", label: "Custom" },
];

const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

interface RecurrenceSelectorProps {
  value: RecurrencePattern | null;
  onChange: (pattern: RecurrencePattern | null) => void;
  disabled?: boolean;
}

export function RecurrenceSelector({
  value,
  onChange,
  disabled = false,
}: RecurrenceSelectorProps) {
  const [isEnabled, setIsEnabled] = useState(value !== null);

  const handleToggle = () => {
    if (isEnabled) {
      onChange(null);
    } else {
      onChange({
        frequency: "daily",
        interval: 1,
      });
    }
    setIsEnabled(!isEnabled);
  };

  const handleFrequencyChange = (frequency: RecurrenceFrequency) => {
    if (!value) return;
    const newPattern: RecurrencePattern = {
      ...value,
      frequency,
      daysOfWeek: frequency === "weekly" ? [0] : undefined,
      dayOfMonth: frequency === "monthly" ? 1 : undefined,
    };
    onChange(newPattern);
  };

  const handleIntervalChange = (interval: number) => {
    if (!value) return;
    onChange({ ...value, interval: Math.max(1, interval) });
  };

  const handleDaysOfWeekChange = (day: number) => {
    if (!value || !value.daysOfWeek) return;
    const days = value.daysOfWeek.includes(day)
      ? value.daysOfWeek.filter((d) => d !== day)
      : [...value.daysOfWeek, day].sort();
    onChange({ ...value, daysOfWeek: days.length > 0 ? days : [0] });
  };

  const handleDayOfMonthChange = (day: number) => {
    if (!value) return;
    onChange({ ...value, dayOfMonth: Math.min(31, Math.max(1, day)) });
  };

  const handleEndDateChange = (date: string) => {
    if (!value) return;
    onChange({ ...value, endDate: date || undefined });
  };

  const handleMaxOccurrencesChange = (max: number | undefined) => {
    if (!value) return;
    onChange({ ...value, maxOccurrences: max });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={isEnabled}
            onChange={handleToggle}
            disabled={disabled}
            className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Repeat this task
          </span>
        </label>
      </div>

      {isEnabled && value && (
        <div className="pl-6 space-y-4 border-l-2 border-blue-200 dark:border-blue-800">
          {/* Frequency */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Frequency
            </label>
            <div className="flex flex-wrap gap-2">
              {FREQUENCY_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => handleFrequencyChange(option.value)}
                  disabled={disabled}
                  className={`
                    px-3 py-1.5 text-sm font-medium rounded-md border transition-all
                    ${value.frequency === option.value
                      ? "bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300"
                      : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                    }
                    disabled:opacity-50 disabled:cursor-not-allowed
                  `}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Interval */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600 dark:text-gray-400">Every</span>
            <input
              type="number"
              min="1"
              max="365"
              value={value.interval}
              onChange={(e) => handleIntervalChange(parseInt(e.target.value) || 1)}
              disabled={disabled}
              className="w-16 px-2 py-1 text-sm border rounded-md
                bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                disabled:opacity-50"
            />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {value.frequency === "daily" && (value.interval === 1 ? "day" : "days")}
              {value.frequency === "weekly" && (value.interval === 1 ? "week" : "weeks")}
              {value.frequency === "monthly" && (value.interval === 1 ? "month" : "months")}
              {value.frequency === "yearly" && (value.interval === 1 ? "year" : "years")}
              {value.frequency === "custom" && (value.interval === 1 ? "day" : "days")}
            </span>
          </div>

          {/* Days of Week (for weekly) */}
          {value.frequency === "weekly" && (
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                On days
              </label>
              <div className="flex flex-wrap gap-1">
                {DAY_NAMES.map((day, index) => (
                  <button
                    key={day}
                    type="button"
                    onClick={() => handleDaysOfWeekChange(index)}
                    disabled={disabled}
                    className={`
                      w-10 h-10 text-sm font-medium rounded-full border transition-all
                      ${value.daysOfWeek?.includes(index)
                        ? "bg-blue-600 border-blue-600 text-white"
                        : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                      }
                      disabled:opacity-50 disabled:cursor-not-allowed
                    `}
                  >
                    {day.charAt(0)}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Day of Month (for monthly) */}
          {value.frequency === "monthly" && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">On day</span>
              <input
                type="number"
                min="1"
                max="31"
                value={value.dayOfMonth || 1}
                onChange={(e) => handleDayOfMonthChange(parseInt(e.target.value) || 1)}
                disabled={disabled}
                className="w-16 px-2 py-1 text-sm border rounded-md
                  bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                  focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                  disabled:opacity-50"
              />
              <span className="text-sm text-gray-600 dark:text-gray-400">of the month</span>
            </div>
          )}

          {/* End Conditions */}
          <div className="space-y-3 pt-2 border-t border-gray-200 dark:border-gray-700">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Ends
            </label>
            <div className="space-y-2">
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="endCondition"
                  checked={!value.endDate && !value.maxOccurrences}
                  onChange={() => {
                    onChange({ ...value, endDate: undefined, maxOccurrences: undefined });
                  }}
                  disabled={disabled}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">Never</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="endCondition"
                  checked={!!value.endDate}
                  onChange={() => handleEndDateChange(new Date().toISOString().split('T')[0])}
                  disabled={disabled}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">On date</span>
                {value.endDate && (
                  <input
                    type="date"
                    value={value.endDate.split('T')[0]}
                    onChange={(e) => handleEndDateChange(e.target.value)}
                    disabled={disabled}
                    className="px-2 py-1 text-sm border rounded-md
                      bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                      focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                      disabled:opacity-50"
                  />
                )}
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="endCondition"
                  checked={!!value.maxOccurrences}
                  onChange={() => handleMaxOccurrencesChange(10)}
                  disabled={disabled}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">After</span>
                {value.maxOccurrences !== undefined && (
                  <>
                    <input
                      type="number"
                      min="1"
                      max="1000"
                      value={value.maxOccurrences}
                      onChange={(e) => handleMaxOccurrencesChange(parseInt(e.target.value) || 1)}
                      disabled={disabled}
                      className="w-16 px-2 py-1 text-sm border rounded-md
                        bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700
                        focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                        disabled:opacity-50"
                    />
                    <span className="text-sm text-gray-600 dark:text-gray-400">occurrences</span>
                  </>
                )}
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export function RecurrenceBadge({ pattern }: { pattern: RecurrencePattern | null }) {
  if (!pattern) return null;

  const getLabel = () => {
    const interval = pattern.interval;
    switch (pattern.frequency) {
      case "daily":
        return interval === 1 ? "Daily" : `Every ${interval} days`;
      case "weekly":
        if (pattern.daysOfWeek && pattern.daysOfWeek.length > 0) {
          const days = pattern.daysOfWeek.map(d => DAY_NAMES[d]).join(", ");
          return interval === 1 ? `Weekly (${days})` : `Every ${interval} weeks (${days})`;
        }
        return interval === 1 ? "Weekly" : `Every ${interval} weeks`;
      case "monthly":
        return interval === 1
          ? `Monthly (day ${pattern.dayOfMonth || 1})`
          : `Every ${interval} months`;
      case "yearly":
        return interval === 1 ? "Yearly" : `Every ${interval} years`;
      case "custom":
        return `Every ${interval} days`;
      default:
        return "Recurring";
    }
  };

  return (
    <span className="inline-flex items-center px-2 py-0.5 text-xs font-medium rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
      <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      {getLabel()}
    </span>
  );
}
