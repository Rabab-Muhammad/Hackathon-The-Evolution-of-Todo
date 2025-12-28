# UI Specification: Pages

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the application pages, their layouts, user flows, and routing behavior for the full-stack todo application.

## Page Overview

| Page | Route | Auth Required | Description |
|------|-------|---------------|-------------|
| Home/Landing | `/` | No | Welcome page, redirects authenticated users |
| Login | `/login` | No | User authentication |
| Signup | `/signup` | No | User registration |
| Dashboard | `/dashboard` | Yes | Main task management view |

---

## Home/Landing Page

**Route**: `/`

### Purpose

Welcome new visitors and direct them to authentication.

### Layout

```
┌────────────────────────────────────────────────────────────┐
│                         Header                              │
│  [Logo]                              [Login] [Sign Up]      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│                     Welcome Message                         │
│                                                             │
│              "Organize your tasks with ease"                │
│                                                             │
│                   [Get Started →]                           │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                         Footer                              │
└────────────────────────────────────────────────────────────┘
```

### Behavior

- If user is authenticated: Redirect to `/dashboard`
- If user is not authenticated: Show welcome content
- "Get Started" button links to `/signup`

### User Scenarios

**Given** I am a new visitor, **When** I visit the home page, **Then** I see welcome content and options to login or signup.

**Given** I am logged in, **When** I visit the home page, **Then** I am redirected to my dashboard.

### Acceptance Criteria

- [ ] Welcome message explains the application value
- [ ] Clear calls-to-action for login and signup
- [ ] Authenticated users are redirected immediately

---

## Login Page

**Route**: `/login`

### Purpose

Allow existing users to authenticate and access their tasks.

### Layout

```
┌────────────────────────────────────────────────────────────┐
│                         Header                              │
│  [Logo]                              [Login] [Sign Up]      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│                  ┌─────────────────────┐                    │
│                  │    Welcome Back     │                    │
│                  │                     │                    │
│                  │  Email:             │                    │
│                  │  [_______________]  │                    │
│                  │                     │                    │
│                  │  Password:          │                    │
│                  │  [_______________]  │                    │
│                  │                     │                    │
│                  │  [    Sign In    ]  │                    │
│                  │                     │                    │
│                  │  Don't have an      │                    │
│                  │  account? Sign up   │                    │
│                  └─────────────────────┘                    │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                         Footer                              │
└────────────────────────────────────────────────────────────┘
```

### Form Fields

| Field | Type | Validation | Required |
|-------|------|------------|----------|
| Email | email | Valid email format | Yes |
| Password | password | Non-empty | Yes |

### Behavior

- If user is authenticated: Redirect to `/dashboard`
- On successful login: Redirect to `/dashboard`
- On failed login: Show error message (generic, not revealing which field was wrong)
- Link to signup page for new users

### User Scenarios

**Given** I am on the login page with valid credentials, **When** I submit the form, **Then** I am logged in and redirected to my dashboard.

**Given** I am on the login page with invalid credentials, **When** I submit the form, **Then** I see an error message.

**Given** I am already logged in, **When** I visit the login page, **Then** I am redirected to my dashboard.

### Acceptance Criteria

- [ ] Form validates email format
- [ ] Form validates password presence
- [ ] Error messages don't reveal account existence
- [ ] Loading state shown during authentication
- [ ] Link to signup is visible
- [ ] Form is keyboard navigable

---

## Signup Page

**Route**: `/signup`

### Purpose

Allow new users to create an account.

### Layout

```
┌────────────────────────────────────────────────────────────┐
│                         Header                              │
│  [Logo]                              [Login] [Sign Up]      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│                  ┌─────────────────────┐                    │
│                  │   Create Account    │                    │
│                  │                     │                    │
│                  │  Email:             │                    │
│                  │  [_______________]  │                    │
│                  │                     │                    │
│                  │  Password:          │                    │
│                  │  [_______________]  │                    │
│                  │  (min 8 characters) │                    │
│                  │                     │                    │
│                  │  [   Sign Up    ]   │                    │
│                  │                     │                    │
│                  │  Already have an    │                    │
│                  │  account? Sign in   │                    │
│                  └─────────────────────┘                    │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                         Footer                              │
└────────────────────────────────────────────────────────────┘
```

### Form Fields

| Field | Type | Validation | Required |
|-------|------|------------|----------|
| Email | email | Valid email format, unique | Yes |
| Password | password | Minimum 8 characters | Yes |

### Behavior

- If user is authenticated: Redirect to `/dashboard`
- On successful signup: Redirect to `/dashboard` (auto-login)
- On failed signup (email exists): Show error message
- Show password requirements hint
- Link to login page for existing users

### User Scenarios

**Given** I am on the signup page with valid data, **When** I submit the form, **Then** my account is created and I am redirected to my dashboard.

**Given** I am on the signup page with an existing email, **When** I submit the form, **Then** I see an error indicating the email is taken.

**Given** I am on the signup page with a weak password, **When** I try to submit, **Then** I see a validation error about password requirements.

### Acceptance Criteria

- [ ] Form validates email format
- [ ] Form validates email uniqueness (server-side)
- [ ] Form validates password minimum length
- [ ] Password requirements shown before submission
- [ ] Error messages are clear and actionable
- [ ] Loading state shown during registration
- [ ] Link to login is visible

---

## Dashboard Page

**Route**: `/dashboard`

### Purpose

Main task management interface where users create, view, edit, and delete their tasks.

### Layout

```
┌────────────────────────────────────────────────────────────┐
│                         Header                              │
│  [Logo]                              [user@email] [Logout]  │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  My Tasks                              [+ New Task]         │
│  ─────────────────────────────────────────────────         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ [✓] Task 1 Title                    [Edit] [Delete]  │  │
│  │     Task 1 description                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ [ ] Task 2 Title                    [Edit] [Delete]  │  │
│  │     Task 2 description                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  [Empty State when no tasks]                                │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                         Footer                              │
└────────────────────────────────────────────────────────────┘
```

### Features

1. **Task List**: Display all user's tasks
2. **Create Task**: Add new task via form/modal
3. **Edit Task**: Modify existing task
4. **Delete Task**: Remove task with confirmation
5. **Toggle Status**: Mark task complete/incomplete

### Task Creation Flow

```
1. User clicks "New Task" button
2. Task form appears (modal or inline)
3. User enters title (required) and description (optional)
4. User clicks "Save"
5. Task appears in list
6. Form closes/resets
```

### Task Edit Flow

```
1. User clicks "Edit" on a task
2. Task form appears with current values
3. User modifies title and/or description
4. User clicks "Save"
5. Task updates in list
6. Form closes
```

### Task Delete Flow

```
1. User clicks "Delete" on a task
2. Confirmation dialog appears
3. User confirms deletion
4. Task removed from list
5. Success feedback shown
```

### Empty State

When user has no tasks, show encouraging message:
- "No tasks yet"
- "Create your first task to get started"
- Prominent "New Task" button

### Behavior

- If user is not authenticated: Redirect to `/login`
- Tasks load automatically on page visit
- All operations update UI optimistically when possible
- Errors shown via Alert component

### User Scenarios

**Given** I am logged in with existing tasks, **When** I visit the dashboard, **Then** I see all my tasks listed.

**Given** I am logged in with no tasks, **When** I visit the dashboard, **Then** I see the empty state with instructions.

**Given** I am not logged in, **When** I try to access the dashboard, **Then** I am redirected to login.

**Given** I create a new task, **When** the operation succeeds, **Then** the task appears in my list immediately.

### Acceptance Criteria

- [ ] Page loads tasks on initial visit
- [ ] Tasks display title, description, and status
- [ ] Users can create new tasks
- [ ] Users can edit existing tasks
- [ ] Users can delete tasks with confirmation
- [ ] Users can toggle task completion
- [ ] Empty state is shown when no tasks
- [ ] User email shown in header
- [ ] Logout button ends session
- [ ] Unauthorized access redirects to login

---

## Route Protection

### Protected Routes

| Route | Protection |
|-------|------------|
| `/dashboard` | Requires authentication |

### Redirect Behavior

| Scenario | Redirect To |
|----------|-------------|
| Unauthenticated user visits protected route | `/login?redirect={original_path}` |
| Authenticated user visits `/login` or `/signup` | `/dashboard` |
| Authenticated user visits `/` | `/dashboard` |
| User logs out | `/login` |

## Responsive Behavior

### Mobile (< 640px)

- Full-width forms
- Stacked task actions
- Hamburger menu for navigation
- Touch-friendly button sizes

### Tablet (640-1024px)

- Centered forms with max-width
- Side-by-side task actions
- Full navigation visible

### Desktop (> 1024px)

- Centered content with max-width container
- Comfortable spacing
- Full navigation visible

## Loading States

| Page/Action | Loading Indicator |
|-------------|-------------------|
| Initial page load | Full page spinner |
| Task list loading | Skeleton or spinner |
| Form submission | Button loading state |
| Task operations | Inline loading indicator |

## Error States

| Error Type | Display |
|------------|---------|
| Authentication failure | Alert on login/signup form |
| Task operation failure | Toast/Alert notification |
| Network error | Alert with retry option |
| 404 page not found | Friendly 404 page |

## Success Criteria

### Measurable Outcomes

- **SC-001**: Dashboard loads and displays tasks within 3 seconds
- **SC-002**: Users can complete task creation in under 10 seconds
- **SC-003**: All pages are usable on 320px minimum width
- **SC-004**: Protected routes redirect unauthenticated users within 1 second
- **SC-005**: Form submissions provide feedback within 500ms
