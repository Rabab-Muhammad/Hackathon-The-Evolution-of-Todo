# Quickstart: Deploy Todo Chatbot to Minikube

**Feature**: 004-k8s-deployment
**Date**: 2026-02-09
**Purpose**: Step-by-step guide for deploying the AI-powered Todo Chatbot to a local Minikube cluster

## Overview

This guide walks you through deploying the Phase III Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm. The deployment includes containerized frontend and backend applications with externalized configuration.

**Estimated Time**: 30-45 minutes (first-time setup)

**Prerequisites**: Basic familiarity with command line, Docker, and Kubernetes concepts

---

## Prerequisites

### Required Software

Verify the following tools are installed:

| Tool | Minimum Version | Check Command | Installation |
|------|----------------|---------------|--------------|
| Docker Desktop | 20.10+ | `docker --version` | https://docs.docker.com/get-docker/ |
| Minikube | 1.25+ | `minikube version` | https://minikube.sigs.k8s.io/docs/start/ |
| kubectl | 1.25+ | `kubectl version --client` | https://kubernetes.io/docs/tasks/tools/ |
| Helm | 3.0+ | `helm version` | https://helm.sh/docs/intro/install/ |

### Optional AI Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Docker AI (Gordon) | Dockerfile optimization | https://github.com/docker/gordon |
| kubectl-ai | AI-assisted Kubernetes operations | https://github.com/sozercan/kubectl-ai |
| Kagent | Cluster health analysis | https://github.com/kagent/kagent |

**Note**: AI tools are optional. Standard CLI commands are provided as fallbacks.

### System Requirements

- **CPU**: 2+ cores available for Minikube
- **Memory**: 4GB+ RAM available for Minikube
- **Disk**: 20GB+ free space
- **Network**: Internet access for pulling images and accessing database

---

## Step 1: Start Minikube

### 1.1 Start Minikube Cluster

```bash
minikube start --cpus=2 --memory=4096
```

**Expected Output**:
```
😄  minikube v1.32.0 on Darwin 14.0
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

### 1.2 Verify Cluster Status

```bash
minikube status
```

**Expected Output**:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### 1.3 Enable Metrics (Optional)

For resource monitoring:

```bash
minikube addons enable metrics-server
```

---

## Step 2: Build Container Images

### 2.1 Configure Docker to Use Minikube's Docker Daemon

This allows images to be built directly in Minikube without pushing to a registry:

```bash
eval $(minikube docker-env)
```

**Verification**:
```bash
docker ps
# Should show Minikube's containers
```

### 2.2 Build Frontend Image

**Option A: Using Docker AI (Gordon)** - If available:
```bash
gordon build --app frontend --framework nextjs --tag todo-chatbot-frontend:latest
```

**Option B: Standard Docker Build**:
```bash
docker build -f deployment/docker/frontend.Dockerfile -t todo-chatbot-frontend:latest ./frontend
```

**Expected Output**:
```
[+] Building 180.5s (15/15) FINISHED
 => [internal] load build definition from frontend.Dockerfile
 => => transferring dockerfile: 1.2kB
 => [internal] load .dockerignore
 => [stage-2 1/5] FROM docker.io/library/node:20-alpine
 => CACHED [stage-2 2/5] WORKDIR /app
 => [stage-2 3/5] COPY --from=builder /app/.next/standalone ./
 => [stage-2 4/5] COPY --from=builder /app/.next/static ./.next/static
 => [stage-2 5/5] COPY --from=builder /app/public ./public
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/todo-chatbot-frontend:latest
```

**Verify Image**:
```bash
docker images | grep todo-chatbot-frontend
```

### 2.3 Build Backend Image

**Option A: Using Docker AI (Gordon)** - If available:
```bash
gordon build --app backend --framework fastapi --tag todo-chatbot-backend:latest
```

**Option B: Standard Docker Build**:
```bash
docker build -f deployment/docker/backend.Dockerfile -t todo-chatbot-backend:latest ./backend
```

**Verify Image**:
```bash
docker images | grep todo-chatbot-backend
```

---

## Step 3: Configure Deployment

### 3.1 Create values-dev.yaml

Create a file at `deployment/helm/todo-chatbot/values-dev.yaml`:

```yaml
global:
  environment: development

frontend:
  replicaCount: 1
  env:
    NEXT_PUBLIC_API_URL: http://localhost:30081

backend:
  replicaCount: 1
  env:
    LOG_LEVEL: DEBUG
  secrets:
    # REQUIRED: Replace with your actual values
    DATABASE_URL: "postgresql://user:password@host.neon.tech:5432/database?sslmode=require"
    BETTER_AUTH_SECRET: "your-32-character-secret-here-change-this"
    NEXT_PUBLIC_OPENROUTER_KEY: "sk-or-v1-your-key-here"
```

**Important**:
- Replace `DATABASE_URL` with your Neon PostgreSQL connection string
- Replace `BETTER_AUTH_SECRET` with a secure 32+ character string
- Replace `NEXT_PUBLIC_OPENROUTER_KEY` with your OpenRouter API key

### 3.2 Add values-dev.yaml to .gitignore

**CRITICAL**: Never commit secrets to version control!

```bash
echo "deployment/helm/todo-chatbot/values-dev.yaml" >> .gitignore
```

### 3.3 Verify Configuration

```bash
helm lint deployment/helm/todo-chatbot -f deployment/helm/todo-chatbot/values-dev.yaml
```

**Expected Output**:
```
==> Linting deployment/helm/todo-chatbot
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

---

## Step 4: Deploy to Minikube

### 4.1 Install Helm Chart

```bash
helm install todo-chatbot deployment/helm/todo-chatbot -f deployment/helm/todo-chatbot/values-dev.yaml
```

**Expected Output**:
```
NAME: todo-chatbot
LAST DEPLOYED: Sun Feb  9 20:00:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Thank you for installing todo-chatbot!

Your release is named todo-chatbot.

To access the application:
  Frontend: http://localhost:30080
  Backend API: http://localhost:30081
  API Docs: http://localhost:30081/docs

To check the status:
  kubectl get pods -l app.kubernetes.io/name=todo-chatbot
```

### 4.2 Watch Deployment Progress

```bash
kubectl get pods -w
```

**Expected Output** (after 1-2 minutes):
```
NAME                                        READY   STATUS    RESTARTS   AGE
todo-chatbot-frontend-7d8f9c5b6d-x7k2m     1/1     Running   0          90s
todo-chatbot-backend-6c9d8b4f5e-p3m9n      1/1     Running   0          90s
todo-chatbot-backend-6c9d8b4f5e-q4n8p      1/1     Running   0          90s
```

Press `Ctrl+C` to stop watching.

---

## Step 5: Verify Deployment

### 5.1 Check Deployment Status

```bash
kubectl get deployments
```

**Expected Output**:
```
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
todo-chatbot-frontend   1/1     1            1           2m
todo-chatbot-backend    2/2     2            2           2m
```

### 5.2 Check Services

```bash
kubectl get services
```

**Expected Output**:
```
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes              ClusterIP   10.96.0.1       <none>        443/TCP          10m
todo-chatbot-frontend   NodePort    10.96.123.45    <none>        3000:30080/TCP   2m
todo-chatbot-backend    NodePort    10.96.234.56    <none>        8000:30081/TCP   2m
```

### 5.3 Check Pod Health

```bash
kubectl get pods -l app.kubernetes.io/name=todo-chatbot
```

All pods should show `READY 1/1` and `STATUS Running`.

### 5.4 Check Pod Logs

**Frontend logs**:
```bash
kubectl logs -l app.kubernetes.io/component=frontend --tail=20
```

**Backend logs**:
```bash
kubectl logs -l app.kubernetes.io/component=backend --tail=20
```

Look for successful startup messages and no errors.

---

## Step 6: Access the Application

### 6.1 Access Frontend

Open your browser and navigate to:
```
http://localhost:30080
```

You should see the Todo Chatbot UI.

### 6.2 Access Backend API

Open your browser and navigate to:
```
http://localhost:30081/docs
```

You should see the FastAPI Swagger documentation.

### 6.3 Test Health Endpoints

**Frontend health**:
```bash
curl http://localhost:30080/
```

**Backend health**:
```bash
curl http://localhost:30081/api/health
```

Both should return HTTP 200.

---

## Step 7: Test Application Functionality

### 7.1 Sign Up

1. Navigate to `http://localhost:30080/signup`
2. Create a new account
3. Verify you're redirected to the dashboard or chat

### 7.2 Test AI Chatbot

1. Navigate to `http://localhost:30080/chat`
2. Try natural language commands:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark buy groceries as complete"

### 7.3 Verify Database Connectivity

Check backend logs for database connection:
```bash
kubectl logs -l app.kubernetes.io/component=backend | grep -i database
```

Should show successful connection messages.

---

## Step 8: Scale the Application

### 8.1 Scale Backend Replicas

**Option A: Using kubectl-ai** - If available:
```bash
kubectl-ai "scale backend to 4 replicas"
```

**Option B: Standard kubectl**:
```bash
kubectl scale deployment todo-chatbot-backend --replicas=4
```

### 8.2 Verify Scaling

```bash
kubectl get pods -l app.kubernetes.io/component=backend
```

Should show 4 backend pods running.

### 8.3 Scale via Helm

```bash
helm upgrade todo-chatbot deployment/helm/todo-chatbot \
  -f deployment/helm/todo-chatbot/values-dev.yaml \
  --set backend.replicaCount=3
```

---

## Troubleshooting

### Pods Not Starting

**Check pod status**:
```bash
kubectl describe pod <pod-name>
```

**Common issues**:
- Image pull errors: Verify images exist (`docker images`)
- Resource constraints: Check Minikube resources (`minikube status`)
- Configuration errors: Check logs (`kubectl logs <pod-name>`)

### Cannot Access Application

**Check Minikube IP**:
```bash
minikube ip
```

If not `localhost`, use the returned IP instead.

**Check service**:
```bash
minikube service todo-chatbot-frontend --url
```

Use the returned URL to access the frontend.

### Database Connection Failures

**Verify DATABASE_URL**:
```bash
kubectl get secret todo-chatbot-backend-secret -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

**Test connectivity from pod**:
```bash
kubectl exec -it <backend-pod> -- curl -v telnet://host.neon.tech:5432
```

### Health Check Failures

**Check health endpoint directly**:
```bash
kubectl exec -it <pod-name> -- curl localhost:3000/  # Frontend
kubectl exec -it <pod-name> -- curl localhost:8000/api/health  # Backend
```

---

## Cleanup

### Uninstall Helm Chart

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

---

## Next Steps

- **Production Deployment**: Adapt for cloud providers (AWS EKS, GCP GKE, Azure AKS)
- **Monitoring**: Add Prometheus and Grafana for observability
- **CI/CD**: Automate builds and deployments
- **Ingress**: Configure Ingress controller for production-like routing
- **Secrets Management**: Use external secret stores (Vault, AWS Secrets Manager)

---

## References

- Specification: [spec.md](./spec.md)
- Implementation Plan: [plan.md](./plan.md)
- Research: [research.md](./research.md)
- Contracts: [contracts/](./contracts/)
- Minikube Documentation: https://minikube.sigs.k8s.io/docs/
- Helm Documentation: https://helm.sh/docs/
- Kubernetes Documentation: https://kubernetes.io/docs/
