# Implementation Plan: Frontend UI & Task Management

**Branch**: `003-frontend-ui` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `phase-2/specs/003-frontend-ui/spec.md`

## Summary

Build a Next.js 14+ frontend with Better Auth authentication, responsive task management UI, and seamless integration with the FastAPI backend. The application will feature a modern card-based design, optimistic updates for instant feedback, and full accessibility compliance (WCAG 2.1 AA).

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Next.js 14+, React 18+, Better Auth, SWR, Tailwind CSS, Radix UI, Lucide React, Sonner
**Storage**: N/A (frontend only, data via API)
**Testing**: Manual testing for MVP (Playwright recommended for future)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (frontend)
**Performance Goals**: FCP < 1.5s, TTI < 3s, LCP < 2.5s, CLS < 0.1, 60fps animations
**Constraints**: Must work offline-gracefully (show cached data), < 200KB JS bundle (gzipped)
**Scale/Scope**: Single user per session, ~100 tasks per user maximum

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Simplicity | PASS | Using established patterns (Next.js App Router, SWR caching) |
| Security | PASS | JWT tokens handled by Better Auth, HTTPS required |
| Accessibility | PASS | WCAG 2.1 AA compliance required |
| Testing | DEFER | Manual testing for MVP, automated tests recommended for production |

## Project Structure

### Documentation (this feature)

```text
phase-2/specs/003-frontend-ui/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── README.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output
```

### Source Code

```text
phase-2/frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── layout.tsx
│   │   ├── (protected)/
│   │   │   ├── dashboard/page.tsx
│   │   │   └── layout.tsx
│   │   ├── api/
│   │   │   └── auth/[...all]/route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── LogoutButton.tsx
│   │   ├── tasks/
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskFilters.tsx
│   │   │   └── DeleteConfirmDialog.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Modal.tsx
│   │       ├── EmptyState.tsx
│   │       └── Skeleton.tsx
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── auth-client.ts
│   │   ├── api.ts
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
├── .env.example
├── .env.local
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

**Structure Decision**: Single frontend application using Next.js App Router with route groups for auth and protected pages. Components organized by domain (auth, tasks, ui).

## Architecture Decisions

### AD-001: Authentication with Better Auth

**Decision**: Use Better Auth library for client-side authentication
**Rationale**:
- Integrates seamlessly with Next.js
- Handles JWT token management automatically
- Provides session persistence
- Works with our existing backend JWT verification

### AD-002: Data Fetching with SWR

**Decision**: Use SWR for data fetching and caching
**Rationale**:
- Automatic caching and revalidation
- Built-in optimistic updates
- Works well with React hooks
- Lightweight compared to alternatives

### AD-003: Styling with Tailwind CSS

**Decision**: Use Tailwind CSS for styling
**Rationale**:
- Industry standard for Next.js applications
- Utility-first approach enables rapid development
- Built-in responsive design utilities
- Excellent performance (unused styles purged)

### AD-004: UI Components with Radix UI

**Decision**: Use Radix UI for dialogs, dropdowns, and other complex components
**Rationale**:
- Fully accessible out of the box
- Unstyled (works with Tailwind)
- Handles keyboard navigation and focus management
- Production-tested primitives

## Integration Points

### Backend API (Module 1 & 2)

| Endpoint | Method | Auth | Frontend Usage |
|----------|--------|------|----------------|
| GET /api/{user_id}/tasks | GET | Yes | TaskList fetch |
| POST /api/{user_id}/tasks | POST | Yes | TaskForm create |
| PUT /api/{user_id}/tasks/{id} | PUT | Yes | TaskForm edit |
| PATCH /api/{user_id}/tasks/{id}/complete | PATCH | Yes | TaskCard toggle |
| DELETE /api/{user_id}/tasks/{id} | DELETE | Yes | DeleteConfirmDialog |

### Environment Variables

```bash
# Better Auth
BETTER_AUTH_SECRET=<must-match-backend-JWT_SECRET>
BETTER_AUTH_URL=http://localhost:3000

# Database (Better Auth server-side)
DATABASE_URL=<neon-connection-string>

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Better Auth version incompatibility | High | Low | Pin specific version, test thoroughly |
| CORS issues with backend | Medium | Medium | Configure backend CORS, test early |
| JWT secret mismatch | High | Low | Document clearly, validate in dev |
| Slow initial load | Medium | Low | Use Next.js optimizations, lazy loading |

## Dependencies

### NPM Packages

```json
{
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "better-auth": "^1.2.0",
    "swr": "^2.2.0",
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-dialog": "^1.1.0",
    "@radix-ui/react-dropdown-menu": "^2.1.0",
    "@radix-ui/react-checkbox": "^1.1.0",
    "lucide-react": "^0.400.0",
    "sonner": "^1.5.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0"
  }
}
```

## Complexity Tracking

> No violations requiring justification.

| Item | Complexity | Justification |
|------|------------|---------------|
| Better Auth setup | Medium | Standard auth pattern, well-documented |
| SWR optimistic updates | Medium | SWR provides built-in support |
| Responsive design | Low | Tailwind utilities handle breakpoints |
| Accessibility | Medium | Radix UI provides accessible primitives |
