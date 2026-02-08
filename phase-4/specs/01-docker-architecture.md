# Specification: Docker Containerization Architecture

**Feature ID**: PHASE4-01
**Status**: Draft
**Created**: 2026-02-04
**Dependencies**: Phase 3 (Application code)

## Purpose

Design and implement a comprehensive Docker containerization strategy for the AI-powered todo application. Create optimized, secure, production-ready container images for the frontend (Next.js), backend (FastAPI), and provide local development support with Docker Compose.

## User Stories

**As a DevOps engineer**, I want to:
1. Build optimized Docker images with minimal size and attack surface
2. Use multi-stage builds to separate build and runtime dependencies
3. Ensure containers run securely (non-root, minimal privileges)
4. Test the entire stack locally with Docker Compose
5. Load images into Minikube for Kubernetes deployment

**As a developer**, I want to:
1. Build and test containers locally before Kubernetes deployment
2. Use Docker Compose for quick local development
3. Have consistent environments across development and production
4. Debug containerized applications easily

## Acceptance Criteria

### AC1: Backend Dockerfile (FastAPI)
- [ ] Multi-stage build (builder + runtime)
- [ ] Python 3.13+ base image (Alpine or slim)
- [ ] Dependencies installed in builder stage
- [ ] Source code copied in runtime stage
- [ ] Non-root user (UID 1000)
- [ ] Port 8000 exposed
- [ ] Health check endpoint configured
- [ ] Image size < 200MB
- [ ] No secrets in image

### AC2: Frontend Dockerfile (Next.js)
- [ ] Multi-stage build (dependencies + builder + runtime)
- [ ] Node.js 18+ base image (Alpine)
- [ ] Dependencies installed separately from build
- [ ] Production build created
- [ ] Static files served efficiently
- [ ] Non-root user
- [ ] Port 3000 exposed
- [ ] Image size < 150MB
- [ ] Environment variables configurable at runtime

### AC3: Docker Compose Configuration
- [ ] Backend service defined
- [ ] Frontend service defined
- [ ] PostgreSQL service defined (for local dev)
- [ ] Network configuration
- [ ] Volume mounts for development
- [ ] Environment variables
- [ ] Health checks
- [ ] Depends_on relationships

### AC4: .dockerignore Files
- [ ] Exclude node_modules, .venv
- [ ] Exclude .git, .env files
- [ ] Exclude test files and documentation
- [ ] Exclude build artifacts
- [ ] Minimize build context size

### AC5: Build Optimization
- [ ] Layer caching optimized
- [ ] Dependencies cached separately from code
- [ ] Build time < 5 minutes (cold cache)
- [ ] Build time < 1 minute (warm cache)
- [ ] Parallel builds supported

### AC6: Security
- [ ] No root user in containers
- [ ] Minimal base images
- [ ] No unnecessary packages
- [ ] Security scanning passed
- [ ] Read-only root filesystem where possible

### AC7: Testing
- [ ] Containers build successfully
- [ ] Containers run successfully
- [ ] Health checks pass
- [ ] Services communicate correctly
- [ ] Docker Compose stack works end-to-end

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Architecture                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Frontend   │  │   Backend    │  │  PostgreSQL  │ │
│  │   (Next.js)  │  │  (FastAPI)   │  │   (DB)       │ │
│  │              │  │              │  │              │ │
│  │  Port: 3000  │  │  Port: 8000  │  │  Port: 5432  │ │
│  │  Image: 150MB│  │  Image: 200MB│  │  Official    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                    Docker Network                        │
│                    (todo-network)                        │
└─────────────────────────────────────────────────────────┘
```

### Backend Dockerfile

**File**: `docker/backend/Dockerfile`

```dockerfile
# Multi-stage build for FastAPI backend

# Stage 1: Builder - Install dependencies
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - Minimal image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser alembic.ini .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Size Optimization**:
- Use `python:3.13-slim` instead of full Python image (saves ~500MB)
- Multi-stage build separates build tools from runtime
- `--no-cache-dir` prevents pip cache in image
- Remove apt lists after installation
- Target size: ~180-200MB

### Frontend Dockerfile

**File**: `docker/frontend/Dockerfile`

```dockerfile
# Multi-stage build for Next.js frontend

# Stage 1: Dependencies - Install node modules
FROM node:18-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Stage 2: Builder - Build Next.js app
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Set build-time environment variables
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build Next.js application
RUN npm run build

# Stage 3: Runtime - Serve the app
FROM node:18-alpine AS runner

WORKDIR /app

# Set runtime environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set ownership
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})" || exit 1

# Run Next.js
CMD ["node", "server.js"]
```

**Size Optimization**:
- Use `node:18-alpine` (saves ~600MB vs full Node image)
- Three-stage build: deps → builder → runner
- Only copy production dependencies
- Use Next.js standalone output
- Target size: ~130-150MB

### Docker Compose Configuration

**File**: `docker/docker-compose.yml`

```yaml
version: '3.9'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: todo-postgres
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo_user -d todo_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - todo-network

  # FastAPI Backend
  backend:
    build:
      context: ../../phase-3/backend
      dockerfile: ../../phase-4/docker/backend/Dockerfile
    container_name: todo-backend
    environment:
      DATABASE_URL: postgresql://todo_user:todo_password@postgres:5432/todo_db
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      OPENAI_MODEL: gpt-4-turbo-preview
      CORS_ORIGINS: http://localhost:3000
      LOG_LEVEL: INFO
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - todo-network
    restart: unless-stopped

  # Next.js Frontend
  frontend:
    build:
      context: ../../phase-3/frontend
      dockerfile: ../../phase-4/docker/frontend/Dockerfile
    container_name: todo-frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      NEXT_PUBLIC_CHAT_ENDPOINT: http://localhost:8000/api/chat
    ports:
      - "3000:3000"
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - todo-network
    restart: unless-stopped

networks:
  todo-network:
    driver: bridge

volumes:
  postgres_data:
    driver: local
```

### .dockerignore Files

**Backend .dockerignore** (`docker/backend/.dockerignore`):
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Documentation
*.md
docs/

# Environment
.env
.env.*

# Build artifacts
build/
dist/
*.egg-info/
```

**Frontend .dockerignore** (`docker/frontend/.dockerignore`):
```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/

# Testing
coverage/
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Documentation
*.md
docs/

# Environment
.env
.env.*
.env.local
.env.production

# Build artifacts
dist/
build/
```

## Build Process

### Build Script

**File**: `scripts/build-images.sh`

```bash
#!/bin/bash
set -e

echo "🐳 Building Docker images..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build backend image
echo -e "${BLUE}Building backend image...${NC}"
docker build \
  -t todo-backend:latest \
  -f docker/backend/Dockerfile \
  ../phase-3/backend

echo -e "${GREEN}✓ Backend image built${NC}"

# Build frontend image
echo -e "${BLUE}Building frontend image...${NC}"
docker build \
  -t todo-frontend:latest \
  -f docker/frontend/Dockerfile \
  ../phase-3/frontend

echo -e "${GREEN}✓ Frontend image built${NC}"

# Show image sizes
echo -e "\n${BLUE}Image sizes:${NC}"
docker images | grep todo-

echo -e "\n${GREEN}✓ All images built successfully${NC}"
```

### Load Images into Minikube

```bash
#!/bin/bash
set -e

echo "📦 Loading images into Minikube..."

# Load backend image
echo "Loading backend image..."
minikube image load todo-backend:latest

# Load frontend image
echo "Loading frontend image..."
minikube image load todo-frontend:latest

echo "✓ Images loaded into Minikube"

# Verify images
echo -e "\nImages in Minikube:"
minikube image ls | grep todo-
```

## Testing Strategy

### Local Testing with Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check service health
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Image Security Scanning

```bash
# Scan backend image
docker scan todo-backend:latest

# Scan frontend image
docker scan todo-frontend:latest

# Alternative: Use Trivy
trivy image todo-backend:latest
trivy image todo-frontend:latest
```

## Performance Optimization

### Build Time Optimization

1. **Layer Caching**:
   - Copy dependency files first
   - Copy source code last
   - Maximize cache hits

2. **Parallel Builds**:
   ```bash
   docker build --parallel -t todo-backend:latest .
   ```

3. **BuildKit**:
   ```bash
   DOCKER_BUILDKIT=1 docker build -t todo-backend:latest .
   ```

### Runtime Optimization

1. **Resource Limits** (in docker-compose.yml):
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
       reservations:
         cpus: '0.5'
         memory: 256M
   ```

2. **Health Check Tuning**:
   - Adjust intervals based on startup time
   - Set appropriate timeouts
   - Configure retries

## Security Considerations

### Container Security Checklist

- [x] Run as non-root user
- [x] Use minimal base images (Alpine/slim)
- [x] No secrets in images
- [x] Security scanning enabled
- [x] Read-only root filesystem (where possible)
- [x] Drop unnecessary capabilities
- [x] Use specific image tags (not `latest` in production)

### Secrets Management

**Never include in images**:
- API keys (OPENAI_API_KEY)
- Database passwords
- JWT secrets
- TLS certificates

**Use instead**:
- Environment variables (Docker Compose)
- Kubernetes Secrets (in K8s deployment)
- External secret managers (Vault, AWS Secrets Manager)

## Edge Cases and Error Handling

### Edge Case 1: Build Failures
**Scenario**: Docker build fails due to network issues
**Handling**:
- Retry with `--no-cache`
- Check network connectivity
- Verify base image availability

### Edge Case 2: Container Crashes on Startup
**Scenario**: Container exits immediately after start
**Handling**:
- Check logs: `docker logs <container>`
- Verify environment variables
- Check health check configuration
- Ensure dependencies are available

### Edge Case 3: Out of Disk Space
**Scenario**: Build fails due to insufficient disk space
**Handling**:
- Clean up unused images: `docker system prune -a`
- Remove unused volumes: `docker volume prune`
- Check disk space: `df -h`

### Edge Case 4: Port Conflicts
**Scenario**: Port already in use
**Handling**:
- Change port mapping in docker-compose.yml
- Stop conflicting services
- Use different ports for local testing

## Dependencies

### External Dependencies
- Docker 24.0+
- Docker Compose 2.20+
- Phase 3 application code

### Internal Dependencies
- Phase 3 backend code
- Phase 3 frontend code
- PostgreSQL database

## Documentation Requirements

- [ ] Dockerfile documentation (inline comments)
- [ ] Docker Compose usage guide
- [ ] Build script documentation
- [ ] Troubleshooting guide
- [ ] Security best practices

## Success Metrics

- Backend image size < 200MB
- Frontend image size < 150MB
- Build time < 5 minutes (cold cache)
- Build time < 1 minute (warm cache)
- All containers start successfully
- Health checks pass
- Services communicate correctly
- Docker Compose stack works end-to-end

## Future Enhancements (Out of Scope for Phase 4)

- Multi-architecture builds (ARM64 support)
- Image signing and verification
- Automated vulnerability scanning in CI/CD
- Container image registry (Harbor, ECR)
- Advanced caching strategies (BuildKit cache mounts)

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: Medium
**Implementation Order**: 1 of 5 (implement first)
