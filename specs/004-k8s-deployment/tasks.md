# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, contracts/, quickstart.md

**Tests**: Not requested in specification - tasks focus on deployment implementation and verification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each deployment capability.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Deployment artifacts**: `deployment/` at repository root
- **Docker files**: `deployment/docker/`
- **Helm charts**: `deployment/helm/todo-chatbot/`
- **Scripts**: `deployment/scripts/`
- **Documentation**: Root `README.md`, `deployment/CLAUDE.md`

---

## Phase 1: Setup (Deployment Infrastructure)

**Purpose**: Create deployment directory structure and initialize deployment artifacts

- [X] T001 Create deployment directory structure at repository root (deployment/, deployment/docker/, deployment/helm/, deployment/scripts/)
- [X] T002 [P] Create deployment/CLAUDE.md with deployment-specific guidance per constitution
- [X] T003 [P] Create deployment/.gitignore to exclude values-dev.yaml and sensitive files
- [X] T004 [P] Create deployment/helm/todo-chatbot/ directory for Helm chart
- [X] T005 [P] Create deployment/helm/todo-chatbot/templates/ directory for Kubernetes manifests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Verify Minikube is installed and accessible (minikube version)
- [ ] T007 Verify Docker Desktop is running (docker ps)
- [ ] T008 Verify Helm 3+ is installed (helm version)
- [ ] T009 Verify kubectl is configured (kubectl version --client)
- [ ] T010 Start Minikube cluster with 2 CPUs and 4GB RAM (minikube start --cpus=2 --memory=4096)
- [ ] T011 Configure Docker to use Minikube's Docker daemon (eval $(minikube docker-env))
- [ ] T012 Verify Minikube cluster is running (minikube status)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Container Image Creation (Priority: P1) 🎯 MVP

**Goal**: Package frontend and backend applications into optimized container images

**Independent Test**: Build images locally, run containers, verify applications start and respond to health checks

### Implementation for User Story 1

- [X] T013 [P] [US1] Generate frontend Dockerfile using Docker AI (Gordon) or create deployment/docker/frontend.Dockerfile with multi-stage build
- [X] T014 [P] [US1] Generate backend Dockerfile using Docker AI (Gordon) or create deployment/docker/backend.Dockerfile with multi-stage build
- [ ] T015 [US1] Build frontend container image (docker build -f deployment/docker/frontend.Dockerfile -t todo-chatbot-frontend:latest ./frontend)
- [ ] T016 [US1] Build backend container image (docker build -f deployment/docker/backend.Dockerfile -t todo-chatbot-backend:latest ./backend)
- [ ] T017 [P] [US1] Verify frontend image exists and size is optimized (docker images | grep todo-chatbot-frontend)
- [ ] T018 [P] [US1] Verify backend image exists and size is optimized (docker images | grep todo-chatbot-backend)
- [ ] T019 [US1] Test frontend container runs locally with environment variables (docker run -e NEXT_PUBLIC_API_URL=http://localhost:8000 -p 3000:3000 todo-chatbot-frontend:latest)
- [ ] T020 [US1] Test backend container runs locally with environment variables (docker run -e DATABASE_URL=... -e BETTER_AUTH_SECRET=... -p 8000:8000 todo-chatbot-backend:latest)
- [ ] T021 [P] [US1] Verify frontend container health check responds (curl http://localhost:3000/)
- [ ] T022 [P] [US1] Verify backend container health check responds (curl http://localhost:8000/api/health)
- [ ] T023 [US1] Stop and remove test containers (docker stop, docker rm)

**Checkpoint**: At this point, User Story 1 should be fully functional - container images built and tested

---

## Phase 4: User Story 2 - Helm Chart Deployment (Priority: P2)

**Goal**: Deploy containerized applications to Minikube using Helm charts with parameterized configuration

**Independent Test**: Install Helm chart on fresh Minikube cluster, verify all pods start and services are accessible

### Implementation for User Story 2

- [X] T024 [P] [US2] Create deployment/helm/todo-chatbot/Chart.yaml with chart metadata (name, version, description)
- [X] T025 [P] [US2] Create deployment/helm/todo-chatbot/values.yaml with default configuration per helm-values-schema.md
- [X] T026 [P] [US2] Create deployment/helm/todo-chatbot/templates/_helpers.tpl with template helper functions
- [X] T027 [P] [US2] Create deployment/helm/todo-chatbot/templates/frontend-deployment.yaml per frontend-deployment.md contract
- [X] T028 [P] [US2] Create deployment/helm/todo-chatbot/templates/frontend-service.yaml with NodePort 30080
- [X] T029 [P] [US2] Create deployment/helm/todo-chatbot/templates/backend-deployment.yaml per backend-deployment.md contract
- [X] T030 [P] [US2] Create deployment/helm/todo-chatbot/templates/backend-service.yaml with NodePort 30081
- [X] T031 [P] [US2] Create deployment/helm/todo-chatbot/templates/configmap.yaml for non-sensitive configuration
- [X] T032 [P] [US2] Create deployment/helm/todo-chatbot/templates/secrets.yaml for sensitive data (DATABASE_URL, BETTER_AUTH_SECRET)
- [X] T033 [P] [US2] Create deployment/helm/todo-chatbot/templates/NOTES.txt with post-install instructions
- [ ] T034 [US2] Validate Helm chart syntax (helm lint deployment/helm/todo-chatbot)
- [ ] T035 [US2] Create deployment/helm/todo-chatbot/values-dev.yaml with development configuration
- [ ] T036 [US2] Perform dry-run installation to validate templates (helm install todo-chatbot deployment/helm/todo-chatbot -f deployment/helm/todo-chatbot/values-dev.yaml --dry-run --debug)
- [ ] T037 [US2] Install Helm chart to Minikube (helm install todo-chatbot deployment/helm/todo-chatbot -f deployment/helm/todo-chatbot/values-dev.yaml)
- [ ] T038 [US2] Wait for pods to reach running state (kubectl get pods -w)
- [ ] T039 [P] [US2] Verify frontend deployment status (kubectl get deployment todo-chatbot-frontend)
- [ ] T040 [P] [US2] Verify backend deployment status (kubectl get deployment todo-chatbot-backend)
- [ ] T041 [P] [US2] Verify frontend service is exposed (kubectl get service todo-chatbot-frontend)
- [ ] T042 [P] [US2] Verify backend service is exposed (kubectl get service todo-chatbot-backend)
- [ ] T043 [P] [US2] Check frontend pod logs for errors (kubectl logs -l app.kubernetes.io/component=frontend)
- [ ] T044 [P] [US2] Check backend pod logs for errors (kubectl logs -l app.kubernetes.io/component=backend)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - applications deployed to Minikube

---

## Phase 5: User Story 4 - Configuration Management (Priority: P2)

**Goal**: Manage environment-specific configuration externally via Helm values

**Independent Test**: Deploy with different configuration values, verify application behaves correctly in each scenario

### Implementation for User Story 4

- [X] T045 [P] [US4] Create deployment/helm/todo-chatbot/values-prod.yaml with production configuration template
- [ ] T046 [US4] Test configuration override by upgrading with different replica count (helm upgrade todo-chatbot deployment/helm/todo-chatbot --set backend.replicaCount=3)
- [ ] T047 [US4] Verify backend scaled to 3 replicas (kubectl get pods -l app.kubernetes.io/component=backend)
- [ ] T048 [US4] Test environment variable injection by checking pod environment (kubectl exec -it <backend-pod> -- env | grep ENVIRONMENT)
- [ ] T049 [US4] Verify secrets are base64 encoded in Kubernetes (kubectl get secret todo-chatbot-backend-secret -o yaml)
- [ ] T050 [US4] Test resource limits are enforced (kubectl describe pod <backend-pod> | grep -A 5 "Limits")
- [ ] T051 [US4] Rollback to previous configuration (helm rollback todo-chatbot)
- [ ] T052 [US4] Verify rollback succeeded and pods are healthy (kubectl get pods)

**Checkpoint**: At this point, User Stories 1, 2, AND 4 should all work - configuration is externalized and manageable

---

## Phase 6: User Story 5 - Deployment Verification (Priority: P1)

**Goal**: Verify deployed application works correctly in Kubernetes environment

**Independent Test**: Run verification suite against deployed application, confirm all checks pass

### Implementation for User Story 5

- [ ] T053 [P] [US5] Verify frontend is accessible via NodePort (curl http://localhost:30080/)
- [ ] T054 [P] [US5] Verify backend API is accessible via NodePort (curl http://localhost:30081/api/health)
- [ ] T055 [P] [US5] Verify backend API documentation is accessible (curl http://localhost:30081/docs)
- [ ] T056 [US5] Test frontend loads in browser (open http://localhost:30080 and verify UI renders)
- [ ] T057 [US5] Test user signup functionality (navigate to /signup, create account)
- [ ] T058 [US5] Test user login functionality (navigate to /login, sign in)
- [ ] T059 [US5] Test AI chatbot interface (navigate to /chat, send message "Add a task to buy groceries")
- [ ] T060 [US5] Verify task was created via chatbot (send message "Show me my tasks")
- [ ] T061 [US5] Test task completion via chatbot (send message "Mark buy groceries as complete")
- [ ] T062 [US5] Verify database connectivity from backend pods (kubectl logs -l app.kubernetes.io/component=backend | grep -i "database connection")
- [ ] T063 [P] [US5] Check all pods are healthy (kubectl get pods -l app.kubernetes.io/name=todo-chatbot)
- [ ] T064 [P] [US5] Check all services have endpoints (kubectl get endpoints)
- [ ] T065 [US5] Test pod restart resilience by deleting a backend pod (kubectl delete pod <backend-pod>)
- [ ] T066 [US5] Verify Kubernetes recreated the pod automatically (kubectl get pods -w)
- [ ] T067 [US5] Verify application still works after pod restart (curl http://localhost:30081/api/health)

**Checkpoint**: All core user stories complete - application is deployed, configured, and verified

---

## Phase 7: User Story 3 - AI-Assisted Operations (Priority: P3)

**Goal**: Use AI-assisted tools for deployment operations and cluster management

**Independent Test**: Use AI tools to perform operations, verify they produce correct results with helpful guidance

### Implementation for User Story 3

- [ ] T068 [US3] Document Docker AI (Gordon) commands used for Dockerfile generation in deployment/AI-COMMANDS.md
- [ ] T069 [US3] Test kubectl-ai for scaling operation if available (kubectl-ai "scale backend to 4 replicas") or use standard kubectl
- [ ] T070 [US3] Verify scaling via kubectl-ai succeeded (kubectl get pods -l app.kubernetes.io/component=backend)
- [ ] T071 [US3] Test kubectl-ai for pod inspection if available (kubectl-ai "why is pod failing?") or use standard kubectl describe
- [ ] T072 [US3] Test Kagent for cluster health analysis if available (kagent analyze cluster) or use standard kubectl top nodes
- [ ] T073 [US3] Test Kagent for resource optimization if available (kagent optimize resources) or use standard kubectl top pods
- [ ] T074 [US3] Document all kubectl-ai commands used in deployment/AI-COMMANDS.md
- [ ] T075 [US3] Document all Kagent commands used in deployment/AI-COMMANDS.md
- [ ] T076 [US3] Document CLI fallback commands for each AI tool in deployment/AI-COMMANDS.md

**Checkpoint**: AI-assisted operations documented and tested

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, deployment scripts, and final verification

- [X] T077 [P] Create deployment/scripts/build-images.sh script for building container images
- [X] T078 [P] Create deployment/scripts/deploy.sh script for deploying to Minikube
- [X] T079 [P] Create deployment/scripts/verify.sh script for verifying deployment
- [X] T080 [P] Create deployment/scripts/scale.sh script for scaling replicas
- [X] T081 Update root README.md with Phase IV deployment section referencing quickstart.md
- [X] T082 [P] Create deployment/helm/todo-chatbot/values-dev.yaml.example with placeholder values
- [X] T083 [P] Add deployment/helm/todo-chatbot/values-dev.yaml to .gitignore
- [ ] T084 Test complete deployment from scratch using deployment/scripts/deploy.sh
- [ ] T085 Verify deployment reproducibility by uninstalling and reinstalling (helm uninstall todo-chatbot && helm install...)
- [ ] T086 [P] Capture deployment logs for documentation (kubectl logs, helm status)
- [ ] T087 [P] Take screenshots of running application for verification evidence
- [ ] T088 Run quickstart.md validation to ensure all steps work correctly
- [ ] T089 Create deployment verification report documenting all success criteria (SC-016 to SC-025)
- [ ] T090 Final cleanup: Stop Minikube if needed (minikube stop)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase - Container images required for deployment
- **User Story 2 (Phase 4)**: Depends on User Story 1 - Needs container images to deploy
- **User Story 4 (Phase 5)**: Depends on User Story 2 - Needs deployment to test configuration
- **User Story 5 (Phase 6)**: Depends on User Story 2 - Needs deployment to verify
- **User Story 3 (Phase 7)**: Depends on User Story 2 - Needs deployment for AI operations
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (needs container images)
- **User Story 4 (P2)**: Depends on User Story 2 (needs deployment to test configuration)
- **User Story 5 (P1)**: Depends on User Story 2 (needs deployment to verify)
- **User Story 3 (P3)**: Depends on User Story 2 (needs deployment for AI operations)

### Within Each User Story

- **User Story 1**: Dockerfiles → Build images → Test containers → Verify health
- **User Story 2**: Helm templates → Validate chart → Install → Verify deployment
- **User Story 4**: Configuration files → Test overrides → Verify injection
- **User Story 5**: Access checks → Functional tests → Resilience tests
- **User Story 3**: AI tool usage → Documentation → Fallback validation

### Parallel Opportunities

- **Setup (Phase 1)**: All tasks marked [P] can run in parallel
- **Foundational (Phase 2)**: Verification tasks (T006-T009) can run in parallel
- **User Story 1**: Dockerfile generation (T013, T014), image verification (T017, T018), health checks (T021, T022) can run in parallel
- **User Story 2**: All template creation tasks (T024-T032) can run in parallel, verification tasks (T039-T044) can run in parallel
- **User Story 5**: Access verification tasks (T053-T055), health checks (T063-T064) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch Dockerfile generation in parallel:
Task: "Generate frontend Dockerfile using Docker AI (Gordon)"
Task: "Generate backend Dockerfile using Docker AI (Gordon)"

# After images are built, verify in parallel:
Task: "Verify frontend image exists and size is optimized"
Task: "Verify backend image exists and size is optimized"

# After containers are running, check health in parallel:
Task: "Verify frontend container health check responds"
Task: "Verify backend container health check responds"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 5 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Container images)
4. Complete Phase 4: User Story 2 (Helm deployment)
5. Complete Phase 6: User Story 5 (Verification)
6. **STOP and VALIDATE**: Test deployment end-to-end
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Container images ready
3. Add User Story 2 → Test independently → Deployed to Minikube (MVP!)
4. Add User Story 4 → Test independently → Configuration management working
5. Add User Story 5 → Test independently → Full verification complete
6. Add User Story 3 → Test independently → AI operations documented
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Container images)
   - Developer B: User Story 2 (Helm charts) - waits for US1
   - Developer C: User Story 4 (Configuration) - waits for US2
3. Stories complete and integrate sequentially due to dependencies

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User Story 1 must complete before User Story 2 (images needed for deployment)
- User Story 2 must complete before User Stories 3, 4, 5 (deployment needed)
- Verify deployment works after each user story
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- AI tools (Gordon, kubectl-ai, Kagent) are optional with CLI fallbacks
- All secrets must be externalized in values-dev.yaml (never commit to git)
