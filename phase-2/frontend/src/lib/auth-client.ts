"use client";

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

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
