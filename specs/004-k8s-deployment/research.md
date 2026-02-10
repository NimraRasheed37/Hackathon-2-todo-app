# Research: Phase 4 Local Kubernetes Deployment

**Feature**: 004-k8s-deployment
**Date**: 2026-02-03
**Status**: Complete

## Research Areas

### 1. Next.js Standalone Output for Docker

**Decision**: Add `output: "standalone"` to next.config.ts

**Rationale**: The existing Dockerfile copies from `.next/standalone` directory which is only created when Next.js is configured with standalone output. Without this setting, the Docker build will fail because the standalone directory doesn't exist.

**Alternatives Considered**:
- **Standard build + node_modules**: Larger image (~500MB+), includes dev dependencies
- **Standalone output**: Minimal image (~100-150MB), only production dependencies

**Implementation**:
```typescript
const nextConfig: NextConfig = {
  output: "standalone",
  serverExternalPackages: ["pg"],
};
```

### 2. Backend Health Endpoints for Kubernetes Probes

**Decision**: Add dedicated `/health` and `/ready` endpoints

**Rationale**: Kubernetes requires separate endpoints for liveness (is the app running?) and readiness (is the app ready to serve traffic?). The existing `/` endpoint combines both checks, which doesn't allow for proper separation of concerns.

**Alternatives Considered**:
- **Single / endpoint**: Simpler but can't distinguish between liveness and readiness
- **Separate /health and /ready**: Best practice, allows independent probe configuration

**Implementation**:
```python
@app.get("/health", tags=["health"])
async def liveness_check():
    """Liveness probe - is the application running?"""
    return {"status": "alive"}

@app.get("/ready", tags=["health"])
async def readiness_check():
    """Readiness probe - is the application ready to serve traffic?"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "disconnected"},
        )
```

### 3. Minikube vs Kind vs Docker Desktop Kubernetes

**Decision**: Use Minikube

**Rationale**:
- Most popular local Kubernetes solution with extensive documentation
- Built-in addons for Ingress, metrics, and more
- Easy image loading with `minikube image load`
- Cross-platform support (Windows, macOS, Linux)
- Constitution specifies Minikube 1.32+

**Alternatives Considered**:
- **Kind**: Faster startup, but less feature-rich, no built-in ingress
- **Docker Desktop K8s**: Easy if already using Docker Desktop, but limited configuration
- **k3d/k3s**: Lightweight but different from production K8s

### 4. Helm Chart Structure Best Practices

**Decision**: Follow standard Helm chart structure with separate deployment and service files

**Rationale**: Aligns with Article IV of the constitution. Separate files make templates easier to understand and maintain.

**Chart Structure**:
```
todo-app/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default values
├── values-local.yaml    # Local overrides
├── .helmignore          # Files to ignore
├── README.md            # Usage documentation
└── templates/
    ├── _helpers.tpl     # Template helpers for naming
    ├── NOTES.txt        # Post-install notes
    ├── configmap.yaml
    ├── secret.yaml
    ├── deployment-frontend.yaml
    ├── deployment-backend.yaml
    ├── service-frontend.yaml
    ├── service-backend.yaml
    └── ingress.yaml
```

### 5. Resource Requests and Limits

**Decision**: Use conservative defaults per constitution Article VII

**Rationale**: Local development doesn't need aggressive resource allocation. Conservative limits prevent Minikube from becoming resource-starved.

**Frontend (Next.js)**:
- Requests: 128Mi memory, 100m CPU
- Limits: 256Mi memory, 200m CPU

**Backend (FastAPI + AI)**:
- Requests: 256Mi memory, 200m CPU
- Limits: 512Mi memory, 400m CPU

### 6. Ingress Path-Based Routing

**Decision**: Use NGINX Ingress with path-based routing

**Rationale**: Single entry point for both frontend and backend simplifies DNS and SSL management.

**Routing**:
- `/` → frontend service (port 3000)
- `/api` → backend service (port 8000)

**Configuration**:
```yaml
rules:
  - host: todo.local
    http:
      paths:
        - path: /api
          pathType: Prefix
          backend:
            service:
              name: todo-backend
              port:
                number: 8000
        - path: /
          pathType: Prefix
          backend:
            service:
              name: todo-frontend
              port:
                number: 3000
```

### 7. Secrets Management Strategy

**Decision**: Use Helm --set flags for secrets at install time

**Rationale**:
- Secrets never committed to git
- Easy to rotate by upgrading Helm release
- Works with existing environment variables

**Implementation**:
```bash
helm upgrade --install todo ./k8s/helm/todo-app \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.openaiApiKey="$OPENAI_API_KEY" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"
```

### 8. Image Versioning Strategy

**Decision**: Use semantic versioning tags, avoid :latest in production

**Rationale**: Per constitution Article II, avoid :latest tags for reproducibility. Use `v1.0.0` format.

**Development workflow**:
1. Build with version tag: `docker build -t todo-frontend:v1.0.0 ./phase-2/frontend`
2. Load into Minikube: `minikube image load todo-frontend:v1.0.0`
3. Update Helm values: `helm upgrade todo ./k8s/helm/todo-app --set frontend.image.tag=v1.0.0`

### 9. Windows Compatibility

**Decision**: Provide both bash (.sh) and PowerShell (.ps1) scripts

**Rationale**: Project is being developed on Windows. Bash scripts require WSL or Git Bash; PowerShell scripts run natively.

**Script pairs**:
- build-images.sh / build-images.ps1
- deploy-local.sh / deploy-local.ps1
- test-deployment.sh / test-deployment.ps1

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Where should k8s/ directory live? | Repository root (not inside phase-2/) |
| Should we create a namespace? | No, use default namespace for simplicity |
| How to handle DNS for todo.local? | Manual hosts file entry (documented in quickstart) |
| Should manifests/ be created alongside Helm? | Yes, for learning purposes and fallback |
