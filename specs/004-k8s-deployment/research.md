# Research: Local Kubernetes Deployment

**Feature**: 004-k8s-deployment
**Date**: 2026-02-09
**Purpose**: Research findings for deploying Todo Chatbot to Minikube with AI-assisted DevOps tools

## Research Summary

This document consolidates research findings for Phase IV deployment decisions, covering Docker containerization, Helm charts, Minikube networking, AI DevOps tools, and Kubernetes configuration management.

---

## R1: Docker Multi-Stage Build Best Practices

### Decision: Use Multi-Stage Builds with Official Base Images

**Rationale**:
- Multi-stage builds separate build dependencies from runtime, reducing final image size by 60-80%
- Official base images (node:alpine, python:slim) provide security updates and minimal attack surface
- Layer caching significantly improves rebuild times (2-3x faster for incremental changes)

### Next.js Frontend Build Pattern

**Recommended Approach**:
```dockerfile
# Stage 1: Dependencies (cached layer)
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build (separate from runtime)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runtime (minimal)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Key Decisions**:
- Use `node:20-alpine` for minimal size (~50MB base vs ~900MB for node:20)
- Next.js standalone output reduces runtime dependencies
- Non-root user (nextjs:1001) for security
- Separate dependency installation for better caching

**Expected Results**:
- Final image size: ~150-200MB (vs 800MB+ without optimization)
- Build time: 3-5 minutes (first build), 30-60 seconds (cached rebuilds)
- Security: No root user, minimal attack surface

### FastAPI Backend Build Pattern

**Recommended Approach**:
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
RUN addgroup --system --gid 1001 appuser
RUN adduser --system --uid 1001 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Decisions**:
- Use `python:3.11-slim` for balance of size and compatibility (~120MB base)
- Install build tools (gcc) only in builder stage
- Non-root user (appuser:1001) for security
- Copy only installed packages to runtime stage

**Expected Results**:
- Final image size: ~180-220MB
- Build time: 2-4 minutes (first build), 20-40 seconds (cached rebuilds)
- Security: No root user, no build tools in runtime

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Alpine-based Python | Smaller base (~40MB) | Compilation issues with some packages | Rejected: python:slim more compatible |
| Distroless images | Maximum security | Harder to debug, no shell | Deferred: Use for production, not dev |
| Single-stage builds | Simpler Dockerfile | Larger images, slower builds | Rejected: Multi-stage is industry standard |

---

## R2: Helm Chart Structure and Best Practices

### Decision: Standard Helm 3 Chart with Separate Frontend/Backend Resources

**Rationale**:
- Single chart with both applications simplifies deployment and version management
- Separate templates for frontend/backend maintain clear separation of concerns
- values.yaml parameterization enables environment-specific configuration
- Follows Helm best practices for web application deployments

### Chart Structure

```
helm/todo-chatbot/
├── Chart.yaml              # Chart metadata (name, version, description)
├── values.yaml             # Default configuration values
├── values-dev.yaml         # Development overrides
├── values-prod.yaml        # Production overrides (future)
├── templates/
│   ├── _helpers.tpl        # Template helpers (labels, selectors)
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml      # Non-sensitive config
│   ├── secrets.yaml        # Sensitive config (base64 encoded)
│   └── NOTES.txt           # Post-install instructions
└── .helmignore             # Files to exclude from chart
```

### Key Patterns

**1. Template Helpers (_helpers.tpl)**:
```yaml
{{- define "todo-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-chatbot.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "todo-chatbot.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "todo-chatbot.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

**2. Parameterized Deployments**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-frontend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app.kubernetes.io/component: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
      app.kubernetes.io/component: frontend
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
        app.kubernetes.io/component: frontend
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
        imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
        ports:
        - containerPort: 3000
        resources:
          {{- toYaml .Values.frontend.resources | nindent 10 }}
        env:
        - name: NEXT_PUBLIC_API_URL
          value: {{ .Values.frontend.env.NEXT_PUBLIC_API_URL | quote }}
```

**3. Values File Organization**:
```yaml
# Global settings
global:
  environment: development

# Frontend configuration
frontend:
  enabled: true
  image:
    repository: todo-chatbot-frontend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
```

### Chart Versioning

**Decision**: Use Semantic Versioning (SemVer)
- Chart version: Independent of application version
- App version: Tracks application release
- Example: Chart v1.0.0 with App v0.4.0

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Separate charts per app | Independent versioning | More complex deployment | Rejected: Single chart simpler for monorepo |
| Kustomize instead of Helm | Simpler, no templating | Less parameterization | Rejected: Helm is industry standard |
| Raw Kubernetes YAML | No dependencies | No parameterization | Rejected: Violates DRY principle |

---

## R3: Minikube Networking and Service Exposure

### Decision: Use NodePort Services for Local Development

**Rationale**:
- NodePort exposes services on a static port on each node (30000-32767 range)
- Simple to access from host machine: `http://localhost:<nodePort>`
- No additional configuration required (unlike LoadBalancer or Ingress)
- Compatible with Minikube's networking model

### Service Configuration

**Frontend Service (NodePort)**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-frontend
spec:
  type: NodePort
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30080  # Fixed port for consistency
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/component: frontend
```

**Backend Service (NodePort)**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-backend
spec:
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30081  # Fixed port for consistency
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/component: backend
```

### Access Patterns

**From Host Machine**:
- Frontend: `http://localhost:30080`
- Backend API: `http://localhost:30081`

**From Frontend to Backend (within cluster)**:
- Use ClusterIP service name: `http://todo-chatbot-backend:8000`
- Or use NodePort from host: `http://localhost:30081`

### Minikube Service Command

Alternative access method:
```bash
minikube service todo-chatbot-frontend --url
minikube service todo-chatbot-backend --url
```

This returns the accessible URL (handles port mapping automatically).

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| LoadBalancer | Cloud-like experience | Requires `minikube tunnel` | Rejected: Extra complexity for local dev |
| ClusterIP + Port Forward | More secure | Manual port forwarding | Rejected: Less convenient for development |
| Ingress Controller | Production-like | Requires ingress addon, DNS config | Deferred: Use for production, not Phase IV |

---

## R4: AI DevOps Tools Integration

### Decision: Optional AI Tools with CLI Fallbacks

**Rationale**:
- AI tools (Gordon, kubectl-ai, Kagent) provide intelligent recommendations but may not be universally available
- Standard CLI commands (docker, kubectl, helm) are always available and well-documented
- Hybrid approach: Use AI tools when available, fallback to CLI otherwise
- Document both approaches for reproducibility

### Docker AI (Gordon)

**Capabilities**:
- Dockerfile generation with best practices
- Image optimization recommendations
- Security vulnerability scanning
- Multi-stage build suggestions

**Integration Approach**:
```bash
# If Gordon available:
gordon generate dockerfile --app frontend --framework nextjs --output deployment/docker/frontend.Dockerfile

# Fallback (standard docker):
docker build -f deployment/docker/frontend.Dockerfile -t todo-chatbot-frontend:latest frontend/
```

**Decision**: Use Gordon for initial Dockerfile generation, then maintain manually with version control.

### kubectl-ai

**Capabilities**:
- Natural language to kubectl commands
- Deployment troubleshooting
- Resource optimization suggestions
- Intelligent scaling recommendations

**Integration Approach**:
```bash
# If kubectl-ai available:
kubectl-ai "deploy frontend with 2 replicas"
kubectl-ai "scale backend to 3 replicas"
kubectl-ai "why is frontend pod failing?"

# Fallback (standard kubectl):
kubectl scale deployment todo-chatbot-frontend --replicas=2
kubectl scale deployment todo-chatbot-backend --replicas=3
kubectl describe pod <pod-name>
```

**Decision**: Document kubectl-ai commands as examples, provide standard kubectl equivalents.

### Kagent

**Capabilities**:
- Cluster health analysis
- Resource utilization insights
- Performance optimization recommendations
- Cost analysis (for cloud deployments)

**Integration Approach**:
```bash
# If Kagent available:
kagent analyze cluster
kagent optimize resources
kagent health check

# Fallback (standard kubectl):
kubectl top nodes
kubectl top pods
kubectl get events --sort-by='.lastTimestamp'
```

**Decision**: Use Kagent for post-deployment analysis, provide kubectl alternatives for monitoring.

### Tool Availability Matrix

| Tool | Installation | Availability | Fallback |
|------|--------------|--------------|----------|
| Docker AI (Gordon) | Separate install | Optional | docker CLI |
| kubectl-ai | kubectl plugin | Optional | kubectl CLI |
| Kagent | Separate install | Optional | kubectl + metrics-server |

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Require AI tools | Consistent experience | Blocks users without tools | Rejected: Too restrictive |
| CLI only | Universal availability | No AI benefits | Rejected: Misses AI-assisted value |
| Hybrid (chosen) | Best of both worlds | More documentation | Accepted: Balances flexibility and innovation |

---

## R5: Environment Variable Management in Kubernetes

### Decision: ConfigMaps for Non-Sensitive, Secrets for Sensitive Data

**Rationale**:
- Kubernetes Secrets provide base64 encoding and RBAC protection
- ConfigMaps are appropriate for non-sensitive configuration
- Helm values.yaml provides single source of truth for all configuration
- Environment-specific values files (values-dev.yaml, values-prod.yaml) enable easy environment switching

### Configuration Categories

**ConfigMap (Non-Sensitive)**:
- Environment name (development, staging, production)
- Log levels (INFO, DEBUG, ERROR)
- Feature flags (enable_chatbot, enable_analytics)
- API URLs (when not sensitive)
- Resource limits and replica counts

**Secret (Sensitive)**:
- Database connection strings (DATABASE_URL)
- JWT signing secrets (BETTER_AUTH_SECRET)
- API keys (OPENROUTER_KEY)
- Third-party service credentials

### Helm Integration Pattern

**values.yaml**:
```yaml
backend:
  env:
    ENVIRONMENT: development  # ConfigMap
    LOG_LEVEL: INFO           # ConfigMap
  secrets:
    DATABASE_URL: ""          # Secret (must be provided)
    BETTER_AUTH_SECRET: ""    # Secret (must be provided)
```

**ConfigMap Template**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-backend-config
data:
  ENVIRONMENT: {{ .Values.backend.env.ENVIRONMENT | quote }}
  LOG_LEVEL: {{ .Values.backend.env.LOG_LEVEL | quote }}
```

**Secret Template**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-backend-secret
type: Opaque
data:
  DATABASE_URL: {{ .Values.backend.secrets.DATABASE_URL | b64enc | quote }}
  BETTER_AUTH_SECRET: {{ .Values.backend.secrets.BETTER_AUTH_SECRET | b64enc | quote }}
```

### Environment-Specific Values

**values-dev.yaml**:
```yaml
backend:
  secrets:
    DATABASE_URL: "postgresql://user:pass@neon.tech/todo_dev"
    BETTER_AUTH_SECRET: "dev-secret-32-characters-long"
```

**Deployment Command**:
```bash
helm install todo-chatbot ./helm/todo-chatbot -f helm/todo-chatbot/values-dev.yaml
```

### Secret Management Best Practices

1. **Never commit secrets to version control**
   - Add `values-dev.yaml` to `.gitignore`
   - Provide `values-dev.yaml.example` with placeholder values

2. **Use external secret management for production**
   - Sealed Secrets (for GitOps)
   - External Secrets Operator (for cloud secret stores)
   - Vault (for enterprise)

3. **Validate required secrets**
   - Helm chart should fail if required secrets are empty
   - Provide clear error messages

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| All environment variables | Simple | No security distinction | Rejected: Exposes secrets |
| External secret store | Most secure | Complex setup | Deferred: Use for production |
| Hardcoded in Dockerfile | No runtime config | Insecure, inflexible | Rejected: Violates security principles |
| ConfigMaps + Secrets (chosen) | Kubernetes native, secure | Requires careful categorization | Accepted: Industry standard |

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Docker Builds | Multi-stage with alpine/slim bases | Minimal size, security, fast rebuilds |
| Helm Structure | Single chart, separate templates | Simplified deployment, clear separation |
| Service Exposure | NodePort for local dev | Simple access, no extra config |
| AI Tools | Optional with CLI fallbacks | Flexibility, universal availability |
| Configuration | ConfigMaps + Secrets via Helm | Secure, flexible, Kubernetes native |

---

## Implementation Readiness

All research questions resolved. Ready to proceed with Phase 1 design and contract generation.

**Next Steps**:
1. Generate deployment contracts based on research findings
2. Create quickstart guide with step-by-step instructions
3. Proceed to task generation (`/sp.tasks`)
