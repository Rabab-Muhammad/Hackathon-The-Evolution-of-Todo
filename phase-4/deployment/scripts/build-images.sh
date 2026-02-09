#!/bin/bash
# Build container images for Todo Chatbot
# Usage: ./build-images.sh [--push]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOYMENT_DIR="$REPO_ROOT/deployment"

echo "=========================================="
echo "Building Todo Chatbot Container Images"
echo "=========================================="

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if using Minikube's Docker daemon
if [ -n "$MINIKUBE_ACTIVE_DOCKERD" ]; then
    echo "✓ Using Minikube's Docker daemon"
else
    echo "WARNING: Not using Minikube's Docker daemon."
    echo "Run: eval \$(minikube docker-env)"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build frontend image
echo ""
echo "Building frontend image..."
docker build \
    -f "$DEPLOYMENT_DIR/docker/frontend.Dockerfile" \
    -t todo-chatbot-frontend:latest \
    "$REPO_ROOT/frontend"

if [ $? -eq 0 ]; then
    echo "✓ Frontend image built successfully"
else
    echo "✗ Frontend image build failed"
    exit 1
fi

# Build backend image
echo ""
echo "Building backend image..."
docker build \
    -f "$DEPLOYMENT_DIR/docker/backend.Dockerfile" \
    -t todo-chatbot-backend:latest \
    "$REPO_ROOT/backend"

if [ $? -eq 0 ]; then
    echo "✓ Backend image built successfully"
else
    echo "✗ Backend image build failed"
    exit 1
fi

# Display image information
echo ""
echo "=========================================="
echo "Image Build Summary"
echo "=========================================="
docker images | grep todo-chatbot

echo ""
echo "✓ All images built successfully!"
echo ""
echo "Next steps:"
echo "  1. Create deployment/helm/todo-chatbot/values-dev.yaml with your secrets"
echo "  2. Run: ./deploy.sh"
