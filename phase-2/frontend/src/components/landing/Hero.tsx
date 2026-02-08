"use client";

import Link from "next/link";
import {
  CheckCircle2,
  Sparkles,
  ArrowRight,
  Play,
} from "lucide-react";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Gradient orbs */}
        <div className="absolute top-1/4 -left-32 w-72 h-72 md:w-[500px] md:h-[500px] bg-primary/20 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-72 h-72 md:w-[500px] md:h-[500px] bg-accent/20 rounded-full blur-[100px] animate-pulse delay-500" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent/10 rounded-full blur-[120px]" />

        {/* Grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `linear-gradient(var(--foreground) 1px, transparent 1px),
                              linear-gradient(90deg, var(--foreground) 1px, transparent 1px)`,
            backgroundSize: "80px 80px",
          }}
        />

        {/* Floating elements */}
        <div className="absolute top-20 left-[10%] w-3 h-3 bg-primary rounded-full animate-float opacity-60" />
        <div className="absolute top-40 right-[15%] w-2 h-2 bg-accent rounded-full animate-float delay-300 opacity-60" />
        <div className="absolute bottom-32 left-[20%] w-4 h-4 bg-accent rounded-full animate-float delay-500 opacity-40" />
        <div className="absolute bottom-48 right-[25%] w-2 h-2 bg-primary rounded-full animate-float delay-700 opacity-50" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-20 md:pt-36 md:pb-28">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-semibold mb-8 animate-slide-down opacity-0" style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}>
            <Sparkles className="w-4 h-4" />
            <span>Intelligent Task Management</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-foreground leading-[1.1] mb-6 animate-slide-up opacity-0" style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}>
            Master Your Tasks.
            <br />
            <span className="text-gradient-primary">Achieve Excellence.</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl lg:text-2xl text-foreground-secondary max-w-2xl mx-auto mb-10 leading-relaxed animate-slide-up opacity-0" style={{ animationDelay: '300ms', animationFillMode: 'forwards' }}>
            MarkIt combines elegant design with powerful AI to help you organize, prioritize, and accomplish your goals effortlessly.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12 animate-slide-up opacity-0" style={{ animationDelay: '400ms', animationFillMode: 'forwards' }}>
            <Link
              href="/register"
              className={cn(
                "group inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full",
                "bg-primary text-primary-foreground font-semibold text-lg",
                "hover:shadow-primary hover:scale-[1.02]",
                "transform transition-all duration-300",
                "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
              )}
            >
              Get Started Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="#features"
              className={cn(
                "group inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full",
                "bg-card text-foreground font-semibold text-lg",
                "border-2 border-border hover:border-primary",
                "shadow-theme hover:shadow-theme-lg",
                "transform hover:scale-[1.02] transition-all duration-300",
                "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
              )}
            >
              <Play className="w-5 h-5 text-primary" />
              See How It Works
            </Link>
          </div>

          {/* Trust indicators */}
          <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-4 text-foreground-muted animate-fade-in opacity-0" style={{ animationDelay: '500ms', animationFillMode: 'forwards' }}>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-primary" />
              <span className="font-medium">Free Forever</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-primary" />
              <span className="font-medium">No Credit Card</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-primary" />
              <span className="font-medium">AI-Powered</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-primary" />
              <span className="font-medium">Secure & Private</span>
            </div>
          </div>
        </div>

        {/* Dashboard Preview */}
        <div className="mt-16 md:mt-20 relative animate-scale-in opacity-0" style={{ animationDelay: '600ms', animationFillMode: 'forwards' }}>
          <div className="relative mx-auto max-w-5xl">
            {/* Glow effect behind preview */}
            <div className="absolute inset-0 bg-gradient-to-t from-primary/20 via-transparent to-transparent blur-3xl -z-10" />

            {/* Dashboard mockup */}
            <div
              className={cn(
                "relative rounded-2xl md:rounded-3xl overflow-hidden",
                "bg-card border-2 border-border",
                "shadow-theme-xl"
              )}
            >
              {/* Top bar */}
              <div className="flex items-center gap-3 px-4 md:px-6 py-3 md:py-4 bg-background-secondary border-b border-border">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-error/70" />
                  <div className="w-3 h-3 rounded-full bg-warning/70" />
                  <div className="w-3 h-3 rounded-full bg-success/70" />
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="px-4 py-1.5 rounded-lg bg-background-tertiary text-foreground-muted text-xs md:text-sm font-medium">
                    app.markit.com/dashboard
                  </div>
                </div>
              </div>

              {/* Dashboard content preview */}
              <div className="p-4 md:p-8 bg-background">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
                  {/* Stats cards */}
                  <div className="p-4 md:p-6 rounded-xl bg-card border border-border">
                    <div className="w-10 h-10 rounded-lg bg-primary-light flex items-center justify-center mb-3">
                      <span className="text-primary font-bold">12</span>
                    </div>
                    <p className="text-sm text-foreground-muted">Total Tasks</p>
                    <p className="text-2xl font-bold text-foreground">Active</p>
                  </div>
                  <div className="p-4 md:p-6 rounded-xl bg-card border border-border">
                    <div className="w-10 h-10 rounded-lg bg-success-light flex items-center justify-center mb-3">
                      <span className="text-success font-bold">8</span>
                    </div>
                    <p className="text-sm text-foreground-muted">Completed</p>
                    <p className="text-2xl font-bold text-foreground">This Week</p>
                  </div>
                  <div className="p-4 md:p-6 rounded-xl bg-card border border-border">
                    <div className="w-10 h-10 rounded-lg bg-warning-light flex items-center justify-center mb-3">
                      <span className="text-warning font-bold">4</span>
                    </div>
                    <p className="text-sm text-foreground-muted">In Progress</p>
                    <p className="text-2xl font-bold text-foreground">Today</p>
                  </div>
                </div>

                {/* Task list preview */}
                <div className="mt-6 space-y-3">
                  {[
                    { title: "Review quarterly reports", priority: "high", done: false },
                    { title: "Team standup meeting", priority: "medium", done: false },
                    { title: "Update project documentation", priority: "low", done: true },
                  ].map((task, i) => (
                    <div key={i} className={cn(
                      "flex items-center gap-4 p-4 rounded-xl border transition-all",
                      task.done ? "bg-success-light/30 border-success/20" : "bg-card border-border hover:border-primary"
                    )}>
                      <div className={cn(
                        "w-6 h-6 rounded-lg border-2 flex items-center justify-center",
                        task.done ? "bg-success border-success" : "border-border"
                      )}>
                        {task.done && <CheckCircle2 className="w-4 h-4 text-white" />}
                      </div>
                      <span className={cn(
                        "flex-1 font-medium",
                        task.done ? "line-through text-foreground-muted" : "text-foreground"
                      )}>{task.title}</span>
                      <div className={cn(
                        "w-3 h-3 rounded-full",
                        task.priority === "high" && "bg-error",
                        task.priority === "medium" && "bg-warning",
                        task.priority === "low" && "bg-info"
                      )} />
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Floating cards */}
            <div className="absolute -top-4 -right-4 md:-right-8 p-4 rounded-xl bg-card border border-border shadow-theme-lg hidden sm:flex items-center gap-3 animate-float">
              <div className="w-10 h-10 rounded-full bg-success-light flex items-center justify-center">
                <CheckCircle2 className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-xs text-foreground-muted">Completion Rate</p>
                <p className="text-lg font-bold text-foreground">94%</p>
              </div>
            </div>

            <div className="absolute -bottom-4 -left-4 md:-left-8 p-4 rounded-xl bg-card border border-border shadow-theme-lg hidden sm:flex items-center gap-3 animate-float delay-500">
              <div className="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-xs text-foreground-muted">AI Suggestions</p>
                <p className="text-lg font-bold text-foreground">3 New</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
