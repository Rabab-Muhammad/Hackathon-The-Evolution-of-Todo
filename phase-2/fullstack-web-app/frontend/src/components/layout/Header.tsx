/**
 * Header component with navigation.
 * Reference: @specs/002-fullstack-web-app/ui/components.md Header
 */

"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "../ui/Button";
import { getUser, isAuthenticated, logout } from "@/lib/auth";
import { signout } from "@/lib/api";

interface HeaderProps {
  showAuthLinks?: boolean;
}

export function Header({ showAuthLinks = true }: HeaderProps) {
  const router = useRouter();
  const [user, setUser] = React.useState<{ email: string } | null>(null);
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  React.useEffect(() => {
    setIsLoggedIn(isAuthenticated());
    setUser(getUser());
  }, []);

  const handleLogout = async () => {
    try {
      await signout();
    } catch {
      // Ignore errors, logout anyway
    }
    logout();
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <span className="text-xl font-bold text-blue-600">Todo App</span>
          </Link>

          {/* Navigation */}
          {showAuthLinks && (
            <nav className="flex items-center gap-4">
              {isLoggedIn ? (
                <>
                  <span className="text-gray-600 text-sm hidden sm:block">
                    {user?.email}
                  </span>
                  <Link href="/dashboard">
                    <Button variant="secondary" className="text-sm">
                      Dashboard
                    </Button>
                  </Link>
                  <Button
                    variant="secondary"
                    onClick={handleLogout}
                    className="text-sm"
                  >
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Link href="/login">
                    <Button variant="secondary" className="text-sm">
                      Login
                    </Button>
                  </Link>
                  <Link href="/signup">
                    <Button variant="primary" className="text-sm">
                      Sign Up
                    </Button>
                  </Link>
                </>
              )}
            </nav>
          )}
        </div>
      </div>
    </header>
  );
}
