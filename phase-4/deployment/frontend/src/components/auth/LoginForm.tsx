/**
 * Login form component.
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Login Page
 * Reference: @specs/002-fullstack-web-app/features/authentication.md User Story 2
 */

"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { Alert } from "../ui/Alert";
import { signin } from "@/lib/api";
import { setToken, setUser } from "@/lib/auth";

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!email) {
      errors.email = "Email is required";
    }

    if (!password) {
      errors.password = "Password is required";
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
      const response = await signin({ email, password });
      setToken(response.token);
      setUser(response.user);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
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
        placeholder="Your password"
        autoComplete="current-password"
        disabled={loading}
      />

      <Button
        type="submit"
        variant="primary"
        loading={loading}
        className="w-full"
      >
        Sign In
      </Button>
    </form>
  );
}
