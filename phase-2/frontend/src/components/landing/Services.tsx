"use client";

import {
  Briefcase,
  GraduationCap,
  Home,
  Heart,
  Target,
  Users,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

const services = [
  {
    icon: Briefcase,
    title: "For Professionals",
    description: "Manage work projects, meetings, and deadlines efficiently. Track progress and collaborate with your team.",
    features: ["Project tracking", "Meeting reminders", "Priority management", "Progress reports"],
    gradient: "from-primary to-accent",
  },
  {
    icon: GraduationCap,
    title: "For Students",
    description: "Stay on top of assignments, exams, and study schedules. Never miss a deadline again.",
    features: ["Assignment tracking", "Exam reminders", "Study schedules", "Course organization"],
    gradient: "from-info to-primary",
  },
  {
    icon: Home,
    title: "For Personal Use",
    description: "Organize daily routines, shopping lists, and personal goals. Simplify your everyday life.",
    features: ["Daily routines", "Shopping lists", "Personal goals", "Habit tracking"],
    gradient: "from-success to-info",
  },
  {
    icon: Heart,
    title: "For Health & Wellness",
    description: "Track fitness goals, medication schedules, and wellness activities. Stay healthy and organized.",
    features: ["Fitness goals", "Medication reminders", "Wellness tracking", "Appointment scheduling"],
    gradient: "from-error to-warning",
  },
  {
    icon: Target,
    title: "For Goal Setting",
    description: "Break down big goals into actionable tasks. Track progress and celebrate achievements.",
    features: ["Goal breakdown", "Milestone tracking", "Progress visualization", "Achievement badges"],
    gradient: "from-warning to-primary",
  },
  {
    icon: Users,
    title: "For Teams",
    description: "Coordinate team activities, delegate tasks, and ensure everyone stays aligned.",
    features: ["Team coordination", "Task delegation", "Shared calendars", "Team analytics"],
    gradient: "from-primary to-info",
  },
];

export function Services() {
  return (
    <section className="py-20 md:py-28 bg-background-secondary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-4">
            Use Cases
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6">
            Perfect for{" "}
            <span className="text-gradient-primary">Every Lifestyle</span>
          </h2>
          <p className="text-lg md:text-xl text-foreground-secondary">
            Whether you&apos;re a busy professional, a student, or managing your home, MarkIt adapts to your needs.
          </p>
        </div>

        {/* Services grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className={cn(
                "group relative p-8 rounded-2xl overflow-hidden",
                "bg-card border border-border",
                "hover:border-transparent hover:shadow-primary",
                "transition-all duration-500"
              )}
            >
              {/* Gradient background on hover */}
              <div className={cn(
                "absolute inset-0 opacity-0 group-hover:opacity-5",
                "bg-gradient-to-br",
                service.gradient,
                "transition-opacity duration-500"
              )} />

              {/* Content */}
              <div className="relative">
                <div className={cn(
                  "w-16 h-16 rounded-2xl flex items-center justify-center mb-6",
                  "bg-gradient-to-br",
                  service.gradient
                )}>
                  <service.icon className="w-8 h-8 text-white" />
                </div>

                <h3 className="text-xl font-bold text-foreground mb-3">
                  {service.title}
                </h3>
                <p className="text-foreground-secondary mb-6 leading-relaxed">
                  {service.description}
                </p>

                {/* Features list */}
                <ul className="space-y-2 mb-6">
                  {service.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center gap-2 text-sm text-foreground-secondary">
                      <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                      {feature}
                    </li>
                  ))}
                </ul>

                <Link
                  href="/register"
                  className={cn(
                    "inline-flex items-center gap-2 text-primary font-semibold",
                    "group-hover:gap-3 transition-all duration-300"
                  )}
                >
                  Get Started
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
