/**
 * Dashboard page (protected).
 * Reference: @specs/002-fullstack-web-app/ui/pages.md Dashboard Page
 */

"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
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
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-50 to-white">
      <Header />

      <main className="flex-1 py-6 sm:py-8 lg:py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header with gradient */}
          <div className="text-center mb-8 sm:mb-10 lg:mb-12">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-2 sm:mb-3">
              My <span className="text-blue-600">Tasks</span>
            </h1>
            <p className="text-gray-600 text-base sm:text-lg px-4">
              Organize and manage your tasks efficiently
            </p>
          </div>

          {/* Error message */}
          {error && (
            <Alert type="error" className="mb-6">
              {error}
            </Alert>
          )}

          {/* Action Buttons - Prominent */}
          {!showForm && (
            <div className="flex flex-col sm:flex-row justify-center gap-3 sm:gap-4 mb-6 sm:mb-8">
              <Button
                variant="primary"
                onClick={handleCreateNewClick}
                className="w-full sm:w-auto px-6 sm:px-8 py-2.5 sm:py-3 text-base sm:text-lg shadow-lg hover:shadow-xl transition-shadow"
              >
                <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create New Task
              </Button>
              <Link href="/chat" className="w-full sm:w-auto">
                <Button
                  variant="secondary"
                  className="w-full px-6 sm:px-8 py-2.5 sm:py-3 text-base sm:text-lg shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 border-0"
                >
                  <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                  AI Chatbot
                </Button>
              </Link>
            </div>
          )}

          {/* Task form modal */}
          {showForm && (
            <Card className="mb-6 sm:mb-8 shadow-xl border-2 border-blue-100">
              <h2 className="text-lg sm:text-xl font-semibold mb-4 sm:mb-6 text-gray-900">
                {editingTask ? "✏️ Edit Task" : "✨ Create New Task"}
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
            <div className="py-12 sm:py-16 lg:py-20">
              <LoadingSpinner size="large" />
              <p className="text-center text-gray-600 mt-4 sm:mt-6 text-base sm:text-lg px-4">Loading your tasks...</p>
            </div>
          ) : (
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-xl p-4 sm:p-6 border border-gray-100">
              <TaskList
                tasks={tasks}
                onToggle={handleToggleTask}
                onEdit={handleEditClick}
                onDelete={handleDeleteTask}
                onCreateNew={handleCreateNewClick}
              />
            </div>
          )}

          {/* Task count with better styling */}
          {!loading && tasks.length > 0 && (
            <div className="mt-6 sm:mt-8 text-center">
              <div className="inline-flex items-center gap-2 bg-blue-50 px-4 sm:px-6 py-2 sm:py-3 rounded-full">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-blue-900 font-medium text-sm sm:text-base">
                  {tasks.filter((t) => t.completed).length} of {tasks.length} tasks completed
                </span>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
