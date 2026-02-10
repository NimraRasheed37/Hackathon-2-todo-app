"use client";

import { useEffect, useState, useCallback } from "react";
import { getToken } from "@/lib/auth-client";
import { chatApi } from "@/lib/chat-api";
import { ChatMessage, ChatResponse, ConversationSummary } from "@/types";
import { MessageList } from "@/components/chat/MessageList";
import { MessageInput } from "@/components/chat/MessageInput";
import {
  Loader2,
  Plus,
  Trash2,
  MessageSquare,
  History,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

export default function ChatPage() {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const t = await getToken();
        setToken(t);
        if (t) {
          chatApi.setToken(t);
          loadConversations();
        }
      } catch (error) {
        console.error("Failed to get token:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchToken();
  }, []);

  const loadConversations = async () => {
    setIsLoadingConversations(true);
    try {
      const convs = await chatApi.getConversations(20);
      setConversations(convs);
    } catch (error) {
      console.error("Failed to load conversations:", error);
    } finally {
      setIsLoadingConversations(false);
    }
  };

  const loadConversation = async (id: number) => {
    setIsLoading(true);
    try {
      const conv = await chatApi.getConversation(id);
      setMessages(conv.messages);
      setConversationId(id);
    } catch (error) {
      console.error("Failed to load conversation:", error);
      toast.error("Failed to load conversation");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isSending) return;

      const userMessage: ChatMessage = {
        id: Date.now(),
        role: "user",
        content: content.trim(),
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsSending(true);

      try {
        const response: ChatResponse = await chatApi.sendMessage(
          content.trim(),
          conversationId
        );

        const assistantMessage: ChatMessage = {
          id: Date.now() + 1,
          role: "assistant",
          content: response.message,
          tool_calls: response.tool_calls
            ? { calls: response.tool_calls }
            : undefined,
          created_at: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, assistantMessage]);

        if (!conversationId && response.conversation_id) {
          setConversationId(response.conversation_id);
          loadConversations();
        }
      } catch (error) {
        console.error("Failed to send message:", error);
        toast.error("Failed to send message. Please try again.");
        setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
      } finally {
        setIsSending(false);
      }
    },
    [conversationId, isSending]
  );

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setConversationId(null);
  }, []);

  const handleDeleteConversation = useCallback(
    async (id: number, e?: React.MouseEvent) => {
      e?.stopPropagation();

      try {
        await chatApi.deleteConversation(id);
        setConversations((prev) => prev.filter((c) => c.id !== id));

        if (id === conversationId) {
          handleNewChat();
        }

        toast.success("Conversation deleted");
      } catch (error) {
        console.error("Failed to delete conversation:", error);
        toast.error("Failed to delete conversation");
      }
    },
    [conversationId, handleNewChat]
  );

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return "Today";
    if (days === 1) return "Yesterday";
    if (days < 7) return `${days} days ago`;
    return date.toLocaleDateString();
  };

  if (isLoading && !token) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!token) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <p className="text-error">
          Failed to authenticate. Please try logging in again.
        </p>
      </div>
    );
  }

  return (
    <div className="flex gap-4 h-[calc(100vh-8rem)]">
      {/* Sidebar - Conversation History */}
      <div className="hidden md:flex flex-col w-64 bg-card rounded-xl border border-border overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-3 border-b border-border">
          <div className="flex items-center gap-2">
            <History className="w-4 h-4 text-foreground-secondary" />
            <span className="font-medium text-sm text-foreground">History</span>
          </div>
          <button
            onClick={handleNewChat}
            className="p-1.5 hover:bg-secondary rounded-lg transition-colors"
            title="New chat"
          >
            <Plus className="w-4 h-4 text-foreground-secondary" />
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto p-2">
          {isLoadingConversations ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-5 h-5 animate-spin text-primary" />
            </div>
          ) : conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <MessageSquare className="w-8 h-8 text-foreground-muted mb-2" />
              <p className="text-sm text-foreground-secondary">No conversations</p>
              <p className="text-xs text-foreground-muted mt-1">
                Start chatting to create one
              </p>
            </div>
          ) : (
            <div className="space-y-1">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => loadConversation(conv.id)}
                  className={cn(
                    "flex items-center justify-between p-2.5 rounded-lg cursor-pointer transition-colors group",
                    conv.id === conversationId
                      ? "bg-primary/10 border border-primary/20"
                      : "hover:bg-secondary"
                  )}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">
                      {conv.title}
                    </p>
                    <p className="text-xs text-foreground-muted">
                      {formatDate(conv.updated_at)}
                    </p>
                  </div>
                  <button
                    onClick={(e) => handleDeleteConversation(conv.id, e)}
                    className="p-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 hover:bg-error/10 hover:text-error rounded transition-all"
                    title="Delete"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-card rounded-xl border border-border overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-primary text-primary-foreground">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5" />
            <span className="font-semibold">MarkIt Assistant</span>
          </div>
          <div className="flex items-center gap-2">
            {conversationId && (
              <span className="text-xs text-primary-foreground/70">
                #{conversationId}
              </span>
            )}
            <button
              onClick={handleNewChat}
              className="p-1.5 hover:bg-white/20 rounded-lg transition-colors md:hidden"
              title="New chat"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} isLoading={isSending} />
        </div>

        {/* Input */}
        <div className="border-t border-border p-3 bg-background">
          <MessageInput
            onSend={handleSendMessage}
            isLoading={isSending}
            placeholder="Ask me to manage your tasks..."
          />
        </div>
      </div>
    </div>
  );
}
