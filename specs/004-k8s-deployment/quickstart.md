# Quickstart: Phase 4 Local Kubernetes Deployment

**Feature**: 004-k8s-deployment
**Time to Deploy**: ~15 minutes (first time), ~5 minutes (subsequent)

## Prerequisites

### Required Software

| Tool | Version | Installation |
|------|---------|--------------|
| Docker | 24+ | https://docs.docker.com/get-docker/ |
| Minikube | 1.32+ | https://minikube.sigs.k8s.io/docs/start/ |
| kubectl | 1.28+ | Comes with Minikube or https://kubernetes.io/docs/tasks/tools/ |
| Helm | 3.13+ | https://helm.sh/docs/intro/install/ |

### Verify Installation

```bash
# Check versions
docker --version      # Docker version 24.x.x
minikube version      # minikube version: v1.32.x
kubectl version --client  # Client Version: v1.28.x
helm version          # version.BuildInfo{Version:"v3.13.x"...}
```

### Required Secrets

You'll need these values from your environment:

- `DATABASE_URL`: Neon PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key
- `JWT_SECRET`: JWT signing secret
- `BETTER_AUTH_SECRET`: Better Auth secret

## Quick Deploy (Automated Scripts)

### Using Deployment Script (Recommended)

**Linux/macOS:**
```bash
# 1. Create values-local.yaml with your secrets
cp k8s/helm/todo-app/values.yaml k8s/helm/todo-app/values-local.yaml
# Edit values-local.yaml with your DATABASE_URL, OPENAI_API_KEY, JWT_SECRET, BETTER_AUTH_SECRET

# 2. Run the deployment script
./scripts/deploy-local.sh

# 3. Add hosts entry (script will show the IP)
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# 4. Access http://todo.local
```

**Windows (PowerShell):**
```powershell
# 1. Create values-local.yaml with your secrets
Copy-Item k8s\helm\todo-app\values.yaml k8s\helm\todo-app\values-local.yaml
# Edit values-local.yaml with your DATABASE_URL, OPENAI_API_KEY, JWT_SECRET, BETTER_AUTH_SECRET

# 2. Run the deployment script
.\scripts\deploy-local.ps1

# 3. Add hosts entry (run as Admin)
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "$(minikube ip) todo.local"

# 4. Access http://todo.local
```

### Manual Quick Deploy (5 commands)

```bash
# 1. Start Minikube
minikube start --memory=4096 --cpus=2

# 2. Enable Ingress
minikube addons enable ingress

# 3. Build and load images (using Minikube's Docker)
eval $(minikube docker-env)
docker build -t todo-frontend:local ./phase-2/frontend
docker build -t todo-backend:local ./phase-2/backend

# 4. Deploy with Helm
helm upgrade --install todo-app ./k8s/helm/todo-app \
    -f ./k8s/helm/todo-app/values-local.yaml

# 5. Add hosts entry and access
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
# Open http://todo.local in your browser
```

## Detailed Steps

### Step 1: Start Minikube Cluster

```bash
# Start with recommended resources
minikube start --memory=4096 --cpus=2

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### Step 2: Enable Ingress Addon

```bash
# Enable NGINX Ingress Controller
minikube addons enable ingress

# Verify ingress is running
kubectl get pods -n ingress-nginx
# Wait for the ingress-nginx-controller pod to be Running
```

### Step 3: Build Docker Images

```bash
# From repository root
cd path/to/Hackathon-2-todo-app

# Build frontend image
docker build -t todo-frontend:latest ./phase-2/frontend

# Build backend image
docker build -t todo-backend:latest ./phase-2/backend

# Verify images
docker images | grep todo
```

### Step 4: Load Images into Minikube

```bash
# Load both images into Minikube's container runtime
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Verify images are loaded
minikube image ls | grep todo
```

### Step 5: Deploy with Helm

```bash
# Set environment variables (or export them)
export DATABASE_URL="postgresql://user:pass@host/db"
export OPENAI_API_KEY="sk-..."
export JWT_SECRET="your-jwt-secret"
export BETTER_AUTH_SECRET="your-better-auth-secret"

# Install/upgrade the Helm release
helm upgrade --install todo ./k8s/helm/todo-app \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.openaiApiKey="$OPENAI_API_KEY" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

# Watch pods come up
kubectl get pods -w
# Wait until all pods show Running status (Ctrl+C to exit watch)
```

### Step 6: Configure DNS

**Windows** (Run as Administrator):
```powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "127.0.0.1 todo.local"
```

**macOS/Linux**:
```bash
echo "127.0.0.1 todo.local" | sudo tee -a /etc/hosts
```

### Step 7: Start Minikube Tunnel

```bash
# In a separate terminal (keep running)
minikube tunnel

# This routes traffic from localhost to the Ingress
```

### Step 8: Access the Application

Open your browser and navigate to:
- **Frontend**: http://todo.local
- **API Docs**: http://todo.local/api/docs (if enabled)

## Verification Checklist

```bash
# ✅ Pods running
kubectl get pods
# Should show 2 frontend and 2 backend pods in Running state

# ✅ Services created
kubectl get services
# Should show todo-frontend and todo-backend services

# ✅ Ingress configured
kubectl get ingress
# Should show todo-ingress with host todo.local

# ✅ Health checks passing
kubectl describe pod -l app.kubernetes.io/component=frontend | grep -A5 "Liveness"
kubectl describe pod -l app.kubernetes.io/component=backend | grep -A5 "Liveness"

# ✅ No errors in logs
kubectl logs -l app.kubernetes.io/instance=todo --tail=20
```

## Common Commands

```bash
# View all resources
kubectl get all -l app.kubernetes.io/instance=todo

# View pod logs
kubectl logs -f deployment/todo-frontend
kubectl logs -f deployment/todo-backend

# Execute into a pod
kubectl exec -it deployment/todo-backend -- /bin/sh

# Port forward for debugging
kubectl port-forward svc/todo-backend 8000:8000
# Then access http://localhost:8000

# View Helm release
helm list
helm status todo
helm history todo

# Update after code changes
./scripts/build-images.sh v1.0.1
minikube image load todo-frontend:v1.0.1 todo-backend:v1.0.1
helm upgrade todo ./k8s/helm/todo-app --set frontend.image.tag=v1.0.1 --set backend.image.tag=v1.0.1
```

## Cleanup

### Using Cleanup Script (Recommended)

**Linux/macOS:**
```bash
./scripts/cleanup.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\cleanup.ps1
```

### Manual Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app

# Stop Minikube
minikube stop

# Delete Minikube cluster (optional)
minikube delete

# Remove hosts entry
# Linux/macOS: sudo sed -i '/todo.local/d' /etc/hosts
# Windows: Edit C:\Windows\System32\drivers\etc\hosts and remove the todo.local line
```

## Testing Deployment

Run the test script to verify your deployment:

**Linux/macOS:**
```bash
./scripts/test-deployment.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\test-deployment.ps1
```

## Troubleshooting

### Pods not starting

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check for image pull errors (ensure images are loaded)
minikube image ls | grep todo
```

### Database connection errors

```bash
# Verify secret is created correctly
kubectl get secret todo-secrets -o yaml

# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend
```

### Ingress not working

```bash
# Verify ingress controller is running
kubectl get pods -n ingress-nginx

# Check ingress configuration
kubectl describe ingress todo-ingress

# Ensure minikube tunnel is running
minikube tunnel
```

### Out of resources

```bash
# Check node resources
kubectl top nodes
kubectl describe node minikube

# Increase Minikube resources
minikube stop
minikube delete
minikube start --memory=6144 --cpus=4
```
