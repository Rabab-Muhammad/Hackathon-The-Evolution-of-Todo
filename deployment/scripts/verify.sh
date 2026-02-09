#!/bin/bash
# Verify Todo Chatbot deployment on Minikube
# Usage: ./verify.sh

set -e

RELEASE_NAME="todo-chatbot"

echo "=========================================="
echo "Verifying Todo Chatbot Deployment"
echo "=========================================="

# Check if deployment exists
if ! helm list | grep -q "$RELEASE_NAME"; then
    echo "ERROR: Release '$RELEASE_NAME' not found."
    echo "Deploy first with: ./deploy.sh"
    exit 1
fi

echo "✓ Helm release found"

# Check deployments
echo ""
echo "Checking deployments..."
kubectl get deployments -l app.kubernetes.io/name=todo-chatbot

FRONTEND_READY=$(kubectl get deployment todo-chatbot-frontend -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
BACKEND_READY=$(kubectl get deployment todo-chatbot-backend -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

if [ "$FRONTEND_READY" -gt 0 ]; then
    echo "✓ Frontend deployment ready ($FRONTEND_READY replicas)"
else
    echo "✗ Frontend deployment not ready"
fi

if [ "$BACKEND_READY" -gt 0 ]; then
    echo "✓ Backend deployment ready ($BACKEND_READY replicas)"
else
    echo "✗ Backend deployment not ready"
fi

# Check services
echo ""
echo "Checking services..."
kubectl get services -l app.kubernetes.io/name=todo-chatbot

# Check pods
echo ""
echo "Checking pods..."
kubectl get pods -l app.kubernetes.io/name=todo-chatbot

# Check pod health
echo ""
echo "Checking pod health..."
UNHEALTHY_PODS=$(kubectl get pods -l app.kubernetes.io/name=todo-chatbot --field-selector=status.phase!=Running --no-headers 2>/dev/null | wc -l)

if [ "$UNHEALTHY_PODS" -eq 0 ]; then
    echo "✓ All pods are running"
else
    echo "✗ $UNHEALTHY_PODS pod(s) not running"
    kubectl get pods -l app.kubernetes.io/name=todo-chatbot --field-selector=status.phase!=Running
fi

# Check endpoints
echo ""
echo "Checking service endpoints..."
kubectl get endpoints -l app.kubernetes.io/name=todo-chatbot

# Test frontend accessibility
echo ""
echo "Testing frontend accessibility..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:30080/ | grep -q "200"; then
    echo "✓ Frontend is accessible at http://localhost:30080"
else
    echo "✗ Frontend is not accessible"
    echo "  Try: minikube service todo-chatbot-frontend --url"
fi

# Test backend health endpoint
echo ""
echo "Testing backend health endpoint..."
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:30081/api/health)

if [ "$BACKEND_HEALTH" = "200" ]; then
    echo "✓ Backend health check passed (http://localhost:30081/api/health)"
else
    echo "✗ Backend health check failed (HTTP $BACKEND_HEALTH)"
    echo "  Try: minikube service todo-chatbot-backend --url"
fi

# Test backend API docs
echo ""
echo "Testing backend API documentation..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:30081/docs | grep -q "200"; then
    echo "✓ Backend API docs accessible (http://localhost:30081/docs)"
else
    echo "✗ Backend API docs not accessible"
fi

# Check for errors in logs
echo ""
echo "Checking for errors in logs..."
FRONTEND_ERRORS=$(kubectl logs -l app.kubernetes.io/component=frontend --tail=50 2>/dev/null | grep -i error | wc -l)
BACKEND_ERRORS=$(kubectl logs -l app.kubernetes.io/component=backend --tail=50 2>/dev/null | grep -i error | wc -l)

if [ "$FRONTEND_ERRORS" -eq 0 ]; then
    echo "✓ No errors in frontend logs"
else
    echo "⚠ $FRONTEND_ERRORS error(s) found in frontend logs"
fi

if [ "$BACKEND_ERRORS" -eq 0 ]; then
    echo "✓ No errors in backend logs"
else
    echo "⚠ $BACKEND_ERRORS error(s) found in backend logs"
fi

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="

TOTAL_CHECKS=6
PASSED_CHECKS=0

[ "$FRONTEND_READY" -gt 0 ] && ((PASSED_CHECKS++))
[ "$BACKEND_READY" -gt 0 ] && ((PASSED_CHECKS++))
[ "$UNHEALTHY_PODS" -eq 0 ] && ((PASSED_CHECKS++))
[ "$(curl -s -o /dev/null -w "%{http_code}" http://localhost:30080/)" = "200" ] && ((PASSED_CHECKS++))
[ "$BACKEND_HEALTH" = "200" ] && ((PASSED_CHECKS++))
[ "$(curl -s -o /dev/null -w "%{http_code}" http://localhost:30081/docs)" = "200" ] && ((PASSED_CHECKS++))

echo "Passed: $PASSED_CHECKS/$TOTAL_CHECKS checks"

if [ "$PASSED_CHECKS" -eq "$TOTAL_CHECKS" ]; then
    echo ""
    echo "✓ All verification checks passed!"
    echo ""
    echo "Your Todo Chatbot is ready to use:"
    echo "  Frontend: http://localhost:30080"
    echo "  Backend API: http://localhost:30081"
    echo "  API Docs: http://localhost:30081/docs"
    exit 0
else
    echo ""
    echo "⚠ Some verification checks failed."
    echo ""
    echo "Troubleshooting:"
    echo "  View pod details: kubectl describe pod <pod-name>"
    echo "  View logs: kubectl logs <pod-name>"
    echo "  Check events: kubectl get events --sort-by='.lastTimestamp'"
    exit 1
fi
