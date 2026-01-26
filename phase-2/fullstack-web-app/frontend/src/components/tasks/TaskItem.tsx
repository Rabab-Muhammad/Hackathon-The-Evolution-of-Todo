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
        border rounded-lg p-4 transition-colors
        ${task.completed ? "bg-gray-50 border-gray-200" : "bg-white border-gray-300"}
      `}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={`
            mt-1 w-5 h-5 rounded border-2 flex-shrink-0
            flex items-center justify-center transition-colors
            ${task.completed
              ? "bg-green-500 border-green-500 text-white"
              : "border-gray-300 hover:border-blue-500"
            }
            ${isToggling ? "opacity-50" : ""}
          `}
          aria-label={task.completed ? "Mark incomplete" : "Mark complete"}
        >
          {task.completed && (
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
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
            className={`font-medium ${
              task.completed ? "text-gray-500 line-through" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`text-sm mt-1 ${
                task.completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 flex-shrink-0">
          <Button
            variant="secondary"
            onClick={() => onEdit(task)}
            className="text-sm px-3 py-1"
          >
            Edit
          </Button>
          {showDeleteConfirm ? (
            <div className="flex gap-1">
              <Button
                variant="danger"
                onClick={handleDelete}
                loading={isDeleting}
                className="text-sm px-3 py-1"
              >
                Confirm
              </Button>
              <Button
                variant="secondary"
                onClick={() => setShowDeleteConfirm(false)}
                className="text-sm px-3 py-1"
              >
                Cancel
              </Button>
            </div>
          ) : (
            <Button
              variant="danger"
              onClick={() => setShowDeleteConfirm(true)}
              className="text-sm px-3 py-1"
            >
              Delete
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
