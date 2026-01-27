# Requirements Checklist: Frontend UI & Task Management

## Pre-Implementation Checklist

### Dependencies Ready
- [x] Module 1 (Backend API) complete
- [x] Module 2 (Authentication) complete
- [x] Backend server accessible at localhost:8000
- [ ] Neon database running with users/tasks tables

### Environment Ready
- [ ] Node.js 18+ installed
- [ ] npm or pnpm available
- [ ] Git repository initialized

---

## Functional Requirements Checklist

### Authentication UI (FR-001 to FR-007)
- [ ] FR-001: /register page with email, name, password fields
- [ ] FR-002: /login page with email, password fields
- [ ] FR-003: Loading state during authentication
- [ ] FR-004: User-friendly error messages
- [ ] FR-005: Redirect authenticated users from auth pages
- [ ] FR-006: Logout button on protected pages
- [ ] FR-007: Session clear and redirect on logout

### Protected Routes (FR-008 to FR-010)
- [ ] FR-008: Redirect unauthenticated users to /login
- [ ] FR-009: Show user info (name) on protected pages
- [ ] FR-010: JWT token included in API requests

### Task Management UI (FR-011 to FR-020)
- [ ] FR-011: Display task list on dashboard
- [ ] FR-012: Empty state when no tasks
- [ ] FR-013: Add Task button and modal form
- [ ] FR-014: Edit functionality per task
- [ ] FR-015: Toggle completion functionality
- [ ] FR-016: Delete with confirmation dialog
- [ ] FR-017: Loading states during API operations
- [ ] FR-018: Toast notifications for success/error
- [ ] FR-019: Filter by status (all/pending/completed)
- [ ] FR-020: Sort by (newest/oldest/alphabetical)

### Optimistic Updates (FR-021 to FR-024)
- [ ] FR-021: Immediate UI update on create
- [ ] FR-022: Immediate UI update on toggle
- [ ] FR-023: Immediate UI update on delete
- [ ] FR-024: Revert and show error on API failure

---

## Non-Functional Requirements Checklist

- [ ] NFR-001: Page load < 3s on 3G
- [ ] NFR-002: Responsive design (mobile/tablet/desktop)
- [ ] NFR-003: WCAG 2.1 AA accessibility
- [ ] NFR-004: 60fps animations

---

## User Story Acceptance

### US-M3-001: View Task Dashboard
- [ ] Card-based layout
- [ ] Visual distinction pending vs completed
- [ ] Task count displayed
- [ ] Empty state shown
- [ ] Responsive design

### US-M3-002: Create New Task
- [ ] Add Task button prominent
- [ ] Modal form opens
- [ ] Title required, description optional
- [ ] Character counter (max 200)
- [ ] Disabled submit until valid
- [ ] Optimistic update
- [ ] Success feedback
- [ ] Form clears after success

### US-M3-003: Edit Existing Task
- [ ] Edit button on hover
- [ ] Pre-filled form
- [ ] Save changes
- [ ] Cancel without saving

### US-M3-004: Mark Complete/Incomplete
- [ ] Checkbox per task
- [ ] Toggle functionality
- [ ] Visual distinction (strikethrough, dimmed)
- [ ] Immediate reflection
- [ ] Smooth animation

### US-M3-005: Delete Task
- [ ] Delete button on hover
- [ ] Confirmation dialog
- [ ] Permanent action explained
- [ ] Immediate removal
- [ ] Success message
- [ ] Cancel option

### US-M3-006: Filter and Sort
- [ ] Filter buttons with counts
- [ ] Active filter highlighted
- [ ] Sort dropdown
- [ ] Immediate view update
- [ ] State persists in session

### US-M3-007: Responsive Design
- [ ] Mobile (< 768px): Single column
- [ ] Tablet (768-1024px): Two columns
- [ ] Desktop (> 1024px): Multi-column
- [ ] Readable text all sizes
- [ ] Touch-friendly buttons (44x44px min)

---

## Component Checklist

- [ ] TaskCard component
- [ ] AddTaskForm component (modal)
- [ ] EditTaskForm component
- [ ] DeleteConfirmDialog component
- [ ] TaskFilters component
- [ ] EmptyState component
- [ ] LoadingSkeletons component
- [ ] Toast notifications (Sonner)

---

## Accessibility Checklist

- [ ] All elements keyboard accessible
- [ ] ARIA labels present
- [ ] Color contrast >= 4.5:1
- [ ] Focus indicators visible
- [ ] Form labels associated
- [ ] Errors announced to screen readers
- [ ] Tab navigation works
- [ ] Escape closes modals

---

## Performance Checklist

- [ ] FCP < 1.5s
- [ ] TTI < 3s
- [ ] CLS < 0.1
- [ ] LCP < 2.5s
- [ ] React.memo for TaskCard
- [ ] Lazy load modals
