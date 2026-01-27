# Feature Specification: Authentication & User Management

**Feature Branch**: `002-auth-user-management`
**Created**: 2026-01-25
**Status**: Draft
**Input**: Phase 2 - Module 2: Authentication & User Management - Implement user authentication using Better Auth, secure API endpoints with JWT tokens, and ensure users can only access their own task data.

## Module Overview

This module implements user authentication for the Todo application, enabling secure user registration, login, and session management. The backend API endpoints from Module 1 will be protected with JWT token verification, and data isolation will be enforced to ensure users can only access their own tasks.

**Core Value Proposition**: Enable secure, private task management where each user has exclusive access to their own data through industry-standard authentication practices.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

As a new user, I want to sign up with email and password so that I can create my own account and manage my tasks.

**Why this priority**: Without user accounts, there is no way to identify users or protect their data. Registration is the entry point to the entire application.

**Independent Test**: Can be fully tested by submitting registration form with various inputs and verifying account creation in database and automatic login after success.

**Acceptance Scenarios**:

1. **Given** a visitor on the registration page, **When** they submit valid email, name, and password (8+ characters), **Then** a new user account is created and they are automatically logged in
2. **Given** a visitor attempting to register, **When** they submit an email that already exists, **Then** they see a clear error message "Email already exists"
3. **Given** a visitor attempting to register, **When** they submit a password shorter than 8 characters, **Then** they see a validation error indicating minimum password length
4. **Given** a visitor attempting to register, **When** they submit an invalid email format, **Then** they see a validation error for email format
5. **Given** a successful registration, **When** the account is created, **Then** the user receives a JWT token and is redirected to the dashboard

---

### User Story 2 - User Login (Priority: P1)

As a registered user, I want to sign in with my credentials so that I can access my tasks.

**Why this priority**: Login is essential for returning users to access their data. Without it, users would need to re-register each time.

**Independent Test**: Can be fully tested by submitting login form with valid/invalid credentials and verifying token issuance and error handling.

**Acceptance Scenarios**:

1. **Given** a registered user on the login page, **When** they submit correct email and password, **Then** they receive a JWT token and are redirected to the dashboard
2. **Given** a user attempting to login, **When** they submit an incorrect password, **Then** they see a clear error message "Invalid credentials"
3. **Given** a user attempting to login, **When** they submit a non-existent email, **Then** they see a clear error message "Invalid credentials" (same message for security)
4. **Given** a successful login, **When** the token is issued, **Then** it contains user ID and has a 7-day expiration

---

### User Story 3 - Protected API Access (Priority: P1)

As a backend developer, I want all API endpoints to require authentication so that unauthorized users cannot access or modify task data.

**Why this priority**: API security is fundamental to data protection. Without it, anyone could access any user's tasks.

**Independent Test**: Can be fully tested by sending API requests with and without valid tokens and verifying appropriate responses (401/403).

**Acceptance Scenarios**:

1. **Given** a valid JWT token, **When** accessing any `/api/{user_id}/tasks/*` endpoint, **Then** the request is processed normally
2. **Given** no token provided, **When** accessing any protected endpoint, **Then** the system returns 401 Unauthorized
3. **Given** an expired token, **When** accessing any protected endpoint, **Then** the system returns 401 Unauthorized with message "Token has expired"
4. **Given** an invalid/malformed token, **When** accessing any protected endpoint, **Then** the system returns 401 Unauthorized with message "Invalid token"
5. **Given** a valid token, **When** the Authorization header format is correct (Bearer <token>), **Then** the token is extracted and verified

---

### User Story 4 - User Authorization (Priority: P1)

As a user, I want to only see and modify my own tasks so that my data remains private.

**Why this priority**: Data isolation is critical for privacy and security. Users must never see or modify other users' data.

**Independent Test**: Can be fully tested by having two users and attempting cross-user access via API calls, verifying 403 responses.

**Acceptance Scenarios**:

1. **Given** a user with valid token, **When** they request their own tasks (user_id matches token), **Then** they receive their tasks
2. **Given** a user with valid token, **When** they attempt to access another user's tasks, **Then** they receive 403 Forbidden
3. **Given** a user with valid token, **When** they attempt to create a task for another user_id, **Then** they receive 403 Forbidden
4. **Given** a user with valid token, **When** they attempt to update/delete another user's task, **Then** they receive 403 Forbidden

---

### User Story 5 - Session Management (Priority: P2)

As a user, I want my session to persist across page refreshes so that I don't have to log in repeatedly.

**Why this priority**: Session persistence improves user experience but is not critical for basic functionality.

**Independent Test**: Can be fully tested by logging in, refreshing the page, and verifying the session remains active.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they refresh the page, **Then** they remain logged in
2. **Given** a logged-in user, **When** they close and reopen the browser (within token expiry), **Then** they remain logged in
3. **Given** a JWT token, **When** API requests are made, **Then** the token is automatically included in headers
4. **Given** a token expires (after 7 days), **When** the user attempts an action, **Then** they are prompted to log in again

---

### User Story 6 - User Logout (Priority: P2)

As a user, I want to log out of my account so that others using my device cannot access my tasks.

**Why this priority**: Logout is important for security on shared devices but core functionality works without it.

**Independent Test**: Can be fully tested by logging out and verifying token is cleared and subsequent requests fail.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they click the logout button, **Then** their JWT token is cleared from storage
2. **Given** a user who just logged out, **When** they are on the application, **Then** they are redirected to the login page
3. **Given** a user who logged out, **When** they attempt to access a protected page, **Then** they are redirected to login
4. **Given** a user who logged out, **When** making API requests, **Then** requests receive 401 Unauthorized

---

### Edge Cases

- **What happens when a user's account is deleted while they have an active session?** The JWT token becomes invalid on next API call, returning 401.
- **What happens during concurrent login from multiple devices?** All sessions are valid until token expiration; no single-session enforcement for MVP.
- **What happens if the JWT secret is compromised?** All existing tokens become invalid when secret is rotated; users must re-login.
- **What happens when a user tries to register with same email in different cases (Test@email.com vs test@email.com)?** Email comparison is case-insensitive; treated as same email.
- **What happens if the database connection fails during authentication?** Return 500 Internal Server Error with user-friendly message.

---

## Requirements *(mandatory)*

### Functional Requirements

#### User Registration

- **FR-001**: System MUST allow users to register with email, name, and password
- **FR-002**: System MUST validate email format and uniqueness (case-insensitive comparison)
- **FR-003**: System MUST require password minimum of 8 characters
- **FR-004**: System MUST hash passwords securely before storage (bcrypt)
- **FR-005**: System MUST automatically log in users after successful registration
- **FR-006**: System MUST display clear, specific error messages for registration failures

#### User Login

- **FR-007**: System MUST authenticate users with email and password
- **FR-008**: System MUST issue JWT token upon successful authentication
- **FR-009**: System MUST include user ID (sub claim) in JWT token
- **FR-010**: System MUST set token expiration to 7 days
- **FR-011**: System MUST return generic "Invalid credentials" message for failed login (security)
- **FR-012**: System MUST store JWT token securely in browser (httpOnly cookie preferred, localStorage acceptable)

#### API Protection

- **FR-013**: System MUST require valid JWT token for all `/api/{user_id}/tasks/*` endpoints
- **FR-014**: System MUST extract token from `Authorization: Bearer <token>` header
- **FR-015**: System MUST return 401 Unauthorized for missing, expired, or invalid tokens
- **FR-016**: System MUST verify JWT signature using shared secret
- **FR-017**: System MUST check token expiration before processing requests

#### User Authorization

- **FR-018**: System MUST validate that JWT user ID matches `user_id` in URL path
- **FR-019**: System MUST return 403 Forbidden when user attempts to access other users' data
- **FR-020**: System MUST enforce authorization on all CRUD operations (list, create, read, update, delete)
- **FR-021**: System MUST log authorization failures for security monitoring

#### Session Management

- **FR-022**: System MUST persist JWT token across page refreshes
- **FR-023**: System MUST automatically include token in all API requests
- **FR-024**: System MUST handle token expiration gracefully (redirect to login)
- **FR-025**: System MUST provide logout functionality that clears stored token

#### Database Requirements

- **FR-026**: System MUST create users table with id (UUID), email, name, password_hash, timestamps
- **FR-027**: System MUST enforce unique constraint on email column
- **FR-028**: System MUST update tasks.user_id to reference users.id with foreign key constraint
- **FR-029**: System MUST cascade delete user's tasks when user account is deleted

### Key Entities

- **User**: Represents a registered user account with id (UUID), email (unique), name, password_hash, created_at, updated_at
- **Task** (updated): Now includes foreign key relationship to User via user_id (UUID type)
- **Session/Token**: JWT token containing sub (user_id), email, name, iat (issued at), exp (expiration)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration in under 30 seconds with valid input
- **SC-002**: Users can log in and reach their dashboard in under 5 seconds
- **SC-003**: 100% of unauthenticated API requests receive 401 Unauthorized response
- **SC-004**: 100% of cross-user access attempts receive 403 Forbidden response
- **SC-005**: Sessions persist across page refreshes without re-authentication for 7 days
- **SC-006**: All authentication errors display user-friendly messages without exposing system details
- **SC-007**: Password breach attempts (wrong password) are indistinguishable from invalid email attempts in responses
- **SC-008**: System handles 100 concurrent authentication requests without degradation
- **SC-009**: Token validation adds less than 50ms latency to API requests
- **SC-010**: All security-related events (login, logout, failed attempts) are logged for audit

---

## Assumptions

1. **Better Auth**: Using Better Auth library for frontend authentication (handles password hashing, session management)
2. **PyJWT**: Using PyJWT library for backend JWT verification
3. **Shared Secret**: Frontend and backend share the same JWT secret (BETTER_AUTH_SECRET = JWT_SECRET)
4. **No Email Verification**: Email verification is disabled for MVP (can be enabled in production)
5. **No Password Reset**: Password reset functionality is out of scope for this module
6. **No OAuth/SSO**: Only email/password authentication for MVP
7. **No Rate Limiting**: Rate limiting on auth endpoints is recommended but not required for MVP
8. **Single Region**: No geographic distribution considerations for token validation

---

## Dependencies

### External Dependencies

- **Module 1**: Backend API & Database Layer must be complete (provides task endpoints to secure)
- **Neon PostgreSQL**: Database must support UUID generation and foreign key constraints
- **Better Auth**: Frontend authentication library (handles bcrypt, session management)

### Environment Variables Required

**Frontend (.env.local)**:
- BETTER_AUTH_SECRET: JWT signing secret (min 32 characters)
- BETTER_AUTH_URL: Application base URL
- DATABASE_URL: PostgreSQL connection string
- NEXT_PUBLIC_API_URL: Backend API URL

**Backend (.env)**:
- JWT_SECRET: Must match BETTER_AUTH_SECRET
- JWT_ALGORITHM: HS256
- JWT_EXPIRATION_DAYS: 7

### Follow-on Modules

- **Module 3 - Frontend UI**: Will use authentication state for protected routes and user context

---

## Out of Scope

The following are explicitly OUT OF SCOPE for this module:

- Password reset/forgot password functionality
- Email verification
- OAuth/SSO providers (Google, GitHub, etc.)
- Two-factor authentication (2FA)
- Account lockout after failed attempts
- Password complexity rules beyond minimum length
- Remember me with extended duration
- Multiple active sessions management
- Session revocation/force logout
- Refresh token rotation
- API key authentication
- Role-based access control (RBAC)
- Admin user management interface

---

## Next Steps

After this specification is approved:

1. Run `/sp.plan` to create implementation plan with technical architecture
2. Run `/sp.tasks` to generate executable task list
3. Implement Module 2 following spec-driven development workflow
4. Upon completion, proceed to Module 3 (Frontend UI) to build the user interface
