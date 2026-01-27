# Data Model: Frontend UI & Task Management

**Feature**: 003-frontend-ui
**Date**: 2026-01-26

## Overview

This document defines the TypeScript types and interfaces for the frontend application. These types mirror the backend API responses and enable type-safe development.

---

## Core Types

### User

```typescript
// types/index.ts

/**
 * User information from authentication session
 */
export interface User {
  id: string;        // UUID
  email: string;
  name: string;
}

/**
 * Session information from Better Auth
 */
export interface Session {
  user: User;
  token: string;     // JWT token for API calls
  expiresAt: Date;
}
```

### Task

```typescript
// types/index.ts

/**
 * Task entity from backend API
 */
export interface Task {
  id: number;
  user_id: string;   // UUID
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;  // ISO datetime
  updated_at: string;  // ISO datetime
}

/**
 * Request payload for creating a task
 */
export interface TaskCreate {
  title: string;         // 1-200 characters, required
  description?: string;  // 0-1000 characters, optional
}

/**
 * Request payload for updating a task
 */
export interface TaskUpdate {
  title?: string;        // 1-200 characters
  description?: string;  // 0-1000 characters
}
```

---

## API Response Types

### Success Responses

```typescript
// types/index.ts

/**
 * List of tasks response
 */
export type TaskListResponse = Task[];

/**
 * Single task response (create, update, toggle)
 */
export type TaskResponse = Task;
```

### Error Responses

```typescript
// types/index.ts

/**
 * Standard error response from backend
 */
export interface ErrorResponse {
  detail: string;
  error_code: string;
  field?: string;
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
```

---

## Component Props Types

### TaskCard

```typescript
// components/tasks/TaskCard.tsx

export interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
}
```

### TaskForm

```typescript
// components/tasks/TaskForm.tsx

export interface TaskFormProps {
  mode: "create" | "edit";
  initialData?: Task;
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}
```

### TaskFilters

```typescript
// components/tasks/TaskFilters.tsx

export type FilterStatus = "all" | "pending" | "completed";
export type SortOption = "created" | "title" | "updated";

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
```

### DeleteConfirmDialog

```typescript
// components/tasks/DeleteConfirmDialog.tsx

export interface DeleteConfirmDialogProps {
  isOpen: boolean;
  taskTitle: string;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}
```

---

## State Types

### Dashboard State

```typescript
// app/(protected)/dashboard/page.tsx

export interface DashboardState {
  filter: FilterStatus;
  sort: SortOption;
  isCreateModalOpen: boolean;
  editingTask: Task | null;
  deletingTaskId: number | null;
}
```

### Auth State

```typescript
// lib/auth-client.ts

export interface AuthState {
  isLoading: boolean;
  isAuthenticated: boolean;
  user: User | null;
  error: string | null;
}
```

---

## Validation Rules

### Task Title
- Required
- Minimum: 1 character (after trimming whitespace)
- Maximum: 200 characters
- Trimmed before submission

### Task Description
- Optional
- Maximum: 1000 characters
- Empty string treated as null

### Email (Registration/Login)
- Required
- Must be valid email format
- Case-insensitive comparison

### Password (Registration)
- Required
- Minimum: 8 characters

---

## State Transitions

### Task Lifecycle

```
┌─────────────┐
│   Create    │
│   (Modal)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│   Pending   │◄───►│  Completed  │
│             │     │             │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│    Edit     │     │    Edit     │
│   (Modal)   │     │   (Modal)   │
└─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────┐
│            Delete               │
│      (Confirmation Dialog)      │
└─────────────────────────────────┘
```

### Authentication Flow

```
┌─────────────┐
│  Anonymous  │
└──────┬──────┘
       │
       ├───────────────┬───────────────┐
       ▼               ▼               │
┌─────────────┐ ┌─────────────┐        │
│   Login     │ │  Register   │        │
│   Page      │ │   Page      │        │
└──────┬──────┘ └──────┬──────┘        │
       │               │               │
       ▼               ▼               │
┌─────────────────────────────────────┐│
│         Authenticated               ││
│         (Dashboard)                 ││
└──────────────────┬──────────────────┘│
                   │                    │
                   ▼                    │
            ┌─────────────┐            │
            │   Logout    │────────────┘
            └─────────────┘
```

---

## Type Exports

```typescript
// types/index.ts

export type {
  // User & Auth
  User,
  Session,
  AuthState,

  // Task
  Task,
  TaskCreate,
  TaskUpdate,
  TaskListResponse,
  TaskResponse,

  // Errors
  ErrorResponse,
  AuthErrorCode,
  TaskErrorCode,

  // Components
  TaskCardProps,
  TaskFormProps,
  TaskFiltersProps,
  DeleteConfirmDialogProps,

  // State
  DashboardState,
  FilterStatus,
  SortOption,
};
```
