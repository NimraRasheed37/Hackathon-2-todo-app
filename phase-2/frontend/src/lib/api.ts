import { Task, TaskCreate, TaskUpdate, ApiError } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async fetch<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
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

  // Health check
  async healthCheck(): Promise<{ status: string; database: string }> {
    return this.fetch("/");
  }

  // Task operations
  async getTasks(
    userId: string,
    status?: string,
    sort?: string
  ): Promise<Task[]> {
    const params = new URLSearchParams();
    if (status && status !== "all") params.set("status", status);
    if (sort) params.set("sort", sort);
    const query = params.toString() ? `?${params}` : "";
    return this.fetch<Task[]>(`/api/${userId}/tasks${query}`);
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdate
  ): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    return this.fetch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.fetch<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }
}

export const api = new ApiClient();
