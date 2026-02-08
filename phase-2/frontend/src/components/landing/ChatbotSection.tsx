"use client";

import {
  Bot,
  Sparkles,
  MessageSquare,
  Wand2,
  Brain,
  Lightbulb,
  Send,
} from "lucide-react";
import { cn } from "@/lib/utils";

const chatFeatures = [
  {
    icon: Wand2,
    title: "Natural Language Input",
    description: "Just tell the AI what you need to do in plain English. It understands context and intent.",
  },
  {
    icon: Brain,
    title: "Smart Task Creation",
    description: "The AI automatically extracts task details like due dates, priorities, and categories from your message.",
  },
  {
    icon: Lightbulb,
    title: "Intelligent Suggestions",
    description: "Get personalized recommendations on how to organize and prioritize your tasks effectively.",
  },
  {
    icon: MessageSquare,
    title: "Conversational Interface",
    description: "Chat naturally with your task assistant. Ask questions, get updates, and manage tasks conversationally.",
  },
];

const sampleConversation = [
  {
    role: "user",
    message: "I need to prepare a presentation for Monday's meeting and review the Q4 budget report",
  },
  {
    role: "assistant",
    message: "I've created 2 tasks for you:\n\n1. **Prepare presentation for Monday meeting** - Due: Monday, Priority: High\n2. **Review Q4 budget report** - Priority: Medium\n\nWould you like me to set reminders for these?",
  },
  {
    role: "user",
    message: "Yes, remind me about the presentation on Sunday evening",
  },
  {
    role: "assistant",
    message: "Done! I've set a reminder for Sunday at 6:00 PM for the presentation task. You'll be notified before your Monday meeting. Anything else I can help with?",
  },
];

export function ChatbotSection() {
  return (
    <section className="py-20 md:py-28 bg-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -right-32 w-96 h-96 bg-primary/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-1/4 -left-32 w-96 h-96 bg-accent/10 rounded-full blur-[100px]" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        {/* Section header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-4">
            <Bot className="w-4 h-4" />
            AI-Powered Assistant
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6">
            Your Personal{" "}
            <span className="text-gradient-primary">AI Task Assistant</span>
          </h2>
          <p className="text-lg md:text-xl text-foreground-secondary">
            Meet your intelligent companion that understands natural language and helps you manage tasks effortlessly.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Chat demo */}
          <div className="order-2 lg:order-1">
            <div className={cn(
              "relative rounded-2xl overflow-hidden",
              "bg-card border border-border",
              "shadow-theme-xl"
            )}>
              {/* Chat header */}
              <div className="flex items-center gap-3 p-4 bg-background-secondary border-b border-border">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-foreground">MarkIt Assistant</p>
                  <p className="text-xs text-foreground-muted flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
                    Online
                  </p>
                </div>
                <Sparkles className="w-5 h-5 text-primary ml-auto" />
              </div>

              {/* Chat messages */}
              <div className="p-4 space-y-4 max-h-[400px] overflow-y-auto bg-background">
                {sampleConversation.map((msg, index) => (
                  <div
                    key={index}
                    className={cn(
                      "flex",
                      msg.role === "user" ? "justify-end" : "justify-start"
                    )}
                  >
                    <div
                      className={cn(
                        "max-w-[85%] p-4 rounded-2xl",
                        msg.role === "user"
                          ? "bg-primary text-primary-foreground rounded-br-md"
                          : "bg-card border border-border rounded-bl-md"
                      )}
                    >
                      <p className={cn(
                        "text-sm whitespace-pre-line",
                        msg.role === "assistant" && "text-foreground"
                      )}>
                        {msg.message}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Chat input */}
              <div className="p-4 border-t border-border bg-background-secondary">
                <div className="flex items-center gap-3 bg-background rounded-xl p-3 border border-border">
                  <input
                    type="text"
                    placeholder="Ask me anything about your tasks..."
                    className="flex-1 bg-transparent text-sm text-foreground placeholder:text-foreground-muted focus:outline-none"
                    readOnly
                  />
                  <button className="w-9 h-9 rounded-lg bg-primary text-primary-foreground flex items-center justify-center hover:bg-primary-hover transition-colors">
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Features list */}
          <div className="order-1 lg:order-2 space-y-6">
            {chatFeatures.map((feature, index) => (
              <div
                key={index}
                className={cn(
                  "flex gap-4 p-5 rounded-xl",
                  "bg-card border border-border",
                  "hover:border-primary hover:shadow-primary",
                  "transition-all duration-300"
                )}
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-foreground mb-1">
                    {feature.title}
                  </h3>
                  <p className="text-foreground-secondary text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
