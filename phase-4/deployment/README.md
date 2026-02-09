# Phase IV - Kubernetes Deployment

Complete Kubernetes deployment setup for the Evolution of Todo AI-Powered Chatbot application.

## 📋 Overview

This directory contains all the necessary files to deploy the Todo application to a Kubernetes cluster using Helm charts. The deployment includes:

- **Frontend**: Next.js 16 application with AI chatbot interface
- **Backend**: FastAPI server with OpenAI Agents SDK (deployed separately on Hugging Face Space)
- **Database**: Neon PostgreSQL (external managed service)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                    │
│  ┌────────────────────┐      ┌────────────────────┐    │
│  │  Frontend Pods     │      │  Backend Pods      │    │
│  │  (Next.js 16)      │      │  (FastAPI)         │    │
│  │  Replicas: 1       │      │  Replicas: 2       │    │
│  └────────────────────┘      └────────────────────┘    │
│           │                           │                  │
│  ┌────────────────────┐      ┌────────────────────┐    │
│  │  Frontend Service  │      │  Backend Service   │    │
│  │  NodePort: 30080   │      │  NodePort: 30081   │    │
│  └────────────────────┘      └────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
            User Browser          Hugging Face Space Backend
                                           │
                                           ▼
                                  Neon PostgreSQL Database
```

## 📁 Directory Structure

```
phase-4/deployment/
├── docker/                      # Dockerfiles
│   ├── frontend.Dockerfile      # Multi-stage build for Next.js
│   └── backend.Dockerfile       # Multi-stage build for FastAPI
├── helm/                        # Helm chart
│   └── todo-chatbot/
│       ├── Chart.yaml           # Chart metadata
│       ├── values.yaml          # Default configuration
│       ├── values-dev.yaml.example  # Example dev values
│       └── templates/           # Kubernetes manifests
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── configmap.yaml
│           └── secrets.yaml
├── scripts/                     # Automation scripts
│   ├── build-images.sh          # Build Docker images
│   ├── deploy.sh                # Deploy to Kubernetes
│   ├── verify.sh                # Verify deployment
│   └── scale.sh                 # Scale replicas
├── frontend/                    # Frontend source (for building)
├── backend/                     # Backend source (for building)
├── CLAUDE.md                    # AI agent instructions
├── DEPLOYMENT_REPORT.md         # Deployment verification report
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Docker Desktop** - Running and configured
2. **Minikube** - v1.38.0 or higher
3. **Helm** - v3.0 or higher
4. **kubectl** - Configured to work with Minikube

### Installation Steps

```bash
# 1. Start Minikube
minikube start --cpus=2 --memory=3072

# 2. Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# 3. Build Docker images
cd scripts
./build-images.sh

# 4. Create values file with your secrets
cd ../helm/todo-chatbot
cp values-dev.yaml.example values-dev.yaml
# Edit values-dev.yaml with your actual credentials

# 5. Deploy using Helm
cd ../../scripts
./deploy.sh

# 6. Verify deployment
./verify.sh
```

### Access the Application

**Option 1: Port Forwarding (Recommended - Fixed URL)**
```bash
# Frontend
kubectl port-forward service/todo-chatbot-frontend 3000:3000

# Access at: http://localhost:3000
```

**Option 2: Minikube Service (Dynamic URL)**
```bash
# Frontend
minikube service todo-chatbot-frontend --url

# Backend
minikube service todo-chatbot-backend --url
```

## 🔧 Configuration

### Environment Variables

Edit `helm/todo-chatbot/values.yaml` or create `values-dev.yaml`:

```yaml
frontend:
  env:
    NEXT_PUBLIC_API_URL: https://your-backend-url.com

backend:
  secrets:
    DATABASE_URL: postgresql://user:pass@host:5432/db
    BETTER_AUTH_SECRET: your-32-char-secret
    NEXT_PUBLIC_OPENROUTER_KEY: your-openrouter-key
```

### Scaling

```bash
# Scale backend to 4 replicas
cd scripts
./scale.sh backend 4

# Scale frontend to 2 replicas
./scale.sh frontend 2
```

## 🐳 Docker Images

### Frontend Image
- **Base**: node:20-alpine
- **Size**: ~207MB
- **Build**: Multi-stage (builder + runtime)
- **User**: nextjs (UID 1001)
- **Port**: 3000

### Backend Image
- **Base**: python:3.11-slim
- **Size**: ~228MB
- **Build**: Multi-stage (builder + runtime)
- **User**: appuser (UID 1001)
- **Port**: 8000

### Rebuild Images

```bash
# Configure Docker
eval $(minikube docker-env)

# Build frontend
docker build -f docker/frontend.Dockerfile -t todo-chatbot-frontend:latest ./frontend

# Build backend
docker build -f docker/backend.Dockerfile -t todo-chatbot-backend:latest ./backend

# Restart pods to use new images
kubectl delete pods -l app.kubernetes.io/component=frontend
kubectl delete pods -l app.kubernetes.io/component=backend
```

## 📊 Monitoring

### Check Pod Status
```bash
kubectl get pods -l app.kubernetes.io/name=todo-chatbot
```

### View Logs
```bash
# Frontend logs
kubectl logs -f -l app.kubernetes.io/component=frontend

# Backend logs
kubectl logs -f -l app.kubernetes.io/component=backend

# Last 50 lines
kubectl logs -l app.kubernetes.io/component=frontend --tail=50
```

### Check Services
```bash
kubectl get services -l app.kubernetes.io/name=todo-chatbot
```

### Resource Usage
```bash
kubectl top pods
```

## 🔍 Troubleshooting

### Pods Not Starting

```bash
# Describe pod to see events
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Check if images are available
docker images | grep todo-chatbot
```

### Port Forwarding Issues

```bash
# Update Minikube context
minikube update-context

# Restart Minikube
minikube stop
minikube start

# Check if services exist
kubectl get services
```

### Image Pull Errors

```bash
# Ensure Docker is using Minikube daemon
eval $(minikube docker-env)

# Rebuild images
cd scripts
./build-images.sh
```

### Authentication Not Working

1. Check if token is being stored correctly in localStorage
2. Verify backend URL in frontend configuration
3. Check browser console for errors
4. Verify JWT secret matches between frontend and backend

### Chat Not Working

1. Verify `NEXT_PUBLIC_API_URL` points to correct backend
2. Check if backend is accessible from browser
3. Verify OpenRouter API key is configured
4. Check backend logs for errors

## 🔄 Update Deployment

### Update Configuration
```bash
# Edit values
vim helm/todo-chatbot/values.yaml

# Upgrade deployment
helm upgrade todo-chatbot helm/todo-chatbot
```

### Update Code
```bash
# 1. Make changes to frontend/backend code
# 2. Rebuild images
eval $(minikube docker-env)
cd scripts
./build-images.sh

# 3. Restart pods
kubectl delete pods -l app.kubernetes.io/name=todo-chatbot
```

## 🗑️ Cleanup

### Uninstall Deployment
```bash
helm uninstall todo-chatbot
```

### Stop Minikube
```bash
minikube stop
```

### Delete Minikube Cluster
```bash
minikube delete
```

## 📝 Helm Chart Details

### Chart Information
- **Name**: todo-chatbot
- **Version**: 1.0.0
- **App Version**: 1.0.0

### Resources Created
- 2 Deployments (frontend, backend)
- 2 Services (NodePort)
- 1 ConfigMap (backend configuration)
- 1 Secret (sensitive credentials)

### Default Resource Limits

**Frontend**:
- Requests: 250m CPU, 256Mi Memory
- Limits: 500m CPU, 512Mi Memory

**Backend**:
- Requests: 200m CPU, 256Mi Memory
- Limits: 1000m CPU, 1Gi Memory

## 🔐 Security

### Best Practices Implemented
- ✅ Non-root container users (UID 1001)
- ✅ Secrets stored in Kubernetes Secrets (not in code)
- ✅ Multi-stage Docker builds (minimal attack surface)
- ✅ Health checks configured (liveness and readiness probes)
- ✅ Resource limits defined (prevent resource exhaustion)
- ✅ No hardcoded credentials

### Secrets Management
Never commit `values-dev.yaml` with real secrets to git. Use:
```bash
# Add to .gitignore
echo "values-dev.yaml" >> helm/todo-chatbot/.gitignore
```

## 📚 Additional Resources

- **Specification**: `../../specs/004-k8s-deployment/spec.md`
- **Implementation Plan**: `../../specs/004-k8s-deployment/plan.md`
- **Quickstart Guide**: `../../specs/004-k8s-deployment/quickstart.md`
- **Deployment Report**: `DEPLOYMENT_REPORT.md`
- **Constitution**: `../../.specify/memory/constitution.md`

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review deployment logs: `kubectl logs -l app.kubernetes.io/name=todo-chatbot`
3. Check Minikube status: `minikube status`
4. Verify Helm release: `helm status todo-chatbot`

## 📄 License

This deployment configuration is part of the Evolution of Todo project, following Spec-Driven Development principles.

---

**Generated with Claude Code** - All deployment artifacts are AI-generated following Phase IV specifications.
