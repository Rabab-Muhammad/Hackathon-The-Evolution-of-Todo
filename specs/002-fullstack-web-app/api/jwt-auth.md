# API Specification: JWT Authentication

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-28
**Status**: Draft

## Purpose

Define the JWT (JSON Web Token) authentication flow and token handling between the frontend client and backend server using Better Auth.

## JWT Overview

JSON Web Tokens are used to securely transmit user identity between the frontend and backend. The token is issued upon successful authentication and must be included in all subsequent API requests.

## Token Structure

### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload (Claims)

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "iat": 1703764800,
  "exp": 1703851200
}
```

| Claim | Description |
|-------|-------------|
| sub | Subject - User's unique identifier (UUID) |
| email | User's email address |
| iat | Issued At - Unix timestamp when token was created |
| exp | Expiration - Unix timestamp when token expires |

### Signature

The signature is created using HMAC-SHA256 with the `BETTER_AUTH_SECRET` environment variable.

## Authentication Flow

### Token Issuance (Login/Signup)

```
1. User submits credentials (email/password)
2. Backend validates credentials
3. Backend generates JWT with user claims
4. Backend signs JWT with BETTER_AUTH_SECRET
5. Backend returns JWT to frontend
6. Frontend stores JWT (localStorage or secure cookie)
```

### Token Usage (API Requests)

```
1. Frontend retrieves stored JWT
2. Frontend adds Authorization header: "Bearer <token>"
3. Backend extracts token from header
4. Backend verifies signature using BETTER_AUTH_SECRET
5. Backend validates token is not expired
6. Backend extracts user_id from "sub" claim
7. Backend processes request with user context
```

### Token Refresh (Session Extension)

```
1. Frontend detects token approaching expiration
2. Frontend requests new token with current valid token
3. Backend validates current token
4. Backend issues new token with extended expiration
5. Frontend replaces stored token with new token
```

## Frontend Token Handling

### Storage

- **Primary**: HTTP-only cookie (when server supports it)
- **Fallback**: localStorage (for API-only backend)

### Request Attachment

All requests to protected endpoints MUST include:

```
Authorization: Bearer <jwt-token>
```

### Token Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                     Token Lifecycle                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Login/Signup ──► Token Issued ──► Token Stored               │
│                        │                                      │
│                        ▼                                      │
│               ┌─────────────────┐                             │
│               │   Valid Token   │◄──── Refresh Token          │
│               └────────┬────────┘         │                   │
│                        │                  │                   │
│         ┌──────────────┼──────────────────┘                   │
│         │              │                                      │
│         ▼              ▼                                      │
│   Token Expired    Logout                                     │
│         │              │                                      │
│         ▼              ▼                                      │
│   Redirect to      Clear Token                                │
│     Login                                                     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Backend Token Validation

### Validation Steps

1. **Extract Token**: Parse Authorization header, extract Bearer token
2. **Verify Signature**: Decode and verify using BETTER_AUTH_SECRET
3. **Check Expiration**: Ensure current time < exp claim
4. **Extract Claims**: Get user_id from sub claim

### Validation Results

| Result | Action |
|--------|--------|
| Token missing | Return 401 Unauthorized |
| Invalid signature | Return 401 Unauthorized |
| Token expired | Return 401 Unauthorized |
| Valid token | Extract user context, proceed |

## Data Flow / Interaction

### Successful Authentication Flow

```
Frontend                         Backend                        Database
   │                                │                               │
   │  POST /api/auth/signin         │                               │
   │  {email, password}             │                               │
   │ ──────────────────────────────►│                               │
   │                                │  Query user by email          │
   │                                │ ─────────────────────────────►│
   │                                │                               │
   │                                │  User record                  │
   │                                │ ◄─────────────────────────────│
   │                                │                               │
   │                                │  Verify password hash         │
   │                                │                               │
   │                                │  Generate JWT                 │
   │                                │  Sign with SECRET             │
   │                                │                               │
   │  {user, token}                 │                               │
   │ ◄──────────────────────────────│                               │
   │                                │                               │
   │  Store token                   │                               │
   │                                │                               │
```

### Protected Request Flow

```
Frontend                         Backend                        Database
   │                                │                               │
   │  GET /api/tasks                │                               │
   │  Authorization: Bearer <token> │                               │
   │ ──────────────────────────────►│                               │
   │                                │                               │
   │                                │  Verify JWT signature         │
   │                                │  Check expiration             │
   │                                │  Extract user_id              │
   │                                │                               │
   │                                │  Query tasks WHERE            │
   │                                │  user_id = extracted_id       │
   │                                │ ─────────────────────────────►│
   │                                │                               │
   │                                │  User's tasks                 │
   │                                │ ◄─────────────────────────────│
   │                                │                               │
   │  {tasks: [...]}                │                               │
   │ ◄──────────────────────────────│                               │
   │                                │                               │
```

## Security Requirements

### Token Security

- **FR-JWT-001**: Tokens MUST be signed with BETTER_AUTH_SECRET
- **FR-JWT-002**: BETTER_AUTH_SECRET MUST be at least 32 characters
- **FR-JWT-003**: BETTER_AUTH_SECRET MUST NOT be committed to source control
- **FR-JWT-004**: Token expiration MUST be set to 24 hours maximum
- **FR-JWT-005**: Expired tokens MUST be rejected

### Transport Security

- **FR-JWT-006**: All authentication requests MUST use HTTPS in production
- **FR-JWT-007**: Tokens MUST NOT be logged or included in error messages
- **FR-JWT-008**: Tokens MUST NOT be passed as URL parameters

### Client Security

- **FR-JWT-009**: Frontend MUST clear token on logout
- **FR-JWT-010**: Frontend MUST redirect to login on 401 responses
- **FR-JWT-011**: Frontend SHOULD refresh token before expiration

## Error Handling

### Authentication Errors

| Scenario | HTTP Status | Error Code | Message |
|----------|-------------|------------|---------|
| Missing token | 401 | UNAUTHORIZED | "Authentication required" |
| Invalid token | 401 | UNAUTHORIZED | "Invalid authentication token" |
| Expired token | 401 | UNAUTHORIZED | "Authentication token has expired" |
| Malformed header | 401 | UNAUTHORIZED | "Invalid authorization header format" |

## Acceptance Criteria

- [ ] JWT tokens are issued on successful login/signup
- [ ] JWT tokens are signed with BETTER_AUTH_SECRET
- [ ] Protected endpoints reject requests without valid tokens
- [ ] Expired tokens are rejected
- [ ] Invalid signatures are rejected
- [ ] User ID is correctly extracted from token claims
- [ ] Token is included in all frontend API requests
- [ ] Frontend clears token on logout
- [ ] Frontend redirects to login on 401 responses

## Success Criteria

### Measurable Outcomes

- **SC-001**: Token validation completes within 10ms
- **SC-002**: 100% of protected endpoints validate tokens
- **SC-003**: 0% of invalid tokens result in authorized access
- **SC-004**: Token refresh completes without user intervention
- **SC-005**: All 401 errors result in login redirect within 1 second
