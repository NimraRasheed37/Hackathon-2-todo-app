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

// Phase 5: Priority Types
export type TaskPriority = "critical" | "high" | "medium" | "low" | "none";

// Phase 5: Recurrence Types
export type RecurrenceFrequency = "daily" | "weekly" | "monthly" | "yearly" | "custom";

export interface RecurrencePattern {
  frequency: RecurrenceFrequency;
  interval: number;
  daysOfWeek?: number[];
  dayOfMonth?: number;
  endDate?: string;
  maxOccurrences?: number;
}

// Phase 5: Tag Types
export interface Tag {
  id: string;
  user_id: string;
  name: string;
  color: string;
  icon?: string;
  usage_count: number;
  created_at: string;
}

// Phase 5: Reminder Types
export type ReminderType = "relative" | "absolute";
export type ReminderChannel = "in_app" | "email" | "push";
export type ReminderStatus = "pending" | "sent" | "cancelled";

export interface TaskReminder {
  id: string;
  task_id: string;
  user_id: string;
  reminder_type: ReminderType;
  relative_minutes?: number;
  absolute_time?: string;
  channels: ReminderChannel[];
  status: ReminderStatus;
  scheduled_at: string;
  sent_at?: string;
  created_at: string;
}

// Phase 5: Notification Types
export interface Notification {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message?: string;
  reference_type?: string;
  reference_id?: string;
  read: boolean;
  created_at: string;
}

/**
 * Task entity from backend API
 */
export interface Task {
  id: number;
  user_id: string; // UUID
  title: string;
  description: string | null;
  completed: boolean;
  // Phase 5: New fields
  priority: TaskPriority;
  due_date: string | null;
  recurrence_pattern: RecurrencePattern | null;
  parent_task_id: string | null;
  occurrence_number: number;
  tags: Tag[];
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}

/**
 * Request payload for creating a task
 */
export interface TaskCreate {
  title: string; // 1-200 characters, required
  description?: string; // 0-1000 characters, optional
  // Phase 5: New fields
  priority?: TaskPriority;
  due_date?: string;
  recurrence_pattern?: RecurrencePattern;
  tag_ids?: string[];
}

/**
 * Request payload for updating a task
 */
export interface TaskUpdate {
  title?: string; // 1-200 characters
  description?: string; // 0-1000 characters
  // Phase 5: New fields
  priority?: TaskPriority;
  due_date?: string | null;
  recurrence_pattern?: RecurrencePattern | null;
  tag_ids?: string[];
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
export type SortOption = "created" | "title" | "updated" | "priority" | "due_date";

// Phase 5: Search Types
export interface SearchQuery {
  text?: string;
  status?: FilterStatus[];
  priority?: TaskPriority[];
  tags?: string[];
  dueDateFrom?: string;
  dueDateTo?: string;
  hasRecurrence?: boolean;
  sortBy?: "relevance" | "dueDate" | "priority" | "createdAt";
  sortOrder?: "asc" | "desc";
  limit?: number;
  offset?: number;
}

export interface SearchResults {
  results: Task[];
  total: number;
  hasMore: boolean;
}

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

// Chat Types (Phase 3)

/**
 * Chat message entity
 */
export interface ChatMessage {
  id: number;
  role: "user" | "assistant" | "tool";
  content: string;
  tool_calls?: {
    calls?: Array<{
      name: string;
      arguments: Record<string, unknown>;
      result: Record<string, unknown>;
    }>;
  };
  created_at: string;
}

/**
 * Conversation summary for list display
 */
export interface ConversationSummary {
  id: number;
  title: string;
  updated_at: string;
  message_count: number;
}

/**
 * Full conversation with messages
 */
export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages: ChatMessage[];
}

/**
 * Tool call result from AI
 */
export interface ToolCallResult {
  name: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
}

/**
 * Chat API request
 */
export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

/**
 * Chat API response
 */
export interface ChatResponse {
  message: string;
  conversation_id: number;
  tool_calls?: ToolCallResult[] | null;
}
