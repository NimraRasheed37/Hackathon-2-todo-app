#!/bin/bash
# test-deployment.sh - Test the deployed Todo App
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Todo App Deployment Tests ===${NC}"

FAILED=0
PASSED=0

# Test function
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_code="${3:-200}"

    echo -n "Testing $name... "

    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10 2>/dev/null || echo "000")

    if [ "$HTTP_CODE" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS (HTTP $HTTP_CODE)${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL (HTTP $HTTP_CODE, expected $expected_code)${NC}"
        ((FAILED++))
    fi
}

# Check if pods are running
echo -e "\n${YELLOW}1. Checking pod status...${NC}"
FRONTEND_POD=$(kubectl get pods -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
BACKEND_POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -n "$FRONTEND_POD" ]; then
    FRONTEND_STATUS=$(kubectl get pod "$FRONTEND_POD" -o jsonpath='{.status.phase}')
    if [ "$FRONTEND_STATUS" = "Running" ]; then
        echo -e "${GREEN}✓ Frontend pod is running: $FRONTEND_POD${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Frontend pod is not running: $FRONTEND_STATUS${NC}"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ Frontend pod not found${NC}"
    ((FAILED++))
fi

if [ -n "$BACKEND_POD" ]; then
    BACKEND_STATUS=$(kubectl get pod "$BACKEND_POD" -o jsonpath='{.status.phase}')
    if [ "$BACKEND_STATUS" = "Running" ]; then
        echo -e "${GREEN}✓ Backend pod is running: $BACKEND_POD${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Backend pod is not running: $BACKEND_STATUS${NC}"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ Backend pod not found${NC}"
    ((FAILED++))
fi

# Check services
echo -e "\n${YELLOW}2. Checking services...${NC}"
FRONTEND_SVC=$(kubectl get svc -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
BACKEND_SVC=$(kubectl get svc -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -n "$FRONTEND_SVC" ]; then
    echo -e "${GREEN}✓ Frontend service exists: $FRONTEND_SVC${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Frontend service not found${NC}"
    ((FAILED++))
fi

if [ -n "$BACKEND_SVC" ]; then
    echo -e "${GREEN}✓ Backend service exists: $BACKEND_SVC${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Backend service not found${NC}"
    ((FAILED++))
fi

# Check ingress
echo -e "\n${YELLOW}3. Checking ingress...${NC}"
INGRESS=$(kubectl get ingress -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$INGRESS" ]; then
    echo -e "${GREEN}✓ Ingress exists: $INGRESS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Ingress not found${NC}"
    ((FAILED++))
fi

# Test endpoints via ingress
echo -e "\n${YELLOW}4. Testing endpoints via ingress...${NC}"
echo "(Make sure 'todo.local' is in your /etc/hosts file)"

test_endpoint "Frontend home page" "http://todo.local/"
test_endpoint "Frontend health endpoint" "http://todo.local/api/health"
test_endpoint "Backend health (liveness)" "http://todo.local/api/health"
test_endpoint "Backend readiness" "http://todo.local/api/ready"

# Test health probes via kubectl
echo -e "\n${YELLOW}5. Checking health probes...${NC}"
if [ -n "$FRONTEND_POD" ]; then
    FRONTEND_READY=$(kubectl get pod "$FRONTEND_POD" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
    if [ "$FRONTEND_READY" = "True" ]; then
        echo -e "${GREEN}✓ Frontend readiness probe passing${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Frontend readiness probe failing${NC}"
        ((FAILED++))
    fi
fi

if [ -n "$BACKEND_POD" ]; then
    BACKEND_READY=$(kubectl get pod "$BACKEND_POD" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
    if [ "$BACKEND_READY" = "True" ]; then
        echo -e "${GREEN}✓ Backend readiness probe passing${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Backend readiness probe failing${NC}"
        ((FAILED++))
    fi
fi

# Summary
echo -e "\n${GREEN}=== Test Summary ===${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Check the output above for details.${NC}"
    exit 1
fi
