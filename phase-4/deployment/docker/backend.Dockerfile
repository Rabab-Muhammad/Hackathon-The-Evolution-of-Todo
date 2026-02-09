# Multi-stage Dockerfile for FastAPI Backend
# Based on research findings from specs/004-k8s-deployment/research.md
# Optimized for production deployment with minimal image size

# Stage 1: Build dependencies (includes build tools)
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies (gcc for compiling Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (minimal production image)
FROM python:3.11-slim
WORKDIR /app

# Create non-root user for security (UID 1001)
RUN addgroup --system --gid 1001 appuser && \
    adduser --system --uid 1001 appuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Set Python to run in unbuffered mode (better for container logs)
ENV PYTHONUNBUFFERED=1

# Expose port 8000
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

# Start FastAPI application with uvicorn
# --host 0.0.0.0 allows external connections
# --port 8000 matches the exposed port
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
