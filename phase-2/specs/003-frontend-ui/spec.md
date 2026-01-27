# Feature Specification: Frontend UI & Task Management

**Feature Branch**: `003-frontend-ui`
**Created**: 2026-01-26
**Status**: Draft
**Input**: Phase 2 - Module 3: Frontend UI & Task Management - Build a beautiful, modern, responsive web interface for managing tasks with excellent UX, smooth interactions, and a polished design.

---

## Module Overview

This module creates a beautiful, modern, responsive web interface for managing tasks. It focuses on excellent UX, smooth interactions, and a polished design that makes task management delightful.

**Core Value Proposition**: Provide users with an intuitive, visually appealing interface to manage their tasks securely, with seamless authentication and delightful interactions.

---

## User Stories

### US-M3-001: View Task Dashboard

**As a** user
**I want** to see all my tasks in a clean, organized dashboard
**So that** I can quickly understand my workload

**Acceptance Criteria:**
- Tasks are displayed in a card-based layout
- Pending tasks are visually distinct from completed tasks
- Task count is displayed (e.g., "5 pending, 3 completed")
- Empty state is shown when no tasks exist
- Dashboard is responsive (mobile, tablet, desktop)

---

### US-M3-002: Create New Task

**As a** user
**I want** to quickly add a new task
**So that** I can capture ideas without interrupting my flow

**Acceptance Criteria:**
- "Add Task" button is prominently displayed
- Clicking opens a modal/inline form
- Form has fields for title (required) and description (optional)
- Title has character counter (max 200)
- Submit button is disabled until title is filled
- Task appears immediately after creation (optimistic update)
- Success feedback is shown briefly
- Form clears after successful submission

---

### US-M3-003: Edit Existing Task

**As a** user
**I want** to edit a task's details
**So that** I can update information as things change

**Acceptance Criteria:**
- Each task has an "Edit" button (visible on hover)
- Clicking opens edit form with pre-filled data
- Can update title and/or description
- Changes save on submit
- Updated task reflects changes immediately
- Can cancel editing without saving

---

### US-M3-004: Mark Task Complete/Incomplete

**As a** user
**I want** to toggle task completion with a single click
**So that** I can track my progress easily

**Acceptance Criteria:**
- Each task has a checkbox for completion status
- Clicking checkbox toggles between pending/completed
- Completed tasks show visual distinction (strikethrough, dimmed)
- Change is reflected immediately
- Animation plays on status change (smooth transition)

---

### US-M3-005: Delete Task

**As a** user
**I want** to delete tasks I no longer need
**So that** my list stays focused and relevant

**Acceptance Criteria:**
- Each task has a "Delete" button (visible on hover)
- Clicking shows confirmation dialog
- Confirmation dialog explains action is permanent
- Task is removed immediately after confirmation
- Brief success message is shown
- Can cancel deletion

---

### US-M3-006: Filter and Sort Tasks

**As a** user
**I want** to filter and sort my tasks
**So that** I can focus on what's important right now

**Acceptance Criteria:**
- Filter buttons: "All", "Pending", "Completed"
- Active filter is visually highlighted
- Sort options: "Newest first", "Oldest first", "A-Z"
- Filters and sorts update view immediately
- Filter/sort state persists during session

---

### US-M3-007: Responsive Design

**As a** user on any device
**I want** the app to work well on mobile, tablet, and desktop
**So that** I can manage tasks from anywhere

**Acceptance Criteria:**
- Mobile (< 768px): Single column, touch-friendly buttons
- Tablet (768px - 1024px): Two columns, adaptive layout
- Desktop (> 1024px): Multi-column, hover interactions
- Text is readable on all screen sizes
- Buttons are easy to tap on mobile (min 44x44px)

---

## Technical Specifications

### Technology Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui (for dialogs and forms)
- **Icons**: Lucide React
- **State Management**: React hooks (useState, useEffect)
- **Data Fetching**: SWR or TanStack Query (for caching and optimistic updates)
- **Authentication**: Better Auth (client-side)
- **Toast Notifications**: Sonner

### Design System

#### Color Palette

```typescript
const colors = {
  // Primary
  primary: {
    50: '#EFF6FF',
    100: '#DBEAFE',
    500: '#3B82F6',  // Main brand color
    600: '#2563EB',
    700: '#1D4ED8',
  },

  // Status colors
  success: '#10B981',  // Green
  warning: '#F59E0B',  // Amber
  error: '#EF4444',    // Red

  // Neutrals
  gray: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    500: '#6B7280',
    700: '#374151',
    900: '#111827',
  },

  // Background
  background: '#FFFFFF',
  backgroundSecondary: '#F9FAFB',
}
```

#### Typography

```typescript
const typography = {
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',

  sizes: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '30px',
    '4xl': '36px',
  },

  weights: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
}
```

#### Spacing (8px grid system)

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px
- **3xl**: 64px

#### Border Radius

- **sm**: 4px
- **md**: 8px
- **lg**: 12px
- **xl**: 16px
- **full**: 9999px (pills/circles)

#### Shadows

```css
.shadow-sm { box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
.shadow-md { box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
.shadow-lg { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); }
```

---

## UI Components

### 1. Task Card Component

```
┌──────────────────────────────────────────────────┐
│ ☐  Buy groceries                           [Edit] │
│    Milk, eggs, bread, fruits                      │
│    Created: 2 hours ago                           │
│                                          [Delete] │
└──────────────────────────────────────────────────┘

// Completed task (dimmed text)
┌──────────────────────────────────────────────────┐
│ ☑  Buy groceries                           [Edit] │
│    Milk, eggs, bread, fruits                      │
│    Completed: 1 hour ago                          │
│                                          [Delete] │
└──────────────────────────────────────────────────┘
```

**Features:**
- Checkbox on the left (large, easy to click)
- Title in bold, strikethrough when completed
- Description in smaller, gray text
- Timestamp showing when created/completed
- Edit and Delete buttons visible on hover (desktop)
- Smooth hover effect (slight elevation)
- Transition animation on completion toggle

### 2. Add Task Button & Form

```
// Primary action button
┌──────────────────────────┐
│   ➕  Add New Task       │
└──────────────────────────┘

// Modal form when clicked
┌────────────────────────────────────┐
│  Add New Task                  [×] │
│                                    │
│  Title *                           │
│  ┌──────────────────────────────┐ │
│  │ Enter task title...           │ │
│  └──────────────────────────────┘ │
│  200/200 characters                │
│                                    │
│  Description                       │
│  ┌──────────────────────────────┐ │
│  │ Add details... (optional)     │ │
│  └──────────────────────────────┘ │
│                                    │
│  [Cancel]           [Create Task] │
└────────────────────────────────────┘
```

### 3. Filter and Sort Controls

```
// Filter buttons
┌────────────────────────────────────┐
│  [All: 8]  [Pending: 5]  [Done: 3] │
└────────────────────────────────────┘

// Sort dropdown
┌────────────────────────┐
│  Sort by: Newest ▾     │
└────────────────────────┘
```

### 4. Empty States

```
// No tasks yet
┌────────────────────────────────────┐
│         📝                         │
│    No tasks yet!                   │
│    Create your first task to       │
│    get started.                    │
│    [➕  Add Your First Task]       │
└────────────────────────────────────┘

// All tasks completed
┌────────────────────────────────────┐
│         ✓                          │
│    All caught up!                  │
│    No pending tasks.               │
└────────────────────────────────────┘
```

### 5. Toast Notifications

```
// Success toast
┌────────────────────────────────┐
│ ✓  Task created successfully!  │
└────────────────────────────────┘

// Error toast
┌────────────────────────────────┐
│ ✗  Failed to delete task       │
│    [Retry]                     │
└────────────────────────────────┘
```

---

## Page Layouts

### Desktop Layout (> 1024px)

```
┌────────────────────────────────────────────────────────────┐
│  🗂️ Todo App                     👤 John Doe    [Logout]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  My Tasks                        [➕  Add New Task]   │ │
│  │  5 pending, 3 completed                               │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  [All: 8]  [Pending: 5]  [Done: 3]                   │ │
│  │                                Sort by: Newest ▾      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌───────────────────────┐  ┌───────────────────────┐    │
│  │  Task Card 1          │  │  Task Card 2          │    │
│  └───────────────────────┘  └───────────────────────┘    │
│                                                            │
│  ┌───────────────────────┐  ┌───────────────────────┐    │
│  │  Task Card 3          │  │  Task Card 4          │    │
│  └───────────────────────┘  └───────────────────────┘    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Mobile Layout (< 768px)

```
┌────────────────────────────┐
│ 🗂️                    ☰   │
│ Todo App                   │
├────────────────────────────┤
│  My Tasks                  │
│  5 pending, 3 completed    │
│                            │
│  [➕  Add New Task]        │
│                            │
│  [All] [Pending] [Done]    │
│                            │
│  ┌──────────────────────┐ │
│  │  Task Card 1         │ │
│  └──────────────────────┘ │
│                            │
│  ┌──────────────────────┐ │
│  │  Task Card 2         │ │
│  └──────────────────────┘ │
│                            │
└────────────────────────────┘
```

---

## Requirements

### Functional Requirements

#### Authentication UI
- **FR-001**: System MUST provide /register page with email, name, password fields
- **FR-002**: System MUST provide /login page with email, password fields
- **FR-003**: System MUST display loading state during authentication requests
- **FR-004**: System MUST display user-friendly error messages for auth failures
- **FR-005**: System MUST redirect authenticated users away from /login and /register
- **FR-006**: System MUST provide logout button on protected pages
- **FR-007**: System MUST clear session and redirect on logout

#### Protected Routes
- **FR-008**: System MUST redirect unauthenticated users to /login for protected routes
- **FR-009**: System MUST show user information (name) on protected pages
- **FR-010**: System MUST include JWT token in all API requests

#### Task Management UI
- **FR-011**: System MUST display list of user's tasks on dashboard
- **FR-012**: System MUST show empty state when user has no tasks
- **FR-013**: System MUST provide "Add Task" button and modal form
- **FR-014**: System MUST provide edit functionality for each task
- **FR-015**: System MUST provide toggle completion functionality
- **FR-016**: System MUST provide delete functionality with confirmation
- **FR-017**: System MUST show loading states during API operations
- **FR-018**: System MUST show success/error feedback via toast notifications
- **FR-019**: System MUST support filtering by status (all/pending/completed)
- **FR-020**: System MUST support sorting (newest/oldest/alphabetical)

#### Optimistic Updates
- **FR-021**: System MUST update UI immediately on task creation
- **FR-022**: System MUST update UI immediately on completion toggle
- **FR-023**: System MUST update UI immediately on task deletion
- **FR-024**: System MUST revert changes and show error on API failure

### Non-Functional Requirements
- **NFR-001**: Pages MUST load in under 3 seconds on 3G connection
- **NFR-002**: UI MUST be responsive (mobile, tablet, desktop)
- **NFR-003**: UI MUST be accessible (WCAG 2.1 AA)
- **NFR-004**: Animations MUST run at 60fps

---

## Implementation Tasks

### Phase 1: Project Setup

- [ ] T001 Create Next.js app with TypeScript: `npx create-next-app@latest`
- [ ] T002 Configure Tailwind CSS
- [ ] T003 Install dependencies (lucide-react, swr, radix-ui, sonner)
- [ ] T004 Set up folder structure: /app, /components, /lib, /types
- [ ] T005 Create environment variables (.env.local)

### Phase 2: Authentication Setup

- [ ] T006 Install and configure Better Auth
- [ ] T007 Create auth configuration (lib/auth.ts)
- [ ] T008 Create /login page with form
- [ ] T009 Create /register page with form
- [ ] T010 Implement protected route middleware
- [ ] T011 Create logout functionality

### Phase 3: API Integration

- [ ] T012 Create API client (lib/api.ts) with typed functions
- [ ] T013 Implement getTasks() with SWR caching
- [ ] T014 Implement createTask() with optimistic update
- [ ] T015 Implement updateTask() with optimistic update
- [ ] T016 Implement deleteTask() with optimistic update
- [ ] T017 Implement toggleComplete() with optimistic update

### Phase 4: UI Components

- [ ] T018 Create TaskCard component
- [ ] T019 Create AddTaskForm component (modal)
- [ ] T020 Create EditTaskForm component
- [ ] T021 Create DeleteConfirmDialog component
- [ ] T022 Create TaskFilters component
- [ ] T023 Create EmptyState component
- [ ] T024 Create LoadingSkeletons component
- [ ] T025 Set up Sonner toast notifications

### Phase 5: Dashboard Page

- [ ] T026 Create /dashboard page layout
- [ ] T027 Implement task list with cards
- [ ] T028 Implement filter and sort controls
- [ ] T029 Implement responsive grid layout
- [ ] T030 Add loading and error states

### Phase 6: Polish & Testing

- [ ] T031 Add smooth transitions and animations
- [ ] T032 Test responsive design (mobile/tablet/desktop)
- [ ] T033 Test keyboard accessibility
- [ ] T034 Test optimistic updates and error recovery
- [ ] T035 Performance optimization (React.memo, lazy loading)

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance
- All interactive elements keyboard accessible
- Proper ARIA labels for screen readers
- Color contrast ratio >= 4.5:1 for text
- Focus indicators visible and clear
- Form labels properly associated
- Error messages announced to screen readers

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate buttons and checkboxes
- Escape to close modals
- Arrow keys for dropdown navigation

---

## Performance Goals

- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Cumulative Layout Shift**: < 0.1
- **Largest Contentful Paint**: < 2.5s

---

## Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "better-auth": "^1.0.0",
    "tailwindcss": "^3.4.0",
    "lucide-react": "^0.300.0",
    "swr": "^2.2.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "sonner": "^1.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "autoprefixer": "^10.0.0",
    "postcss": "^8.0.0"
  }
}
```

---

## Success Criteria

This module is complete when:

- [ ] Dashboard displays all tasks in a beautiful card layout
- [ ] Users can create, edit, delete, and complete tasks
- [ ] Filter and sort controls work correctly
- [ ] UI is fully responsive (mobile, tablet, desktop)
- [ ] All interactions feel smooth with proper animations
- [ ] Loading and error states are handled gracefully
- [ ] Optimistic updates provide instant feedback
- [ ] Design matches specifications (colors, spacing, typography)
- [ ] Accessibility requirements are met (keyboard nav, ARIA labels)
- [ ] Authentication flow works end-to-end (register, login, logout)

---

## Out of Scope

- Server-side rendering of protected content
- Offline support / PWA features
- Real-time updates (WebSocket)
- Drag-and-drop task reordering
- Task categories/labels
- Due dates and reminders
- Dark mode toggle
- Multi-language support
- Task search functionality

---

## Next Steps

After this specification is approved:

1. Run `/sp.plan` to create implementation plan with technical architecture
2. Run `/sp.tasks` to generate executable task list
3. Implement Module 3 following spec-driven development workflow
4. Upon completion, proceed to Module 4 (Integration & Deployment)
