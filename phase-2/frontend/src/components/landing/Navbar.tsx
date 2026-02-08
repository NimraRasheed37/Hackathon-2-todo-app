"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X, CheckSquare } from "lucide-react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { cn } from "@/lib/utils";

const navLinks = [
  { href: "#features", label: "Features" },
  { href: "#", label: "Pricing" },
  { href: "#", label: "About" },
];

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setIsMobileMenuOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isMobileMenuOpen]);

  return (
    <>
      <header
        className={cn(
          "fixed top-0 left-0 right-0 z-50 transition-all duration-500",
          isScrolled
            ? "bg-card/90 backdrop-blur-xl shadow-theme border-b border-border"
            : "bg-transparent"
        )}
      >
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 md:h-20">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className={cn(
                "relative w-10 h-10 md:w-11 md:h-11 flex items-center justify-center rounded-xl",
                "bg-gradient-to-br from-primary to-accent text-white",
                "shadow-primary group-hover:shadow-lg group-hover:scale-105",
                "transition-all duration-300"
              )}>
                <CheckSquare className="w-5 h-5 md:w-6 md:h-6" />
              </div>
              <span className="text-xl md:text-2xl font-bold text-foreground">
                Mark<span className="text-gradient-primary">It</span>
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8">
              {/* Nav links */}
              <div className="flex items-center gap-6">
                {navLinks.map((link) => (
                  <Link
                    key={link.label}
                    href={link.href}
                    className={cn(
                      "text-foreground-secondary font-medium",
                      "hover:text-primary transition-colors duration-200",
                      "relative after:absolute after:bottom-0 after:left-0 after:right-0",
                      "after:h-0.5 after:bg-primary after:scale-x-0 after:origin-right",
                      "after:transition-transform after:duration-300",
                      "hover:after:scale-x-100 hover:after:origin-left"
                    )}
                  >
                    {link.label}
                  </Link>
                ))}
              </div>

              <div className="flex items-center gap-3">
                <ThemeToggle size="md" />
                <Link
                  href="/login"
                  className={cn(
                    "px-5 py-2.5 rounded-full font-semibold",
                    "text-foreground-secondary hover:text-primary",
                    "transition-colors duration-200"
                  )}
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className={cn(
                    "px-6 py-2.5 rounded-full font-semibold",
                    "bg-primary text-primary-foreground",
                    "hover:shadow-primary hover:scale-105",
                    "transition-all duration-300"
                  )}
                >
                  Get Started
                </Link>
              </div>
            </div>

            {/* Mobile Menu Button */}
            <div className="flex md:hidden items-center gap-3">
              <ThemeToggle size="sm" />
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className={cn(
                  "p-2.5 rounded-xl transition-all duration-200",
                  "text-foreground-secondary hover:text-foreground",
                  "hover:bg-secondary",
                  "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                )}
                aria-label="Toggle menu"
                aria-expanded={isMobileMenuOpen}
              >
                {isMobileMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>
        </nav>
      </header>

      {/* Mobile Menu Overlay */}
      <div
        className={cn(
          "fixed inset-0 z-40 md:hidden transition-all duration-300",
          isMobileMenuOpen ? "visible" : "invisible"
        )}
      >
        {/* Backdrop */}
        <div
          className={cn(
            "absolute inset-0 bg-foreground/20 backdrop-blur-sm transition-opacity duration-300",
            isMobileMenuOpen ? "opacity-100" : "opacity-0"
          )}
          onClick={() => setIsMobileMenuOpen(false)}
        />

        {/* Menu panel */}
        <div
          className={cn(
            "absolute top-16 left-4 right-4 p-6 rounded-2xl",
            "bg-card border border-border shadow-theme-xl",
            "transition-all duration-300 transform",
            isMobileMenuOpen
              ? "opacity-100 translate-y-0"
              : "opacity-0 -translate-y-4"
          )}
        >
          {/* Nav links */}
          <div className="space-y-1 mb-6">
            {navLinks.map((link) => (
              <Link
                key={link.label}
                href={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  "block px-4 py-3 rounded-xl",
                  "text-foreground font-medium",
                  "hover:bg-primary/10 hover:text-primary",
                  "transition-colors duration-200"
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="h-px bg-border mb-6" />

          {/* Auth buttons */}
          <div className="space-y-3">
            <Link
              href="/register"
              onClick={() => setIsMobileMenuOpen(false)}
              className={cn(
                "block w-full px-4 py-3.5 rounded-xl text-center font-semibold",
                "bg-primary text-primary-foreground",
                "hover:shadow-primary",
                "transition-all duration-200"
              )}
            >
              Get Started Free
            </Link>
            <Link
              href="/login"
              onClick={() => setIsMobileMenuOpen(false)}
              className={cn(
                "block w-full px-4 py-3.5 rounded-xl text-center font-semibold",
                "bg-secondary text-secondary-foreground",
                "hover:bg-secondary-hover",
                "transition-colors duration-200"
              )}
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
