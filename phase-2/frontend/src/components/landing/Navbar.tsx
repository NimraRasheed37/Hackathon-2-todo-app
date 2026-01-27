"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X, CheckSquare } from "lucide-react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { cn } from "@/lib/utils";

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setIsMobileMenuOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        isScrolled
          ? "bg-card/80 backdrop-blur-lg shadow-theme border-b border-border"
          : "bg-transparent"
      )}
    >
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center gap-2 group"
          >
            <div className="relative w-9 h-9 md:w-10 md:h-10 flex items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md group-hover:shadow-lg transition-shadow">
              <CheckSquare className="w-5 h-5 md:w-6 md:h-6" />
            </div>
            <span className="text-xl md:text-2xl font-bold text-foreground">
              Mark<span className="text-primary">It</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-4">
            <ThemeToggle size="md" />
            <Link
              href="/login"
              className={cn(
                "px-6 py-2.5 rounded-full font-medium transition-all duration-200",
                "bg-primary text-primary-foreground",
                "hover:bg-primary-hover hover:shadow-lg",
                "focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
              )}
            >
              Login
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center gap-2">
            <ThemeToggle size="sm" />
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className={cn(
                "p-2 rounded-lg transition-colors",
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

        {/* Mobile Menu */}
        <div
          className={cn(
            "md:hidden overflow-hidden transition-all duration-300 ease-in-out",
            isMobileMenuOpen ? "max-h-64 pb-4" : "max-h-0"
          )}
        >
          <div className="pt-2 pb-4 space-y-3">
            <Link
              href="/login"
              onClick={() => setIsMobileMenuOpen(false)}
              className={cn(
                "block w-full px-4 py-3 rounded-xl text-center font-medium",
                "bg-primary text-primary-foreground",
                "hover:bg-primary-hover",
                "transition-colors duration-200"
              )}
            >
              Login
            </Link>
            <Link
              href="/register"
              onClick={() => setIsMobileMenuOpen(false)}
              className={cn(
                "block w-full px-4 py-3 rounded-xl text-center font-medium",
                "bg-secondary text-secondary-foreground",
                "hover:bg-secondary-hover",
                "transition-colors duration-200"
              )}
            >
              Create Account
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
