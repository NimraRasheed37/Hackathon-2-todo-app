"use client";

import { useSession, signOut, getToken } from "@/lib/auth-client";
import { useEffect, useCallback } from "react";
import Link from "next/link";
import { CheckSquare, LogOut, User, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { toast } from "sonner";
import { api } from "@/lib/api";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session, isPending } = useSession();

  const fetchAndSetToken = useCallback(async () => {
    try {
      const result = await getToken();
      if (result && "data" in result && result.data?.token) {
        api.setToken(result.data.token);
      }
    } catch (error) {
      console.error("Failed to get JWT token:", error);
    }
  }, []);

  useEffect(() => {
    if (!isPending && !session?.user) {
      window.location.href = "/login";
    }
  }, [session, isPending]);

  useEffect(() => {
    if (session?.user) {
      fetchAndSetToken();
    }
  }, [session?.user, fetchAndSetToken]);

  const handleLogout = async () => {
    try {
      await signOut();
      api.setToken(null);
      toast.success("Logged out successfully");
      window.location.href = "/login";
    } catch {
      toast.error("Failed to log out");
    }
  };

  if (isPending) {
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
      <header className="bg-card border-b border-border sticky top-0 z-40 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
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
            <div className="flex items-center gap-3">
              <ThemeToggle size="sm" />

              <div className="flex items-center gap-2 text-foreground-secondary px-3 py-1.5 rounded-lg bg-secondary">
                <User className="w-4 h-4" />
                <span className="hidden sm:inline font-medium text-sm">
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

      {/* Main content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
