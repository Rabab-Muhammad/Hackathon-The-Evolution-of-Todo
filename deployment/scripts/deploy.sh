#!/bin/bash
# Deploy Todo Chatbot to Minikube using Helm
# Usage: ./deploy.sh [--upgrade]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HELM_CHART="$REPO_ROOT/deployment/helm/todo-chatbot"
VALUES_FILE="$HELM_CHART/values-dev.yaml"
RELEASE_NAME="todo-chatbot"

echo "=========================================="
echo "Deploying Todo Chatbot to Minikube"
echo "=========================================="

# Check if Minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "ERROR: Minikube is not running."
    echo "Start Minikube with: minikube start --cpus=2 --memory=4096"
    exit 1
fi

echo "✓ Minikube is running"

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "ERROR: Helm is not installed."
    echo "Install Helm: https://helm.sh/docs/intro/install/"
    exit 1
fi

echo "✓ Helm is installed"

# Check if values-dev.yaml exists
if [ ! -f "$VALUES_FILE" ]; then
    echo "ERROR: values-dev.yaml not found at $VALUES_FILE"
    echo ""
    echo "Create it from the example:"
    echo "  cp $HELM_CHART/values-dev.yaml.example $VALUES_FILE"
    echo ""
    echo "Then edit it with your actual secrets:"
    echo "  - DATABASE_URL"
    echo "  - BETTER_AUTH_SECRET"
    echo "  - NEXT_PUBLIC_OPENROUTER_KEY"
    exit 1
fi

echo "✓ values-dev.yaml found"

# Validate Helm chart
echo ""
echo "Validating Helm chart..."
helm lint "$HELM_CHART" -f "$VALUES_FILE"

if [ $? -ne 0 ]; then
    echo "✗ Helm chart validation failed"
    exit 1
fi

echo "✓ Helm chart is valid"

# Check if release already exists
if helm list | grep -q "$RELEASE_NAME"; then
    if [[ "$1" == "--upgrade" ]]; then
        echo ""
        echo "Upgrading existing release..."
        helm upgrade "$RELEASE_NAME" "$HELM_CHART" -f "$VALUES_FILE"
    else
        echo ""
        echo "ERROR: Release '$RELEASE_NAME' already exists."
        echo "Use --upgrade flag to upgrade, or uninstall first:"
        echo "  helm uninstall $RELEASE_NAME"
        exit 1
    fi
else
    # Perform dry-run first
    echo ""
    echo "Performing dry-run..."
    helm install "$RELEASE_NAME" "$HELM_CHART" -f "$VALUES_FILE" --dry-run --debug > /dev/null

    if [ $? -ne 0 ]; then
        echo "✗ Dry-run failed"
        exit 1
    fi

    echo "✓ Dry-run successful"

    # Install the chart
    echo ""
    echo "Installing Helm chart..."
    helm install "$RELEASE_NAME" "$HELM_CHART" -f "$VALUES_FILE"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Deployment successful!"
    echo ""
    echo "=========================================="
    echo "Waiting for pods to be ready..."
    echo "=========================================="

    # Wait for pods to be ready (timeout 5 minutes)
    kubectl wait --for=condition=ready pod \
        -l app.kubernetes.io/name=todo-chatbot \
        --timeout=300s

    echo ""
    echo "=========================================="
    echo "Deployment Complete!"
    echo "=========================================="
    echo ""
    echo "Access the application:"
    echo "  Frontend: http://localhost:30080"
    echo "  Backend API: http://localhost:30081"
    echo "  API Docs: http://localhost:30081/docs"
    echo ""
    echo "Check status:"
    echo "  kubectl get pods -l app.kubernetes.io/name=todo-chatbot"
    echo "  kubectl get services -l app.kubernetes.io/name=todo-chatbot"
    echo ""
    echo "View logs:"
    echo "  kubectl logs -l app.kubernetes.io/component=frontend"
    echo "  kubectl logs -l app.kubernetes.io/component=backend"
    echo ""
    echo "Run verification:"
    echo "  ./verify.sh"
else
    echo "✗ Deployment failed"
    exit 1
fi
