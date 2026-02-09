# Frontend Deployment Contract

**Feature**: 004-k8s-deployment
**Component**: Frontend (Next.js Application)
**Date**: 2026-02-09

## Purpose

Define the Kubernetes deployment specification for the Next.js frontend application, including resource requirements, configuration, health checks, and service exposure.

## Kubernetes Resources

### Deployment

**Resource Type**: `apps/v1/Deployment`

**Metadata**:
- Name: `{release-name}-todo-chatbot-frontend`
- Labels: Standard Helm labels + `app.kubernetes.io/component: frontend`

**Specification**:
- **Replicas**: Configurable via `frontend.replicaCount` (default: 1)
- **Selector**: Matches `app.kubernetes.io/name` and `app.kubernetes.io/component: frontend`
- **Strategy**: RollingUpdate (maxSurge: 1, maxUnavailable: 0)

**Pod Template**:
- **Container Name**: `frontend`
- **Image**: `{frontend.image.repository}:{frontend.image.tag}`
- **Image Pull Policy**: `{frontend.image.pullPolicy}` (default: IfNotPresent)
- **Port**: 3000 (HTTP)
- **Security Context**: Run as non-root user (UID 1001)

### Service

**Resource Type**: `v1/Service`

**Metadata**:
- Name: `{release-name}-todo-chatbot-frontend`
- Labels: Standard Helm labels + `app.kubernetes.io/component: frontend`

**Specification**:
- **Type**: NodePort (for Minikube local access)
- **Port**: 3000 (service port)
- **Target Port**: 3000 (container port)
- **Node Port**: 30080 (fixed for consistency)
- **Selector**: Matches frontend pods

### ConfigMap

**Resource Type**: `v1/ConfigMap`

**Metadata**:
- Name: `{release-name}-todo-chatbot-frontend-config`

**Data**:
- `NEXT_PUBLIC_API_URL`: Backend API URL (e.g., `http://localhost:30081`)
- Additional non-sensitive environment variables as needed

## Configuration Parameters

### Image Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frontend.image.repository` | string | `todo-chatbot-frontend` | Container image repository |
| `frontend.image.tag` | string | `latest` | Container image tag |
| `frontend.image.pullPolicy` | string | `IfNotPresent` | Image pull policy |

### Replica Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frontend.replicaCount` | integer | `1` | Number of pod replicas |

### Resource Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frontend.resources.limits.cpu` | string | `500m` | Maximum CPU allocation |
| `frontend.resources.limits.memory` | string | `512Mi` | Maximum memory allocation |
| `frontend.resources.requests.cpu` | string | `250m` | Requested CPU allocation |
| `frontend.resources.requests.memory` | string | `256Mi` | Requested memory allocation |

### Service Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frontend.service.type` | string | `NodePort` | Kubernetes service type |
| `frontend.service.port` | integer | `3000` | Service port |
| `frontend.service.nodePort` | integer | `30080` | NodePort for external access |

### Environment Configuration

| Parameter | Type | Default | Description | Source |
|-----------|------|---------|-------------|--------|
| `frontend.env.NEXT_PUBLIC_API_URL` | string | `http://localhost:30081` | Backend API URL | ConfigMap |
| `frontend.env.BETTER_AUTH_SECRET` | string | (required) | JWT signing secret | Secret |

## Health Checks

### Liveness Probe

**Purpose**: Determine if the container is running and should be restarted if unhealthy.

**Configuration**:
- **Type**: HTTP GET
- **Path**: `/`
- **Port**: 3000
- **Initial Delay**: 10 seconds
- **Period**: 10 seconds
- **Timeout**: 5 seconds
- **Success Threshold**: 1
- **Failure Threshold**: 3

**Behavior**: If probe fails 3 consecutive times, Kubernetes restarts the container.

### Readiness Probe

**Purpose**: Determine if the container is ready to accept traffic.

**Configuration**:
- **Type**: HTTP GET
- **Path**: `/`
- **Port**: 3000
- **Initial Delay**: 10 seconds
- **Period**: 10 seconds
- **Timeout**: 5 seconds
- **Success Threshold**: 1
- **Failure Threshold**: 3

**Behavior**: If probe fails, pod is removed from service endpoints until it passes again.

## Security Requirements

### Container Security

- **Run as Non-Root**: Container must run as user ID 1001 (nextjs)
- **Read-Only Root Filesystem**: Not enforced (Next.js requires write access to .next directory)
- **Drop Capabilities**: Drop all capabilities except NET_BIND_SERVICE if needed
- **No Privilege Escalation**: `allowPrivilegeEscalation: false`

### Secret Management

- **BETTER_AUTH_SECRET**: Must be provided via Kubernetes Secret
- **No Hardcoded Secrets**: Container image must not contain any secrets
- **Environment Variable Injection**: Secrets injected at runtime via Secret references

## Scaling Behavior

### Horizontal Scaling

- **Manual Scaling**: Adjust `frontend.replicaCount` in values.yaml
- **Deployment Command**: `helm upgrade todo-chatbot ./helm/todo-chatbot --set frontend.replicaCount=3`
- **Expected Behavior**: New pods created within 30-60 seconds
- **Load Balancing**: Service automatically distributes traffic across all healthy pods

### Resource Limits

- **CPU Throttling**: If pod exceeds CPU limit, it is throttled (not terminated)
- **Memory Limits**: If pod exceeds memory limit, it is terminated and restarted
- **Recommended Limits**: Set based on observed usage + 20% buffer

## Access Patterns

### From Host Machine

- **URL**: `http://localhost:30080`
- **Alternative**: `minikube service todo-chatbot-frontend --url`

### From Other Pods (within cluster)

- **Service DNS**: `todo-chatbot-frontend.default.svc.cluster.local:3000`
- **Short DNS**: `todo-chatbot-frontend:3000` (within same namespace)

## Verification Steps

### Deployment Verification

1. **Check Deployment Status**:
   ```bash
   kubectl get deployment todo-chatbot-frontend
   ```
   Expected: `READY 1/1`, `UP-TO-DATE 1`, `AVAILABLE 1`

2. **Check Pod Status**:
   ```bash
   kubectl get pods -l app.kubernetes.io/component=frontend
   ```
   Expected: `STATUS Running`, `READY 1/1`

3. **Check Service**:
   ```bash
   kubectl get service todo-chatbot-frontend
   ```
   Expected: `TYPE NodePort`, `PORT(S) 3000:30080/TCP`

### Functional Verification

1. **Access Frontend**:
   ```bash
   curl http://localhost:30080
   ```
   Expected: HTTP 200, HTML response

2. **Check Logs**:
   ```bash
   kubectl logs -l app.kubernetes.io/component=frontend
   ```
   Expected: Next.js server startup logs, no errors

3. **Test Health Endpoint**:
   ```bash
   curl http://localhost:30080/
   ```
   Expected: HTTP 200

## Troubleshooting

### Pod Not Starting

**Symptoms**: Pod stuck in `Pending`, `ContainerCreating`, or `CrashLoopBackOff`

**Checks**:
1. Image pull issues: `kubectl describe pod <pod-name>` (check Events)
2. Resource constraints: `kubectl describe node minikube` (check Allocated resources)
3. Configuration errors: `kubectl logs <pod-name>` (check application logs)

### Service Not Accessible

**Symptoms**: Cannot access `http://localhost:30080`

**Checks**:
1. Service exists: `kubectl get service todo-chatbot-frontend`
2. Endpoints exist: `kubectl get endpoints todo-chatbot-frontend`
3. Pod is ready: `kubectl get pods -l app.kubernetes.io/component=frontend`
4. Minikube tunnel: Ensure Minikube is running and accessible

### Health Check Failures

**Symptoms**: Pod restarts frequently, readiness probe failing

**Checks**:
1. Application startup time: Increase `initialDelaySeconds` if app takes longer to start
2. Application health: Check logs for errors during startup
3. Resource limits: Ensure pod has sufficient CPU/memory

## Dependencies

- **Backend Service**: Frontend requires backend API to be accessible
- **Database**: Backend must be connected to database for full functionality
- **Secrets**: `BETTER_AUTH_SECRET` must be provided in values.yaml

## References

- Specification: [spec.md](../spec.md) - FR-001 to FR-008, FR-035 to FR-036
- Research: [research.md](../research.md) - R1 (Docker builds), R3 (Service exposure)
- Helm Values: [helm-values-schema.md](./helm-values-schema.md)
