"use client";

import { Users, CheckCircle2, Zap, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

const stats = [
  {
    icon: Users,
    value: "10K+",
    label: "Active Users",
    description: "Trust MarkIt daily",
  },
  {
    icon: CheckCircle2,
    value: "1M+",
    label: "Tasks Completed",
    description: "And counting",
  },
  {
    icon: Zap,
    value: "99.9%",
    label: "Uptime",
    description: "Always reliable",
  },
  {
    icon: Clock,
    value: "2hrs",
    label: "Saved Daily",
    description: "Per user average",
  },
];

export function Stats() {
  return (
    <section className="py-16 md:py-20 bg-background-secondary border-y border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="text-center group"
            >
              <div className={cn(
                "w-14 h-14 mx-auto mb-4 rounded-2xl",
                "bg-primary/10 flex items-center justify-center",
                "group-hover:bg-primary group-hover:scale-110",
                "transition-all duration-300"
              )}>
                <stat.icon className="w-7 h-7 text-primary group-hover:text-primary-foreground transition-colors" />
              </div>
              <p className="text-3xl md:text-4xl font-bold text-foreground mb-1">
                {stat.value}
              </p>
              <p className="text-lg font-semibold text-foreground-secondary mb-1">
                {stat.label}
              </p>
              <p className="text-sm text-foreground-muted">
                {stat.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
