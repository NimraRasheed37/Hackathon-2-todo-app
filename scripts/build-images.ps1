# ===================================================
# Build Docker images for Todo App (PowerShell)
# ===================================================
param(
    [string]$Version = "latest"
)

$ErrorActionPreference = "Stop"

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=================================================="
Write-Host "Building Todo App Docker Images (v$Version)"
Write-Host "=================================================="

# Build frontend image
Write-Host ""
Write-Host "Building frontend image..."
docker build -t "todo-frontend:$Version" "$ProjectRoot\phase-2\frontend"
if ($LASTEXITCODE -ne 0) { throw "Frontend build failed" }

# Build backend image
Write-Host ""
Write-Host "Building backend image..."
docker build -t "todo-backend:$Version" "$ProjectRoot\phase-2\backend"
if ($LASTEXITCODE -ne 0) { throw "Backend build failed" }

Write-Host ""
Write-Host "=================================================="
Write-Host "Build Complete!"
Write-Host "=================================================="

Write-Host ""
Write-Host "Images built:"
docker images | Select-String "todo" | Select-Object -First 4

Write-Host ""
Write-Host "Image sizes:"
$frontendSize = docker images "todo-frontend:$Version" --format '{{.Size}}'
$backendSize = docker images "todo-backend:$Version" --format '{{.Size}}'
Write-Host "  Frontend: $frontendSize"
Write-Host "  Backend:  $backendSize"

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Load images into Minikube: minikube image load todo-frontend:$Version todo-backend:$Version"
Write-Host "  2. Deploy with Helm: helm upgrade --install todo ./k8s/helm/todo-app"
