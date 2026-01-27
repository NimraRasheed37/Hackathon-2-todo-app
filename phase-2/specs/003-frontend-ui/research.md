# Research: Frontend UI & Task Management

**Feature**: 003-frontend-ui
**Date**: 2026-01-26

## Research Tasks

### R1: Better Auth Integration with Next.js 14

**Question**: How to configure Better Auth with Next.js App Router for JWT-based authentication?

**Decision**: Use Better Auth's Next.js integration with server-side session handling

**Rationale**:
- Better Auth provides first-class Next.js support
- Server actions for auth operations (login, register, logout)
- Client-side hooks for session access
- Automatic JWT token management

**Implementation**:
```typescript
// lib/auth.ts - Server configuration
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({ connectionString: process.env.DATABASE_URL }),
  emailAndPassword: { enabled: true },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    cookieCache: { enabled: true, maxAge: 60 * 5 }, // 5 minutes
  },
});

// lib/auth-client.ts - Client configuration
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

**Alternatives Considered**:
- NextAuth.js: More complex, overkill for our needs
- Custom JWT handling: More work, less secure
- Auth0/Clerk: External service, adds latency

---

### R2: SWR for Data Fetching with Optimistic Updates

**Question**: How to implement optimistic updates with SWR for instant UI feedback?

**Decision**: Use SWR's mutate function with optimistic data

**Rationale**:
- SWR provides built-in optimistic update support
- Automatic revalidation on error
- Simple API with React hooks

**Implementation**:
```typescript
// Optimistic create
const createTask = async (task: TaskCreate) => {
  const optimisticTask = { ...task, id: Date.now(), completed: false };

  await mutate(
    `/api/${userId}/tasks`,
    async (current: Task[]) => {
      const newTask = await api.createTask(userId, task);
      return [...current, newTask];
    },
    {
      optimisticData: (current: Task[]) => [...current, optimisticTask],
      rollbackOnError: true,
      revalidate: false,
    }
  );
};

// Optimistic toggle
const toggleComplete = async (taskId: number) => {
  await mutate(
    `/api/${userId}/tasks`,
    async (current: Task[]) => {
      await api.toggleComplete(userId, taskId);
      return current.map(t =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      );
    },
    {
      optimisticData: (current: Task[]) =>
        current.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t),
      rollbackOnError: true,
    }
  );
};
```

**Alternatives Considered**:
- TanStack Query: More features but heavier
- Plain fetch: No caching or optimistic updates
- Redux: Overkill for this use case

---

### R3: Better Auth JWT Token for API Requests

**Question**: How to pass JWT token from Better Auth to our FastAPI backend?

**Decision**: Extract session token and include in Authorization header

**Rationale**:
- Better Auth stores session info server-side
- We need to extract JWT for API calls
- Backend expects `Authorization: Bearer <token>` header

**Implementation**:
```typescript
// lib/api.ts
import { authClient } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const session = await authClient.getSession();

  if (!session?.session?.token) {
    throw new Error("Not authenticated");
  }

  return fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      "Content-Type": "application/json",
      "Authorization": `Bearer ${session.session.token}`,
    },
  });
}

export const api = {
  getTasks: (userId: string) => fetchWithAuth(`/api/${userId}/tasks`).then(r => r.json()),
  createTask: (userId: string, data: TaskCreate) =>
    fetchWithAuth(`/api/${userId}/tasks`, { method: "POST", body: JSON.stringify(data) }).then(r => r.json()),
  // ... other methods
};
```

**Note**: Better Auth and backend JWT_SECRET must match for token verification.

---

### R4: Radix UI for Accessible Components

**Question**: Which Radix UI components needed and how to style with Tailwind?

**Decision**: Use Dialog, DropdownMenu, and Checkbox from Radix UI

**Rationale**:
- All components are fully accessible
- Unstyled primitives work perfectly with Tailwind
- Handles keyboard navigation and focus management

**Components Needed**:
| Radix Component | Use Case |
|-----------------|----------|
| Dialog | Add/Edit task modals |
| AlertDialog | Delete confirmation |
| DropdownMenu | Sort dropdown |
| Checkbox | Task completion toggle |

**Implementation**:
```typescript
// Example: Dialog with Tailwind
import * as Dialog from "@radix-ui/react-dialog";

export function TaskDialog({ children, trigger }: Props) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 shadow-lg w-full max-w-md">
          <Dialog.Title className="text-lg font-semibold">
            Add New Task
          </Dialog.Title>
          {children}
          <Dialog.Close asChild>
            <button className="absolute top-4 right-4">×</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

### R5: Toast Notifications with Sonner

**Question**: How to implement toast notifications for success/error feedback?

**Decision**: Use Sonner for toast notifications

**Rationale**:
- Lightweight and performant
- Beautiful default styling
- Easy API with promise support
- Accessible announcements

**Implementation**:
```typescript
// app/layout.tsx
import { Toaster } from "sonner";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster position="top-right" richColors />
      </body>
    </html>
  );
}

// Usage in components
import { toast } from "sonner";

// Success
toast.success("Task created successfully!");

// Error with action
toast.error("Failed to delete task", {
  action: { label: "Retry", onClick: () => deleteTask(taskId) },
});

// Promise-based
toast.promise(createTask(data), {
  loading: "Creating task...",
  success: "Task created!",
  error: "Failed to create task",
});
```

---

### R6: Responsive Design Patterns

**Question**: How to implement responsive layouts for mobile/tablet/desktop?

**Decision**: Use Tailwind's responsive utilities with mobile-first approach

**Rationale**:
- Tailwind's breakpoint system is intuitive
- Mobile-first ensures good mobile experience
- Grid and flex utilities handle complex layouts

**Breakpoints**:
| Breakpoint | Width | Layout |
|------------|-------|--------|
| Default | < 768px | Single column, stacked |
| md | >= 768px | Two columns |
| lg | >= 1024px | Two columns, larger spacing |
| xl | >= 1280px | Three columns (optional) |

**Implementation**:
```typescript
// TaskList responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4">
  {tasks.map(task => <TaskCard key={task.id} task={task} />)}
</div>

// Mobile-friendly touch targets
<button className="p-3 min-w-[44px] min-h-[44px]">
  <Icon className="w-5 h-5" />
</button>

// Hide on mobile, show on desktop
<div className="hidden md:flex gap-2">
  <EditButton />
  <DeleteButton />
</div>

// Show on mobile only
<div className="flex md:hidden">
  <MobileMenu />
</div>
```

---

## Summary of Decisions

| Area | Decision | Confidence |
|------|----------|------------|
| Auth | Better Auth with Next.js | High |
| Data Fetching | SWR with optimistic updates | High |
| API Integration | Fetch with Bearer token | High |
| UI Components | Radix UI primitives | High |
| Notifications | Sonner toasts | High |
| Styling | Tailwind CSS mobile-first | High |
| Responsive | Grid-based with breakpoints | High |

All NEEDS CLARIFICATION items resolved.
