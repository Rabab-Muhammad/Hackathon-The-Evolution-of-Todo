/**
 * Authentication utilities for token management.
 * Reference: @specs/002-fullstack-web-app/api/jwt-auth.md Frontend Token Handling
 */

const TOKEN_KEY = "todo_auth_token";
const USER_KEY = "todo_user";

import type { User } from "./types";

/**
 * Get stored JWT token.
 */
export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Store JWT token.
 */
export function setToken(token: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Clear stored token and user data.
 * Reference: @specs/api/jwt-auth.md FR-JWT-009
 */
export function clearToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

/**
 * Get stored user data.
 */
export function getUser(): User | null {
  if (typeof window === "undefined") return null;
  const userData = localStorage.getItem(USER_KEY);
  if (!userData) return null;
  try {
    return JSON.parse(userData) as User;
  } catch {
    return null;
  }
}

/**
 * Store user data.
 */
export function setUser(user: User): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  return getToken() !== null;
}

/**
 * Handle logout - clear data and redirect.
 * Reference: @specs/features/authentication.md User Story 3
 */
export function logout(): void {
  clearToken();
  if (typeof window !== "undefined") {
    window.location.href = "/login";
  }
}
