# Phase 4: Local Kubernetes Deployment with Docker, Minikube, Helm, and k9s

**Status**: Specification Complete, Ready for Implementation
**Version**: 4.1.0
**Created**: 2026-02-04
**Updated**: 2026-02-08 (Migrated to free tools only)

## Overview

Phase 4 transforms the AI-powered todo application into a cloud-native, containerized system deployed on local Kubernetes (Minikube). This phase demonstrates production-ready containerization, orchestration, and cluster management using modern DevOps tools.

**🎉 100% FREE - No paid tools required!**

## Key Features

### 🐳 Docker Containerization
- Multi-stage builds for optimized image sizes
- Backend: FastAPI in Python 3.13-slim (~180-200MB)
- Frontend: Next.js in Node 18-alpine (~130-150MB)
- Security: Non-root users, minimal base images
- Local testing with Docker Compose

### ☸️ Kubernetes Orchestration
- Deployed on Minikube (local Kubernetes cluster)
- High availability: 2+ replicas for frontend and backend
- StatefulSet for PostgreSQL with persistent storage
- Health probes: Liveness, readiness, and startup
- Resource limits and requests configured
- Rolling updates with zero downtime

### 📦 Helm Package Management
- Complete Helm chart for declarative deployment
- Environment-specific values (dev, prod)
- Templated Kubernetes resources
- One-command deployment and upgrades
- Easy rollback capability

### 🎯 k9s Terminal UI (FREE Alternative)
- Interactive terminal UI for Kubernetes
- Real-time cluster monitoring and management
- Keyboard shortcuts for fast navigation
- Resource viewing and editing
- Log streaming and pod shell access
- No API keys or paid services required
- Completely free and open source

## Technology Stack

### Containerization
- **Docker**: 24.0+ for building and running containers
- **Docker Compose**: 2.20+ for local multi-container testing

### Orchestration
- **Minikube**: 1.32+ for local Kubernetes cluster
- **Kubernetes**: 1.28+ (via Minikube)
- **kubectl**: 1.28+ for cluster management

### Package Management
- **Helm**: 3.13+ for Kubernetes package management

### Cluster Management Tools (FREE)
- **k9s**: Terminal UI for Kubernetes (FREE, open source)
- **kubectl**: Standard Kubernetes CLI
- **kubectx/kubens**: Context and namespace switching (optional)

### Existing Stack (Phase 3)
- **Backend**: FastAPI, SQLModel, PostgreSQL, Google Gemini API (FREE)
- **Frontend**: Next.js, React, TypeScript, Custom Chat UI
- **Database**: PostgreSQL 16 (in Kubernetes)

**Total Cost: $0/month** 🎉

## Project Structure

```
phase-4/
├── constitution.md                 # Cloud-native principles
├── README.md                       # This file
├── specs/                          # Detailed specifications
│   ├── 01-docker-architecture.md
│   ├── 02-kubernetes-design.md
│   ├── 03-helm-charts.md
│   └── 04-k9s-setup.md            # FREE alternative to kubectl-ai
├── docker/                         # Docker configuration
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   └── docker-compose.yml
├── kubernetes/                     # Kubernetes manifests
│   ├── namespace.yaml
│   ├── backend/
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   └── service.yaml
│   └── frontend/
│       ├── configmap.yaml
│       └── service.yaml
├── helm/                           # Helm charts
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       └── templates/
│           ├── NOTES.txt
│           └── _helpers.tpl
├── scripts/                        # Automation scripts
│   ├── setup-minikube.sh
│   ├── build-images.sh
│   ├── deploy-local.sh
│   ├── cleanup.sh
│   └── kubectl-ai-examples.sh
├── kubectl-ai/                     # kubectl-ai configuration
│   ├── config.yaml
│   └── examples.md
└── kagent/                         # kagent configuration
    ├── config.yaml
    └── examples.md
```

## Quick Start

### Prerequisites

- Docker 24.0+
- Minikube 1.32+
- kubectl 1.28+
- Helm 3.13+
- OpenAI API key
- 8GB RAM, 20GB disk space

### Installation

#### 1. Setup Minikube

```bash
cd phase-4

# Start Minikube cluster
./scripts/setup-minikube.sh

# Verify cluster is running
kubectl cluster-info
minikube status
```

#### 2. Build Docker Images

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Build images and load into Minikube
./scripts/build-images.sh

# Verify images
minikube image ls | grep todo-
```

#### 3. Deploy with Helm

```bash
# Deploy application
./scripts/deploy-local.sh

# Wait for pods to be ready
kubectl get pods -n todo-app-dev -w
```

#### 4. Access Application

```bash
# Get frontend URL
minikube service todo-app-frontend -n todo-app-dev --url

# Or use port forwarding
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app-dev

# Open in browser
open http://localhost:3000
```

#### 5. Setup kubectl-ai (Optional)

```bash
# Install kubectl-ai
kubectl krew install ai

# Configure
export OPENAI_API_KEY="sk-proj-your-key-here"

# Test
kubectl ai "show me all pods in todo-app-dev"
```

#### 6. Setup kagent (Optional)

```bash
# Install kagent
curl -LO https://github.com/kagent-io/kagent/releases/latest/download/kagent-linux-amd64
chmod +x kagent-linux-amd64
sudo mv kagent-linux-amd64 /usr/local/bin/kagent

# Start kagent
kagent start --config kagent/config.yaml

# Check status
kagent status
```

## Deployment Workflow

### Complete Deployment

```bash
# 1. Start Minikube
./scripts/setup-minikube.sh

# 2. Build Docker images
./scripts/build-images.sh

# 3. Deploy with Helm
./scripts/deploy-local.sh

# 4. Access application
minikube service todo-app-frontend -n todo-app-dev

# 5. Use kubectl-ai
kubectl ai "show pod status in todo-app-dev"

# 6. Use kagent
kagent analyze cluster
```

### Update Deployment

```bash
# Rebuild images
./scripts/build-images.sh

# Upgrade Helm release
helm upgrade todo-app ./helm/todo-app \
  -f helm/todo-app/values-dev.yaml \
  -n todo-app-dev \
  --wait

# Verify rollout
kubectl rollout status deployment/todo-app-backend -n todo-app-dev
kubectl rollout status deployment/todo-app-frontend -n todo-app-dev
```

### Rollback Deployment

```bash
# View release history
helm history todo-app -n todo-app-dev

# Rollback to previous version
helm rollback todo-app -n todo-app-dev

# Rollback to specific revision
helm rollback todo-app 2 -n todo-app-dev
```

### Cleanup

```bash
# Remove all resources
./scripts/cleanup.sh

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Minikube Cluster                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Namespace: todo-app-dev                                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │    │
│  │  │  Frontend    │  │   Backend    │  │  Database   │ │    │
│  │  │  Deployment  │  │  Deployment  │  │ StatefulSet │ │    │
│  │  │  (2 replicas)│  │  (2 replicas)│  │  (1 replica)│ │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘ │    │
│  │         │                  │                  │        │    │
│  │  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼──────┐ │    │
│  │  │  Frontend    │  │   Backend    │  │  Database   │ │    │
│  │  │   Service    │  │   Service    │  │   Service   │ │    │
│  │  │  (NodePort)  │  │  (ClusterIP) │  │ (ClusterIP) │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐                  │    │
│  │  │  ConfigMaps  │  │   Secrets    │                  │    │
│  │  └──────────────┘  └──────────────┘                  │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐    │    │
│  │  │  Persistent Volume (Database Storage)        │    │    │
│  │  └──────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  AI-Powered Management:                                         │
│  ┌────────────────┐  ┌────────────────┐                       │
│  │   kubectl-ai   │  │     kagent     │                       │
│  │  (CLI plugin)  │  │  (Autonomous)  │                       │
│  └────────────────┘  └────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

### Resource Requirements

| Component | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|----------|-------------|-----------|----------------|--------------|
| Frontend  | 2        | 200m        | 400m      | 256Mi          | 512Mi        |
| Backend   | 2        | 250m        | 500m      | 256Mi          | 512Mi        |
| Database  | 1        | 250m        | 500m      | 256Mi          | 512Mi        |
| **Total** | **5**    | **1150m**   | **2300m** | **1280Mi**     | **2560Mi**   |

**Minikube Requirements**: 4GB RAM, 2 CPUs minimum

## Key Capabilities

### Docker Containerization

- **Multi-stage Builds**: Separate build and runtime stages
- **Optimized Images**: Backend ~200MB, Frontend ~150MB
- **Security**: Non-root users, minimal base images
- **Health Checks**: Built-in container health checks
- **Local Testing**: Docker Compose for quick testing

### Kubernetes Features

- **High Availability**: Multiple replicas with anti-affinity
- **Health Probes**: Liveness, readiness, and startup probes
- **Rolling Updates**: Zero-downtime deployments
- **Resource Management**: Requests and limits configured
- **Persistent Storage**: StatefulSet with PVC for database
- **Configuration**: ConfigMaps and Secrets for externalized config

### Helm Benefits

- **Declarative**: Infrastructure as Code
- **Templated**: Reusable Kubernetes manifests
- **Versioned**: Track deployment history
- **Environment-specific**: Different values for dev/prod
- **Easy Rollback**: One command to rollback

### kubectl-ai Features

- **Natural Language**: "show me failing pods"
- **Intelligent Debugging**: AI-powered troubleshooting
- **Resource Optimization**: Suggest improvements
- **Safety**: Confirmation for destructive operations
- **Context-Aware**: Understands cluster state

### kagent Capabilities

- **Auto-Remediation**: Restart crashed pods automatically
- **Predictive Scaling**: Scale before load increases
- **Resource Optimization**: Right-size resources
- **Proactive Monitoring**: Detect issues early
- **Autonomous**: Minimal human intervention

## Common Operations

### View Resources

```bash
# All resources
kubectl get all -n todo-app-dev

# Pods
kubectl get pods -n todo-app-dev

# Services
kubectl get services -n todo-app-dev

# Deployments
kubectl get deployments -n todo-app-dev
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/todo-app-backend -n todo-app-dev

# Frontend logs
kubectl logs -f deployment/todo-app-frontend -n todo-app-dev

# Database logs
kubectl logs -f statefulset/todo-app-database -n todo-app-dev

# All logs
kubectl logs -l app.kubernetes.io/name=todo-app -n todo-app-dev --all-containers=true
```

### Scale Deployments

```bash
# Scale backend
kubectl scale deployment todo-app-backend -n todo-app-dev --replicas=3

# Scale frontend
kubectl scale deployment todo-app-frontend -n todo-app-dev --replicas=3

# Verify
kubectl get deployments -n todo-app-dev
```

### Debug Issues

```bash
# Describe pod
kubectl describe pod <pod-name> -n todo-app-dev

# Get events
kubectl get events -n todo-app-dev --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n todo-app-dev

# Use kubectl-ai
kubectl ai "why is my backend pod crashing?"
```

### Access Services

```bash
# Frontend (NodePort)
minikube service todo-app-frontend -n todo-app-dev --url

# Backend (Port Forward)
kubectl port-forward svc/todo-app-backend 8000:8000 -n todo-app-dev

# Database (Port Forward)
kubectl port-forward svc/todo-app-database 5432:5432 -n todo-app-dev
```

## kubectl-ai Examples

```bash
# Show pods
kubectl ai "show me all pods in todo-app-dev"

# Check health
kubectl ai "are there any failing pods?"

# View logs
kubectl ai "show logs from backend pods"

# Scale
kubectl ai "scale backend to 3 replicas"

# Debug
kubectl ai "why is my pod crashing?"

# Optimize
kubectl ai "suggest resource optimizations"
```

## kagent Examples

```bash
# Analyze cluster
kagent analyze cluster

# Get recommendations
kagent recommend optimizations

# View auto-remediation history
kagent auto-heal history

# Enable predictive scaling
kagent predict enable

# Monitor in real-time
kagent monitor
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n todo-app-dev

# Describe pod
kubectl describe pod <pod-name> -n todo-app-dev

# Check events
kubectl get events -n todo-app-dev

# Check logs
kubectl logs <pod-name> -n todo-app-dev
```

### Images Not Found

```bash
# Verify images in Minikube
minikube image ls | grep todo-

# Rebuild images
./scripts/build-images.sh

# Check imagePullPolicy (should be "Never" for local images)
kubectl get deployment todo-app-backend -n todo-app-dev -o yaml | grep imagePullPolicy
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n todo-app-dev

# Check endpoints
kubectl get endpoints -n todo-app-dev

# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -n todo-app-dev -- wget -O- http://todo-app-backend:8000/health
```

### Helm Issues

```bash
# Lint chart
helm lint ./helm/todo-app

# Dry-run
helm install todo-app ./helm/todo-app --dry-run --debug -n todo-app-dev

# Check release
helm list -n todo-app-dev

# View release history
helm history todo-app -n todo-app-dev
```

## Performance Optimization

### Resource Tuning

```bash
# Check current usage
kubectl top pods -n todo-app-dev

# Adjust resources in values.yaml
# Then upgrade
helm upgrade todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml -n todo-app-dev
```

### Horizontal Pod Autoscaling

```bash
# Create HPA
kubectl autoscale deployment todo-app-backend \
  --cpu-percent=70 \
  --min=2 \
  --max=5 \
  -n todo-app-dev

# Check HPA
kubectl get hpa -n todo-app-dev
```

## Security

### Best Practices

- ✅ Non-root containers
- ✅ Minimal base images
- ✅ Secrets in Kubernetes Secrets (not in Git)
- ✅ Resource limits configured
- ✅ Security context defined
- ✅ Network policies (optional)
- ✅ RBAC configured

### Secrets Management

```bash
# Create secret
kubectl create secret generic todo-secrets \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  -n todo-app-dev

# View secrets (base64 encoded)
kubectl get secret todo-secrets -n todo-app-dev -o yaml

# Decode secret
kubectl get secret todo-secrets -n todo-app-dev -o jsonpath='{.data.openai-api-key}' | base64 -d
```

## Monitoring

### Kubernetes Dashboard

```bash
# Open dashboard
minikube dashboard
```

### Metrics

```bash
# Node metrics
kubectl top nodes

# Pod metrics
kubectl top pods -n todo-app-dev

# Resource usage over time
kubectl top pods -n todo-app-dev --containers
```

## Documentation

- **Constitution**: `constitution.md` - Cloud-native principles
- **Specifications**: `specs/` - Detailed feature specifications
- **Docker**: `docker/` - Containerization configuration
- **Kubernetes**: `kubernetes/` - K8s manifests
- **Helm**: `helm/` - Helm charts
- **Scripts**: `scripts/` - Automation scripts
- **kubectl-ai**: `kubectl-ai/` - AI CLI configuration
- **kagent**: `kagent/` - Autonomous agent configuration

## Success Criteria

Phase 4 is complete when:

- ✅ All services deploy successfully to Minikube
- ✅ Frontend accessible from host machine
- ✅ Backend API responds to requests
- ✅ Database persists data across pod restarts
- ✅ Health checks pass for all services
- ✅ Multiple replicas running for HA
- ✅ kubectl-ai executes AI-powered commands
- ✅ kagent monitors and manages cluster
- ✅ Helm upgrade works without downtime
- ✅ All Phase 3 functionality works in Kubernetes
- ✅ Resource usage is optimized
- ✅ Documentation is complete

## Next Steps

After Phase 4 completion:

1. **Production Deployment**: Deploy to cloud Kubernetes (EKS, GKE, AKS)
2. **CI/CD Pipeline**: Automate build and deployment
3. **Monitoring**: Add Prometheus and Grafana
4. **Service Mesh**: Implement Istio or Linkerd
5. **GitOps**: Use ArgoCD or Flux
6. **Multi-cluster**: Deploy across multiple clusters

## Support

For issues or questions:
1. Check specifications in `specs/`
2. Review troubleshooting section above
3. Check Kubernetes events: `kubectl get events -n todo-app-dev`
4. Use kubectl-ai: `kubectl ai "help me debug this issue"`
5. Check kagent logs: `kagent logs`

## License

MIT License - See LICENSE file for details

---

**Phase 4 Status**: Specification Complete ✅
**Next Step**: Begin implementation following the Quick Start guide
**Estimated Completion**: 1-2 weeks
