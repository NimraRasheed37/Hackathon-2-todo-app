# Implementation Plan: Integration, Testing & Deployment

**Branch**: `004-integration-deployment` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `phase-2/specs/004-integration-deployment/spec.md`

## Summary

This module integrates the existing FastAPI backend (Module 1-2) and Next.js frontend (Module 3) into a cohesive full-stack application. Key deliverables include Docker Compose for local development, production deployment to Railway/Vercel, and comprehensive documentation for hackathon submission.

## Technical Context

**Backend Stack**:
- Language/Version: Python 3.11+
- Framework: FastAPI with uvicorn
- Database: PostgreSQL (Neon) with SQLAlchemy
- Authentication: JWT-based (custom implementation)
- Testing: Manual testing (automated tests deferred)

**Frontend Stack**:
- Language/Version: TypeScript with Node.js 18+
- Framework: Next.js 14+ with App Router
- Authentication: Better Auth (client + server)
- Styling: Tailwind CSS
- State Management: SWR

**Deployment Targets**:
- Backend: Railway, Render, or Fly.io
- Frontend: Vercel
- Database: Neon PostgreSQL (already configured)

**Project Type**: Web application (monorepo with backend + frontend)

**Performance Goals**: N/A (integration/deployment module)

**Constraints**:
- Docker Compose must work cross-platform (Windows, Mac, Linux)
- Production must use HTTPS
- No secrets in repository

## Constitution Check

*GATE: This module is infrastructure/deployment focused, so standard development gates apply.*

| Check | Status | Notes |
|-------|--------|-------|
| Clear requirements | PASS | Spec defines all user stories and acceptance criteria |
| Testable deliverables | PASS | Each story has independent test criteria |
| Minimal changes | PASS | Module adds no new features, only integration |
| Security compliance | PASS | No secrets in repo, HTTPS in production |

## Project Structure

### Documentation (this feature)

```text
phase-2/specs/004-integration-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (N/A - no new data models)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A - no new APIs)
│   └── README.md        # Contract documentation reference
├── checklists/          # Requirements checklist
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
Hackathon-2-todo-app/
├── README.md                    # Main project documentation
├── CLAUDE.md                    # AI assistant context (existing)
├── AGENTS.md                    # Multi-agent workflow documentation (new)
├── DEPLOYMENT.md                # Deployment guide (new)
├── docker-compose.yml           # Local development setup (new)
├── .gitignore                   # Combined Python + Node.js ignores (update)
├── .env.example                 # Root environment template (new)
│
├── phase-1/                     # Phase 1: Console app (existing)
│
├── phase-2/                     # Phase 2: Full-stack web app
│   ├── backend/                 # FastAPI backend (existing)
│   │   ├── src/
│   │   │   ├── main.py          # App entry point
│   │   │   ├── config.py        # Settings
│   │   │   ├── database.py      # Database connection
│   │   │   ├── models/          # SQLAlchemy models
│   │   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── repositories/    # Data access layer
│   │   │   ├── api/             # API routes
│   │   │   └── core/            # Core utilities
│   │   ├── requirements.txt
│   │   ├── Dockerfile           # (new)
│   │   └── .env.example         # (existing)
│   │
│   └── frontend/                # Next.js frontend (existing)
│       ├── src/
│       │   ├── app/             # App Router pages
│       │   ├── components/      # React components
│       │   ├── lib/             # Utilities and clients
│       │   └── types/           # TypeScript types
│       ├── package.json
│       ├── Dockerfile           # (new)
│       └── .env.example         # (existing)
│
├── history/                     # PHR records
│   └── prompts/
│       ├── 001-backend-api-database/
│       ├── 002-auth-user-management/
│       ├── 003-frontend-ui/
│       ├── 004-integration-deployment/
│       ├── constitution/
│       └── general/
│
└── .specify/                    # Spec-Kit Plus configuration
```

**Structure Decision**: Web application monorepo with clear separation between backend (Python/FastAPI) and frontend (TypeScript/Next.js). Phase-1 and Phase-2 are kept separate for historical reference.

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRODUCTION                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐        ┌──────────────┐        ┌──────────┐ │
│   │   Vercel     │        │   Railway    │        │   Neon   │ │
│   │  (Frontend)  │───────▶│  (Backend)   │───────▶│ (Postgres)│ │
│   │  Next.js     │        │  FastAPI     │        │          │ │
│   └──────────────┘        └──────────────┘        └──────────┘ │
│         │                        │                              │
│         │      HTTPS + JWT       │                              │
│         └────────────────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐        ┌──────────────┐        ┌──────────┐ │
│   │  localhost   │        │  localhost   │        │ Postgres │ │
│   │    :3000     │───────▶│    :8000     │───────▶│  (Docker)│ │
│   │  Next.js     │        │  FastAPI     │        │          │ │
│   └──────────────┘        └──────────────┘        └──────────┘ │
│                                                                  │
│   docker-compose up                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Points

### Authentication Flow

1. User registers/logs in via Better Auth (frontend)
2. Better Auth stores session in PostgreSQL via frontend
3. Better Auth issues JWT token
4. Frontend includes JWT in Authorization header for backend API calls
5. Backend validates JWT and extracts user_id
6. Backend queries tasks filtered by user_id

### CORS Configuration

**Development**:
```python
CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
```

**Production**:
```python
CORS_ORIGINS = ["https://your-frontend.vercel.app"]
```

### Environment Variable Synchronization

| Variable | Backend | Frontend | Notes |
|----------|---------|----------|-------|
| DATABASE_URL | Yes | Yes | Same Neon database |
| JWT_SECRET | Yes | No | Backend validates tokens |
| BETTER_AUTH_SECRET | No | Yes | Must match for JWT signing |
| CORS_ORIGINS | Yes | No | Must include frontend URL |
| NEXT_PUBLIC_API_URL | No | Yes | Points to backend URL |

## Implementation Phases

### Phase 1: Documentation & Structure
- Update CLAUDE.md with project architecture
- Create AGENTS.md for spec-driven development methodology
- Update .gitignore for combined Python + Node.js

### Phase 2: Docker Compose
- Create Dockerfile for backend
- Create Dockerfile for frontend
- Create docker-compose.yml with all services
- Test local development environment

### Phase 3: Production Deployment
- Deploy backend to Railway
- Deploy frontend to Vercel
- Configure CORS for production domains
- Test end-to-end in production

### Phase 4: Final Documentation
- Create comprehensive README.md
- Create DEPLOYMENT.md
- Add screenshots to README
- Update all live demo URLs

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Docker compatibility issues | Medium | Medium | Test on multiple platforms, use official base images |
| CORS errors in production | High | High | Document troubleshooting, test with browser devtools |
| JWT validation mismatch | Medium | High | Ensure BETTER_AUTH_SECRET matches JWT_SECRET |
| Database connection limits | Low | High | Use connection pooling (already implemented) |
| Vercel build timeout | Low | Medium | Optimize build, use build cache |

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Docker Compose startup | < 2 minutes | `time docker-compose up -d` |
| Production API response | < 500ms p95 | Manual testing with Network tab |
| Documentation completeness | All sections | Checklist in requirements.md |
| Zero secrets in repo | 0 exposed | `git grep -i secret` returns empty |

## Complexity Tracking

> No complexity violations detected. This module focuses on integration and documentation, not new features.

---

## Next Steps

After this plan is approved:
1. Run `/sp.tasks` to generate detailed task list
2. Execute tasks in order: Documentation → Docker → Deployment → Polish
3. Submit to hackathon upon completion
