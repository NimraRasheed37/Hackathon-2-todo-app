"use client";

import { Navbar } from "./Navbar";
import { Hero } from "./Hero";
import { Footer } from "./Footer";

export function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Hero />
      </main>
      <Footer />
    </div>
  );
}
