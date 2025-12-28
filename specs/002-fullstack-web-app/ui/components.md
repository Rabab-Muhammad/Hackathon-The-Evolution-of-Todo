# UI Specification: Components

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the reusable UI components that make up the application interface, ensuring consistency, accessibility, and responsive behavior across all pages.

## Component Overview

| Category | Components |
|----------|------------|
| Forms | InputField, Button, Form |
| Layout | Header, Footer, Container, Card |
| Navigation | NavLink, UserMenu |
| Task | TaskItem, TaskList, TaskForm |
| Feedback | Alert, LoadingSpinner, EmptyState |

---

## Form Components

### InputField

A reusable form input with label and validation feedback.

**User Scenarios**:
- User enters email address for login
- User enters password for authentication
- User enters task title when creating/editing tasks

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| label | Yes | Display label for the field |
| type | Yes | Input type (text, email, password) |
| placeholder | No | Placeholder text |
| error | No | Validation error message |
| disabled | No | Disable input interaction |

**Behavior**:
- Shows label above input field
- Displays error message below input when validation fails
- Error state changes border color to indicate problem
- Supports keyboard navigation (Tab to focus)

**Acceptance Criteria**:
- [ ] Label is associated with input for accessibility
- [ ] Error message is announced to screen readers
- [ ] Focus state is visually distinct
- [ ] Works on mobile (touch targets >= 44px)

---

### Button

A clickable button for form submission and actions.

**User Scenarios**:
- User submits login form
- User creates a new task
- User deletes a task

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| label | Yes | Button text |
| variant | No | Style variant (primary, secondary, danger) |
| disabled | No | Disable button interaction |
| loading | No | Show loading state |
| type | No | Button type (button, submit) |

**Variants**:
- **Primary**: Main actions (Submit, Save)
- **Secondary**: Alternative actions (Cancel)
- **Danger**: Destructive actions (Delete)

**Behavior**:
- Primary variant has prominent styling
- Danger variant uses warning color
- Loading state shows spinner and disables click
- Disabled state grays out button

**Acceptance Criteria**:
- [ ] Keyboard accessible (Enter/Space to activate)
- [ ] Loading state prevents multiple submissions
- [ ] Touch target meets minimum size (44x44px)
- [ ] Focus state is clearly visible

---

## Layout Components

### Header

Top navigation bar with branding and user actions.

**User Scenarios**:
- User sees application name/logo
- User accesses their account menu
- User navigates to different sections

**Structure**:
```
┌────────────────────────────────────────────────────────┐
│  Logo/Name              [User Menu / Auth Links]       │
└────────────────────────────────────────────────────────┘
```

**Behavior**:
- Displays application name on left
- Shows login/signup links when unauthenticated
- Shows user menu with logout option when authenticated
- Remains fixed at top on scroll (optional)

**Acceptance Criteria**:
- [ ] Logo/name links to dashboard when authenticated
- [ ] User menu shows current user's email
- [ ] Responsive: collapses to hamburger menu on mobile

---

### Card

A container for grouped content.

**User Scenarios**:
- Task items displayed in cards
- Login/signup forms wrapped in cards

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| title | No | Card header text |
| padding | No | Internal spacing |

**Behavior**:
- Provides visual grouping with border/shadow
- Optional header section for title

**Acceptance Criteria**:
- [ ] Consistent padding across all usages
- [ ] Readable contrast between card and background

---

## Task Components

### TaskItem

Displays a single task with actions.

**User Scenarios**:
- User views task title and status
- User marks task as complete
- User edits task details
- User deletes task

**Structure**:
```
┌──────────────────────────────────────────────────────┐
│ [✓] Task Title                          [Edit][Delete]│
│     Task description (if present)                     │
└──────────────────────────────────────────────────────┘
```

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| task | Yes | Task data object |
| onToggle | Yes | Handler for completion toggle |
| onEdit | Yes | Handler for edit action |
| onDelete | Yes | Handler for delete action |

**Behavior**:
- Checkbox toggles completion status
- Completed tasks show strikethrough on title
- Edit button opens edit mode or modal
- Delete button shows confirmation before deleting
- Description shown below title if present

**Acceptance Criteria**:
- [ ] Checkbox is keyboard accessible
- [ ] Completed state is visually distinct
- [ ] Delete requires confirmation
- [ ] Actions are discoverable but not intrusive

---

### TaskList

Container for displaying multiple tasks.

**User Scenarios**:
- User views all their tasks
- User sees empty state when no tasks exist

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| tasks | Yes | Array of task objects |
| onToggle | Yes | Handler for completion toggle |
| onEdit | Yes | Handler for edit action |
| onDelete | Yes | Handler for delete action |

**Behavior**:
- Renders TaskItem for each task
- Shows EmptyState when no tasks
- Tasks ordered by creation date (newest first)

**Acceptance Criteria**:
- [ ] Renders all tasks correctly
- [ ] Empty state is helpful and actionable
- [ ] List is scrollable when many tasks

---

### TaskForm

Form for creating and editing tasks.

**User Scenarios**:
- User creates a new task
- User edits an existing task

**Structure**:
```
┌─────────────────────────────────────────┐
│ Title:     [________________]           │
│ Description: [________________]         │
│            [________________]           │
│                                         │
│            [Cancel]  [Save]             │
└─────────────────────────────────────────┘
```

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| task | No | Existing task for edit mode |
| onSubmit | Yes | Handler for form submission |
| onCancel | Yes | Handler for cancel action |

**Behavior**:
- Title field is required
- Description field is optional, multiline
- Pre-fills fields when editing existing task
- Validates before submission
- Shows loading state during save

**Acceptance Criteria**:
- [ ] Title validation shows error if empty
- [ ] Form submits on Enter in title field
- [ ] Cancel clears form and dismisses
- [ ] Loading prevents duplicate submissions

---

## Feedback Components

### Alert

Displays success, error, or informational messages.

**User Scenarios**:
- User sees success message after creating task
- User sees error message after failed login

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| type | Yes | Alert type (success, error, info, warning) |
| message | Yes | Alert message text |
| dismissible | No | Allow user to dismiss |

**Behavior**:
- Color-coded by type (green=success, red=error)
- Optional close button for dismissal
- Auto-dismiss after timeout (optional)

**Acceptance Criteria**:
- [ ] Screen readers announce alerts
- [ ] Color is not only indicator (use icons)
- [ ] Dismissible alerts have clear close action

---

### LoadingSpinner

Indicates loading state.

**User Scenarios**:
- User waits for tasks to load
- User waits for form submission

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| size | No | Spinner size (small, medium, large) |
| label | No | Accessible loading text |

**Behavior**:
- Animated spinner indicates activity
- Accessible label for screen readers

**Acceptance Criteria**:
- [ ] Animation doesn't cause accessibility issues
- [ ] Loading state is communicated to screen readers

---

### EmptyState

Displays when a list has no items.

**User Scenarios**:
- New user sees empty task list
- User deletes all tasks

**Props/Attributes**:
| Attribute | Required | Description |
|-----------|----------|-------------|
| title | Yes | Empty state headline |
| message | No | Helpful description |
| action | No | Call-to-action button |

**Behavior**:
- Shows friendly message
- Optionally includes action to create first item

**Acceptance Criteria**:
- [ ] Message is encouraging, not critical
- [ ] Action is clear and prominent

---

## Accessibility Requirements

All components MUST:
- Support keyboard navigation
- Have sufficient color contrast (WCAG AA)
- Include appropriate ARIA labels
- Work with screen readers
- Have focus indicators

## Responsive Behavior

| Breakpoint | Behavior |
|------------|----------|
| Mobile (< 640px) | Single column, stacked layouts |
| Tablet (640-1024px) | Flexible layouts, side margins |
| Desktop (> 1024px) | Centered content, max-width container |

## Success Criteria

### Measurable Outcomes

- **SC-001**: All interactive elements have 44x44px minimum touch target
- **SC-002**: Color contrast ratio meets WCAG AA (4.5:1 for text)
- **SC-003**: All forms are completable using keyboard only
- **SC-004**: Components render correctly on 320px minimum width
- **SC-005**: Loading states appear within 100ms of action
