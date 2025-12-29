/**
 * API client for backend communication.
 * Reference: @specs/002-fullstack-web-app/architecture.md API Client Architecture
 * Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
 */

import { getToken, logout } from "./auth";
import type {
  AuthResponse,
  SignupRequest,
  SigninRequest,
  Task,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskResponse,
  TaskListResponse,
  ErrorResponse,
} from "./types";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

/**
 * Base fetch wrapper with authentication and error handling.
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add Authorization header if token exists
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle 401 - redirect to login
  // Reference: @specs/api/jwt-auth.md FR-JWT-010
  if (response.status === 401) {
    logout();
    throw new Error("Authentication required");
  }

  const data = await response.json();

  // Check if response is an error
  if (!response.ok) {
    const error = data as ErrorResponse;
    throw new Error(error.error?.message || "An error occurred");
  }

  return data as T;
}

// ============================================
// Authentication API
// Reference: @specs/contracts/api-contract.md
// ============================================

/**
 * Register a new user.
 * POST /api/auth/signup
 */
export async function signup(request: SignupRequest): Promise<AuthResponse> {
  return apiFetch<AuthResponse>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

/**
 * Sign in existing user.
 * POST /api/auth/signin
 */
export async function signin(request: SigninRequest): Promise<AuthResponse> {
  return apiFetch<AuthResponse>("/api/auth/signin", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

/**
 * Sign out current user.
 * POST /api/auth/signout
 */
export async function signout(): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/api/auth/signout", {
    method: "POST",
  });
}

// ============================================
// Task API
// Reference: @specs/contracts/api-contract.md
// ============================================

/**
 * Get all tasks for current user.
 * GET /api/tasks
 */
export async function getTasks(): Promise<TaskListResponse> {
  return apiFetch<TaskListResponse>("/api/tasks");
}

/**
 * Create a new task.
 * POST /api/tasks
 */
export async function createTask(
  request: TaskCreateRequest
): Promise<TaskResponse> {
  return apiFetch<TaskResponse>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

/**
 * Get a single task by ID.
 * GET /api/tasks/{task_id}
 */
export async function getTask(taskId: string): Promise<TaskResponse> {
  return apiFetch<TaskResponse>(`/api/tasks/${taskId}`);
}

/**
 * Update an existing task.
 * PUT /api/tasks/{task_id}
 */
export async function updateTask(
  taskId: string,
  request: TaskUpdateRequest
): Promise<TaskResponse> {
  return apiFetch<TaskResponse>(`/api/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(request),
  });
}

/**
 * Delete a task.
 * DELETE /api/tasks/{task_id}
 */
export async function deleteTask(
  taskId: string
): Promise<{ message: string }> {
  return apiFetch<{ message: string }>(`/api/tasks/${taskId}`, {
    method: "DELETE",
  });
}

/**
 * Toggle task completion status.
 * PATCH /api/tasks/{task_id}/toggle
 */
export async function toggleTask(taskId: string): Promise<TaskResponse> {
  return apiFetch<TaskResponse>(`/api/tasks/${taskId}/toggle`, {
    method: "PATCH",
  });
}
