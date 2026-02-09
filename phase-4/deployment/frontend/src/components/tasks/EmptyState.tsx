/**
 * Empty state component for task list.
 * Reference: @specs/002-fullstack-web-app/ui/components.md EmptyState
 */

import React from "react";
import { Button } from "../ui/Button";

interface EmptyStateProps {
  onCreateNew: () => void;
}

export function EmptyState({ onCreateNew }: EmptyStateProps) {
  return (
    <div className="text-center py-8 sm:py-12 px-4">
      <div className="w-14 h-14 sm:w-16 sm:h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
        <svg
          className="w-7 h-7 sm:w-8 sm:h-8 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
          />
        </svg>
      </div>
      <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-2">No tasks yet</h3>
      <p className="text-sm sm:text-base text-gray-600 mb-4 sm:mb-6">
        Get started by creating your first task.
      </p>
      <Button variant="primary" onClick={onCreateNew} className="w-full sm:w-auto">
        Create Your First Task
      </Button>
    </div>
  );
}
