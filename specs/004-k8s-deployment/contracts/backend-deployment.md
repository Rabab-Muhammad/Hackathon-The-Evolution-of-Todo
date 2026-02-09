# Backend Deployment Contract

**Feature**: 004-k8s-deployment
**Component**: Backend (FastAPI Application)
**Date**: 2026-02-09

## Purpose

Define the Kubernetes deployment specification for the FastAPI backend application, including resource requirements, configuration, health checks, database connectivity, and service exposure.

## Kubernetes Resources

### Deployment

**Resource Type**: `apps/v1/Deployment`

**Metadata**:
- Name: `{release-name}-todo-chatbot-backend`
- Labels: Standard Helm labels + `app.kubernetes.io/component: backend`

**Specification**:
- **Replicas**: Configurable via `backend.replicaCount` (default: 2)
- **Selector**: Matches `app.kubernetes.io/name` and `app.kubernetes.io/component: backend`
- **Strategy**: RollingUpdate (maxSurge: 1, maxUnavailable: 0)

**Pod Template**:
- **Container Name**: `backend`
- **Image**: `{backend.image.repository}:{backend.image.tag}`
- **Image Pull Policy**: `{backend.image.pullPolicy}` (default: IfNotPresent)
- **Port**: 8000 (HTTP)
- **Security Context**: Run as non-root user (UID 1001)

### Service

**Resource Type**: `v1/Service`

**Metadata**:
- Name: `{release-name}-todo-chatbot-backend`
- Labels: Standard Helm labels + `app.kubernetes.io/component: backend`

**Specification**:
- **Type**: NodePort (for Minikube local access and frontend connectivity)
- **Port**: 8000 (service port)
- **Target Port**: 8000 (container port)
- **Node Port**: 30081 (fixed for consistency)
- **Selector**: Matches backend pods

### ConfigMap

**Resource Type**: `v1/ConfigMap`

**Metadata**:
- Name: `{release-name}-todo-chatbot-backend-config`

**Data**:
- `ENVIRONMENT`: Environment name (development, staging, production)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- Additional non-sensitive environment variables

### Secret

**Resource Type**: `v1/Secret`

**Metadata**:
- Name: `{release-name}-todo-chatbot-backend-secret`

**Type**: `Opaque`

**Data** (base64 encoded):
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (must match frontend)
- `NEXT_PUBLIC_OPENROUTER_KEY`: OpenRouter API key (if needed by backend)

## Configuration Parameters

### Image Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend.image.repository` | string | `todo-chatbot-backend` | Container image repository |
| `backend.image.tag` | string | `latest` | Container image tag |
| `backend.image.pullPolicy` | string | `IfNotPresent` | Image pull policy |

### Replica Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend.replicaCount` | integer | `2` | Number of pod replicas |

### Resource Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend.resources.limits.cpu` | string | `1000m` | Maximum CPU allocation (1 core) |
| `backend.resources.limits.memory` | string | `1Gi` | Maximum memory allocation |
| `backend.resources.requests.cpu` | string | `500m` | Requested CPU allocation |
| `backend.resources.requests.memory` | string | `512Mi` | Requested memory allocation |

### Service Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend.service.type` | string | `NodePort` | Kubernetes service type |
| `backend.service.port` | integer | `8000` | Service port |
| `backend.service.nodePort` | integer | `30081` | NodePort for external access |

### Environment Configuration

| Parameter | Type | Default | Description | Source |
|-----------|------|---------|-------------|--------|
| `backend.env.ENVIRONMENT` | string | `development` | Environment name | ConfigMap |
| `backend.env.LOG_LEVEL` | string | `INFO` | Logging level | ConfigMap |
| `backend.secrets.DATABASE_URL` | string | (required) | PostgreSQL connection string | Secret |
| `backend.secrets.BETTER_AUTH_SECRET` | string | (required) | JWT signing secret | Secret |

## Health Checks

### Liveness Probe

**Purpose**: Determine if the container is running and should be restarted if unhealthy.

**Configuration**:
- **Type**: HTTP GET
- **Path**: `/api/health`
- **Port**: 8000
- **Initial Delay**: 15 seconds (longer than frontend due to database connection)
- **Period**: 10 seconds
- **Timeout**: 5 seconds
- **Success Threshold**: 1
- **Failure Threshold**: 3

**Behavior**: If probe fails 3 consecutive times, Kubernetes restarts the container.

**Health Endpoint Requirements**:
- Must return HTTP 200 when application is healthy
- Should check database connectivity
- Should be lightweight (no heavy operations)

### Readiness Probe

**Purpose**: Determine if the container is ready to accept traffic.

**Configuration**:
- **Type**: HTTP GET
- **Path**: `/api/health`
- **Port**: 8000
- **Initial Delay**: 15 seconds
- **Period**: 10 seconds
- **Timeout**: 5 seconds
- **Success Threshold**: 1
- **Failure Threshold**: 3

**Behavior**: If probe fails, pod is removed from service endpoints until it passes again.

**Readiness Criteria**:
- Application server is running
- Database connection is established
- All critical dependencies are available

## Security Requirements

### Container Security

- **Run as Non-Root**: Container must run as user ID 1001 (appuser)
- **Read-Only Root Filesystem**: Not enforced (application may need write access for logs)
- **Drop Capabilities**: Drop all capabilities
- **No Privilege Escalation**: `allowPrivilegeEscalation: false`

### Secret Management

- **DATABASE_URL**: Must be provided via Kubernetes Secret (contains credentials)
- **BETTER_AUTH_SECRET**: Must be provided via Kubernetes Secret (32+ characters)
- **No Hardcoded Secrets**: Container image must not contain any secrets
- **Environment Variable Injection**: Secrets injected at runtime via Secret references

### Network Security

- **Database Access**: Backend must be able to reach external Neon PostgreSQL
- **Egress Rules**: Allow outbound HTTPS (443) for database and API calls
- **Ingress Rules**: Allow inbound HTTP (8000) from frontend pods and NodePort

## Scaling Behavior

### Horizontal Scaling

- **Manual Scaling**: Adjust `backend.replicaCount` in values.yaml
- **Deployment Command**: `helm upgrade todo-chatbot ./helm/todo-chatbot --set backend.replicaCount=4`
- **Expected Behavior**: New pods created within 30-60 seconds
- **Load Balancing**: Service automatically distributes traffic across all healthy pods
- **Stateless Requirement**: All pods must be stateless (no in-memory session state)

### Database Connection Pooling

- **Connection Pool**: Each pod maintains its own connection pool to database
- **Pool Size**: Configure based on expected load (default: 10 connections per pod)
- **Scaling Consideration**: Total database connections = replicaCount × poolSize
- **Database Limits**: Ensure Neon PostgreSQL can handle total connections

### Resource Limits

- **CPU Throttling**: If pod exceeds CPU limit, it is throttled (not terminated)
- **Memory Limits**: If pod exceeds memory limit, it is terminated and restarted
- **Recommended Limits**: Set based on observed usage + 20% buffer

## Access Patterns

### From Host Machine

- **URL**: `http://localhost:30081`
- **API Docs**: `http://localhost:30081/docs` (FastAPI Swagger UI)
- **Alternative**: `minikube service todo-chatbot-backend --url`

### From Frontend Pods (within cluster)

- **Service DNS**: `todo-chatbot-backend.default.svc.cluster.local:8000`
- **Short DNS**: `todo-chatbot-backend:8000` (within same namespace)
- **Recommended**: Use short DNS for internal communication

### From External (via NodePort)

- **URL**: `http://localhost:30081`
- **Use Case**: Direct API testing, frontend running on host machine

## Database Connectivity

### Connection Requirements

- **Protocol**: PostgreSQL wire protocol (port 5432)
- **TLS**: Required for Neon PostgreSQL
- **Connection String Format**: `postgresql://user:password@host.neon.tech:5432/database?sslmode=require`

### Connection Validation

**Startup Check**:
1. Application attempts database connection on startup
2. If connection fails, application logs error and exits (pod restarts)
3. Readiness probe prevents traffic until connection succeeds

**Runtime Monitoring**:
1. Health endpoint checks database connectivity
2. If database becomes unavailable, health check fails
3. Pod marked as not ready, traffic stops
4. Pod attempts reconnection automatically

### Network Access from Minikube

**Requirement**: Minikube cluster must be able to reach external Neon PostgreSQL

**Verification**:
```bash
# From within a pod:
kubectl exec -it <backend-pod> -- curl -v telnet://host.neon.tech:5432
```

**Potential Issues**:
- Firewall blocking outbound connections
- DNS resolution failures
- Network policies blocking egress

## Verification Steps

### Deployment Verification

1. **Check Deployment Status**:
   ```bash
   kubectl get deployment todo-chatbot-backend
   ```
   Expected: `READY 2/2`, `UP-TO-DATE 2`, `AVAILABLE 2`

2. **Check Pod Status**:
   ```bash
   kubectl get pods -l app.kubernetes.io/component=backend
   ```
   Expected: `STATUS Running`, `READY 1/1` for all pods

3. **Check Service**:
   ```bash
   kubectl get service todo-chatbot-backend
   ```
   Expected: `TYPE NodePort`, `PORT(S) 8000:30081/TCP`

### Functional Verification

1. **Access Health Endpoint**:
   ```bash
   curl http://localhost:30081/api/health
   ```
   Expected: HTTP 200, JSON response with health status

2. **Access API Documentation**:
   ```bash
   curl http://localhost:30081/docs
   ```
   Expected: HTTP 200, HTML response (Swagger UI)

3. **Check Database Connectivity**:
   ```bash
   kubectl logs -l app.kubernetes.io/component=backend | grep -i database
   ```
   Expected: Successful database connection logs, no errors

4. **Test API Endpoint**:
   ```bash
   curl http://localhost:30081/api/tasks
   ```
   Expected: HTTP 401 (unauthorized - requires JWT token)

### Load Balancing Verification

1. **Check Endpoints**:
   ```bash
   kubectl get endpoints todo-chatbot-backend
   ```
   Expected: Multiple IP addresses (one per pod)

2. **Test Load Distribution**:
   ```bash
   for i in {1..10}; do curl -s http://localhost:30081/api/health | grep -o "pod-name"; done
   ```
   Expected: Requests distributed across different pods

## Troubleshooting

### Pod Not Starting

**Symptoms**: Pod stuck in `Pending`, `ContainerCreating`, or `CrashLoopBackOff`

**Checks**:
1. Image pull issues: `kubectl describe pod <pod-name>` (check Events)
2. Resource constraints: `kubectl describe node minikube` (check Allocated resources)
3. Configuration errors: `kubectl logs <pod-name>` (check application logs)
4. Secret missing: `kubectl get secret todo-chatbot-backend-secret`

### Database Connection Failures

**Symptoms**: Pods crash on startup, health checks fail, logs show database errors

**Checks**:
1. DATABASE_URL correct: `kubectl get secret todo-chatbot-backend-secret -o yaml` (decode base64)
2. Network connectivity: `kubectl exec -it <pod> -- ping host.neon.tech`
3. Database accessible: Check Neon dashboard for connection limits, IP allowlist
4. Connection string format: Ensure `sslmode=require` is included

### Service Not Accessible

**Symptoms**: Cannot access `http://localhost:30081`

**Checks**:
1. Service exists: `kubectl get service todo-chatbot-backend`
2. Endpoints exist: `kubectl get endpoints todo-chatbot-backend`
3. Pods are ready: `kubectl get pods -l app.kubernetes.io/component=backend`
4. Minikube running: `minikube status`

### Health Check Failures

**Symptoms**: Pods restart frequently, readiness probe failing

**Checks**:
1. Health endpoint working: `kubectl exec -it <pod> -- curl localhost:8000/api/health`
2. Database connectivity: Check logs for database errors
3. Resource limits: Ensure pod has sufficient CPU/memory
4. Initial delay: Increase if application takes longer to start

### High Memory Usage

**Symptoms**: Pods terminated with OOMKilled, memory limit exceeded

**Checks**:
1. Memory usage: `kubectl top pod -l app.kubernetes.io/component=backend`
2. Memory leaks: Check application logs for unusual patterns
3. Connection pool size: Reduce if too many database connections
4. Increase limits: Adjust `backend.resources.limits.memory` if needed

## Dependencies

- **Database**: Neon PostgreSQL must be accessible from Minikube cluster
- **Secrets**: `DATABASE_URL` and `BETTER_AUTH_SECRET` must be provided
- **Frontend**: Frontend depends on backend API being available
- **Network**: Outbound HTTPS access required for database and external APIs

## References

- Specification: [spec.md](../spec.md) - FR-001 to FR-008, FR-029 to FR-034, FR-037 to FR-039
- Research: [research.md](../research.md) - R1 (Docker builds), R3 (Service exposure), R5 (Environment variables)
- Helm Values: [helm-values-schema.md](./helm-values-schema.md)
