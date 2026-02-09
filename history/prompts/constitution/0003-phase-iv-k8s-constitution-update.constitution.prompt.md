---
id: 0003
title: phase-iv-k8s-constitution-update
stage: constitution
date: 2026-02-09
surface: CLI
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: developer
command: /sp.constitution
labels: [phase-iv, kubernetes, cloud-native, deployment, helm, docker, ai-devops]
links:
  spec: specs/004-k8s-deployment/
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    status: modified
    lines_added: 453
    lines_removed: 350
tests:
  - N/A
---

## Prompt

```text
You are an autonomous Cloud-Native DevOps + AI Agent operating under a strict
Spec-Driven Development workflow.

PROJECT TITLE
Cloud Native Todo Chatbot – Phase IV (Local Kubernetes Deployment)

PRIMARY OBJECTIVE
Deploy the existing Phase-III AI Todo Chatbot on a local Kubernetes cluster
using Minikube, Helm Charts, and AI-assisted DevOps tooling.

ABSOLUTE RULES (NON-NEGOTIABLE)
1. NO manual coding by the human.
2. ALL implementation must be generated via AI agents, prompts, or AI tools.
3. Follow Agentic Dev Stack strictly:
   Spec → Plan → Tasks → Implement → Verify
4. Every output must be explainable and reproducible.
5. Prefer AI-assisted tools over manual CLI usage whenever available.

SYSTEM BOUNDARIES
- Target environment: Local machine
- Kubernetes distribution: Minikube
- Container runtime: Docker Desktop
- Orchestration: Kubernetes
- Package manager: Helm
- AI DevOps tools: Docker AI Agent (Gordon), kubectl-ai, Kagent
- Application source: Phase-III Todo Chatbot (frontend + backend)

ARCHITECTURAL CONSTRAINTS
- Frontend and backend MUST be containerized separately.
- Containers MUST be deployable on Kubernetes.
- Helm charts MUST define:
  - Deployments
  - Services
  - Replica counts
  - Environment variables
- No cloud providers (AWS, GCP, Azure) allowed.
- Local-only deployment using Minikube.

AI TOOLING DIRECTIVES

DOCKER (GORDON)
- Use Docker AI Agent (Gordon) for:
  - Dockerfile generation
  - Image build optimization
  - Container best practices
- If Gordon is unavailable:
  - Ask Claude Code to generate equivalent Docker CLI commands.

KUBERNETES (kubectl-ai & kagent)
- Use kubectl-ai for:
  - Deployments
  - Scaling
  - Debugging pods
- Use Kagent for:
  - Cluster health analysis
  - Resource optimization
  - Deployment insights

HELM
- Helm charts must be generated or assisted by AI agents.
- Charts must be reusable and parameterized.
- Values.yaml must support:
  - Replica counts
  - Image tags
  - Resource limits

DELIVERABLES
The system must produce:
1. Containerized frontend image
2. Containerized backend image
3. Helm chart(s) for deployment
4. Minikube deployment instructions
5. AI-generated commands used (Docker AI, kubectl-ai, kagent)
6. Verification steps showing:
   - Pods running
   - Services accessible
   - Chatbot functional

VERIFICATION CRITERIA
- Frontend accessible via Minikube service or ingress
- Backend responding correctly
- AI Todo Chatbot works end-to-end
- Scaling works (replica count change)
- No manual edits performed

RESEARCH & LEARNING MODE
- Treat infrastructure as code governed by specifications.
- Apply Spec-Driven Development principles to DevOps.
- Explore blueprint-based infrastructure automation.
- Prefer declarative outputs over imperative steps.

OUTPUT EXPECTATION
You must:
- Generate a clear plan
- Break it into actionable tasks
- Implement using AI tools
- Explain each AI decision
- Provide validation evidence

You are judged not only on the final deployment,
but on HOW well you followed the spec-driven,
agent-orchestrated development process.

Proceed only when the specification is fully understood.
```

## Response snapshot

Updated the project constitution from v2.1.0 to v2.2.0 to incorporate Phase IV (Cloud-Native Kubernetes Deployment) requirements.

**Key Changes:**

1. **Added Principle IX: Cloud-Native Infrastructure**
   - Mandates containerization via Docker with AI-assisted generation
   - Requires Kubernetes orchestration (Minikube local, cloud-ready)
   - Enforces Helm charts for all deployments
   - Prohibits manual YAML editing (must use AI agents)
   - Specifies AI DevOps tools: Gordon (Docker), kubectl-ai, Kagent

2. **Expanded Existing Principles:**
   - **Principle I (Spec-Driven)**: Added infrastructure as code requirement
   - **Principle II (Traceability)**: Added Dockerfile/Helm chart traceability
   - **Principle III (Security)**: Added Kubernetes secrets, no hardcoded secrets in images
   - **Principle IV (Separation)**: Added Infrastructure as distinct concern
   - **Principle V (Scalability)**: Added K8s HPA, Helm parameterization
   - **Principle VI (Stateless)**: Added ephemeral pod requirement

3. **New Standards Sections:**
   - **Deployment Standards**: Helm-first, no raw YAML, version control
   - **AI-Assisted DevOps**: Gordon/kubectl-ai/Kagent usage patterns
   - **Container Standards**: Multi-stage builds, minimal images, non-root users
   - **Helm Chart Standards**: Resource definitions, values.yaml structure

4. **Updated Technology Constraints:**
   - Added: Docker Desktop, Minikube, Helm 3+, AI DevOps tools

5. **Expanded Monorepo Structure:**
   - Added: `deployment/` directory (docker/, helm/, k8s/)
   - Added: `specs/004-k8s-deployment/` for Phase IV specs
   - Added: `deployment/CLAUDE.md` for infrastructure guidance

6. **New Success Criteria (SC-016 to SC-023):**
   - SC-016: Containerized frontend/backend via AI
   - SC-017: Helm chart deploys to Minikube
   - SC-018: Pods running and healthy
   - SC-019: Frontend accessible
   - SC-020: End-to-end chatbot works in K8s
   - SC-021: Horizontal scaling works
   - SC-022: All artifacts AI-generated
   - SC-023: Deployment reproducible

7. **Updated Prohibited Actions:**
   - Added: Manual Dockerfile/Helm/K8s manifest editing
   - Added: Committing secrets to version control

**Version Bump Rationale:**
- MINOR version (2.1.0 → 2.2.0) because:
  - New principle added (IX. Cloud-Native Infrastructure)
  - Materially expanded guidance across multiple sections
  - No backward-incompatible changes to existing principles
  - Additive changes only (no removals or redefinitions)

## Outcome

- ✅ Impact: Constitution updated to v2.2.0 with comprehensive Phase IV cloud-native deployment requirements
- 🧪 Tests: N/A (constitution document, no code tests)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts:
  1. Create Phase IV specification: `/sp.specify` for 004-k8s-deployment
  2. Update root CLAUDE.md to reference Phase IV
  3. Create deployment/CLAUDE.md for infrastructure guidance
  4. Generate implementation plan: `/sp.plan` for Phase IV
- 🧠 Reflection: Successfully integrated cloud-native deployment principles while maintaining consistency with existing Phase II/III requirements. The AI-assisted DevOps approach (Gordon, kubectl-ai, Kagent) aligns with the project's spec-driven philosophy by treating infrastructure as code that must be generated, not manually written.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution update, not code generation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate that the new constitution principles can be successfully applied in Phase IV specification and planning stages
