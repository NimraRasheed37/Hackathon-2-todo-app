# Research: Authentication & User Management

**Branch**: `002-auth-user-management` | **Date**: 2026-01-26 | **Plan**: [plan.md](./plan.md)

This document consolidates research findings for the authentication module implementation.

---

## Research Task 1: PyJWT Token Verification

### Findings

**JWT Structure (RFC 7519)**:
- Header: `{"alg": "HS256", "typ": "JWT"}`
- Payload: `{"sub": "user-uuid", "email": "user@example.com", "name": "User Name", "iat": 1706140800, "exp": 1706745600}`
- Signature: HMAC-SHA256 of header.payload with secret

**PyJWT Verification Pattern**:
```python
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def verify_token(token: str, secret: str) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"require": ["sub", "exp"]}
        )
        return payload
    except ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except InvalidTokenError:
        raise AuthenticationError("Invalid token")
```

**Key Points**:
- Always specify `algorithms` list to prevent algorithm confusion attacks
- Use `options={"require": [...]}` to enforce required claims
- Handle `ExpiredSignatureError` separately for specific error messages
- `jwt.decode()` verifies signature and expiration automatically

**Error Handling**:
- `ExpiredSignatureError`: Token has expired → 401 with "Token has expired"
- `InvalidTokenError`: Malformed or invalid signature → 401 with "Invalid token"
- `DecodeError`: Cannot parse token → 401 with "Invalid token"

---

## Research Task 2: Better Auth JWT Structure

### Findings

**Better Auth Token Claims**:
```json
{
  "sub": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "email": "user@example.com",
  "name": "User Name",
  "iat": 1706140800,
  "exp": 1706745600,
  "session_token": "session-identifier"
}
```

**Claim Details**:
- `sub` (Subject): User's UUID (primary identifier)
- `email`: User's email address
- `name`: User's display name
- `iat` (Issued At): Unix timestamp when token was created
- `exp` (Expiration): Unix timestamp when token expires
- `session_token`: Better Auth session identifier (optional claim)

**Token Storage**:
- Better Auth stores tokens in httpOnly cookies by default (more secure)
- Can be configured for localStorage (less secure, but simpler CORS)
- For API calls, token is sent via `Authorization: Bearer <token>` header

**Token Expiration**:
- Configured via `BETTER_AUTH_SECRET` and session settings
- Default expiration is 7 days (604800 seconds)
- Frontend handles token refresh automatically

**Integration Points**:
- Frontend (Better Auth): Creates tokens on signup/signin
- Backend (PyJWT): Verifies tokens on API requests
- Shared secret: `BETTER_AUTH_SECRET` = `JWT_SECRET`

---

## Research Task 3: UUID Foreign Key with SQLModel

### Findings

**SQLModel UUID Field**:
```python
import uuid
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class User(SQLModel, table=True):
    """User entity with UUID primary key."""
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
```

**Foreign Key Constraint**:
```python
class Task(SQLModel, table=True):
    """Task entity with UUID foreign key."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            index=True
        )
    )
```

**Migration Strategy**:
1. Create users table with UUID primary key
2. Alter tasks table: drop existing user_id column
3. Add new user_id column with UUID type and FK constraint
4. Add cascade delete behavior

**Neon PostgreSQL UUID Support**:
- Native UUID type supported (`uuid-ossp` extension available)
- No additional configuration needed
- Indexes on UUID columns work efficiently

**Important**: Migration requires careful handling to avoid data loss. For new deployments, simply use UUID from the start.

---

## Research Task 4: FastAPI Dependency Injection for Auth

### Findings

**Authentication Dependency Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """Extract and verify JWT token from Authorization header."""
    token = credentials.credentials
    try:
        payload = verify_token(token, settings.jwt_secret)
        return TokenPayload(**payload)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
```

**Protected Route Usage**:
```python
@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify user_id matches token
    if str(current_user.sub) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Proceed with authorized request
    return repository.get_all_by_user(user_id)
```

**Key Benefits**:
- Declarative: Add `Depends(get_current_user)` to any route
- Type-safe: Token payload is typed `TokenPayload`
- Automatic 401: Missing/invalid token raises HTTPException
- Swagger UI: Shows lock icon for protected endpoints

**HTTPBearer vs OAuth2PasswordBearer**:
- `HTTPBearer`: Simpler, just validates Authorization header format
- `OAuth2PasswordBearer`: More complex, supports OAuth2 flows
- For JWT verification with Better Auth, `HTTPBearer` is sufficient

---

## Research Task 5: Security Logging Best Practices

### Findings

**Events to Log**:
| Event | Level | Required Fields |
|-------|-------|-----------------|
| Successful login | INFO | user_id, email, timestamp, ip_address |
| Failed login | WARNING | email (not password), timestamp, ip_address, reason |
| Logout | INFO | user_id, timestamp |
| Token validation failure | WARNING | reason, timestamp, request_id |
| Authorization failure (403) | WARNING | user_id, requested_resource, timestamp |
| Account creation | INFO | user_id, email, timestamp |

**Structured Log Format** (JSON for SIEM integration):
```json
{
  "timestamp": "2026-01-26T10:30:00Z",
  "level": "WARNING",
  "event": "auth.login_failed",
  "request_id": "abc-123",
  "data": {
    "email": "user@example.com",
    "reason": "invalid_password",
    "ip_address": "192.168.1.1"
  }
}
```

**Sensitive Data Handling**:
- NEVER log passwords (plain or hashed)
- NEVER log full JWT tokens (log token ID if available)
- MASK email if needed: `u***@example.com`
- DO log user IDs (non-sensitive identifiers)

**Log Levels for Security Events**:
- INFO: Successful operations (login, logout, registration)
- WARNING: Failed attempts (wrong password, expired token, unauthorized access)
- ERROR: System failures (database errors, configuration issues)
- CRITICAL: Security breaches (multiple failed attempts, potential attack patterns)

**Request ID Correlation**:
- Include `X-Request-ID` in all security logs
- Enables tracing authentication flow across services
- Already implemented in Module 1 middleware

**Implementation**:
```python
import structlog

logger = structlog.get_logger()

def log_security_event(event: str, user_id: str = None, **kwargs):
    """Log a security event with structured data."""
    logger.info(
        event,
        user_id=user_id,
        **kwargs
    )
```

---

## Summary of Key Decisions

Based on research findings:

1. **JWT Verification**: Use PyJWT with HS256 algorithm, require `sub` and `exp` claims
2. **Token Structure**: Compatible with Better Auth defaults (sub, email, name, iat, exp)
3. **UUID Implementation**: Use PostgreSQL native UUID with SQLModel/SQLAlchemy
4. **Auth Dependency**: FastAPI `Depends()` with `HTTPBearer` security scheme
5. **Security Logging**: Structured JSON logs with request ID correlation

---

## References

- [PyJWT Documentation](https://pyjwt.readthedocs.io/en/stable/)
- [Better Auth Documentation](https://www.better-auth.com/docs)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLModel UUID Fields](https://sqlmodel.tiangolo.com/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
