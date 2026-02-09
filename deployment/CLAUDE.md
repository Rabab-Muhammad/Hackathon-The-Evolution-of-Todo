# Deployment Guide for Claude Code

This directory contains Kubernetes deployment artifacts for the Evolution of Todo application (Phase IV).

## Purpose

Deploy the Phase III AI-powered Todo Chatbot to a local Minikube cluster using containerization and Helm charts, following cloud-native infrastructure principles.

## Directory Structure

```
deployment/
├── CLAUDE.md              # This file - deployment guidance
├── .gitignore             # Excludes sensitive files (values-dev.yaml)
├── docker/                # Container image definitions
│   ├── frontend.Dockerfile    # Next.js multi-stage build
│   └── backend.Dockerfile     # FastAPI multi-stage build
├── helm/                  # Helm chart for Kubernetes deployment
│   └── todo-chatbot/
│       ├── Chart.yaml         # Chart metadata
│       ├── values.yaml        # Default configuration
│       ├── values-dev.yaml    # Development overrides (NOT in git)
│       ├── values-prod.yaml   # Production template
│       └── templates/         # Kubernetes manifests
│           ├── _helpers.tpl
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── configmap.yaml
│           ├── secrets.yaml
│           └── NOTES.txt
└── scripts/               # Deployment automation scripts
    ├── build-images.sh        # Build container images
    ├── deploy.sh              # Deploy to Minikube
    ├── verify.sh              # Verify deployment
    └── scale.sh               # Scale replicas
```

## Constitution Compliance

This deployment follows Constitution v2.2.0 principles:

- **Principle I (Spec-Driven)**: All artifacts generated from specs/004-k8s-deployment/
- **Principle III (Security)**: No hardcoded secrets, Kubernetes Secrets for sensitive data
- **Principle IV (Separation)**: Infrastructure isolated from application code (frontend/, backend/)
- **Principle VI (Stateless)**: Pods are ephemeral, external database (Neon PostgreSQL)
- **Principle IX (Cloud-Native)**: Containerization, Helm charts, Kubernetes deployment

## Key Standards

### Container Images

- **Multi-stage builds**: Separate build and runtime stages for minimal image size
- **Non-root users**: Containers run as UID 1001 (nextjs/appuser)
- **Base images**: node:20-alpine (frontend), python:3.11-slim (backend)
- **Image tags**: Use `latest` for development, semantic versioning for production

### Helm Charts

- **Parameterization**: All configuration via values.yaml
- **Environment-specific**: values-dev.yaml (local), values-prod.yaml (cloud)
- **Resource limits**: CPU and memory constraints defined
- **Health checks**: Liveness and readiness probes configured

### Configuration Management

- **ConfigMaps**: Non-sensitive configuration (log level, environment name)
- **Secrets**: Sensitive data (DATABASE_URL, BETTER_AUTH_SECRET, API keys)
- **Never commit**: values-dev.yaml contains secrets, excluded via .gitignore

### Service Exposure

- **Frontend**: NodePort 30080 (http://localhost:30080)
- **Backend**: NodePort 30081 (http://localhost:30081)
- **API Docs**: http://localhost:30081/docs

## Quick Start

### Prerequisites

- Docker Desktop running
- Minikube installed and started
- Helm 3+ installed
- kubectl configured

### Build Images

```bash
# Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# Build images
docker build -f deployment/docker/frontend.Dockerfile -t todo-chatbot-frontend:latest ./frontend
docker build -f deployment/docker/backend.Dockerfile -t todo-chatbot-backend:latest ./backend
```

### Configure Deployment

Create `deployment/helm/todo-chatbot/values-dev.yaml`:

```yaml
backend:
  secrets:
    DATABASE_URL: "postgresql://user:pass@host.neon.tech:5432/db?sslmode=require"
    BETTER_AUTH_SECRET: "your-32-character-secret-here"
    NEXT_PUBLIC_OPENROUTER_KEY: "sk-or-v1-your-key-here"
```

### Deploy to Minikube

```bash
# Install Helm chart
helm install todo-chatbot deployment/helm/todo-chatbot -f deployment/helm/todo-chatbot/values-dev.yaml

# Wait for pods to be ready
kubectl get pods -w

# Access application
open http://localhost:30080
```

### Verify Deployment

```bash
# Check deployment status
kubectl get deployments
kubectl get services
kubectl get pods

# Check logs
kubectl logs -l app.kubernetes.io/component=frontend
kubectl logs -l app.kubernetes.io/component=backend

# Test health endpoints
curl http://localhost:30080/
curl http://localhost:30081/api/health
```

## AI-Assisted DevOps Tools

This deployment supports optional AI-assisted tools with CLI fallbacks:

### Docker AI (Gordon)

- **Purpose**: Dockerfile generation and optimization
- **Usage**: `gordon build --app frontend --framework nextjs`
- **Fallback**: Standard `docker build` commands

### kubectl-ai

- **Purpose**: AI-assisted Kubernetes operations
- **Usage**: `kubectl-ai "scale backend to 4 replicas"`
- **Fallback**: Standard `kubectl` commands

### Kagent

- **Purpose**: Cluster health analysis and optimization
- **Usage**: `kagent analyze cluster`
- **Fallback**: Standard `kubectl top` commands

## Scaling

```bash
# Scale backend replicas
helm upgrade todo-chatbot deployment/helm/todo-chatbot --set backend.replicaCount=4

# Or use kubectl
kubectl scale deployment todo-chatbot-backend --replicas=4
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints

# Use Minikube service URL
minikube service todo-chatbot-frontend --url
```

### Database Connection Issues

```bash
# Verify secret
kubectl get secret todo-chatbot-backend-secret -o yaml

# Test connectivity from pod
kubectl exec -it <backend-pod> -- curl -v telnet://host.neon.tech:5432
```

## Cleanup

```bash
# Uninstall Helm chart
helm uninstall todo-chatbot

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## References

- **Specification**: specs/004-k8s-deployment/spec.md
- **Implementation Plan**: specs/004-k8s-deployment/plan.md
- **Research Findings**: specs/004-k8s-deployment/research.md
- **Deployment Contracts**: specs/004-k8s-deployment/contracts/
- **Quickstart Guide**: specs/004-k8s-deployment/quickstart.md
- **Constitution**: .specify/memory/constitution.md (v2.2.0)

## Notes

- All deployment artifacts are AI-generated following Spec-Driven Development
- No manual YAML editing - regenerate from specs if changes needed
- Secrets must be externalized in values-dev.yaml (never commit to git)
- Architecture is cloud-ready for future migration to AWS/GCP/Azure
