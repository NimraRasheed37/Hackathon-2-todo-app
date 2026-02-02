"use client";

import { createAuthClient } from "better-auth/react";

// Don't specify baseURL - better-auth will use current origin automatically
// This works for both localhost and production (Vercel)
export const authClient = createAuthClient({});

export const { signIn, signUp, signOut, useSession } = authClient;

// Fetch JWT token from our custom endpoint for API authentication
export const getToken = async (): Promise<string | null> => {
  try {
    const response = await fetch("/api/token", {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      return data.token;
    }
    return null;
  } catch (error) {
    console.error("Failed to fetch token:", error);
    return null;
  }
};
