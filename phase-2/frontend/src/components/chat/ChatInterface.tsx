"use client";

import { useState, useCallback, useEffect } from "react";
import { chatApi } from "@/lib/chat-api";
import { ChatMessage, ChatResponse } from "@/types";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";

interface ChatInterfaceProps {
  token: string;
  initialConversationId?: number | null;
}

export function ChatInterface({
  token,
  initialConversationId = null,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(
    initialConversationId
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Set token on mount
  useEffect(() => {
    chatApi.setToken(token);
  }, [token]);

  // Load existing conversation if provided
  useEffect(() => {
    if (initialConversationId) {
      loadConversation(initialConversationId);
    }
  }, [initialConversationId]);

  const loadConversation = async (id: number) => {
    try {
      setIsLoading(true);
      const conversation = await chatApi.getConversation(id);
      setMessages(conversation.messages);
      setConversationId(id);
    } catch (err) {
      console.error("Failed to load conversation:", err);
      setError("Failed to load conversation");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = useCallback(
    async (content: string) => {
      setError(null);
      setIsLoading(true);

      // Optimistically add user message
      const tempUserMessage: ChatMessage = {
        id: Date.now(), // Temporary ID
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, tempUserMessage]);

      try {
        const response: ChatResponse = await chatApi.sendMessage(
          content,
          conversationId
        );

        // Update conversation ID if this was a new conversation
        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        // Add assistant response
        const assistantMessage: ChatMessage = {
          id: Date.now() + 1, // Temporary ID
          role: "assistant",
          content: response.message,
          tool_calls: response.tool_calls
            ? { calls: response.tool_calls }
            : undefined,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error("Failed to send message:", err);
        setError("Failed to send message. Please try again.");

        // Remove optimistic user message on error
        setMessages((prev) =>
          prev.filter((msg) => msg.id !== tempUserMessage.id)
        );
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId]
  );

  return (
    <div className="flex flex-col h-full bg-card rounded-xl shadow-sm border border-border overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-primary text-primary-foreground">
        <h2 className="text-lg font-semibold">MarkIt Assistant</h2>
        {conversationId && (
          <span className="text-xs text-primary-foreground/70">
            #{conversationId}
          </span>
        )}
      </div>

      {/* Error banner */}
      {error && (
        <div className="px-4 py-2 bg-error-light text-error text-sm">
          {error}
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input */}
      <div className="border-t border-border p-3 bg-background">
        <MessageInput
          onSend={handleSendMessage}
          isLoading={isLoading}
          placeholder="Ask me to manage your tasks..."
        />
      </div>
    </div>
  );
}
