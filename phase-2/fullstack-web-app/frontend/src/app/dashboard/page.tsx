/**
 * Dashboard page (protected).
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Dashboard Page
 */

"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";
import { isAuthenticated } from "@/lib/auth";
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleTask,
} from "@/lib/api";
import type { Task, TaskCreateRequest, TaskUpdateRequest } from "@/lib/types";

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formLoading, setFormLoading] = useState(false);

  // Check authentication
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
    }
  }, [router]);

  // Load tasks
  const loadTasks = useCallback(async () => {
    try {
      setError("");
      const response = await getTasks();
      setTasks(response.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated()) {
      loadTasks();
    }
  }, [loadTasks]);

  // Handle create task
  const handleCreateTask = async (data: TaskCreateRequest) => {
    setFormLoading(true);
    try {
      const response = await createTask(data);
      setTasks((prev) => [response.task, ...prev]);
      setShowForm(false);
    } finally {
      setFormLoading(false);
    }
  };

  // Handle update task
  const handleUpdateTask = async (data: TaskUpdateRequest) => {
    if (!editingTask) return;
    setFormLoading(true);
    try {
      const response = await updateTask(editingTask.id, data);
      setTasks((prev) =>
        prev.map((t) => (t.id === editingTask.id ? response.task : t))
      );
      setEditingTask(null);
      setShowForm(false);
    } finally {
      setFormLoading(false);
    }
  };

  // Handle toggle task
  const handleToggleTask = async (taskId: string) => {
    try {
      const response = await toggleTask(taskId);
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? response.task : t))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle task");
    }
  };

  // Handle delete task
  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTask(taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  };

  // Handle edit click
  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  // Handle form cancel
  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  // Handle create new click
  const handleCreateNewClick = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  if (!isAuthenticated()) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
            {!showForm && (
              <Button variant="primary" onClick={handleCreateNewClick}>
                New Task
              </Button>
            )}
          </div>

          {/* Error message */}
          {error && (
            <Alert type="error" className="mb-6">
              {error}
            </Alert>
          )}

          {/* Task form modal */}
          {showForm && (
            <Card className="mb-6">
              <h2 className="text-lg font-semibold mb-4">
                {editingTask ? "Edit Task" : "Create New Task"}
              </h2>
              <TaskForm
                task={editingTask}
                onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
                onCancel={handleFormCancel}
                loading={formLoading}
              />
            </Card>
          )}

          {/* Task list */}
          {loading ? (
            <div className="py-12">
              <LoadingSpinner size="large" />
              <p className="text-center text-gray-600 mt-4">Loading tasks...</p>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onToggle={handleToggleTask}
              onEdit={handleEditClick}
              onDelete={handleDeleteTask}
              onCreateNew={handleCreateNewClick}
            />
          )}

          {/* Task count */}
          {!loading && tasks.length > 0 && (
            <p className="text-sm text-gray-500 mt-4 text-center">
              {tasks.filter((t) => t.completed).length} of {tasks.length} tasks
              completed
            </p>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
