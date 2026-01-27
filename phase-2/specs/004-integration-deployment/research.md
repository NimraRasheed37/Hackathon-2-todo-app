# Research: Integration, Testing & Deployment

**Feature**: 004-integration-deployment
**Date**: 2026-01-26
**Purpose**: Resolve technical decisions and best practices for deployment and integration

---

## Research Areas

### 1. Docker Compose Configuration for Monorepo

**Decision**: Use Docker Compose with separate services for backend, frontend, and database

**Rationale**:
- Docker Compose simplifies local development by managing all services together
- Volume mounting enables hot reloading during development
- Consistent environment across developer machines
- Easy to add new services (e.g., Redis, email service) later

**Alternatives Considered**:
- **Podman Compose**: Good alternative but Docker has wider adoption
- **Individual Docker containers**: Harder to manage networking
- **Native local development**: Works but requires manual setup for each developer

**Best Practices**:
```yaml
# Use multi-stage builds for smaller images
# Use specific version tags, not 'latest'
# Mount volumes for development hot-reload
# Use environment files for secrets
# Define health checks for dependencies
```

---

### 2. Backend Deployment Platform

**Decision**: Railway (primary) or Render (backup)

**Rationale**:
- Railway offers simple GitHub integration and automatic deployments
- Free tier sufficient for hackathon demo
- Built-in PostgreSQL option (though using Neon)
- Easy environment variable management

**Alternatives Considered**:
- **Render**: Similar to Railway, good backup option
- **Fly.io**: More complex setup but better for production
- **Heroku**: No longer has free tier
- **AWS/GCP**: Overkill for hackathon

**Configuration**:
```bash
# Railway deployment
railway up

# Environment variables
DATABASE_URL=postgresql://...
JWT_SECRET=...
CORS_ORIGINS=https://frontend.vercel.app
```

---

### 3. Frontend Deployment Platform

**Decision**: Vercel

**Rationale**:
- Native Next.js support (Vercel created Next.js)
- Automatic previews for pull requests
- Edge network for fast global delivery
- Free tier generous for hackathon
- Built-in environment variable management

**Alternatives Considered**:
- **Netlify**: Good but less optimized for Next.js
- **Cloudflare Pages**: Good but newer Next.js support
- **Self-hosted**: More control but more complexity

**Configuration**:
```bash
# Vercel settings
Build Command: npm run build
Output Directory: .next
Install Command: npm install

# Environment variables
BETTER_AUTH_SECRET=...
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=https://backend.railway.app
```

---

### 4. CORS Configuration Strategy

**Decision**: Environment-based CORS origins list

**Rationale**:
- Separate development and production origins
- Configurable via environment variables
- Supports multiple frontend URLs if needed

**Implementation**:
```python
# backend/src/config.py
class Settings(BaseSettings):
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
```

**Common Issues**:
- Credentials + wildcard origin not allowed
- Preflight requests (OPTIONS) must be handled
- Headers must include Access-Control-Allow-Origin

---

### 5. Documentation Standards for Hackathon

**Decision**: Follow standard open-source project structure

**Rationale**:
- Familiar to judges and developers
- Comprehensive but not overwhelming
- Clear call-to-action (try the demo)

**README.md Structure**:
1. Project title and badges
2. Demo link and screenshot
3. Features list
4. Tech stack
5. Quick start (3 steps max)
6. Project structure
7. API documentation summary
8. Contributing (optional)
9. License
10. Acknowledgments

**AGENTS.md Purpose**:
- Document AI-assisted development methodology
- Show spec-driven development workflow
- Highlight multi-module planning approach
- Link to specs and PHRs

---

### 6. Docker Multi-Stage Builds

**Decision**: Use multi-stage builds for production images

**Rationale**:
- Smaller final image size
- Build dependencies not in production
- Faster deployment and startup

**Backend Dockerfile Pattern**:
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile Pattern**:
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
CMD ["npm", "start"]
```

---

### 7. Environment Variable Management

**Decision**: Use .env.example files with documentation

**Rationale**:
- Clear documentation of required variables
- Prevents secrets from being committed
- Easy onboarding for new developers

**Strategy**:
```
.env.example  # Committed - template with placeholders
.env          # Not committed - actual secrets
.env.local    # Not committed - Next.js specific
```

**Root .env.example**:
```bash
# Shared secrets (must match across services)
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
BETTER_AUTH_SECRET=${JWT_SECRET}  # Must match JWT_SECRET

# Database
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Service URLs (development)
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

# Service URLs (production - update these)
PRODUCTION_FRONTEND_URL=https://your-app.vercel.app
PRODUCTION_BACKEND_URL=https://your-api.railway.app
```

---

### 8. Health Check Endpoints

**Decision**: Standardized health check endpoints for monitoring

**Backend** (already implemented):
```python
@app.get("/")
async def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"}
        )
```

**Frontend** (to add if needed):
```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({ status: "healthy" });
}
```

---

## Summary of Decisions

| Area | Decision | Confidence |
|------|----------|------------|
| Container orchestration | Docker Compose | High |
| Backend deployment | Railway | High |
| Frontend deployment | Vercel | High |
| CORS strategy | Env-based origins | High |
| Documentation | Standard OSS structure | High |
| Docker builds | Multi-stage | High |
| Env management | .env.example pattern | High |
| Health checks | REST endpoints | High |

---

## Open Questions

1. **Custom domain**: Not in scope for hackathon, but platforms support it
2. **CI/CD**: Deferred to future enhancement
3. **Monitoring**: Rely on platform dashboards for now
