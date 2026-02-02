"use client";

import { useState, useCallback, KeyboardEvent } from "react";
import { Send } from "lucide-react";

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function MessageInput({
  onSend,
  isLoading = false,
  placeholder = "Type a message...",
}: MessageInputProps) {
  const [message, setMessage] = useState("");

  const handleSend = useCallback(() => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !isLoading) {
      onSend(trimmedMessage);
      setMessage("");
    }
  }, [message, isLoading, onSend]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  return (
    <div className="flex items-end gap-2">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={isLoading}
        rows={1}
        className="flex-1 resize-none rounded-xl border border-border
                   bg-card px-4 py-2.5 text-sm
                   focus:outline-none focus:ring-2 focus:ring-primary
                   disabled:opacity-50 disabled:cursor-not-allowed
                   text-foreground placeholder:text-foreground-muted
                   min-h-[44px] max-h-[120px] transition-shadow"
        style={{
          height: "auto",
          minHeight: "44px",
        }}
      />
      <button
        onClick={handleSend}
        disabled={isLoading || !message.trim()}
        className="flex items-center justify-center w-11 h-11 rounded-xl
                   bg-primary hover:bg-primary-hover disabled:bg-secondary
                   text-primary-foreground disabled:text-foreground-muted
                   transition-colors disabled:cursor-not-allowed"
        aria-label="Send message"
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
        ) : (
          <Send className="w-5 h-5" />
        )}
      </button>
    </div>
  );
}
