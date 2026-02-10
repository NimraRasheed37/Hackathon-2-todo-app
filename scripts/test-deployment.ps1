# test-deployment.ps1 - Test the deployed Todo App
$ErrorActionPreference = "Continue"

Write-Host "=== Todo App Deployment Tests ===" -ForegroundColor Green

$FAILED = 0
$PASSED = 0

function Test-Endpoint {
    param (
        [string]$Name,
        [string]$Url,
        [int]$ExpectedCode = 200
    )

    Write-Host -NoNewline "Testing $Name... "

    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
        $httpCode = $response.StatusCode
    } catch {
        $httpCode = 0
        if ($_.Exception.Response) {
            $httpCode = [int]$_.Exception.Response.StatusCode
        }
    }

    if ($httpCode -eq $ExpectedCode) {
        Write-Host "✓ PASS (HTTP $httpCode)" -ForegroundColor Green
        return 1
    } else {
        Write-Host "✗ FAIL (HTTP $httpCode, expected $ExpectedCode)" -ForegroundColor Red
        return 0
    }
}

# Check if pods are running
Write-Host "`n1. Checking pod status..." -ForegroundColor Yellow

$frontendPod = kubectl get pods -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>$null
$backendPod = kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>$null

if ($frontendPod) {
    $frontendStatus = kubectl get pod $frontendPod -o jsonpath='{.status.phase}'
    if ($frontendStatus -eq "Running") {
        Write-Host "✓ Frontend pod is running: $frontendPod" -ForegroundColor Green
        $PASSED++
    } else {
        Write-Host "✗ Frontend pod is not running: $frontendStatus" -ForegroundColor Red
        $FAILED++
    }
} else {
    Write-Host "✗ Frontend pod not found" -ForegroundColor Red
    $FAILED++
}

if ($backendPod) {
    $backendStatus = kubectl get pod $backendPod -o jsonpath='{.status.phase}'
    if ($backendStatus -eq "Running") {
        Write-Host "✓ Backend pod is running: $backendPod" -ForegroundColor Green
        $PASSED++
    } else {
        Write-Host "✗ Backend pod is not running: $backendStatus" -ForegroundColor Red
        $FAILED++
    }
} else {
    Write-Host "✗ Backend pod not found" -ForegroundColor Red
    $FAILED++
}

# Check services
Write-Host "`n2. Checking services..." -ForegroundColor Yellow

$frontendSvc = kubectl get svc -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>$null
$backendSvc = kubectl get svc -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>$null

if ($frontendSvc) {
    Write-Host "✓ Frontend service exists: $frontendSvc" -ForegroundColor Green
    $PASSED++
} else {
    Write-Host "✗ Frontend service not found" -ForegroundColor Red
    $FAILED++
}

if ($backendSvc) {
    Write-Host "✓ Backend service exists: $backendSvc" -ForegroundColor Green
    $PASSED++
} else {
    Write-Host "✗ Backend service not found" -ForegroundColor Red
    $FAILED++
}

# Check ingress
Write-Host "`n3. Checking ingress..." -ForegroundColor Yellow

$ingress = kubectl get ingress -o jsonpath='{.items[0].metadata.name}' 2>$null
if ($ingress) {
    Write-Host "✓ Ingress exists: $ingress" -ForegroundColor Green
    $PASSED++
} else {
    Write-Host "✗ Ingress not found" -ForegroundColor Red
    $FAILED++
}

# Test endpoints via ingress
Write-Host "`n4. Testing endpoints via ingress..." -ForegroundColor Yellow
Write-Host "(Make sure 'todo.local' is in your hosts file)"

$PASSED += Test-Endpoint -Name "Frontend home page" -Url "http://todo.local/"
$PASSED += Test-Endpoint -Name "Frontend health endpoint" -Url "http://todo.local/api/health"
$PASSED += Test-Endpoint -Name "Backend health (liveness)" -Url "http://todo.local/api/health"
$PASSED += Test-Endpoint -Name "Backend readiness" -Url "http://todo.local/api/ready"

# Test health probes via kubectl
Write-Host "`n5. Checking health probes..." -ForegroundColor Yellow

if ($frontendPod) {
    $frontendReady = kubectl get pod $frontendPod -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
    if ($frontendReady -eq "True") {
        Write-Host "✓ Frontend readiness probe passing" -ForegroundColor Green
        $PASSED++
    } else {
        Write-Host "✗ Frontend readiness probe failing" -ForegroundColor Red
        $FAILED++
    }
}

if ($backendPod) {
    $backendReady = kubectl get pod $backendPod -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
    if ($backendReady -eq "True") {
        Write-Host "✓ Backend readiness probe passing" -ForegroundColor Green
        $PASSED++
    } else {
        Write-Host "✗ Backend readiness probe failing" -ForegroundColor Red
        $FAILED++
    }
}

# Summary
Write-Host "`n=== Test Summary ===" -ForegroundColor Green
Write-Host "Passed: $PASSED" -ForegroundColor Green
Write-Host "Failed: $FAILED" -ForegroundColor Red

if ($FAILED -eq 0) {
    Write-Host "`nAll tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nSome tests failed. Check the output above for details." -ForegroundColor Red
    exit 1
}
