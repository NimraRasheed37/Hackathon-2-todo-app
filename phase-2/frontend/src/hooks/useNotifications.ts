"use client";

import { useState, useEffect, useCallback } from "react";
import { Notification } from "@/types";

interface UseNotificationsOptions {
  userId: string;
  token: string;
  apiUrl?: string;
  pollIntervalMs?: number;
  enabled?: boolean;
}

interface UseNotificationsResult {
  notifications: Notification[];
  unreadCount: number;
  isLoading: boolean;
  error: Error | null;
  markAsRead: (notificationId: string) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function useNotifications({
  userId,
  token,
  apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  pollIntervalMs = 30000,
  enabled = true,
}: UseNotificationsOptions): UseNotificationsResult {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchNotifications = useCallback(async () => {
    if (!enabled || !userId || !token) return;

    try {
      const response = await fetch(
        `${apiUrl}/api/${userId}/notifications?limit=50`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch notifications: ${response.status}`);
      }

      const data = await response.json();
      setNotifications(data.notifications || []);
      setUnreadCount(data.unread_count || 0);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Unknown error"));
    } finally {
      setIsLoading(false);
    }
  }, [userId, token, apiUrl, enabled]);

  // Initial fetch and polling
  useEffect(() => {
    if (!enabled) return;

    fetchNotifications();
    const interval = setInterval(fetchNotifications, pollIntervalMs);

    return () => clearInterval(interval);
  }, [fetchNotifications, pollIntervalMs, enabled]);

  const markAsRead = useCallback(
    async (notificationId: string) => {
      try {
        const response = await fetch(
          `${apiUrl}/api/${userId}/notifications/mark-read`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ notification_ids: [parseInt(notificationId)] }),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to mark notification as read");
        }

        setNotifications((prev) =>
          prev.map((n) =>
            n.id === notificationId ? { ...n, read: true } : n
          )
        );
        setUnreadCount((prev) => Math.max(0, prev - 1));
      } catch (err) {
        console.error("Failed to mark notification as read:", err);
        throw err;
      }
    },
    [userId, token, apiUrl]
  );

  const markAllAsRead = useCallback(async () => {
    try {
      const response = await fetch(
        `${apiUrl}/api/${userId}/notifications/mark-all-read`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to mark all notifications as read");
      }

      setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (err) {
      console.error("Failed to mark all as read:", err);
      throw err;
    }
  }, [userId, token, apiUrl]);

  return {
    notifications,
    unreadCount,
    isLoading,
    error,
    markAsRead,
    markAllAsRead,
    refresh: fetchNotifications,
  };
}
