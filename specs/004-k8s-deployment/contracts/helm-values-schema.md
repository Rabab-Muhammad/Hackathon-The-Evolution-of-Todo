# Helm Values Schema Contract

**Feature**: 004-k8s-deployment
**Component**: Helm Chart Configuration
**Date**: 2026-02-09

## Purpose

Define the complete structure, defaults, and validation rules for the Helm chart's values.yaml configuration file. This schema serves as the contract between the Helm chart templates and the deployment configuration.

## Schema Structure

### Global Configuration

```yaml
global:
  # Environment name (affects logging, debugging, etc.)
  environment: development  # Options: development, staging, production
```

**Description**: Global settings that apply to all components.

**Validation**:
- `environment` must be one of: `development`, `staging`, `production`

---

### Frontend Configuration

```yaml
frontend:
  # Enable/disable frontend deployment
  enabled: true

  # Container image configuration
  image:
    repository: todo-chatbot-frontend
    tag: latest
    pullPolicy: IfNotPresent  # Options: Always, IfNotPresent, Never

  # Number of pod replicas
  replicaCount: 1

  # Resource limits and requests
  resources:
    limits:
      cpu: 500m      # 0.5 CPU cores
      memory: 512Mi  # 512 MiB
    requests:
      cpu: 250m      # 0.25 CPU cores
      memory: 256Mi  # 256 MiB

  # Service configuration
  service:
    type: NodePort     # Options: ClusterIP, NodePort, LoadBalancer
    port: 3000         # Service port
    nodePort: 30080    # NodePort (30000-32767 range)

  # Environment variables (non-sensitive)
  env:
    NEXT_PUBLIC_API_URL: http://localhost:30081

  # Health check configuration
  livenessProbe:
    enabled: true
    initialDelaySeconds: 10
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3

  readinessProbe:
    enabled: true
    initialDelaySeconds: 10
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3
```

**Field Descriptions**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enabled` | boolean | Yes | `true` | Enable/disable frontend deployment |
| `image.repository` | string | Yes | `todo-chatbot-frontend` | Container image repository name |
| `image.tag` | string | Yes | `latest` | Container image tag |
| `image.pullPolicy` | string | Yes | `IfNotPresent` | When to pull the image |
| `replicaCount` | integer | Yes | `1` | Number of pod replicas (1-10) |
| `resources.limits.cpu` | string | Yes | `500m` | Maximum CPU allocation |
| `resources.limits.memory` | string | Yes | `512Mi` | Maximum memory allocation |
| `resources.requests.cpu` | string | Yes | `250m` | Requested CPU allocation |
| `resources.requests.memory` | string | Yes | `256Mi` | Requested memory allocation |
| `service.type` | string | Yes | `NodePort` | Kubernetes service type |
| `service.port` | integer | Yes | `3000` | Service port |
| `service.nodePort` | integer | No | `30080` | NodePort (only if type=NodePort) |
| `env.NEXT_PUBLIC_API_URL` | string | Yes | `http://localhost:30081` | Backend API URL |

**Validation Rules**:
- `replicaCount` must be between 1 and 10
- `service.nodePort` must be between 30000 and 32767 (if specified)
- `resources.requests` must be less than or equal to `resources.limits`
- `image.pullPolicy` must be one of: `Always`, `IfNotPresent`, `Never`

---

### Backend Configuration

```yaml
backend:
  # Enable/disable backend deployment
  enabled: true

  # Container image configuration
  image:
    repository: todo-chatbot-backend
    tag: latest
    pullPolicy: IfNotPresent  # Options: Always, IfNotPresent, Never

  # Number of pod replicas
  replicaCount: 2

  # Resource limits and requests
  resources:
    limits:
      cpu: 1000m     # 1 CPU core
      memory: 1Gi    # 1 GiB
    requests:
      cpu: 500m      # 0.5 CPU cores
      memory: 512Mi  # 512 MiB

  # Service configuration
  service:
    type: NodePort     # Options: ClusterIP, NodePort, LoadBalancer
    port: 8000         # Service port
    nodePort: 30081    # NodePort (30000-32767 range)

  # Environment variables (non-sensitive)
  env:
    ENVIRONMENT: development
    LOG_LEVEL: INFO  # Options: DEBUG, INFO, WARNING, ERROR

  # Secrets (sensitive data - must be provided)
  secrets:
    DATABASE_URL: ""              # REQUIRED: PostgreSQL connection string
    BETTER_AUTH_SECRET: ""        # REQUIRED: JWT signing secret (32+ chars)
    NEXT_PUBLIC_OPENROUTER_KEY: "" # OPTIONAL: OpenRouter API key

  # Health check configuration
  livenessProbe:
    enabled: true
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3

  readinessProbe:
    enabled: true
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3
```

**Field Descriptions**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enabled` | boolean | Yes | `true` | Enable/disable backend deployment |
| `image.repository` | string | Yes | `todo-chatbot-backend` | Container image repository name |
| `image.tag` | string | Yes | `latest` | Container image tag |
| `image.pullPolicy` | string | Yes | `IfNotPresent` | When to pull the image |
| `replicaCount` | integer | Yes | `2` | Number of pod replicas (1-10) |
| `resources.limits.cpu` | string | Yes | `1000m` | Maximum CPU allocation |
| `resources.limits.memory` | string | Yes | `1Gi` | Maximum memory allocation |
| `resources.requests.cpu` | string | Yes | `500m` | Requested CPU allocation |
| `resources.requests.memory` | string | Yes | `512Mi` | Requested memory allocation |
| `service.type` | string | Yes | `NodePort` | Kubernetes service type |
| `service.port` | integer | Yes | `8000` | Service port |
| `service.nodePort` | integer | No | `30081` | NodePort (only if type=NodePort) |
| `env.ENVIRONMENT` | string | Yes | `development` | Environment name |
| `env.LOG_LEVEL` | string | Yes | `INFO` | Logging level |
| `secrets.DATABASE_URL` | string | **REQUIRED** | `""` | PostgreSQL connection string |
| `secrets.BETTER_AUTH_SECRET` | string | **REQUIRED** | `""` | JWT signing secret |
| `secrets.NEXT_PUBLIC_OPENROUTER_KEY` | string | Optional | `""` | OpenRouter API key |

**Validation Rules**:
- `replicaCount` must be between 1 and 10
- `service.nodePort` must be between 30000 and 32767 (if specified)
- `resources.requests` must be less than or equal to `resources.limits`
- `env.LOG_LEVEL` must be one of: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `secrets.DATABASE_URL` must not be empty (deployment will fail if empty)
- `secrets.BETTER_AUTH_SECRET` must not be empty and should be 32+ characters
- `image.pullPolicy` must be one of: `Always`, `IfNotPresent`, `Never`

---

## Complete Default Values

```yaml
# Global configuration
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
  service:
    type: NodePort
    port: 3000
    nodePort: 30080
  env:
    NEXT_PUBLIC_API_URL: http://localhost:30081
  livenessProbe:
    enabled: true
    initialDelaySeconds: 10
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3
  readinessProbe:
    enabled: true
    initialDelaySeconds: 10
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3

# Backend configuration
backend:
  enabled: true
  image:
    repository: todo-chatbot-backend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 2
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
  service:
    type: NodePort
    port: 8000
    nodePort: 30081
  env:
    ENVIRONMENT: development
    LOG_LEVEL: INFO
  secrets:
    DATABASE_URL: ""
    BETTER_AUTH_SECRET: ""
    NEXT_PUBLIC_OPENROUTER_KEY: ""
  livenessProbe:
    enabled: true
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3
  readinessProbe:
    enabled: true
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 3
```

---

## Environment-Specific Overrides

### Development (values-dev.yaml)

```yaml
global:
  environment: development

frontend:
  replicaCount: 1
  env:
    NEXT_PUBLIC_API_URL: http://localhost:30081

backend:
  replicaCount: 1  # Single replica for dev
  env:
    LOG_LEVEL: DEBUG  # More verbose logging
  secrets:
    DATABASE_URL: "postgresql://user:pass@host.neon.tech/todo_dev?sslmode=require"
    BETTER_AUTH_SECRET: "dev-secret-must-be-32-chars-long"
    NEXT_PUBLIC_OPENROUTER_KEY: "sk-or-v1-dev-key"
```

### Production (values-prod.yaml)

```yaml
global:
  environment: production

frontend:
  replicaCount: 3  # More replicas for production
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

backend:
  replicaCount: 5  # More replicas for production
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi
  env:
    LOG_LEVEL: WARNING  # Less verbose in production
  secrets:
    DATABASE_URL: "postgresql://user:pass@host.neon.tech/todo_prod?sslmode=require"
    BETTER_AUTH_SECRET: "prod-secret-must-be-32-chars-long-and-secure"
    NEXT_PUBLIC_OPENROUTER_KEY: "sk-or-v1-prod-key"
```

---

## Usage Examples

### Install with Default Values

```bash
helm install todo-chatbot ./helm/todo-chatbot
```

### Install with Development Overrides

```bash
helm install todo-chatbot ./helm/todo-chatbot -f helm/todo-chatbot/values-dev.yaml
```

### Install with Custom Values

```bash
helm install todo-chatbot ./helm/todo-chatbot \
  --set backend.replicaCount=3 \
  --set backend.secrets.DATABASE_URL="postgresql://..." \
  --set backend.secrets.BETTER_AUTH_SECRET="your-secret-here"
```

### Upgrade with New Values

```bash
helm upgrade todo-chatbot ./helm/todo-chatbot \
  --set backend.replicaCount=4 \
  --reuse-values
```

---

## Validation

### Pre-Deployment Validation

The Helm chart should validate required values before deployment:

```yaml
# In templates/_helpers.tpl
{{- define "todo-chatbot.validateSecrets" -}}
{{- if not .Values.backend.secrets.DATABASE_URL }}
{{- fail "backend.secrets.DATABASE_URL is required" }}
{{- end }}
{{- if not .Values.backend.secrets.BETTER_AUTH_SECRET }}
{{- fail "backend.secrets.BETTER_AUTH_SECRET is required" }}
{{- end }}
{{- if lt (len .Values.backend.secrets.BETTER_AUTH_SECRET) 32 }}
{{- fail "backend.secrets.BETTER_AUTH_SECRET must be at least 32 characters" }}
{{- end }}
{{- end }}
```

### Runtime Validation

Applications should validate configuration on startup:
- Backend checks DATABASE_URL format and connectivity
- Backend checks BETTER_AUTH_SECRET length
- Frontend checks NEXT_PUBLIC_API_URL accessibility

---

## Security Considerations

### Secret Management

1. **Never commit secrets to version control**
   - Add `values-dev.yaml` and `values-prod.yaml` to `.gitignore`
   - Provide `values-dev.yaml.example` with placeholder values

2. **Use strong secrets**
   - `BETTER_AUTH_SECRET` should be 32+ characters, randomly generated
   - Use different secrets for each environment

3. **Rotate secrets regularly**
   - Update secrets in values files
   - Run `helm upgrade` to apply changes
   - Pods will restart with new secrets

### Access Control

1. **Kubernetes RBAC**
   - Limit who can read Secrets
   - Limit who can deploy Helm charts

2. **Network Policies** (future enhancement)
   - Restrict pod-to-pod communication
   - Restrict egress to database only

---

## References

- Specification: [spec.md](../spec.md) - FR-014, FR-023 to FR-028
- Research: [research.md](../research.md) - R2 (Helm charts), R5 (Environment variables)
- Frontend Contract: [frontend-deployment.md](./frontend-deployment.md)
- Backend Contract: [backend-deployment.md](./backend-deployment.md)
