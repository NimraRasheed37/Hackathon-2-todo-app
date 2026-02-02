import {
  ChatRequest,
  ChatResponse,
  Conversation,
  ConversationSummary,
  ApiError,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ChatApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async fetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorDetail = "An error occurred";
      let errorCode = "UNKNOWN_ERROR";

      try {
        const error = await response.json();
        errorDetail = error.detail || errorDetail;
        errorCode = error.error_code || errorCode;
      } catch {
        // Response may not be JSON
      }

      throw new ApiError(errorDetail, errorCode, response.status);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  /**
   * Send a message to the AI assistant
   */
  async sendMessage(
    message: string,
    conversationId?: number | null
  ): Promise<ChatResponse> {
    const request: ChatRequest = {
      message,
      conversation_id: conversationId,
    };

    return this.fetch<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  /**
   * Get list of user's conversations
   */
  async getConversations(limit: number = 20): Promise<ConversationSummary[]> {
    return this.fetch<ConversationSummary[]>(
      `/api/conversations?limit=${limit}`
    );
  }

  /**
   * Get a specific conversation with messages
   */
  async getConversation(
    conversationId: number,
    messageLimit: number = 50
  ): Promise<Conversation> {
    return this.fetch<Conversation>(
      `/api/conversations/${conversationId}?message_limit=${messageLimit}`
    );
  }

  /**
   * Delete a conversation
   */
  async deleteConversation(conversationId: number): Promise<void> {
    return this.fetch<void>(`/api/conversations/${conversationId}`, {
      method: "DELETE",
    });
  }
}

export const chatApi = new ChatApiClient();
