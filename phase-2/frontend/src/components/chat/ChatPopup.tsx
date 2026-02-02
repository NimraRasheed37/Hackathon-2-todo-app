"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import {
  MessageSquare,
  X,
  Trash2,
  Minimize2,
  History,
  Plus,
  ChevronLeft,
  Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { chatApi } from "@/lib/chat-api";
import { ChatMessage, ChatResponse, ConversationSummary } from "@/types";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { toast } from "sonner";

const STORAGE_KEY = "markit-active-conversation";

export function ChatPopup() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [hasUnread, setHasUnread] = useState(false);
  const initialLoadDone = useRef(false);

  // Load active conversation ID from localStorage and fetch its messages
  useEffect(() => {
    if (initialLoadDone.current) return;
    initialLoadDone.current = true;

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const id = parseInt(stored, 10);
        if (!isNaN(id)) {
          setConversationId(id);
          loadConversation(id);
        }
      }
    } catch (error) {
      console.error("Failed to load stored conversation:", error);
    }
  }, []);

  // Save active conversation ID to localStorage
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem(STORAGE_KEY, conversationId.toString());
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, [conversationId]);

  // Clear unread when opened
  useEffect(() => {
    if (isOpen && !isMinimized) {
      setHasUnread(false);
    }
  }, [isOpen, isMinimized]);

  // Load conversation history when history panel is opened
  useEffect(() => {
    if (showHistory && conversations.length === 0) {
      loadConversations();
    }
  }, [showHistory]);

  const loadConversations = async () => {
    setIsLoadingHistory(true);
    try {
      const convs = await chatApi.getConversations(20);
      setConversations(convs);
    } catch (error) {
      console.error("Failed to load conversations:", error);
      toast.error("Failed to load chat history");
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const loadConversation = async (id: number) => {
    setIsLoading(true);
    try {
      const conv = await chatApi.getConversation(id);
      setMessages(conv.messages);
      setConversationId(id);
      setShowHistory(false);
    } catch (error) {
      console.error("Failed to load conversation:", error);
      toast.error("Failed to load conversation");
      // Clear invalid conversation ID
      setConversationId(null);
      setMessages([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      const userMessage: ChatMessage = {
        id: Date.now(),
        role: "user",
        content: content.trim(),
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

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
          // Refresh conversations list
          loadConversations();
        }

        // Show unread indicator if minimized
        if (isMinimized) {
          setHasUnread(true);
        }
      } catch (error) {
        console.error("Failed to send message:", error);
        toast.error("Failed to send message. Please try again.");
        setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, isLoading, isMinimized]
  );

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setShowHistory(false);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const handleDeleteConversation = useCallback(
    async (id: number, e?: React.MouseEvent) => {
      e?.stopPropagation();

      try {
        await chatApi.deleteConversation(id);
        setConversations((prev) => prev.filter((c) => c.id !== id));

        // If deleting current conversation, start a new one
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

  const handleToggle = () => {
    if (isMinimized) {
      setIsMinimized(false);
    } else {
      setIsOpen(!isOpen);
    }
    setHasUnread(false);
  };

  const handleMinimize = () => {
    setIsMinimized(true);
  };

  const handleClose = () => {
    setIsOpen(false);
    setIsMinimized(false);
    setShowHistory(false);
  };

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

  return (
    <>
      {/* Chat Popup Window */}
      {isOpen && !isMinimized && (
        <div
          className={cn(
            "fixed z-50 bg-card border border-border rounded-2xl shadow-xl flex flex-col overflow-hidden animate-slide-up",
            "bottom-20 right-4 left-4 top-20",
            "sm:left-auto sm:top-auto sm:bottom-24 sm:right-6 sm:w-80 sm:h-[24rem]",
            "lg:w-96 lg:h-[28rem]"
          )}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-3 py-2.5 bg-primary text-primary-foreground">
            <div className="flex items-center gap-2">
              {showHistory ? (
                <button
                  onClick={() => setShowHistory(false)}
                  className="p-1 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
              ) : (
                <MessageSquare className="w-5 h-5" />
              )}
              <span className="font-semibold text-sm">
                {showHistory ? "Chat History" : "MarkIt Assistant"}
              </span>
            </div>
            <div className="flex items-center gap-0.5">
              {!showHistory && (
                <>
                  <button
                    onClick={handleNewChat}
                    className="p-1.5 hover:bg-white/20 rounded-lg transition-colors"
                    title="New chat"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => {
                      setShowHistory(true);
                      loadConversations();
                    }}
                    className="p-1.5 hover:bg-white/20 rounded-lg transition-colors"
                    title="Chat history"
                  >
                    <History className="w-4 h-4" />
                  </button>
                </>
              )}
              <button
                onClick={handleMinimize}
                className="p-1.5 hover:bg-white/20 rounded-lg transition-colors hidden sm:block"
                title="Minimize"
              >
                <Minimize2 className="w-4 h-4" />
              </button>
              <button
                onClick={handleClose}
                className="p-1.5 hover:bg-white/20 rounded-lg transition-colors"
                title="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Content */}
          {showHistory ? (
            // History Panel
            <div className="flex-1 overflow-y-auto">
              {isLoadingHistory ? (
                <div className="flex items-center justify-center h-full">
                  <Loader2 className="w-6 h-6 animate-spin text-primary" />
                </div>
              ) : conversations.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center p-4">
                  <History className="w-10 h-10 text-foreground-muted mb-2" />
                  <p className="text-sm text-foreground-secondary">
                    No chat history yet
                  </p>
                  <p className="text-xs text-foreground-muted mt-1">
                    Start a conversation to see it here
                  </p>
                </div>
              ) : (
                <div className="p-2 space-y-1">
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
                          {formatDate(conv.updated_at)} ·{" "}
                          {conv.message_count} messages
                        </p>
                      </div>
                      <button
                        onClick={(e) => handleDeleteConversation(conv.id, e)}
                        className="p-1.5 opacity-0 group-hover:opacity-100 hover:bg-error/10 hover:text-error rounded-lg transition-all"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            // Chat Panel
            <>
              <div className="flex-1 overflow-hidden">
                <MessageList messages={messages} isLoading={isLoading} />
              </div>
              <div className="border-t border-border p-2.5 bg-background">
                <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
              </div>
            </>
          )}
        </div>
      )}

      {/* Floating Chat Button */}
      <button
        onClick={handleToggle}
        className={cn(
          "fixed z-50 flex items-center justify-center rounded-full shadow-lg transition-all duration-300 hover:scale-105 active:scale-95",
          "bottom-6 right-6",
          "w-14 h-14 sm:w-16 sm:h-16",
          isOpen
            ? "bg-secondary text-foreground hover:bg-secondary-hover"
            : "bg-primary text-primary-foreground hover:bg-primary-hover",
          isMinimized && "animate-pulse"
        )}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen && !isMinimized ? (
          <X className="w-6 h-6 sm:w-7 sm:h-7" />
        ) : (
          <>
            <MessageSquare className="w-6 h-6 sm:w-7 sm:h-7" />
            {hasUnread && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-error rounded-full flex items-center justify-center">
                <span className="w-2 h-2 bg-white rounded-full animate-ping" />
              </span>
            )}
          </>
        )}
      </button>
    </>
  );
}
