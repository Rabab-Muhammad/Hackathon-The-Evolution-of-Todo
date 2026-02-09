/**
 * Task list component.
 * Reference: @specs/002-fullstack-web-app/ui/components.md TaskList
 */

"use client";

import React from "react";
import { TaskItem } from "./TaskItem";
import { EmptyState } from "./EmptyState";
import type { Task } from "@/lib/types";

interface TaskListProps {
  tasks: Task[];
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
  onCreateNew: () => void;
}

export function TaskList({
  tasks,
  onToggle,
  onEdit,
  onDelete,
  onCreateNew,
}: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState onCreateNew={onCreateNew} />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
