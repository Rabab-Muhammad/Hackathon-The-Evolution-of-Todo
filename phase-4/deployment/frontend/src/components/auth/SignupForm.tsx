/**
 * Signup form component.
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Signup Page
 * Reference: @specs/002-fullstack-web-app/features/authentication.md User Story 1
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { Alert } from "../ui/Alert";
import { signup } from "@/lib/api";
import { setToken, setUser } from "@/lib/auth";

export function SignupForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!email) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = "Please enter a valid email address";
    }

    if (!password) {
      errors.password = "Password is required";
    } else if (password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    if (password !== confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const response = await signup({ email, password });
      setToken(response.token);
      setUser(response.user);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert type="error">{error}</Alert>}

      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={fieldErrors.email}
        placeholder="you@example.com"
        autoComplete="email"
        disabled={loading}
      />

      <Input
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={fieldErrors.password}
        placeholder="Minimum 8 characters"
        autoComplete="new-password"
        disabled={loading}
      />

      <Input
        label="Confirm Password"
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        error={fieldErrors.confirmPassword}
        placeholder="Confirm your password"
        autoComplete="new-password"
        disabled={loading}
      />

      <div className="text-sm text-gray-600">
        Password must be at least 8 characters long.
      </div>

      <Button
        type="submit"
        variant="primary"
        loading={loading}
        className="w-full"
      >
        Sign Up
      </Button>
    </form>
  );
}
