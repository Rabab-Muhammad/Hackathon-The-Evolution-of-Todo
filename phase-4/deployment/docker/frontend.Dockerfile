# Multi-stage Dockerfile for Next.js 16 Frontend
# Based on research findings from specs/004-k8s-deployment/research.md
# Optimized for production deployment with minimal image size

# Stage 1: Dependencies (cached layer for faster rebuilds)
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install production dependencies only
RUN npm ci --only=production

# Stage 2: Build (separate from runtime to exclude dev dependencies)
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Set environment variable for Next.js standalone output
ENV NEXT_TELEMETRY_DISABLED=1

# Build Next.js application with standalone output
# This creates a minimal runtime bundle in .next/standalone
RUN npm run build

# Stage 3: Runtime (minimal production image)
FROM node:20-alpine AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user for security (UID 1001)
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy standalone output from builder
# This includes only the necessary files for runtime
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Switch to non-root user
USER nextjs

# Expose port 3000
EXPOSE 3000

# Set hostname to 0.0.0.0 to accept connections from outside container
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

# Start Next.js server
CMD ["node", "server.js"]
