# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/002-fullstack-web-app/`
**Prerequisites**: plan.md, overview.md, research.md, data-model.md, contracts/api-contract.md, quickstart.md
**Branch**: `002-fullstack-web-app`
**Date**: 2025-12-28

**Tests**: Tests are NOT explicitly requested in this phase. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend: Python (FastAPI + SQLModel)
- Frontend: TypeScript (Next.js + React)

## User Story Mapping

| Story ID | Priority | Title | Source |
|----------|----------|-------|--------|
| US1 | P1 | User Registration | @specs/features/authentication.md |
| US2 | P2 | User Login | @specs/features/authentication.md |
| US3 | P3 | User Logout | @specs/features/authentication.md |
| US4 | P4 | Session Persistence | @specs/features/authentication.md |
| US5 | P1 | Create Task | @specs/features/task-crud.md |
| US6 | P2 | View Tasks | @specs/features/task-crud.md |
| US7 | P3 | Update Task | @specs/features/task-crud.md |
| US8 | P4 | Delete Task | @specs/features/task-crud.md |
| US9 | P5 | Toggle Task Completion | @specs/features/task-crud.md |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure
**Reference**: @specs/plan.md Section 1, @constitution Mandatory Monorepo Structure

- [x] T001 Create monorepo folder structure with frontend/, backend/, specs/ directories
- [x] T002 [P] Initialize Next.js 16+ project with TypeScript in frontend/ directory
- [x] T003 [P] Initialize FastAPI project with SQLModel in backend/ directory
- [x] T004 [P] Create root CLAUDE.md with project overview per @constitution SC-005
- [x] T005 [P] Create frontend/CLAUDE.md with frontend-specific instructions per @constitution SC-005
- [x] T006 [P] Create backend/CLAUDE.md with backend-specific instructions per @constitution SC-005
- [x] T007 [P] Create backend/.env.example with DATABASE_URL and BETTER_AUTH_SECRET placeholders
- [x] T008 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET placeholders
- [x] T009 [P] Configure Tailwind CSS in frontend/tailwind.config.js per @specs/ui/components.md
- [x] T010 Create docker-compose.yml for local development per @constitution Mandatory Structure
- [x] T011 [P] Create root README.md with project overview and setup instructions

**Checkpoint**: Project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented
**Reference**: @specs/plan.md Section 2, @specs/database/schema.md, @specs/api/jwt-auth.md

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Infrastructure

- [x] T012 Create backend/src/core/config.py with environment variable loading (DATABASE_URL, BETTER_AUTH_SECRET) per @specs/architecture.md
- [x] T013 Create backend/src/core/database.py with SQLModel engine and session management per @specs/database/schema.md
- [x] T014 Create backend/src/models/__init__.py with model imports
- [x] T015 Create backend/src/models/user.py with User SQLModel entity per @specs/database/schema.md (id, email, password_hash, created_at)
- [x] T016 Create backend/src/models/task.py with Task SQLModel entity per @specs/database/schema.md (id, user_id FK, title, description, completed, created_at, updated_at)
- [x] T017 Create backend/src/db/migrate.py migration script to create tables per @specs/database/schema.md Migration Strategy

### Security Infrastructure

- [x] T018 Create backend/src/core/security.py with password hashing functions (hash_password, verify_password) using bcrypt per @specs/features/authentication.md FR-005
- [x] T019 Add JWT creation function (create_access_token) to backend/src/core/security.py per @specs/api/jwt-auth.md Token Structure
- [x] T020 Add JWT verification function (verify_token) to backend/src/core/security.py per @specs/api/jwt-auth.md Backend Token Validation

### API Infrastructure

- [x] T021 Create backend/src/main.py with FastAPI app initialization and CORS configuration per @specs/architecture.md
- [x] T022 Create backend/src/core/dependencies.py with get_db dependency per @specs/architecture.md Service Layer
- [x] T023 Add get_current_user dependency to backend/src/core/dependencies.py for JWT validation per @specs/api/jwt-auth.md
- [x] T024 Create backend/src/schemas/__init__.py with schema imports
- [x] T025 Create backend/src/schemas/error.py with ErrorResponse schema per @specs/api/rest-endpoints.md Error Response Format
- [x] T026 Create backend/src/api/__init__.py with router imports
- [x] T027 Create backend/src/api/router.py main router aggregating auth and tasks routers per @specs/api/rest-endpoints.md

### Frontend Infrastructure

- [x] T028 Create frontend/src/lib/types.ts with TypeScript interfaces (User, Task, AuthResponse, ErrorResponse) per @specs/data-model.md Frontend Types
- [x] T029 Create frontend/src/lib/api.ts with base API client and token handling per @specs/architecture.md API Client Architecture
- [x] T030 Create frontend/src/lib/auth.ts with token storage utilities (getToken, setToken, clearToken) per @specs/api/jwt-auth.md Frontend Token Handling
- [x] T031 Create frontend/src/app/layout.tsx root layout with basic HTML structure per @specs/ui/pages.md
- [x] T032 Create frontend/src/middleware.ts for route protection per @specs/ui/pages.md Route Protection

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: New users can create an account to access the application
**Reference**: @specs/features/authentication.md User Story 1
**Independent Test**: Complete registration form and verify redirect to dashboard with empty task list

### Backend Implementation

- [x] T033 [P] [US1] Create backend/src/schemas/auth.py with SignupRequest and AuthResponse schemas per @specs/contracts/api-contract.md POST /api/auth/signup
- [x] T034 [US1] Create backend/src/services/__init__.py with service imports
- [x] T035 [US1] Create backend/src/services/auth.py with signup function (validate email uniqueness, hash password, create user, generate JWT) per @specs/features/authentication.md Registration Flow
- [x] T036 [US1] Create backend/src/api/auth.py with POST /api/auth/signup endpoint per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T037 [P] [US1] Create frontend/src/components/ui/Button.tsx with primary, secondary, danger, loading variants per @specs/ui/components.md Button
- [x] T038 [P] [US1] Create frontend/src/components/ui/Input.tsx with label, error, disabled states per @specs/ui/components.md InputField
- [x] T039 [P] [US1] Create frontend/src/components/ui/Card.tsx container component per @specs/ui/components.md Card
- [x] T040 [P] [US1] Create frontend/src/components/ui/Alert.tsx with success, error, info, warning types per @specs/ui/components.md Alert
- [x] T041 [P] [US1] Create frontend/src/components/ui/LoadingSpinner.tsx per @specs/ui/components.md LoadingSpinner
- [x] T042 [US1] Create frontend/src/components/layout/Header.tsx with logo and auth links per @specs/ui/components.md Header
- [x] T043 [US1] Create frontend/src/components/layout/Footer.tsx per @specs/ui/components.md
- [x] T044 [US1] Create frontend/src/components/auth/SignupForm.tsx with email, password fields and validation per @specs/ui/pages.md Signup Page
- [x] T045 [US1] Add signup API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md POST /api/auth/signup
- [x] T046 [US1] Create frontend/src/app/signup/page.tsx signup page with SignupForm per @specs/ui/pages.md Signup Page
- [x] T047 [US1] Create frontend/src/app/page.tsx home/landing page with Get Started CTA per @specs/ui/pages.md Home/Landing Page

**Checkpoint**: User registration fully functional - new users can create accounts

---

## Phase 4: User Story 2 - User Login (Priority: P2)

**Goal**: Existing users can sign in to access their tasks
**Reference**: @specs/features/authentication.md User Story 2
**Independent Test**: Login with valid credentials and verify redirect to dashboard

### Backend Implementation

- [x] T048 [P] [US2] Add SigninRequest schema to backend/src/schemas/auth.py per @specs/contracts/api-contract.md POST /api/auth/signin
- [x] T049 [US2] Add signin function to backend/src/services/auth.py (lookup user, verify password, generate JWT) per @specs/features/authentication.md Login Flow
- [x] T050 [US2] Add POST /api/auth/signin endpoint to backend/src/api/auth.py per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T051 [US2] Create frontend/src/components/auth/LoginForm.tsx with email, password fields and validation per @specs/ui/pages.md Login Page
- [x] T052 [US2] Add signin API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md POST /api/auth/signin
- [x] T053 [US2] Create frontend/src/app/login/page.tsx login page with LoginForm per @specs/ui/pages.md Login Page
- [x] T054 [US2] Update Header component to show user email when authenticated per @specs/ui/components.md Header

**Checkpoint**: User login fully functional - returning users can access their accounts

---

## Phase 5: User Story 3 - User Logout (Priority: P3)

**Goal**: Logged-in users can sign out to secure their session
**Reference**: @specs/features/authentication.md User Story 3
**Independent Test**: Click logout and verify redirect to login page, protected routes inaccessible

### Backend Implementation

- [x] T055 [US3] Add POST /api/auth/signout endpoint to backend/src/api/auth.py (requires auth) per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T056 [US3] Add signout API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md POST /api/auth/signout
- [x] T057 [US3] Add logout button and handler to Header component per @specs/ui/components.md Header
- [x] T058 [US3] Implement token clearing and redirect on logout in frontend/src/lib/auth.ts per @specs/api/jwt-auth.md Frontend Token Handling

**Checkpoint**: User logout fully functional - users can securely end sessions

---

## Phase 6: User Story 4 - Session Persistence (Priority: P4)

**Goal**: Session persists across browser tabs and page refreshes
**Reference**: @specs/features/authentication.md User Story 4
**Independent Test**: Login, refresh page, verify still authenticated

### Frontend Implementation

- [x] T059 [US4] Update frontend/src/middleware.ts to check token on protected routes per @specs/ui/pages.md Route Protection
- [x] T060 [US4] Update frontend/src/app/layout.tsx to initialize auth state from stored token per @specs/api/jwt-auth.md Token Lifecycle
- [x] T061 [US4] Add automatic redirect for authenticated users visiting /login or /signup per @specs/ui/pages.md Redirect Behavior

**Checkpoint**: Session persistence functional - users stay logged in across refreshes

---

## Phase 7: User Story 5 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks
**Reference**: @specs/features/task-crud.md User Story 1
**Independent Test**: Create task and verify it appears in task list

### Backend Implementation

- [x] T062 [P] [US5] Create backend/src/schemas/task.py with TaskCreateRequest, TaskResponse, TaskListResponse schemas per @specs/contracts/api-contract.md
- [x] T063 [US5] Create backend/src/services/task.py with create_task function per @specs/features/task-crud.md Create Task Flow
- [x] T064 [US5] Create backend/src/api/tasks.py with POST /api/tasks endpoint (requires auth) per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T065 [P] [US5] Create frontend/src/components/tasks/TaskForm.tsx with title (required) and description fields per @specs/ui/components.md TaskForm
- [x] T066 [US5] Add createTask API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md POST /api/tasks

**Checkpoint**: Task creation functional - users can add new tasks

---

## Phase 8: User Story 6 - View Tasks (Priority: P2)

**Goal**: Authenticated users can view all their tasks
**Reference**: @specs/features/task-crud.md User Story 2
**Independent Test**: Login and verify task list displays correctly

### Backend Implementation

- [x] T067 [US6] Add get_user_tasks function to backend/src/services/task.py (filtered by user_id) per @specs/features/task-crud.md Read Tasks Flow
- [x] T068 [US6] Add GET /api/tasks endpoint to backend/src/api/tasks.py per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T069 [P] [US6] Create frontend/src/components/tasks/TaskItem.tsx with checkbox, title, description, edit, delete buttons per @specs/ui/components.md TaskItem
- [x] T070 [P] [US6] Create frontend/src/components/tasks/EmptyState.tsx for empty task list per @specs/ui/components.md EmptyState
- [x] T071 [US6] Create frontend/src/components/tasks/TaskList.tsx rendering TaskItem for each task per @specs/ui/components.md TaskList
- [x] T072 [US6] Add getTasks API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md GET /api/tasks
- [x] T073 [US6] Create frontend/src/app/dashboard/page.tsx with TaskList and New Task button per @specs/ui/pages.md Dashboard Page

**Checkpoint**: Task viewing functional - users can see all their tasks

---

## Phase 9: User Story 7 - Update Task (Priority: P3)

**Goal**: Authenticated users can edit their tasks
**Reference**: @specs/features/task-crud.md User Story 3
**Independent Test**: Edit task title/description and verify changes persist

### Backend Implementation

- [x] T074 [P] [US7] Add TaskUpdateRequest schema to backend/src/schemas/task.py per @specs/contracts/api-contract.md PUT /api/tasks/{task_id}
- [x] T075 [US7] Add update_task function to backend/src/services/task.py (verify ownership, update fields) per @specs/features/task-crud.md Update Task Flow
- [x] T076 [US7] Add PUT /api/tasks/{task_id} endpoint to backend/src/api/tasks.py per @specs/api/rest-endpoints.md
- [x] T077 [US7] Add GET /api/tasks/{task_id} endpoint to backend/src/api/tasks.py per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T078 [US7] Add updateTask API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md PUT /api/tasks/{task_id}
- [x] T079 [US7] Update TaskItem component with edit button handler opening TaskForm in edit mode per @specs/ui/pages.md Task Edit Flow
- [x] T080 [US7] Update TaskForm to pre-fill fields when editing existing task per @specs/ui/components.md TaskForm

**Checkpoint**: Task updating functional - users can edit their tasks

---

## Phase 10: User Story 8 - Delete Task (Priority: P4)

**Goal**: Authenticated users can delete their tasks
**Reference**: @specs/features/task-crud.md User Story 4
**Independent Test**: Delete task and verify it no longer appears in list

### Backend Implementation

- [x] T081 [US8] Add delete_task function to backend/src/services/task.py (verify ownership, delete) per @specs/features/task-crud.md Delete Task Flow
- [x] T082 [US8] Add DELETE /api/tasks/{task_id} endpoint to backend/src/api/tasks.py per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T083 [US8] Add deleteTask API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md DELETE /api/tasks/{task_id}
- [x] T084 [US8] Update TaskItem component with delete button and confirmation dialog per @specs/ui/pages.md Task Delete Flow

**Checkpoint**: Task deletion functional - users can remove tasks

---

## Phase 11: User Story 9 - Toggle Task Completion (Priority: P5)

**Goal**: Authenticated users can mark tasks complete/incomplete
**Reference**: @specs/features/task-crud.md User Story 5
**Independent Test**: Toggle task status and verify change persists across refresh

### Backend Implementation

- [x] T085 [US9] Add toggle_task function to backend/src/services/task.py (flip completed boolean) per @specs/features/task-crud.md
- [x] T086 [US9] Add PATCH /api/tasks/{task_id}/toggle endpoint to backend/src/api/tasks.py per @specs/api/rest-endpoints.md

### Frontend Implementation

- [x] T087 [US9] Add toggleTask API call to frontend/src/lib/api.ts per @specs/contracts/api-contract.md PATCH /api/tasks/{task_id}/toggle
- [x] T088 [US9] Update TaskItem checkbox to call toggle API and update local state per @specs/ui/components.md TaskItem

**Checkpoint**: Task toggle functional - users can mark tasks complete/incomplete

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories
**Reference**: @specs/plan.md Section 11, @specs/quickstart.md

- [x] T089 Add rate limiting middleware to backend/src/main.py per @specs/api/rest-endpoints.md Rate Limiting
- [x] T090 Add global error handler to backend/src/main.py per @specs/api/rest-endpoints.md Error Response Format
- [x] T091 [P] Update frontend/src/lib/api.ts to handle 401 responses with redirect to login per @specs/api/jwt-auth.md FR-JWT-010
- [x] T092 [P] Add responsive styles to all components per @specs/ui/components.md Responsive Behavior
- [x] T093 [P] Add loading states to dashboard page per @specs/ui/pages.md Loading States
- [x] T094 Verify all endpoints return correct HTTP status codes per @specs/api/rest-endpoints.md Acceptance Criteria
- [x] T095 Run quickstart.md verification steps per @specs/quickstart.md Verification Steps
- [x] T096 Update root README.md with complete setup instructions per @specs/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-11)**: All depend on Foundational phase completion
  - US1 (Registration) and US5 (Create Task) are P1 - MVP core
  - US2 (Login) depends on US1 (need registered user to login)
  - US3 (Logout) depends on US2 (need logged in user to logout)
  - US4 (Session) depends on US2 (need login to have session)
  - US6 (View Tasks) depends on US5 (need tasks to view)
  - US7 (Update), US8 (Delete), US9 (Toggle) depend on US5 and US6
- **Polish (Phase 12)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
     ↓
Phase 2: Foundational (BLOCKS ALL)
     ↓
┌────┴────┐
↓         ↓
US1       US5
(Reg)     (Create)
↓         ↓
US2       US6
(Login)   (View)
↓         ↓
US3       US7, US8, US9
(Logout)  (Update, Delete, Toggle)
↓
US4
(Session)
     ↓
Phase 12: Polish
```

### Within Each User Story

- Models before services (already in Foundational)
- Schemas before API endpoints
- Backend API before frontend integration
- Components before pages

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T011)
- All Foundational backend schemas [P] can run in parallel
- Frontend UI components marked [P] can run in parallel (T037-T041)
- Once Foundational phase completes, Auth stories and Task stories can proceed in parallel tracks

---

## Parallel Execution Examples

### Phase 1 - Setup (Parallel)
```
Task: T002 - Initialize Next.js project
Task: T003 - Initialize FastAPI project
Task: T004 - Create root CLAUDE.md
Task: T005 - Create frontend/CLAUDE.md
Task: T006 - Create backend/CLAUDE.md
Task: T007 - Create backend/.env.example
Task: T008 - Create frontend/.env.example
Task: T009 - Configure Tailwind CSS
Task: T011 - Create README.md
```

### Phase 3 - US1 Frontend Components (Parallel)
```
Task: T037 - Create Button component
Task: T038 - Create Input component
Task: T039 - Create Card component
Task: T040 - Create Alert component
Task: T041 - Create LoadingSpinner component
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 5, 6)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Registration (US1)
4. Complete Phase 4: User Login (US2)
5. Complete Phase 7: Create Task (US5)
6. Complete Phase 8: View Tasks (US6)
7. **STOP and VALIDATE**: Users can register, login, create and view tasks
8. Deploy/demo MVP

### Incremental Delivery

1. MVP (Phases 1-4, 7-8) → Core functionality
2. Add Logout (Phase 5) → Security complete
3. Add Session Persistence (Phase 6) → UX improvement
4. Add Update Task (Phase 9) → Edit capability
5. Add Delete Task (Phase 10) → Cleanup capability
6. Add Toggle (Phase 11) → Completion tracking
7. Polish (Phase 12) → Production ready

---

## Summary

| Phase | Story | Tasks | Parallel |
|-------|-------|-------|----------|
| 1 | Setup | 11 | 9 |
| 2 | Foundational | 21 | 4 |
| 3 | US1 Registration | 15 | 7 |
| 4 | US2 Login | 7 | 1 |
| 5 | US3 Logout | 4 | 0 |
| 6 | US4 Session | 3 | 0 |
| 7 | US5 Create Task | 5 | 2 |
| 8 | US6 View Tasks | 7 | 2 |
| 9 | US7 Update Task | 7 | 1 |
| 10 | US8 Delete Task | 4 | 0 |
| 11 | US9 Toggle | 4 | 0 |
| 12 | Polish | 8 | 3 |

**Total Tasks**: 96
**Parallelizable Tasks**: 29
**MVP Tasks**: 54 (Phases 1-4, 7-8)

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks reference spec files for traceability per @constitution II. End-to-End Traceability
