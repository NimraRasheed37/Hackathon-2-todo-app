"use client";

import Link from "next/link";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

const benefits = [
  "Free forever - no hidden costs",
  "No credit card required",
  "Set up in under 2 minutes",
  "Cancel anytime",
];

export function CTA() {
  return (
    <section className="py-20 md:py-28 bg-background-secondary relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary/10 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className={cn(
          "relative p-8 md:p-12 lg:p-16 rounded-3xl overflow-hidden",
          "bg-gradient-to-br from-primary via-primary-hover to-accent",
          "shadow-primary"
        )}>
          {/* Decorative elements */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-black/10 rounded-full blur-3xl" />

          {/* Content */}
          <div className="relative text-center">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-primary-foreground mb-6">
              Ready to Transform Your Productivity?
            </h2>
            <p className="text-lg md:text-xl text-primary-foreground/80 max-w-2xl mx-auto mb-8">
              Join thousands of users who have already simplified their task management with MarkIt.
            </p>

            {/* Benefits */}
            <div className="flex flex-wrap justify-center gap-4 md:gap-6 mb-10">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-center gap-2 text-primary-foreground/90">
                  <CheckCircle2 className="w-5 h-5" />
                  <span className="text-sm font-medium">{benefit}</span>
                </div>
              ))}
            </div>

            {/* CTA buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/register"
                className={cn(
                  "group inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full",
                  "bg-white text-primary font-bold text-lg",
                  "hover:bg-background hover:shadow-xl hover:scale-[1.02]",
                  "transform transition-all duration-300"
                )}
              >
                Start Free Today
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className={cn(
                  "inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full",
                  "bg-transparent text-primary-foreground font-bold text-lg",
                  "border-2 border-primary-foreground/30 hover:border-primary-foreground/60",
                  "hover:bg-white/10",
                  "transform transition-all duration-300"
                )}
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
