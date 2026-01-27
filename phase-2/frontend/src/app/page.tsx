"use client";

import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { LandingPage } from "@/components/landing/LandingPage";
import { Loader2 } from "lucide-react";

export default function Home() {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const [showLanding, setShowLanding] = useState(false);

  useEffect(() => {
    if (!isPending) {
      if (session?.user) {
        // User is logged in, redirect to dashboard
        router.replace("/dashboard");
      } else {
        // User is not logged in, show landing page
        setShowLanding(true);
      }
    }
  }, [session, isPending, router]);

  // Show loading state while checking session
  if (isPending || (!showLanding && !session)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
          <p className="text-foreground-muted">Loading...</p>
        </div>
      </div>
    );
  }

  // Show landing page for unauthenticated users
  if (showLanding) {
    return <LandingPage />;
  }

  // Fallback (should not reach here normally)
  return null;
}
