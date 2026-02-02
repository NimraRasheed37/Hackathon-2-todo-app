"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageSquare } from "lucide-react";

interface Tab {
  name: string;
  href: string;
  icon: React.ReactNode;
}

const tabs: Tab[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: <LayoutDashboard className="w-4 h-4" />,
  },
  {
    name: "Chat",
    href: "/chat",
    icon: <MessageSquare className="w-4 h-4" />,
  },
];

export function TabNavigation() {
  const pathname = usePathname();

  return (
    <nav className="flex gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg mb-6">
      {tabs.map((tab) => {
        const isActive = pathname === tab.href;
        return (
          <Link
            key={tab.href}
            href={tab.href}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors
              ${
                isActive
                  ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm"
                  : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-white/50 dark:hover:bg-gray-700/50"
              }`}
          >
            {tab.icon}
            {tab.name}
          </Link>
        );
      })}
    </nav>
  );
}
