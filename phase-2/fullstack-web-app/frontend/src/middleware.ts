/**
 * Next.js middleware for route protection.
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Route Protection
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Routes that require authentication
const protectedRoutes = ["/dashboard"];

// Routes that should redirect authenticated users
const authRoutes = ["/login", "/signup"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for token in cookies (for SSR) or we'll check client-side
  // Note: Since we use localStorage, actual auth check happens client-side
  // This middleware provides basic routing logic

  // For protected routes, we'll let client-side handle the redirect
  // This is because localStorage is not accessible in middleware

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/signup"],
};
