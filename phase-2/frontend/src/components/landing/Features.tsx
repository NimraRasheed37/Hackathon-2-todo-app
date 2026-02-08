"use client";

import {
  ListTodo,
  Bell,
  Tags,
  Search,
  Calendar,
  Repeat,
  Shield,
  Smartphone,
} from "lucide-react";
import { cn } from "@/lib/utils";

const features = [
  {
    icon: ListTodo,
    title: "Smart Task Management",
    description: "Create, organize, and prioritize tasks with intuitive drag-and-drop interface. Set priorities from low to critical.",
    color: "primary",
  },
  {
    icon: Bell,
    title: "Smart Reminders",
    description: "Never miss a deadline with customizable notifications. Get reminded before tasks are due.",
    color: "warning",
  },
  {
    icon: Tags,
    title: "Tags & Categories",
    description: "Organize tasks with custom tags and categories. Filter and find tasks instantly.",
    color: "info",
  },
  {
    icon: Search,
    title: "Powerful Search",
    description: "Full-text search across all your tasks. Find anything in seconds with advanced filters.",
    color: "success",
  },
  {
    icon: Calendar,
    title: "Due Dates & Scheduling",
    description: "Plan ahead with due dates and time-based scheduling. View tasks by day, week, or month.",
    color: "error",
  },
  {
    icon: Repeat,
    title: "Recurring Tasks",
    description: "Set up daily, weekly, monthly, or yearly recurring tasks. Never forget routine activities.",
    color: "primary",
  },
  {
    icon: Shield,
    title: "Secure & Private",
    description: "Your data is encrypted and secure. We never share your information with third parties.",
    color: "success",
  },
  {
    icon: Smartphone,
    title: "Responsive Design",
    description: "Access your tasks from any device. Seamless experience on desktop, tablet, and mobile.",
    color: "info",
  },
];

const colorClasses = {
  primary: {
    bg: "bg-primary/10",
    text: "text-primary",
    hover: "group-hover:bg-primary group-hover:text-primary-foreground",
  },
  warning: {
    bg: "bg-warning/10",
    text: "text-warning",
    hover: "group-hover:bg-warning group-hover:text-white",
  },
  info: {
    bg: "bg-info/10",
    text: "text-info",
    hover: "group-hover:bg-info group-hover:text-white",
  },
  success: {
    bg: "bg-success/10",
    text: "text-success",
    hover: "group-hover:bg-success group-hover:text-white",
  },
  error: {
    bg: "bg-error/10",
    text: "text-error",
    hover: "group-hover:bg-error group-hover:text-white",
  },
};

export function Features() {
  return (
    <section id="features" className="py-20 md:py-28 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-4">
            Features
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6">
            Everything You Need to{" "}
            <span className="text-gradient-primary">Stay Productive</span>
          </h2>
          <p className="text-lg md:text-xl text-foreground-secondary">
            Powerful features designed to help you manage tasks efficiently and achieve your goals faster.
          </p>
        </div>

        {/* Features grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
          {features.map((feature, index) => {
            const colors = colorClasses[feature.color as keyof typeof colorClasses];
            return (
              <div
                key={index}
                className={cn(
                  "group p-6 md:p-8 rounded-2xl",
                  "bg-card border border-border",
                  "hover:border-primary hover:shadow-primary",
                  "transition-all duration-300 hover:-translate-y-1"
                )}
              >
                <div
                  className={cn(
                    "w-14 h-14 rounded-xl flex items-center justify-center mb-5",
                    colors.bg,
                    colors.hover,
                    "transition-all duration-300"
                  )}
                >
                  <feature.icon className={cn("w-7 h-7", colors.text, "group-hover:text-inherit transition-colors")} />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-3">
                  {feature.title}
                </h3>
                <p className="text-foreground-secondary leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
