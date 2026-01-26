# The Evolution of Todo - Project Overview

This repository demonstrates the evolution of a simple todo application from a console application to a full-stack web application.

## Phase I: Console Application

**Location**: `phase-1/console-todo/`

A simple console-based todo application built with Python following object-oriented principles.

### Architecture
- Models: Task entity definitions
- Services: Business logic for task management
- CLI: Command-line interface and user interaction
- Validators: Input validation logic
- Exceptions: Custom exception handling

### Features
- Add, update, delete, and view tasks
- Mark tasks as complete/incomplete
- Console-based menu interface
- Input validation
- Error handling

### Limitations
- Data stored in memory only (no persistence)
- Single user only
- No authentication

## Phase II: Full-Stack Web Application

**Location**: `phase-2/fullstack-web-app/`

A full-stack multi-user todo application with Next.js frontend, FastAPI backend, and PostgreSQL database.

### Architecture
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: FastAPI with SQLModel ORM
- Database: PostgreSQL (Neon recommended)
- Authentication: Better Auth with JWT tokens

### Features
- Multi-user support with authentication
- Persistent storage with PostgreSQL
- Full CRUD operations for tasks
- Responsive web interface
- JWT-based authentication
- User isolation (users only see their own tasks)

### Technology Stack
- Frontend: Next.js 16+, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, Python 3.11+
- Database: PostgreSQL (Neon)
- Auth: Better Auth, JWT (HS256)
- Deployment: Docker, Railway/Vercel

## Evolution Journey

This project demonstrates how a simple console application can evolve into a sophisticated full-stack web application with persistence, authentication, and multi-user support.