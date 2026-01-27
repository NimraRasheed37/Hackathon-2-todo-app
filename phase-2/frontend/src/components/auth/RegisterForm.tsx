"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { signUp } from "@/lib/auth-client";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { toast } from "sonner";
import { Mail, Lock, User, CheckSquare } from "lucide-react";

export function RegisterForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{
    name?: string;
    email?: string;
    password?: string;
  }>({});

  const validate = () => {
    const newErrors: { name?: string; email?: string; password?: string } = {};

    if (!name.trim()) {
      newErrors.name = "Name is required";
    } else if (name.trim().length < 2) {
      newErrors.name = "Name must be at least 2 characters";
    }

    if (!email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsLoading(true);
    try {
      const result = await signUp.email({
        name: name.trim(),
        email: email.trim().toLowerCase(),
        password,
      });

      if (result.error) {
        toast.error(result.error.message || "Registration failed");
        return;
      }

      toast.success("Account created successfully!");
      // Use full page navigation to ensure session cookies are read fresh
      window.location.href = "/dashboard";
    } catch {
      toast.error("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <CheckSquare className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold text-foreground">
            Mark<span className="text-primary">It</span>
          </span>
        </Link>
        <ThemeToggle size="sm" />
      </header>

      {/* Main content */}
      <main className="flex-1 flex items-center justify-center px-4 py-8">
        <div className="w-full max-w-md">
          <div className="bg-card rounded-2xl shadow-theme-lg border border-border p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="text-center mb-6">
                <h1 className="text-2xl font-bold text-foreground">
                  Create an account
                </h1>
                <p className="text-foreground-secondary mt-1">
                  Get started with your todo list
                </p>
              </div>

              <div className="space-y-4">
                <div className="relative">
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted">
                    <User className="w-5 h-5" />
                  </div>
                  <Input
                    type="text"
                    placeholder="Full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    error={errors.name}
                    className="pl-10"
                    autoComplete="name"
                    disabled={isLoading}
                  />
                </div>

                <div className="relative">
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted">
                    <Mail className="w-5 h-5" />
                  </div>
                  <Input
                    type="email"
                    placeholder="Email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    error={errors.email}
                    className="pl-10"
                    autoComplete="email"
                    disabled={isLoading}
                  />
                </div>

                <div className="relative">
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted">
                    <Lock className="w-5 h-5" />
                  </div>
                  <Input
                    type="password"
                    placeholder="Password (min 8 characters)"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    error={errors.password}
                    className="pl-10"
                    autoComplete="new-password"
                    disabled={isLoading}
                  />
                </div>
              </div>

              <Button
                type="submit"
                isLoading={isLoading}
                className="w-full"
                size="lg"
              >
                Create account
              </Button>

              <p className="text-center text-sm text-foreground-secondary">
                Already have an account?{" "}
                <Link
                  href="/login"
                  className="font-medium text-primary hover:text-primary-hover transition-colors"
                >
                  Sign in
                </Link>
              </p>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
