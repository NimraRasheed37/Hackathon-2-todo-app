# deploy-local.ps1 - Deploy Todo App to local Minikube cluster
$ErrorActionPreference = "Stop"

Write-Host "=== Todo App Local Deployment ===" -ForegroundColor Green

# Check prerequisites
Write-Host "`nChecking prerequisites..." -ForegroundColor Yellow

$commands = @("minikube", "kubectl", "helm", "docker")
foreach ($cmd in $commands) {
    if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Error: $cmd is not installed" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ All prerequisites installed" -ForegroundColor Green

# Check if Minikube is running
Write-Host "`nChecking Minikube status..." -ForegroundColor Yellow
$minikubeStatus = minikube status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..." -ForegroundColor Yellow
    minikube start --memory=4096 --cpus=2 --driver=docker
}
Write-Host "✓ Minikube is running" -ForegroundColor Green

# Enable ingress addon
Write-Host "`nEnabling ingress addon..." -ForegroundColor Yellow
minikube addons enable ingress
Write-Host "✓ Ingress addon enabled" -ForegroundColor Green

# Set Docker environment to use Minikube's Docker daemon
Write-Host "`nConfiguring Docker to use Minikube..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
Write-Host "✓ Docker configured for Minikube" -ForegroundColor Green

# Build Docker images
Write-Host "`nBuilding Docker images..." -ForegroundColor Yellow

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "Building frontend image..."
docker build -t todo-frontend:local "$ProjectRoot\phase-2\frontend"
Write-Host "✓ Frontend image built" -ForegroundColor Green

Write-Host "Building backend image..."
docker build -t todo-backend:local "$ProjectRoot\phase-2\backend"
Write-Host "✓ Backend image built" -ForegroundColor Green

# Check for values-local.yaml
$ValuesFile = "$ProjectRoot\k8s\helm\todo-app\values-local.yaml"
if (!(Test-Path $ValuesFile)) {
    Write-Host "Error: values-local.yaml not found" -ForegroundColor Red
    Write-Host "Please create $ValuesFile with your secrets:"
    Write-Host "  Copy-Item $ProjectRoot\k8s\helm\todo-app\values.yaml $ValuesFile"
    Write-Host "  # Then edit values-local.yaml with your secrets"
    exit 1
}

# Deploy with Helm
Write-Host "`nDeploying with Helm..." -ForegroundColor Yellow
helm upgrade --install todo-app "$ProjectRoot\k8s\helm\todo-app" `
    -f $ValuesFile `
    --wait `
    --timeout 5m

Write-Host "✓ Helm deployment complete" -ForegroundColor Green

# Wait for pods to be ready
Write-Host "`nWaiting for pods to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=300s
Write-Host "✓ All pods are ready" -ForegroundColor Green

# Get Minikube IP and add hosts entry reminder
$MinikubeIP = minikube ip

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Green
Write-Host "`nAdd this line to your C:\Windows\System32\drivers\etc\hosts file:" -ForegroundColor Yellow
Write-Host "$MinikubeIP todo.local" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at: http://todo.local" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  kubectl get pods        # Check pod status"
Write-Host "  kubectl logs -f <pod>   # View logs"
Write-Host "  helm status todo-app    # Check Helm release status"
Write-Host "  .\scripts\cleanup.ps1   # Clean up deployment"
