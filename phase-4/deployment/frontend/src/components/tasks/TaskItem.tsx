/**
 * Task item component.
 * Reference: @specs/002-fullstack-web-app/ui/components.md TaskItem
 */

"use client";

import React, { useState } from "react";
import { Button } from "../ui/Button";
import type { Task } from "@/lib/types";

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
}

export function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  return (
    <div
      className={`
        border-2 rounded-xl p-3 sm:p-4 transition-all duration-300 hover:shadow-lg
        ${task.completed
          ? "bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 shadow-sm"
          : "bg-white border-blue-200 shadow-md hover:border-blue-300"
        }
      `}
    >
      <div className="flex items-start gap-2 sm:gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={`
            mt-0.5 sm:mt-1 w-6 h-6 sm:w-7 sm:h-7 rounded-lg border-2 flex-shrink-0
            flex items-center justify-center transition-all duration-300 shadow-sm
            ${task.completed
              ? "bg-gradient-to-br from-green-500 to-emerald-600 border-green-600 text-white scale-110 shadow-md"
              : "border-gray-300 hover:border-blue-500 hover:bg-blue-50 hover:scale-105"
            }
            ${isToggling ? "opacity-50 animate-pulse" : "hover:shadow-md"}
          `}
          aria-label={task.completed ? "Mark incomplete" : "Mark complete"}
        >
          {task.completed && (
            <svg className="w-4 h-4 sm:w-5 sm:h-5 animate-scaleIn" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold text-sm sm:text-base transition-all duration-300 ${
              task.completed
                ? "text-green-700 line-through opacity-75"
                : "text-gray-900 hover:text-blue-600"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`text-xs sm:text-sm mt-1 transition-all duration-300 ${
                task.completed ? "text-green-600 opacity-60" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
          {task.completed && (
            <div className="flex items-center gap-1 mt-2">
              <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-xs text-green-600 font-medium">Completed</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-1 sm:gap-2 flex-shrink-0">
          <Button
            variant="secondary"
            onClick={() => onEdit(task)}
            className="text-xs sm:text-sm px-2 sm:px-3 py-1 whitespace-nowrap bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 border-0 shadow-md hover:shadow-lg transition-all"
          >
            <svg className="w-3 h-3 sm:w-4 sm:h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </Button>
          {showDeleteConfirm ? (
            <div className="flex flex-col sm:flex-row gap-1">
              <Button
                variant="danger"
                onClick={handleDelete}
                loading={isDeleting}
                className="text-xs sm:text-sm px-2 sm:px-3 py-1 whitespace-nowrap bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg transition-all"
              >
                <svg className="w-3 h-3 sm:w-4 sm:h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Confirm
              </Button>
              <Button
                variant="secondary"
                onClick={() => setShowDeleteConfirm(false)}
                className="text-xs sm:text-sm px-2 sm:px-3 py-1 whitespace-nowrap bg-gradient-to-r from-gray-500 to-gray-600 text-white hover:from-gray-600 hover:to-gray-700 border-0 shadow-md hover:shadow-lg transition-all"
              >
                <svg className="w-3 h-3 sm:w-4 sm:h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Cancel
              </Button>
            </div>
          ) : (
            <Button
              variant="danger"
              onClick={() => setShowDeleteConfirm(true)}
              className="text-xs sm:text-sm px-2 sm:px-3 py-1 whitespace-nowrap bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg transition-all"
            >
              <svg className="w-3 h-3 sm:w-4 sm:h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Delete
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
