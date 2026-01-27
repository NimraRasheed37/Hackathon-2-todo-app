// User & Auth Types

/**
 * User information from authentication session
 */
export interface User {
  id: string; // UUID
  email: string;
  name: string;
}

/**
 * Session information from Better Auth
 */
export interface Session {
  user: User;
  token: string; // JWT token for API calls
  expiresAt: Date;
}

// Task Types

/**
 * Task entity from backend API
 */
export interface Task {
  id: number;
  user_id: string; // UUID
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}

/**
 * Request payload for creating a task
 */
export interface TaskCreate {
  title: string; // 1-200 characters, required
  description?: string; // 0-1000 characters, optional
}

/**
 * Request payload for updating a task
 */
export interface TaskUpdate {
  title?: string; // 1-200 characters
  description?: string; // 0-1000 characters
}

// API Response Types

/**
 * List of tasks response
 */
export type TaskListResponse = Task[];

/**
 * Single task response (create, update, toggle)
 */
export type TaskResponse = Task;

// Error Types

/**
 * Standard error response from backend
 */
export interface ErrorResponse {
  detail: string;
  error_code: string;
  field?: string;
}

/**
 * Custom API error class
 */
export class ApiError extends Error {
  code: string;
  status: number;

  constructor(message: string, code: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
    this.name = "ApiError";
  }
}

/**
 * Authentication error codes
 */
export type AuthErrorCode =
  | "NOT_AUTHENTICATED"
  | "INVALID_TOKEN"
  | "TOKEN_EXPIRED"
  | "ACCESS_DENIED";

/**
 * Task operation error codes
 */
export type TaskErrorCode =
  | "NOT_FOUND"
  | "VALIDATION_ERROR"
  | "INTERNAL_ERROR";

// Filter & Sort Types

/**
 * Task filter status options
 */
export type FilterStatus = "all" | "pending" | "completed";

/**
 * Task sort options
 */
export type SortOption = "created" | "title" | "updated";

// Component Props Types

/**
 * TaskCard component props
 */
export interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
}

/**
 * TaskForm component props
 */
export interface TaskFormProps {
  mode: "create" | "edit";
  initialData?: Task;
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * TaskFilters component props
 */
export interface TaskFiltersProps {
  currentFilter: FilterStatus;
  currentSort: SortOption;
  taskCounts: {
    all: number;
    pending: number;
    completed: number;
  };
  onFilterChange: (filter: FilterStatus) => void;
  onSortChange: (sort: SortOption) => void;
}

/**
 * DeleteConfirmDialog component props
 */
export interface DeleteConfirmDialogProps {
  isOpen: boolean;
  taskTitle: string;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

// State Types

/**
 * Dashboard page state
 */
export interface DashboardState {
  filter: FilterStatus;
  sort: SortOption;
  isCreateModalOpen: boolean;
  editingTask: Task | null;
  deletingTaskId: number | null;
}

/**
 * Auth state
 */
export interface AuthState {
  isLoading: boolean;
  isAuthenticated: boolean;
  user: User | null;
  error: string | null;
}
