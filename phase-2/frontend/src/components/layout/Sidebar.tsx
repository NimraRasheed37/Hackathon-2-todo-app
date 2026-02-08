"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import {
  LayoutDashboard,
  ListTodo,
  CheckCircle2,
  MessageSquare,
  X,
  LogOut,
  User,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { Button } from "@/components/ui/Button";

interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  description?: string;
  filter?: string | null;
}

const navItems: NavItem[] = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
    description: "Overview of all tasks",
    filter: null,
  },
  {
    href: "/dashboard?filter=pending",
    label: "Todo Tasks",
    icon: ListTodo,
    description: "Pending tasks",
    filter: "pending",
  },
  {
    href: "/dashboard?filter=completed",
    label: "Completed",
    icon: CheckCircle2,
    description: "Finished tasks",
    filter: "completed",
  },
  {
    href: "/chat",
    label: "Chat",
    icon: MessageSquare,
    description: "AI Assistant",
    filter: null,
  },
];

interface SidebarProps {
  className?: string;
  isMobileOpen?: boolean;
  onMobileClose?: () => void;
  onLogout?: () => void;
  userName?: string;
}

export function Sidebar({
  className,
  isMobileOpen = false,
  onMobileClose,
  onLogout,
  userName,
}: SidebarProps) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const currentFilter = searchParams.get("filter");

  const isActive = (item: NavItem) => {
    if (item.href === "/chat") {
      return pathname === "/chat";
    }
    if (pathname !== "/dashboard") {
      return false;
    }
    // Dashboard items - check filter
    if (item.filter === null) {
      return !currentFilter;
    }
    return currentFilter === item.filter;
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40 animate-fade-in"
          onClick={onMobileClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-16 h-[calc(100vh-4rem)] bg-card border-r border-border z-40 transition-all duration-300 flex flex-col w-56",
          // Desktop
          "hidden lg:flex",
          // Mobile
          isMobileOpen && "!flex",
          className
        )}
      >
        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item);

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onMobileClose}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group relative",
                  active
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "text-foreground-secondary hover:bg-secondary hover:text-foreground"
                )}
              >
                <Icon
                  className={cn(
                    "w-5 h-5 flex-shrink-0 transition-transform group-hover:scale-110",
                    active && "text-primary-foreground"
                  )}
                />
                <div className="flex flex-col min-w-0">
                  <span className="font-medium text-sm truncate">
                    {item.label}
                  </span>
                  {item.description && (
                    <span
                      className={cn(
                        "text-xs truncate",
                        active
                          ? "text-primary-foreground/80"
                          : "text-foreground-muted"
                      )}
                    >
                      {item.description}
                    </span>
                  )}
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Mobile Footer - Theme Toggle & Logout */}
        <div className="lg:hidden border-t border-border p-3 space-y-2">
          {/* User Info */}
          {userName && (
            <div className="flex items-center gap-2 text-foreground-secondary px-3 py-2 rounded-lg bg-secondary">
              <User className="w-4 h-4" />
              <span className="font-medium text-sm truncate">{userName}</span>
            </div>
          )}

          {/* Theme Toggle */}
          <div className="flex items-center justify-between px-3 py-2">
            <span className="text-sm text-foreground-secondary">Theme</span>
            <ThemeToggle size="sm" />
          </div>

          {/* Logout Button */}
          {onLogout && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onLogout}
              className="w-full justify-start text-foreground-secondary hover:text-error"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          )}
        </div>

        {/* Mobile Close Button */}
        {isMobileOpen && (
          <button
            onClick={onMobileClose}
            className="lg:hidden absolute top-3 right-3 p-1.5 rounded-lg text-foreground-muted hover:text-foreground hover:bg-secondary transition-colors"
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </aside>
    </>
  );
}
