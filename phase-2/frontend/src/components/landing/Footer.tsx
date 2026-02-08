"use client";

import Link from "next/link";
import {
  CheckSquare,
  Github,
  Twitter,
  Linkedin,
  Heart,
  Mail,
  MapPin,
} from "lucide-react";
import { cn } from "@/lib/utils";

const footerLinks = {
  product: [
    { href: "#features", label: "Features" },
    { href: "#", label: "Pricing" },
    { href: "#", label: "Integrations" },
    { href: "#", label: "Changelog" },
  ],
  company: [
    { href: "#", label: "About Us" },
    { href: "#", label: "Blog" },
    { href: "#", label: "Careers" },
    { href: "#", label: "Contact" },
  ],
  resources: [
    { href: "#", label: "Documentation" },
    { href: "#", label: "Help Center" },
    { href: "#", label: "API Reference" },
    { href: "#", label: "Status" },
  ],
  legal: [
    { href: "#", label: "Privacy Policy" },
    { href: "#", label: "Terms of Service" },
    { href: "#", label: "Cookie Policy" },
  ],
};

const socialLinks = [
  { href: "https://github.com", icon: Github, label: "GitHub" },
  { href: "https://twitter.com", icon: Twitter, label: "Twitter" },
  { href: "https://linkedin.com", icon: Linkedin, label: "LinkedIn" },
];

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-card border-t border-border">
      {/* Main footer content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-20">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 md:gap-12">
          {/* Brand section */}
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-2.5 mb-6">
              <div
                className={cn(
                  "w-10 h-10 flex items-center justify-center rounded-xl",
                  "bg-gradient-to-br from-primary to-accent text-white",
                )}
              >
                <CheckSquare className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-foreground">
                Mark<span className="text-gradient-primary">It</span>
              </span>
            </Link>
            <p className="text-foreground-secondary max-w-sm mb-6 leading-relaxed">
              The intelligent task management app that helps you stay organized,
              focused, and productive every day.
            </p>

            {/* Contact info */}
            <div className="space-y-3 mb-6">
              <div className="flex items-center gap-3 text-foreground-secondary">
                <Mail className="w-4 h-4 text-primary" />
                <span className="text-sm">hello@markit.app</span>
              </div>
              <div className="flex items-center gap-3 text-foreground-secondary">
                <MapPin className="w-4 h-4 text-primary" />
                <span className="text-sm">San Francisco, CA</span>
              </div>
            </div>

            {/* Social links */}
            <div className="flex items-center gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={cn(
                    "w-10 h-10 flex items-center justify-center rounded-xl",
                    "bg-secondary text-foreground-secondary",
                    "hover:bg-primary hover:text-primary-foreground",
                    "transition-all duration-300",
                  )}
                  aria-label={social.label}
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Product links */}
          <div>
            <h3 className="text-sm font-bold text-foreground uppercase tracking-wider mb-4">
              Product
            </h3>
            <ul className="space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-foreground-secondary hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company links */}
          <div>
            <h3 className="text-sm font-bold text-foreground uppercase tracking-wider mb-4">
              Company
            </h3>
            <ul className="space-y-3">
              {footerLinks.company.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-foreground-secondary hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources links */}
          <div>
            <h3 className="text-sm font-bold text-foreground uppercase tracking-wider mb-4">
              Resources
            </h3>
            <ul className="space-y-3">
              {footerLinks.resources.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-foreground-secondary hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal links */}
          <div>
            <h3 className="text-sm font-bold text-foreground uppercase tracking-wider mb-4">
              Legal
            </h3>
            <ul className="space-y-3">
              {footerLinks.legal.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-foreground-secondary hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
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
            <p className="text-foreground-muted text-sm flex items-center gap-1.5">
              Made with <Heart className="w-4 h-4 text-error fill-error" /> by
              nimrarasheed.com
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
