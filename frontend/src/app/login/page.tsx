/**
 * Login page.
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Login Page
 */

"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Card } from "@/components/ui/Card";
import { LoginForm } from "@/components/auth/LoginForm";
import { isAuthenticated } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      router.push("/dashboard");
    }
  }, [router]);

  return (
    <div className="min-h-screen flex flex-col">
      <Header showAuthLinks={false} />

      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <Card className="w-full max-w-md">
          <h1 className="text-2xl font-bold text-center mb-6">
            Sign In
          </h1>

          <LoginForm />

          <p className="mt-6 text-center text-gray-600">
            Don&apos;t have an account?{" "}
            <Link href="/signup" className="text-blue-600 hover:underline">
              Sign up
            </Link>
          </p>
        </Card>
      </main>

      <Footer />
    </div>
  );
}
