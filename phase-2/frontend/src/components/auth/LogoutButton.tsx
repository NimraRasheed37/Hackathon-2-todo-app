"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signOut } from "@/lib/auth-client";
import { Button, ButtonProps } from "@/components/ui/Button";
import { toast } from "sonner";
import { LogOut } from "lucide-react";
import { api } from "@/lib/api";

interface LogoutButtonProps extends Omit<ButtonProps, "onClick"> {
  showIcon?: boolean;
  showText?: boolean;
}

export function LogoutButton({
  showIcon = true,
  showText = true,
  variant = "ghost",
  ...props
}: LogoutButtonProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await signOut();
      api.setToken(null);
      toast.success("Logged out successfully");
      router.replace("/login");
    } catch {
      toast.error("Failed to log out");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      variant={variant}
      onClick={handleLogout}
      isLoading={isLoading}
      {...props}
    >
      {showIcon && <LogOut className="w-4 h-4" />}
      {showText && <span>Logout</span>}
    </Button>
  );
}
