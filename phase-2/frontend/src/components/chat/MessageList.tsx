"use client";

import { useEffect, useRef } from "react";
import { ChatMessage } from "@/types";
import { User, Bot, Sparkles } from "lucide-react";

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

function formatTime(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  // Skip tool messages in display
  if (message.role === "tool") {
    return null;
  }

  return (
    <div
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} mb-4 message-animate`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
                    ${isUser ? "bg-primary" : "bg-secondary"}`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-primary-foreground" />
        ) : (
          <Bot className="w-4 h-4 text-foreground" />
        )}
      </div>

      {/* Message content */}
      <div
        className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col`}
      >
        <div
          className={`rounded-2xl px-4 py-2.5 ${
            isUser
              ? "bg-primary text-primary-foreground rounded-br-md"
              : "bg-secondary text-secondary-foreground rounded-bl-md"
          }`}
        >
          <p className="text-sm whitespace-pre-wrap break-words leading-relaxed">
            {message.content}
          </p>
        </div>
        <span className="text-xs text-foreground-muted mt-1 px-1">
          {formatTime(message.created_at)}
        </span>
      </div>
    </div>
  );
}

function LoadingIndicator() {
  return (
    <div className="flex gap-3 mb-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-secondary">
        <Bot className="w-4 h-4 text-foreground" />
      </div>
      <div className="bg-secondary rounded-2xl rounded-bl-md px-4 py-3">
        <div className="flex gap-1">
          <span
            className="w-2 h-2 bg-foreground-muted rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <span
            className="w-2 h-2 bg-foreground-muted rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <span
            className="w-2 h-2 bg-foreground-muted rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
        </div>
      </div>
    </div>
  );
}

export function MessageList({
  messages,
  isLoading = false,
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 scrollbar-hide">
      {messages.length === 0 && !isLoading ? (
        <div className="flex flex-col items-center justify-center h-full text-center px-4">
          <div className="w-16 h-16 rounded-full bg-primary-light flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h3 className="text-lg font-semibold text-foreground mb-2">
            How can I help you?
          </h3>
          <p className="text-sm text-foreground-secondary max-w-xs mb-6">
            I can help you manage your tasks through conversation.
          </p>
          <div className="space-y-2 w-full max-w-xs">
            <div className="text-xs text-foreground-muted uppercase tracking-wider mb-2">
              Try saying:
            </div>
            {[
              '"Add buy milk to my tasks"',
              '"Show my pending tasks"',
              '"Mark buy milk as done"',
            ].map((example, i) => (
              <div
                key={i}
                className="bg-secondary/50 rounded-lg px-3 py-2 text-sm text-foreground-secondary"
              >
                {example}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && <LoadingIndicator />}
          <div ref={bottomRef} />
        </>
      )}
    </div>
  );
}
