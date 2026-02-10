# Tasks: Phase 4 Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Manual verification via kubectl, curl, browser (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [x] T001 Create k8s/manifests/ directory structure at repository root
- [x] T002 [P] Create k8s/helm/todo-app/ directory structure at repository root
- [x] T003 [P] Create scripts/ directory at repository root
- [x] T004 [P] Add k8s/ and scripts/ to .gitignore exclusions (ensure they're tracked)

**Checkpoint**: Directory structure ready for artifact creation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: User Story 1 (Docker) depends on these code changes

- [x] T005 Add `output: "standalone"` to phase-2/frontend/next.config.ts for Docker builds
- [x] T006 Create frontend .dockerignore at phase-2/frontend/.dockerignore
- [x] T007 Add /health endpoint (liveness probe) to phase-2/backend/src/main.py
- [x] T008 Add /ready endpoint (readiness probe) to phase-2/backend/src/main.py
- [x] T009 [P] Create frontend /api/health route at phase-2/frontend/src/app/api/health/route.ts

**Checkpoint**: Foundation ready - Docker builds will succeed, health endpoints available

---

## Phase 3: User Story 1 - Docker Containerization (Priority: P1) 🎯 MVP

**Goal**: Containerize frontend and backend applications with optimized, secure images

**Independent Test**: Run `docker build` and `docker run` to verify containers start and respond to health checks

### Implementation for User Story 1

- [x] T010 [US1] Verify frontend Dockerfile multi-stage build at phase-2/frontend/Dockerfile
- [x] T011 [US1] Update frontend Dockerfile with --chown flags at phase-2/frontend/Dockerfile
- [x] T012 [P] [US1] Verify backend Dockerfile at phase-2/backend/Dockerfile
- [x] T013 [US1] Create build-images.sh script at scripts/build-images.sh
- [x] T014 [P] [US1] Create build-images.ps1 script at scripts/build-images.ps1
- [x] T015 [US1] Build and test frontend Docker image (296MB, non-root: nextjs) ⚠️ size above target
- [x] T016 [US1] Build and test backend Docker image (317MB, non-root: appuser) ⚠️ size above target

**Checkpoint**: Both Docker images build successfully, containers run as non-root, health endpoints respond

---

## Phase 4: User Story 2 - Minikube Cluster Setup (Priority: P2)

**Goal**: Set up local Kubernetes cluster with Minikube and required addons

**Independent Test**: Run `kubectl cluster-info` and verify ingress addon is enabled

### Implementation for User Story 2

- [x] T017 [US2] Document Minikube start command with recommended resources (4GB RAM, 2 CPU)
- [x] T018 [US2] Document ingress addon enablement command
- [x] T019 [US2] Document image loading commands for Minikube
- [x] T020 [US2] Add hosts file configuration instructions to quickstart.md
- [ ] T021 [US2] Test Minikube cluster startup and verify kubectl connectivity

**Checkpoint**: Minikube cluster running, ingress enabled, images loaded

---

## Phase 5: User Story 3 - Kubernetes Manifests (Priority: P3)

**Goal**: Create raw Kubernetes manifests for declarative deployment

**Independent Test**: Run `kubectl apply -f k8s/manifests/` and verify all pods reach Running state

### Implementation for User Story 3

- [x] T022 [US3] Create ConfigMap manifest at k8s/manifests/configmap.yaml
- [x] T023 [P] [US3] Create Secret template at k8s/manifests/secret.yaml.example
- [x] T024 [US3] Create frontend Deployment manifest at k8s/manifests/deployment-frontend.yaml
- [x] T025 [P] [US3] Create backend Deployment manifest at k8s/manifests/deployment-backend.yaml
- [x] T026 [US3] Create frontend Service manifest at k8s/manifests/service-frontend.yaml
- [x] T027 [P] [US3] Create backend Service manifest at k8s/manifests/service-backend.yaml
- [x] T028 [US3] Create Ingress manifest at k8s/manifests/ingress.yaml
- [ ] T029 [US3] Test manifest deployment with kubectl apply

**Checkpoint**: All manifests apply successfully, pods running, services have endpoints

---

## Phase 6: User Story 4 - Helm Chart Creation (Priority: P4)

**Goal**: Package application as reusable Helm chart with templating

**Independent Test**: Run `helm lint` and `helm install` to deploy via Helm

### Implementation for User Story 4

- [x] T030 [US4] Create Chart.yaml at k8s/helm/todo-app/Chart.yaml
- [x] T031 [US4] Create values.yaml at k8s/helm/todo-app/values.yaml
- [x] T032 [P] [US4] Create values-local.yaml at k8s/helm/todo-app/values-local.yaml
- [x] T033 [US4] Create _helpers.tpl at k8s/helm/todo-app/templates/_helpers.tpl
- [x] T034 [US4] Create ConfigMap template at k8s/helm/todo-app/templates/configmap.yaml
- [x] T035 [P] [US4] Create Secret template at k8s/helm/todo-app/templates/secret.yaml
- [x] T036 [US4] Create frontend Deployment template at k8s/helm/todo-app/templates/deployment-frontend.yaml
- [x] T037 [P] [US4] Create backend Deployment template at k8s/helm/todo-app/templates/deployment-backend.yaml
- [x] T038 [US4] Create frontend Service template at k8s/helm/todo-app/templates/service-frontend.yaml
- [x] T039 [P] [US4] Create backend Service template at k8s/helm/todo-app/templates/service-backend.yaml
- [x] T040 [US4] Create Ingress template at k8s/helm/todo-app/templates/ingress.yaml
- [x] T041 [P] [US4] Create NOTES.txt at k8s/helm/todo-app/templates/NOTES.txt
- [x] T042 [US4] Create .helmignore at k8s/helm/todo-app/.helmignore
- [x] T043 [P] [US4] Create README.md at k8s/helm/todo-app/README.md
- [x] T044 [US4] Run helm lint to validate chart at k8s/helm/todo-app/ ✅
- [ ] T045 [US4] Test helm install with secrets passed via --set flags

**Checkpoint**: Helm chart passes lint, installs successfully, all resources created

---

## Phase 7: User Story 5 - Deployment & Testing (Priority: P5)

**Goal**: Deploy application and verify all Phase 3 features work in Kubernetes

**Independent Test**: Access http://todo.local and perform CRUD operations plus AI chatbot interactions

### Implementation for User Story 5

- [x] T046 [US5] Create deploy-local.sh at scripts/deploy-local.sh
- [x] T047 [P] [US5] Create deploy-local.ps1 at scripts/deploy-local.ps1
- [x] T048 [US5] Create test-deployment.sh at scripts/test-deployment.sh
- [x] T049 [P] [US5] Create test-deployment.ps1 at scripts/test-deployment.ps1
- [x] T050 [US5] Create cleanup.sh at scripts/cleanup.sh (and cleanup.ps1)
- [ ] T051 [US5] Deploy application using deploy-local script
- [ ] T052 [US5] Verify frontend loads at http://todo.local
- [ ] T053 [US5] Test todo CRUD operations (create, read, update, delete)
- [ ] T054 [US5] Test AI chatbot functionality
- [ ] T055 [US5] Verify health probes are passing with kubectl describe
- [ ] T056 [US5] Check logs for errors with kubectl logs

**Checkpoint**: Application fully functional in Kubernetes, all Phase 3 features working

---

## Phase 8: User Story 6 - AIOps & Optimization (Priority: P6)

**Goal**: Use AIOps tools to analyze and optimize deployment

**Independent Test**: Document AI tool interactions and insights received

### Implementation for User Story 6

- [ ] T057 [US6] Install kubectl-ai plugin (if not already installed)
- [ ] T058 [US6] Use kubectl-ai to analyze pod status
- [ ] T059 [P] [US6] Use Gordon (if available) to analyze Dockerfile optimization
- [ ] T060 [P] [US6] Use kagent (if available) for cluster health analysis
- [x] T061 [US6] Document all AIOps interactions in specs/004-k8s-deployment/aiops-log.md ✅
- [ ] T062 [US6] Apply any recommended optimizations from AIOps tools

**Checkpoint**: AIOps tools used and documented, optimizations applied

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation and validation

- [x] T063 Update specs/004-k8s-deployment/quickstart.md with final tested commands
- [ ] T064 [P] Verify all scripts are executable (chmod +x scripts/*.sh)
- [ ] T065 Run complete deployment from scratch to validate quickstart guide
- [x] T066 [P] Update README.md at repository root with Phase 4 deployment instructions
- [x] T067 Complete pre-deployment checklist in spec.md ✅
- [x] T068 [P] Complete post-deployment checklist in spec.md (pending cluster for verification) ⚠️
- [x] T069 Final review: verify image sizes, non-root users (probes pending cluster) ⚠️

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────────────────────┐
                                                      │
Phase 2: Foundational ◄──────────────────────────────┘
    │
    ▼
Phase 3: US1 Docker Containerization (P1) 🎯 MVP
    │
    ▼
Phase 4: US2 Minikube Setup (P2)
    │
    ▼
Phase 5: US3 Kubernetes Manifests (P3)
    │
    ▼
Phase 6: US4 Helm Chart (P4)
    │
    ▼
Phase 7: US5 Deployment & Testing (P5)
    │
    ▼
Phase 8: US6 AIOps (P6)
    │
    ▼
Phase 9: Polish
```

### User Story Dependencies

- **US1 (Docker)**: Depends on Foundational phase (T005-T009)
- **US2 (Minikube)**: Depends on US1 (needs images to load)
- **US3 (Manifests)**: Depends on US2 (needs cluster running)
- **US4 (Helm)**: Depends on US3 (builds on manifest knowledge)
- **US5 (Deploy)**: Depends on US4 (uses Helm chart)
- **US6 (AIOps)**: Depends on US5 (needs running deployment)

### Within Each User Story

- Scripts before testing
- Configuration before resources
- Resources before deployment
- Deployment before verification

### Parallel Opportunities

Tasks marked [P] can run in parallel within their phase:
- T002, T003, T004 (directory creation)
- T013/T014 (bash/PowerShell scripts)
- T024/T025 (frontend/backend deployments)
- T036/T037 (Helm deployment templates)

---

## Parallel Example: User Story 4 (Helm Chart)

```bash
# Launch parallel template creation:
Task: "Create ConfigMap template at k8s/helm/todo-app/templates/configmap.yaml"
Task: "Create Secret template at k8s/helm/todo-app/templates/secret.yaml"

# Launch parallel deployment templates:
Task: "Create frontend Deployment template at k8s/helm/todo-app/templates/deployment-frontend.yaml"
Task: "Create backend Deployment template at k8s/helm/todo-app/templates/deployment-backend.yaml"

# Launch parallel service templates:
Task: "Create frontend Service template at k8s/helm/todo-app/templates/service-frontend.yaml"
Task: "Create backend Service template at k8s/helm/todo-app/templates/service-backend.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Docker)
4. **STOP and VALIDATE**: Build images, run containers, verify health
5. Demo containerized application running locally

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Docker) → Test images → Demo (MVP!)
3. Add US2 (Minikube) → Test cluster → Demo
4. Add US3 (Manifests) → Test kubectl apply → Demo
5. Add US4 (Helm) → Test helm install → Demo
6. Add US5 (Deploy/Test) → Full validation → Demo
7. Add US6 (AIOps) → Document learnings → Demo
8. Polish → Final docs → Complete

### Estimated Task Counts

| Phase | Tasks | Parallel | Story |
|-------|-------|----------|-------|
| Setup | 4 | 3 | - |
| Foundational | 5 | 1 | - |
| US1 Docker | 7 | 2 | P1 |
| US2 Minikube | 5 | 0 | P2 |
| US3 Manifests | 8 | 3 | P3 |
| US4 Helm | 16 | 7 | P4 |
| US5 Deploy | 11 | 2 | P5 |
| US6 AIOps | 6 | 2 | P6 |
| Polish | 7 | 3 | - |
| **Total** | **69** | **23** | - |

---

## Notes

- [P] tasks = different files, no dependencies
- [US#] label maps task to specific user story
- Each user story is independently testable at its checkpoint
- Verify at each checkpoint before proceeding
- Commit after each phase or logical group
- Stop at any checkpoint to demo progress
- Avoid: cross-story dependencies, uncommitted secrets, skipping foundational tasks
