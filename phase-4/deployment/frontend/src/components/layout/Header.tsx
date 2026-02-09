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
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

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
    <header className="bg-white border-b border-gray-200 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo - Left with icon */}
          <div className="shrink-0">
            <Link href="/" className="flex items-center gap-2 lg:gap-3 group">
              <div className="w-8 h-8 lg:w-10 lg:h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow">
                <svg className="w-5 h-5 lg:w-6 lg:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="text-lg lg:text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-700 bg-clip-text text-transparent">
                Todo App
              </span>
            </Link>
          </div>

          {/* Desktop Navigation - Center (hidden on mobile) */}
          {showAuthLinks && isLoggedIn && (
            <div className="hidden lg:flex flex-1 justify-center items-center gap-3">
              <Link href="/dashboard">
                <button className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-all hover:shadow-md">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                  Tasks
                </button>
              </Link>
              <Link href="/chat">
                <button className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium transition-all shadow-md hover:shadow-lg">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                  AI Chatbot
                </button>
              </Link>
            </div>
          )}

          {/* Desktop Right side (hidden on mobile) */}
          {showAuthLinks && (
            <div className="hidden lg:flex items-center gap-4">
              {isLoggedIn ? (
                <>
                  <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span className="text-blue-900 text-sm font-medium truncate max-w-[150px]">
                      {user?.email}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-50 hover:bg-red-100 text-red-600 font-medium transition-all hover:shadow-md"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link href="/login">
                    <button className="px-6 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-all hover:shadow-md">
                      Login
                    </button>
                  </Link>
                  <Link href="/signup">
                    <button className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium transition-all shadow-md hover:shadow-lg">
                      Sign Up
                    </button>
                  </Link>
                </>
              )}
            </div>
          )}

          {/* Mobile menu button */}
          {showAuthLinks && (
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg className="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          )}
        </div>

        {/* Mobile menu */}
        {showAuthLinks && mobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-200">
            {isLoggedIn ? (
              <div className="space-y-3">
                {/* User info */}
                <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span className="text-blue-900 text-sm font-medium truncate">
                    {user?.email}
                  </span>
                </div>

                {/* Navigation links */}
                <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                  <button className="w-full flex items-center gap-2 px-4 py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-all">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    Tasks
                  </button>
                </Link>

                <Link href="/chat" onClick={() => setMobileMenuOpen(false)}>
                  <button className="w-full flex items-center gap-2 px-4 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium transition-all shadow-md">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    AI Chatbot
                  </button>
                </Link>

                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full flex items-center gap-2 px-4 py-3 rounded-xl bg-red-50 hover:bg-red-100 text-red-600 font-medium transition-all"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                  <button className="w-full px-4 py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-all">
                    Login
                  </button>
                </Link>
                <Link href="/signup" onClick={() => setMobileMenuOpen(false)}>
                  <button className="w-full px-4 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium transition-all shadow-md">
                    Sign Up
                  </button>
                </Link>
              </div>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
