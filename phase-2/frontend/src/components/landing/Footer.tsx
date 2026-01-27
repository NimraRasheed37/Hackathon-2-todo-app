"use client";

import Link from "next/link";
import { CheckSquare, Github, Twitter, Linkedin, Heart } from "lucide-react";
import { cn } from "@/lib/utils";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative bg-card border-t border-border">
      {/* Main footer content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 md:gap-12">
          {/* Brand section */}
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <CheckSquare className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-foreground">
                Mark<span className="text-primary">It</span>
              </span>
            </Link>
            <p className="text-foreground-secondary max-w-sm mb-6">
              A simple yet powerful task management app to help you stay
              organized and boost your productivity.
            </p>
            {/* Social links */}
            <div className="flex items-center gap-4">
              <SocialLink
                href="https://github.com"
                icon={<Github className="w-5 h-5" />}
                label="GitHub"
              />
              <SocialLink
                href="https://twitter.com"
                icon={<Twitter className="w-5 h-5" />}
                label="Twitter"
              />
              <SocialLink
                href="https://linkedin.com"
                icon={<Linkedin className="w-5 h-5" />}
                label="LinkedIn"
              />
            </div>
          </div>

          {/* Quick links */}
          <div>
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-4">
              Quick Links
            </h3>
            <ul className="space-y-3">
              <FooterLink href="/login">Sign In</FooterLink>
              <FooterLink href="/register">Create Account</FooterLink>
              <FooterLink href="#features">Features</FooterLink>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-4">
              Resources
            </h3>
            <ul className="space-y-3">
              <FooterLink href="#">Documentation</FooterLink>
              <FooterLink href="#">Support</FooterLink>
              <FooterLink href="#">Privacy Policy</FooterLink>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-foreground-muted text-sm text-center md:text-left">
              &copy; {currentYear} MarkIt. All rights reserved.
            </p>
            <p className="text-foreground-muted text-sm flex items-center gap-1">
              Made with{" "}
              <Heart className="w-4 h-4 text-error fill-error inline-block" />{" "}
              for productivity enthusiasts
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

function SocialLink({
  href,
  icon,
  label,
}: {
  href: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={cn(
        "w-10 h-10 flex items-center justify-center rounded-full",
        "bg-secondary text-foreground-secondary",
        "hover:bg-primary hover:text-primary-foreground",
        "transition-all duration-200",
        "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
      )}
      aria-label={label}
    >
      {icon}
    </a>
  );
}

function FooterLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <li>
      <Link
        href={href}
        className={cn(
          "text-foreground-secondary hover:text-primary",
          "transition-colors duration-200"
        )}
      >
        {children}
      </Link>
    </li>
  );
}
