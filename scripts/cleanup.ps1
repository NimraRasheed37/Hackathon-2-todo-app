# cleanup.ps1 - Clean up Todo App deployment
$ErrorActionPreference = "Continue"

Write-Host "=== Todo App Cleanup ===" -ForegroundColor Green

# Uninstall Helm release
Write-Host "`nUninstalling Helm release..." -ForegroundColor Yellow
$helmStatus = helm status todo-app 2>&1
if ($LASTEXITCODE -eq 0) {
    helm uninstall todo-app
    Write-Host "✓ Helm release uninstalled" -ForegroundColor Green
} else {
    Write-Host "No Helm release found" -ForegroundColor Yellow
}

# Remove Docker images (optional)
$removeImages = Read-Host "`nDo you want to remove Docker images? (y/N)"
if ($removeImages -match "^[Yy]$") {
    Write-Host "Removing Docker images..."
    docker rmi todo-frontend:local 2>$null
    docker rmi todo-backend:local 2>$null
    Write-Host "✓ Docker images removed" -ForegroundColor Green
}

# Stop Minikube (optional)
$stopMinikube = Read-Host "`nDo you want to stop Minikube? (y/N)"
if ($stopMinikube -match "^[Yy]$") {
    Write-Host "Stopping Minikube..."
    minikube stop
    Write-Host "✓ Minikube stopped" -ForegroundColor Green
}

# Delete Minikube cluster (optional)
$deleteMinikube = Read-Host "`nDo you want to delete the Minikube cluster? (y/N)"
if ($deleteMinikube -match "^[Yy]$") {
    Write-Host "WARNING: This will delete all data in the cluster!" -ForegroundColor Red
    $confirmDelete = Read-Host "Are you sure? (y/N)"

    if ($confirmDelete -match "^[Yy]$") {
        minikube delete
        Write-Host "✓ Minikube cluster deleted" -ForegroundColor Green
    }
}

Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Remember to remove the hosts file entry if no longer needed:"
Write-Host "  Edit C:\Windows\System32\drivers\etc\hosts and remove the todo.local line"
