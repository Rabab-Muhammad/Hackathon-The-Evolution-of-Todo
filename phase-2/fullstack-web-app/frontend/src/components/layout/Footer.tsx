/**
 * Footer component.
 * Reference: @specs/002-fullstack-web-app/ui/components.md
 */

import React from "react";

export function Footer() {
  return (
    <footer className="bg-gray-100 border-t mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <p className="text-center text-gray-600 text-sm">
          Todo App - Phase II | Built with Next.js & FastAPI
        </p>
      </div>
    </footer>
  );
}
