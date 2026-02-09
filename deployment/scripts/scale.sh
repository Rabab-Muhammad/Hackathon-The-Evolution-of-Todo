#!/bin/bash
# Scale Todo Chatbot replicas
# Usage: ./scale.sh <component> <replicas>
#   component: frontend or backend
#   replicas: number of replicas (1-10)

set -e

RELEASE_NAME="todo-chatbot"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HELM_CHART="$REPO_ROOT/deployment/helm/todo-chatbot"
VALUES_FILE="$HELM_CHART/values-dev.yaml"

# Check arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <component> <replicas>"
    echo ""
    echo "Arguments:"
    echo "  component: frontend or backend"
    echo "  replicas: number of replicas (1-10)"
    echo ""
    echo "Examples:"
    echo "  $0 backend 4    # Scale backend to 4 replicas"
    echo "  $0 frontend 2   # Scale frontend to 2 replicas"
    exit 1
fi

COMPONENT=$1
REPLICAS=$2

# Validate component
if [ "$COMPONENT" != "frontend" ] && [ "$COMPONENT" != "backend" ]; then
    echo "ERROR: Component must be 'frontend' or 'backend'"
    exit 1
fi

# Validate replicas
if ! [[ "$REPLICAS" =~ ^[0-9]+$ ]] || [ "$REPLICAS" -lt 1 ] || [ "$REPLICAS" -gt 10 ]; then
    echo "ERROR: Replicas must be a number between 1 and 10"
    exit 1
fi

echo "=========================================="
echo "Scaling Todo Chatbot $COMPONENT"
echo "=========================================="

# Check if release exists
if ! helm list | grep -q "$RELEASE_NAME"; then
    echo "ERROR: Release '$RELEASE_NAME' not found."
    echo "Deploy first with: ./deploy.sh"
    exit 1
fi

echo "Current $COMPONENT replicas:"
kubectl get deployment "todo-chatbot-$COMPONENT" -o jsonpath='{.spec.replicas}'
echo ""

echo ""
echo "Scaling $COMPONENT to $REPLICAS replicas..."

# Scale using Helm upgrade
helm upgrade "$RELEASE_NAME" "$HELM_CHART" \
    -f "$VALUES_FILE" \
    --set "${COMPONENT}.replicaCount=${REPLICAS}" \
    --reuse-values

if [ $? -eq 0 ]; then
    echo "✓ Helm upgrade successful"

    echo ""
    echo "Waiting for rollout to complete..."
    kubectl rollout status deployment "todo-chatbot-$COMPONENT" --timeout=300s

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Scaling complete!"
        echo ""
        echo "Current pods:"
        kubectl get pods -l "app.kubernetes.io/component=$COMPONENT"

        echo ""
        echo "Deployment status:"
        kubectl get deployment "todo-chatbot-$COMPONENT"
    else
        echo "✗ Rollout failed or timed out"
        exit 1
    fi
else
    echo "✗ Helm upgrade failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "Scaling Summary"
echo "=========================================="
echo "Component: $COMPONENT"
echo "New replica count: $REPLICAS"
echo ""
echo "Verify with:"
echo "  kubectl get pods -l app.kubernetes.io/component=$COMPONENT"
echo "  ./verify.sh"
