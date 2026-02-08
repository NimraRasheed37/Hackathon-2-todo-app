"use client";

import { useSession, signOut, getToken } from "@/lib/auth-client";
import { useEffect, useRef, useCallback, useState } from "react";
import Link from "next/link";
import { CheckSquare, LogOut, User, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { chatApi } from "@/lib/chat-api";
import { Sidebar } from "@/components/layout/Sidebar";
import { ChatPopup } from "@/components/chat/ChatPopup";
import { cn } from "@/lib/utils";
import { preload } from "swr";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session, isPending, error } = useSession();
  const hasRedirected = useRef(false);
  const tokenFetched = useRef(false);
  const [isTokenReady, setIsTokenReady] = useState(false);

  // Fetch JWT token for API authentication
  const fetchAndSetToken = useCallback(async (userId: string) => {
    if (tokenFetched.current) return;

    try {
      const token = await getToken();
      if (token) {
        api.setToken(token);
        chatApi.setToken(token);
        tokenFetched.current = true;

        // Preload tasks data immediately after token is set
        const cacheKey = `/api/${userId}/tasks`;
        preload(cacheKey, () => api.getTasks(userId));

        setIsTokenReady(true);
        console.log("API token set and tasks preloaded");
      } else {
        console.log("No token received");
        setIsTokenReady(true); // Allow rendering even without token to show error state
      }
    } catch (error) {
      console.error("Failed to get token:", error);
      setIsTokenReady(true); // Allow rendering to show error state
    }
  }, []);

  // Debug logging - check browser console
  useEffect(() => {
    console.log("=== Session Debug ===");
    console.log("isPending:", isPending);
    console.log("session:", session);
    console.log("session?.user:", session?.user);
    console.log("error:", error);
    console.log("====================");
  }, [session, isPending, error]);

  useEffect(() => {
    // Only redirect once, and only if we're certain there's no session
    if (!isPending && !session?.user && !hasRedirected.current) {
      console.log("Redirecting to login - no session found");
      hasRedirected.current = true;
      window.location.href = "/login";
    }
  }, [session, isPending]);

  // Fetch API token when session is available
  useEffect(() => {
    if (session?.user?.id && !tokenFetched.current) {
      fetchAndSetToken(session.user.id);
    }
  }, [session?.user?.id, fetchAndSetToken]);

  const handleLogout = async () => {
    try {
      await signOut();
      api.setToken(null);
      chatApi.setToken(null);
      tokenFetched.current = false;
      toast.success("Logged out successfully");
      window.location.href = "/login";
    } catch {
      toast.error("Failed to log out");
    }
  };

  if (isPending || (session?.user && !isTokenReady)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
          <p className="text-foreground-muted">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session?.user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b border-border sticky top-0 z-50 shadow-sm">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/dashboard" className="flex items-center gap-2 group">
              <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-primary text-primary-foreground group-hover:shadow-md transition-shadow">
                <CheckSquare className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-foreground hidden sm:inline">
                Mark<span className="text-primary">It</span>
              </span>
            </Link>

            {/* User section */}
            <div className="flex items-center gap-2 sm:gap-3">
              <ThemeToggle size="sm" />

              <div className="flex items-center gap-2 text-foreground-secondary px-2 sm:px-3 py-1.5 rounded-lg bg-secondary">
                <User className="w-4 h-4" />
                <span className="hidden sm:inline font-medium text-sm max-w-[120px] truncate">
                  {session.user.name}
                </span>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="text-foreground-secondary hover:text-foreground"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline ml-1">Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Sidebar */}
      <Sidebar />

      {/* Main content - with sidebar offset */}
      <main
        className={cn(
          "transition-all duration-300 pt-6 pb-24",
          // Desktop: offset for sidebar (w-56 = 224px)
          "lg:pl-60",
          // Mobile: full width with padding
          "px-4 sm:px-6 lg:pr-6"
        )}
      >
        <div className="max-w-5xl">{children}</div>
      </main>

      {/* Floating Chat Button & Popup */}
      <ChatPopup />
    </div>
  );
}
