"use client";

import Link from "next/link";
import {
  CheckCircle2,
  Sparkles,
  LayoutDashboard,
  ArrowRight,
  ListTodo,
  Calendar,
  Target,
} from "lucide-react";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden gradient-hero">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Gradient orbs */}
        <div className="absolute top-1/4 -left-32 w-64 h-64 md:w-96 md:h-96 bg-primary/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -right-32 w-64 h-64 md:w-96 md:h-96 bg-accent/10 rounded-full blur-3xl" />

        {/* Grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.02]"
          style={{
            backgroundImage: `linear-gradient(var(--foreground) 1px, transparent 1px),
                              linear-gradient(90deg, var(--foreground) 1px, transparent 1px)`,
            backgroundSize: "64px 64px",
          }}
        />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16 md:pt-32 md:pb-24">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left side - Content */}
          <div className="text-center lg:text-left">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-light text-primary text-sm font-medium mb-6 md:mb-8">
              <Sparkles className="w-4 h-4" />
              <span>Simple. Powerful. Productive.</span>
            </div>

            {/* Headline */}
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-foreground leading-tight mb-6">
              Organize your day.
              <br />
              <span className="text-primary">Achieve more.</span>
            </h1>

            {/* Subheadline */}
            <p className="text-lg md:text-xl text-foreground-secondary max-w-xl mx-auto lg:mx-0 mb-8 md:mb-10">
              MarkIt helps you capture tasks, stay focused, and accomplish your
              goals with a clean, intuitive interface designed for productivity.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link
                href="/register"
                className={cn(
                  "group inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full",
                  "bg-primary text-primary-foreground font-semibold text-lg",
                  "hover:bg-primary-hover shadow-lg hover:shadow-xl",
                  "transform hover:-translate-y-0.5 transition-all duration-200",
                  "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
                )}
              >
                Start Your List
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className={cn(
                  "inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full",
                  "bg-card text-foreground font-semibold text-lg",
                  "border border-border hover:border-border-hover",
                  "shadow-theme hover:shadow-theme-md",
                  "transform hover:-translate-y-0.5 transition-all duration-200",
                  "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
                )}
              >
                Sign In
              </Link>
            </div>

            {/* Trust indicators */}
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 mt-10 md:mt-12 text-foreground-muted text-sm">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-success" />
                <span>Free to use</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-success" />
                <span>No credit card</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-success" />
                <span>Instant access</span>
              </div>
            </div>
          </div>

          {/* Right side - Dashboard Preview */}
          <div className="relative lg:pl-8">
            {/* Dashboard mockup */}
            <div
              className={cn(
                "relative rounded-2xl overflow-hidden",
                "bg-card border border-border",
                "shadow-theme-xl"
              )}
            >
              {/* Top bar */}
              <div className="flex items-center gap-2 px-4 py-3 bg-background-secondary border-b border-border">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-error/60" />
                  <div className="w-3 h-3 rounded-full bg-warning/60" />
                  <div className="w-3 h-3 rounded-full bg-success/60" />
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="px-4 py-1 rounded-md bg-background-tertiary text-foreground-muted text-xs">
                    markit.app/dashboard
                  </div>
                </div>
              </div>

              {/* Dashboard content */}
              <div className="p-4 md:p-6 space-y-4">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                      <LayoutDashboard className="w-5 h-5 text-primary" />
                      My Tasks
                    </h3>
                    <p className="text-sm text-foreground-muted">
                      3 tasks for today
                    </p>
                  </div>
                  <button className="px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium">
                    + Add Task
                  </button>
                </div>

                {/* Stats cards */}
                <div className="grid grid-cols-3 gap-3">
                  <StatsCard
                    icon={<ListTodo className="w-4 h-4" />}
                    label="Total"
                    value="12"
                    color="primary"
                  />
                  <StatsCard
                    icon={<Target className="w-4 h-4" />}
                    label="Pending"
                    value="5"
                    color="warning"
                  />
                  <StatsCard
                    icon={<CheckCircle2 className="w-4 h-4" />}
                    label="Done"
                    value="7"
                    color="success"
                  />
                </div>

                {/* Task list */}
                <div className="space-y-2">
                  <TaskItem
                    title="Review project proposal"
                    completed={false}
                    priority="high"
                  />
                  <TaskItem
                    title="Team meeting at 2pm"
                    completed={false}
                    priority="medium"
                  />
                  <TaskItem
                    title="Send weekly report"
                    completed={true}
                    priority="low"
                  />
                </div>
              </div>
            </div>

            {/* Floating cards */}
            <div
              className={cn(
                "absolute -top-4 -right-4 md:-right-8 p-3 rounded-xl",
                "bg-card border border-border shadow-theme-lg",
                "hidden sm:flex items-center gap-2",
                "animate-float"
              )}
            >
              <div className="w-8 h-8 rounded-full bg-success-light flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4 text-success" />
              </div>
              <div>
                <p className="text-xs text-foreground-muted">Completed</p>
                <p className="text-sm font-semibold text-foreground">58%</p>
              </div>
            </div>

            <div
              className={cn(
                "absolute -bottom-4 -left-4 md:-left-8 p-3 rounded-xl",
                "bg-card border border-border shadow-theme-lg",
                "hidden sm:flex items-center gap-2",
                "animate-float animation-delay-500"
              )}
            >
              <div className="w-8 h-8 rounded-full bg-primary-light flex items-center justify-center">
                <Calendar className="w-4 h-4 text-primary" />
              </div>
              <div>
                <p className="text-xs text-foreground-muted">This Week</p>
                <p className="text-sm font-semibold text-foreground">
                  15 Tasks
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Animation styles */}
      <style jsx>{`
        @keyframes float {
          0%,
          100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-10px);
          }
        }
        .animate-float {
          animation: float 4s ease-in-out infinite;
        }
        .animation-delay-500 {
          animation-delay: 0.5s;
        }
      `}</style>
    </section>
  );
}

function StatsCard({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: "primary" | "warning" | "success";
}) {
  const colors = {
    primary: "bg-primary-light text-primary",
    warning: "bg-warning-light text-warning",
    success: "bg-success-light text-success",
  };

  return (
    <div className="p-3 rounded-xl bg-background-secondary border border-border">
      <div
        className={cn(
          "w-8 h-8 rounded-lg flex items-center justify-center mb-2",
          colors[color]
        )}
      >
        {icon}
      </div>
      <p className="text-xs text-foreground-muted">{label}</p>
      <p className="text-xl font-bold text-foreground">{value}</p>
    </div>
  );
}

function TaskItem({
  title,
  completed,
  priority,
}: {
  title: string;
  completed: boolean;
  priority: "high" | "medium" | "low";
}) {
  const priorityColors = {
    high: "bg-error",
    medium: "bg-warning",
    low: "bg-info",
  };

  return (
    <div
      className={cn(
        "flex items-center gap-3 p-3 rounded-xl",
        "bg-background-secondary border border-border",
        "transition-all duration-200 hover:border-border-hover"
      )}
    >
      <div
        className={cn(
          "w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors",
          completed
            ? "bg-success border-success"
            : "border-border hover:border-primary"
        )}
      >
        {completed && <CheckCircle2 className="w-3 h-3 text-white" />}
      </div>
      <span
        className={cn(
          "flex-1 text-sm",
          completed
            ? "line-through text-foreground-muted"
            : "text-foreground"
        )}
      >
        {title}
      </span>
      <div className={cn("w-2 h-2 rounded-full", priorityColors[priority])} />
    </div>
  );
}
