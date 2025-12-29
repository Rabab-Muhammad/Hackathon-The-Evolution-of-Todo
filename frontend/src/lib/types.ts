/**
 * TypeScript type definitions.
 * Reference: @specs/002-fullstack-web-app/data-model.md Frontend Types
 * Reference: @specs/002-fullstack-web-app/contracts/api-contract.md
 */

// User types
export interface User {
  id: string;
  email: string;
  created_at?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// Auth request types
export interface SignupRequest {
  email: string;
  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

// Task types
export interface Task {
  id: string;
  title: string;
  description?: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title: string;
  description?: string;
}

export interface TaskResponse {
  task: Task;
}

export interface TaskListResponse {
  tasks: Task[];
  count: number;
}

// Error types
export interface ErrorDetail {
  field: string;
  message: string;
}

export interface ErrorBody {
  code: string;
  message: string;
  details?: ErrorDetail[];
}

export interface ErrorResponse {
  error: ErrorBody;
}

// API Response type helper
export type ApiResponse<T> = T | ErrorResponse;

// Type guard to check if response is an error
export function isErrorResponse(response: unknown): response is ErrorResponse {
  return (
    typeof response === "object" &&
    response !== null &&
    "error" in response &&
    typeof (response as ErrorResponse).error === "object"
  );
}
