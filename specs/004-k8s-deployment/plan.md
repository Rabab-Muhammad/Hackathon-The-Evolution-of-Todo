# Implementation Plan: Local Kubernetes Deployment

**Branch**: `004-k8s-deployment` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-k8s-deployment/spec.md`

**Note**: This plan follows the Spec-Driven Development workflow for cloud-native infrastructure deployment.

## Summary

Deploy the Phase III AI-powered Todo Chatbot to a local Kubernetes cluster using Minikube, with containerized frontend and backend applications managed via Helm charts. All deployment artifacts will be generated using AI-assisted DevOps tools (Docker AI/Gordon, kubectl-ai, Kagent) with fallback to standard CLI commands. The deployment must be reproducible, scalable, and maintain stateless architecture principles.

**Primary Requirement**: Transform Phase III web application into cloud-native deployment on local Minikube cluster.

**Technical Approach**:
1. Containerize frontend (Next.js) and backend (FastAPI) using multi-stage Docker builds
2. Generate Helm charts with parameterized configurations for both applications
3. Deploy to Minikube using Helm with externalized configuration
4. Verify deployment with health checks and end-to-end testing
5. Document all AI-assisted commands for reproducibility

## Technical Context

**Language/Version**:
- Dockerfile syntax (Docker 20+)
- Helm Chart templates (Helm 3+)
- YAML (Kubernetes 1.25+)
- Shell scripts (Bash 4+)

**Primary Dependencies**:
- Docker Desktop (container runtime)
- Minikube (local Kubernetes cluster)
- Helm 3+ (package manager)
- kubectl (Kubernetes CLI)
- AI DevOps Tools: Docker AI (Gordon), kubectl-ai, Kagent (optional with CLI fallbacks)

**Storage**:
- External Neon PostgreSQL (no persistent volumes needed)
- Container images stored locally in Minikube's Docker daemon

**Testing**:
- Manual verification via kubectl commands
- Health check endpoints (HTTP GET requests)
- End-to-end functional testing of deployed application
- Scaling verification (replica count changes)

**Target Platform**:
- Local Minikube cluster (Kubernetes 1.25+)
- Docker Desktop on Windows/macOS/Linux
- Cloud-ready architecture (future migration to AWS/GCP/Azure)

**Project Type**: Infrastructure (deployment artifacts, not application code)

**Performance Goals**:
- Pod startup time: <2 minutes from deployment
- Scaling time: <1 minute for replica changes
- Image build time: <5 minutes per application
- Deployment reproducibility: 100% (same commands = same results)

**Constraints**:
- Local-only deployment (no cloud providers)
- No manual YAML editing (AI-generated only)
- Stateless pods (no in-memory session state)
- External database (Neon PostgreSQL accessible from cluster)
- Resource limits: Minikube default (2 CPUs, 4GB RAM)

**Scale/Scope**:
- 2 applications (frontend, backend)
- 2 Helm charts (one per application)
- 4-6 Kubernetes resources per application (Deployment, Service, ConfigMap, Secret)
- Development environment (single-node Minikube cluster)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
✅ **PASS**: All deployment artifacts specified in spec.md before implementation
- FR-001 to FR-008: Containerization requirements specified
- FR-009 to FR-017: Helm chart requirements specified
- FR-018 to FR-022: AI-assisted DevOps requirements specified

### Principle II: End-to-End Traceability
✅ **PASS**: All infrastructure changes traceable to specs/004-k8s-deployment/
- Dockerfiles will reference FR-001 to FR-008
- Helm charts will reference FR-009 to FR-017
- Deployment procedures will reference FR-029 to FR-034

### Principle III: Security by Design
✅ **PASS**: Security requirements specified
- FR-007: No hardcoded secrets in container images
- FR-013: Kubernetes Secrets for sensitive data
- FR-025: Secrets stored in Kubernetes Secrets, not ConfigMaps
- FR-004: Containers run as non-root users

### Principle IV: Separation of Concerns
✅ **PASS**: Infrastructure separated from application code
- deployment/ directory for all deployment artifacts
- frontend/ and backend/ remain unchanged (application code)
- Clear separation between application and infrastructure

### Principle V: Scalability Ready
✅ **PASS**: Architecture supports future cloud deployment
- FR-010: Configurable replica counts
- FR-015: Resource limits defined
- FR-032: Rolling updates supported
- FR-033: Horizontal scaling supported

### Principle VI: Stateless Architecture
✅ **PASS**: Deployment maintains stateless principles
- No persistent volumes (database is external)
- Pods are ephemeral and replaceable
- Configuration externalized via ConfigMaps and Secrets
- No in-memory session state

### Principle IX: Cloud-Native Infrastructure
✅ **PASS**: Core principle for this feature
- FR-001: Separate container images for frontend and backend
- FR-009: Helm charts for deployment
- FR-018 to FR-020: AI-assisted DevOps tools
- FR-029: Minikube deployment (local Kubernetes)

**Gate Status**: ✅ ALL GATES PASSED - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-deployment/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (AI DevOps tools, best practices)
├── contracts/           # Phase 1 output (deployment contracts)
│   ├── frontend-deployment.md
│   ├── backend-deployment.md
│   └── helm-values-schema.md
└── quickstart.md        # Phase 1 output (deployment guide)
```

### Source Code (repository root)

```text
deployment/                     # NEW: Deployment artifacts
├── CLAUDE.md                   # Deployment-specific guidance
├── docker/
│   ├── frontend.Dockerfile     # Next.js multi-stage build
│   └── backend.Dockerfile      # FastAPI multi-stage build
├── helm/
│   └── todo-chatbot/           # Helm chart
│       ├── Chart.yaml          # Chart metadata
│       ├── values.yaml         # Default values
│       ├── values-dev.yaml     # Development overrides
│       ├── values-prod.yaml    # Production overrides (future)
│       └── templates/
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── configmap.yaml
│           ├── secrets.yaml
│           └── NOTES.txt       # Post-install instructions
└── scripts/
    ├── build-images.sh         # Build container images
    ├── deploy.sh               # Deploy to Minikube
    ├── verify.sh               # Verify deployment
    └── scale.sh                # Scale replicas

frontend/                       # EXISTING: No changes
backend/                        # EXISTING: No changes
```

**Structure Decision**: Infrastructure deployment artifacts are isolated in a new `deployment/` directory at the repository root. This maintains clear separation between application code (frontend/, backend/) and deployment infrastructure (deployment/). The Helm chart follows standard Helm conventions with templates/ directory for Kubernetes manifests and values.yaml for configuration.

## Complexity Tracking

> No constitution violations - this section is not needed.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

#### R1: Docker Multi-Stage Build Best Practices

**Question**: What are the optimal multi-stage build patterns for Next.js and FastAPI applications?

**Research Areas**:
- Next.js production build optimization (standalone output, static assets)
- FastAPI minimal base images (python:slim vs python:alpine)
- Layer caching strategies for faster rebuilds
- Security hardening (non-root users, minimal attack surface)

**Decision Criteria**:
- Image size (<500MB for frontend, <200MB for backend)
- Build time (<5 minutes per image)
- Security (no root users, minimal dependencies)
- Compatibility with Minikube

#### R2: Helm Chart Structure and Best Practices

**Question**: What is the standard Helm chart structure for deploying web applications?

**Research Areas**:
- Helm chart directory layout and naming conventions
- values.yaml parameterization patterns
- Template helpers and named templates
- Chart versioning and dependencies

**Decision Criteria**:
- Reusability across environments (dev, staging, prod)
- Maintainability (clear template structure)
- Helm 3+ compatibility
- Standard Kubernetes resource definitions

#### R3: Minikube Networking and Service Exposure

**Question**: How should services be exposed in Minikube for local development?

**Research Areas**:
- Service types (ClusterIP, NodePort, LoadBalancer)
- Minikube service command for accessing applications
- Port forwarding vs NodePort vs LoadBalancer
- Ingress controllers (optional for Phase IV)

**Decision Criteria**:
- Simplicity (minimal configuration)
- Accessibility (easy to access from host machine)
- Minikube compatibility
- Future cloud migration path

#### R4: AI DevOps Tools Integration

**Question**: How to integrate Docker AI (Gordon), kubectl-ai, and Kagent into the deployment workflow?

**Research Areas**:
- Docker AI (Gordon) capabilities and API
- kubectl-ai command patterns and usage
- Kagent cluster analysis features
- Fallback strategies when AI tools unavailable

**Decision Criteria**:
- Tool availability and installation requirements
- Command reproducibility (can commands be documented?)
- Fallback to standard CLI (docker, kubectl, helm)
- Value-add vs complexity trade-off

#### R5: Environment Variable Management in Kubernetes

**Question**: What is the best practice for managing environment variables in Kubernetes deployments?

**Research Areas**:
- ConfigMaps vs Secrets (when to use each)
- Environment variable injection patterns
- Secret management (base64 encoding, external secret stores)
- Configuration validation and defaults

**Decision Criteria**:
- Security (secrets not exposed in logs or configs)
- Flexibility (easy to change per environment)
- Kubernetes native (no external dependencies)
- Helm integration (values.yaml to ConfigMap/Secret)

### Research Findings

*This section will be populated during Phase 0 execution and consolidated into research.md*

---

## Phase 1: Design & Contracts

### Deployment Contracts

#### Frontend Deployment Contract

**Purpose**: Define the Kubernetes resources and configuration for the Next.js frontend application.

**Resources**:
- **Deployment**: Manages frontend pods with configurable replicas
- **Service**: Exposes frontend via NodePort for Minikube access
- **ConfigMap**: Non-sensitive configuration (API URL, feature flags)

**Configuration Parameters**:
- `frontend.image.repository`: Container image repository
- `frontend.image.tag`: Container image tag (default: latest)
- `frontend.replicaCount`: Number of pod replicas (default: 1)
- `frontend.resources.limits.cpu`: CPU limit (default: 500m)
- `frontend.resources.limits.memory`: Memory limit (default: 512Mi)
- `frontend.env.NEXT_PUBLIC_API_URL`: Backend API URL
- `frontend.env.BETTER_AUTH_SECRET`: JWT signing secret (from Secret)

**Health Checks**:
- Liveness probe: HTTP GET / (port 3000)
- Readiness probe: HTTP GET / (port 3000)
- Initial delay: 10 seconds
- Period: 10 seconds

#### Backend Deployment Contract

**Purpose**: Define the Kubernetes resources and configuration for the FastAPI backend application.

**Resources**:
- **Deployment**: Manages backend pods with configurable replicas
- **Service**: Exposes backend via ClusterIP (internal only)
- **ConfigMap**: Non-sensitive configuration (log level, environment)
- **Secret**: Sensitive configuration (DATABASE_URL, BETTER_AUTH_SECRET)

**Configuration Parameters**:
- `backend.image.repository`: Container image repository
- `backend.image.tag`: Container image tag (default: latest)
- `backend.replicaCount`: Number of pod replicas (default: 2)
- `backend.resources.limits.cpu`: CPU limit (default: 1000m)
- `backend.resources.limits.memory`: Memory limit (default: 1Gi)
- `backend.env.DATABASE_URL`: PostgreSQL connection string (from Secret)
- `backend.env.BETTER_AUTH_SECRET`: JWT signing secret (from Secret)
- `backend.env.ENVIRONMENT`: Environment name (from ConfigMap)

**Health Checks**:
- Liveness probe: HTTP GET /api/health (port 8000)
- Readiness probe: HTTP GET /api/health (port 8000)
- Initial delay: 15 seconds
- Period: 10 seconds

#### Helm Values Schema Contract

**Purpose**: Define the structure and defaults for values.yaml configuration.

**Schema**:
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
    DATABASE_URL: ""  # Must be provided
    BETTER_AUTH_SECRET: ""  # Must be provided
```

### Data Model

*Not applicable for this infrastructure feature. This phase focuses on deployment artifacts, not data entities.*

### Quickstart Guide Outline

**Purpose**: Provide step-by-step instructions for deploying the Todo Chatbot to Minikube.

**Sections**:
1. **Prerequisites**: Verify Minikube, Docker, Helm, kubectl installed
2. **Build Container Images**: Use Docker AI or standard docker build
3. **Configure Deployment**: Create values-dev.yaml with secrets
4. **Deploy to Minikube**: Install Helm chart
5. **Verify Deployment**: Check pods, services, access application
6. **Scale Application**: Change replica counts
7. **Troubleshooting**: Common issues and solutions
8. **Cleanup**: Uninstall Helm chart, stop Minikube

---

## Phase 2: Task Generation

*This phase is handled by the `/sp.tasks` command, not `/sp.plan`.*

The tasks will be generated from this plan and organized into:
- **Phase 1: Setup** - Create deployment directory structure
- **Phase 2: Containerization** - Generate Dockerfiles, build images
- **Phase 3: Helm Charts** - Generate Helm chart templates and values
- **Phase 4: Deployment** - Deploy to Minikube, verify functionality
- **Phase 5: Verification** - End-to-end testing, scaling validation
- **Phase 6: Documentation** - Update README, create deployment guide

---

## Implementation Notes

### AI-Assisted DevOps Workflow

1. **Docker AI (Gordon)** - If available:
   - Use for Dockerfile generation with optimization recommendations
   - Fallback: Standard `docker build` commands with manually optimized Dockerfiles

2. **kubectl-ai** - If available:
   - Use for deployment operations: `kubectl-ai deploy`, `kubectl-ai scale`
   - Fallback: Standard `kubectl` commands

3. **Kagent** - If available:
   - Use for cluster health analysis and optimization recommendations
   - Fallback: Standard `kubectl get`, `kubectl describe` commands

### Critical Success Factors

1. **Reproducibility**: All commands must be documented and produce identical results
2. **Statelessness**: Pods must be ephemeral with no local state
3. **Security**: No secrets in container images or version control
4. **Scalability**: Replica counts must be easily adjustable
5. **Verification**: Health checks must confirm deployment success

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| AI tools unavailable | Provide CLI fallback commands for all operations |
| Minikube resource constraints | Define resource limits, test with minimal replicas |
| Database connectivity issues | Verify network access before deployment, provide troubleshooting guide |
| Image build failures | Use multi-stage builds with explicit dependency versions |
| Configuration errors | Validate values.yaml schema, provide example configurations |

---

## Next Steps

1. **Execute Phase 0**: Generate research.md with AI DevOps tool findings
2. **Execute Phase 1**: Generate deployment contracts and quickstart guide
3. **Run `/sp.tasks`**: Generate actionable task list from this plan
4. **Run `/sp.implement`**: Execute tasks to create deployment artifacts
5. **Verify Deployment**: Test on local Minikube cluster

**Ready for**: Phase 0 Research execution
