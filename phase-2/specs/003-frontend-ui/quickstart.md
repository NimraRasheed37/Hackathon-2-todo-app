# Quickstart: Frontend UI & Task Management

## Prerequisites

- Node.js 18+ installed
- Backend API running (Module 1 & 2) at http://localhost:8000
- Neon PostgreSQL database configured
- Git installed

## Setup Steps

### 1. Create Next.js Application

```bash
cd phase-2
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd frontend
```

### 2. Install Dependencies

```bash
npm install better-auth swr @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-checkbox @radix-ui/react-alert-dialog lucide-react sonner clsx tailwind-merge
```

### 3. Configure Environment Variables

Create `.env.local`:

```bash
# Better Auth
BETTER_AUTH_SECRET=OtrWxSoS9P_eMnA5hUzek6kVDH3c93BL5Yw0Ry2MBfQ
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth server-side)
DATABASE_URL=postgresql://neondb_owner:npg_xxxxx@ep-xxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Important**: `BETTER_AUTH_SECRET` must match `JWT_SECRET` in backend `.env`

### 4. Configure Better Auth

Create `src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },
});
```

Create `src/lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### 5. Create Auth API Route

Create `src/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

### 6. Add Toaster to Layout

Update `src/app/layout.tsx`:

```typescript
import { Toaster } from "sonner";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster position="top-right" richColors />
      </body>
    </html>
  );
}
```

### 7. Start Development Server

```bash
npm run dev
```

Application runs at http://localhost:3000

---

## Validation Checklist

### Environment

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Backend running at http://localhost:8000
- [ ] `.env.local` file created with all variables
- [ ] `BETTER_AUTH_SECRET` matches backend `JWT_SECRET`

### Dependencies

- [ ] All npm packages installed without errors
- [ ] `npm run dev` starts without errors
- [ ] No TypeScript errors in console

### Authentication

- [ ] `/register` page renders
- [ ] `/login` page renders
- [ ] Registration creates user in database
- [ ] Login redirects to dashboard
- [ ] Logout clears session
- [ ] Protected routes redirect to login

### Task Operations

- [ ] Dashboard shows task list
- [ ] Create task modal works
- [ ] Edit task modal pre-fills data
- [ ] Toggle completion updates immediately
- [ ] Delete shows confirmation dialog
- [ ] Filters (All/Pending/Completed) work
- [ ] Sort dropdown works

### UI/UX

- [ ] Responsive on mobile (< 768px)
- [ ] Responsive on tablet (768px - 1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] Loading states shown
- [ ] Error toasts appear
- [ ] Success toasts appear

### Accessibility

- [ ] All buttons keyboard accessible
- [ ] Modals close with Escape
- [ ] Focus visible on interactive elements
- [ ] Color contrast adequate

---

## Common Issues

### CORS Error

If you see CORS errors, verify backend `CORS_ORIGINS` includes `http://localhost:3000`.

### JWT Mismatch

If login works but API calls fail with 401:
1. Check `BETTER_AUTH_SECRET` matches `JWT_SECRET`
2. Verify token is being sent in Authorization header

### Database Connection

If Better Auth fails to connect:
1. Verify `DATABASE_URL` is correct
2. Check Neon dashboard for connection status
3. Ensure SSL mode is correct

### Module Not Found

If imports fail:
1. Run `npm install` again
2. Restart dev server
3. Check `tsconfig.json` paths

---

## Next Steps

After quickstart validation:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement each task following the spec
3. Test each component as built
4. Run full E2E testing before deployment
