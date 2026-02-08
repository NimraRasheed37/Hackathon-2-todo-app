"use client";

import { Navbar } from "./Navbar";
import { Hero } from "./Hero";
import { Features } from "./Features";
import { Services } from "./Services";
import { ChatbotSection } from "./ChatbotSection";
import { Stats } from "./Stats";
import { CTA } from "./CTA";
import { Footer } from "./Footer";

export function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col overflow-x-hidden">
      <Navbar />
      <main className="flex-1">
        <Hero />
        <Stats />
        <Features />
        <Services />
        <ChatbotSection />
        <CTA />
      </main>
      <Footer />
    </div>
  );
}
