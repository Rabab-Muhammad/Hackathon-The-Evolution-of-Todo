# Frontend CLAUDE.md - Next.js Application

## Overview

Next.js 16+ application with App Router, TypeScript, and Tailwind CSS for Phase II todo application.

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page (/)
│   │   ├── login/page.tsx      # Login page
│   │   ├── signup/page.tsx     # Signup page
│   │   └── dashboard/page.tsx  # Dashboard (protected)
│   ├── components/
│   │   ├── ui/                 # Base components
│   │   ├── layout/             # Header, Footer
│   │   ├── auth/               # LoginForm, SignupForm
│   │   └── tasks/              # Task components
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Token utilities
│   │   └── types.ts            # TypeScript types
│   └── middleware.ts           # Route protection
└── package.json
```

## Key Specifications

- **Pages**: `@specs/ui/pages.md`
- **Components**: `@specs/ui/components.md`
- **API Contract**: `@specs/contracts/api-contract.md`
- **JWT Handling**: `@specs/api/jwt-auth.md`

## Implementation Rules

### Authentication
- Store JWT in localStorage
- Attach `Authorization: Bearer <token>` to all API requests
- Redirect to login on 401 responses
- Clear token on logout

### Route Protection
- `/dashboard` requires authentication
- Redirect authenticated users from `/login` and `/signup`
- Use Next.js middleware for route guards

### API Client
- Base URL from `NEXT_PUBLIC_API_URL`
- Handle all error responses consistently
- Support loading states

### Components
- Use Tailwind CSS for styling
- Support responsive design (mobile-first)
- Implement loading and error states

## Type Definitions

All types in `src/lib/types.ts`:
- `User`, `Task`, `AuthResponse`
- `SignupRequest`, `SigninRequest`
- `TaskCreateRequest`, `TaskUpdateRequest`
- `ErrorResponse`

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<32+ character secret>
```

## Testing

- Jest + React Testing Library for unit tests
- Test components in isolation
- Mock API responses
