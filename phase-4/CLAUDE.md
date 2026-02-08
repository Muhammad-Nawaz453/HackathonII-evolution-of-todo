# Phase 4: Local Kubernetes Deployment - Claude Code Instructions

## Project Context

This is Phase 4 of the "Evolution of Todo" hackathon project. Phase 4 focuses on containerizing the AI-powered todo application and deploying it to a local Kubernetes cluster (Minikube) with AI-powered cluster management.

## Phase 4 Overview

**Goal**: Deploy the Phase 3 application (Next.js frontend + FastAPI backend + PostgreSQL) to Kubernetes using Docker, Minikube, Helm, kubectl-ai, and kagent.

**Key Technologies**:
- Docker: Containerization
- Minikube: Local Kubernetes cluster
- Helm: Kubernetes package manager
- k9s: Terminal UI for Kubernetes (FREE alternative to kubectl-ai)
- kubectl: Standard Kubernetes CLI

**🎉 100% FREE - No paid tools or API keys required!**

## Directory Structure

```
phase-4/
├── constitution.md          # Cloud-native principles
├── README.md                # Main documentation
├── specs/                   # Detailed specifications
├── docker/                  # Docker configuration
├── kubernetes/              # K8s manifests
├── helm/                    # Helm charts
├── scripts/                 # Automation scripts
└── k9s/                     # k9s configuration (FREE)
```

## Implementation Status

### ✅ Completed
- Constitution and principles
- All 5 specifications
- Docker configuration (Dockerfiles, docker-compose.yml)
- Kubernetes manifests (deployments, services, configmaps, secrets)
- Helm chart structure (Chart.yaml, values.yaml, templates)
- Automation scripts (setup, build, deploy, cleanup)
- kubectl-ai configuration and examples
- kagent configuration and examples
- Documentation (README, examples)

### 🔄 Ready for Testing
- Docker image builds
- Kubernetes deployment
- Helm installation
- kubectl-ai integration
- kagent integration

## Quick Start for Testing

### 1. Prerequisites Check
```bash
# Verify tools are installed
docker --version
minikube version
kubectl version --client
helm version
```

### 2. Setup Minikube
```bash
cd phase-4
./scripts/setup-minikube.sh
```

### 3. Build Images
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
./scripts/build-images.sh
```

### 4. Deploy Application
```bash
./scripts/deploy-local.sh
```

### 5. Access Application
```bash
minikube service todo-app-frontend -n todo-app-dev
```

## Key Files to Review

### Specifications (specs/)
1. `01-docker-architecture.md` - Containerization strategy
2. `02-kubernetes-design.md` - K8s architecture
3. `03-helm-charts.md` - Helm chart design
4. `04-kubectl-ai-setup.md` - AI CLI integration
5. `05-kagent-integration.md` - Autonomous agent

### Docker (docker/)
- `backend/Dockerfile` - Multi-stage FastAPI build
- `frontend/Dockerfile` - Multi-stage Next.js build
- `docker-compose.yml` - Local testing

### Kubernetes (kubernetes/)
- `namespace.yaml` - Namespace and quotas
- `backend/` - Backend deployment, service, config
- `frontend/` - Frontend deployment, service, config
- `database/` - StatefulSet, service

### Helm (helm/todo-app/)
- `Chart.yaml` - Chart metadata
- `values.yaml` - Default configuration
- `values-dev.yaml` - Development overrides
- `templates/` - Templated K8s resources

### Scripts (scripts/)
- `setup-minikube.sh` - Initialize Minikube cluster
- `build-images.sh` - Build and load Docker images
- `deploy-local.sh` - Deploy with Helm
- `cleanup.sh` - Remove all resources

## Development Workflow

### Making Changes

1. **Update Docker Images**:
   ```bash
   # Modify code in phase-3/
   # Rebuild images
   ./scripts/build-images.sh
   ```

2. **Update Kubernetes Config**:
   ```bash
   # Modify helm/todo-app/values.yaml
   # Upgrade deployment
   helm upgrade todo-app ./helm/todo-app -n todo-app-dev
   ```

3. **Test Changes**:
   ```bash
   # Check pod status
   kubectl get pods -n todo-app-dev

   # View logs
   kubectl logs -f deployment/todo-app-backend -n todo-app-dev
   ```

### Debugging

```bash
# Describe pod
kubectl describe pod <pod-name> -n todo-app-dev

# Get events
kubectl get events -n todo-app-dev --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n todo-app-dev

# Use k9s (FREE alternative)
k9s -n todo-app-dev
# Press :pods to view pods
# Press 'd' to describe
# Press 'l' to view logs
```

## Important Notes

### Image Pull Policy
- Set to `Never` for local Minikube images
- Images must be built and loaded into Minikube
- Don't use `latest` tag in production

### Resource Limits
- Backend: 250m CPU, 256Mi memory (request)
- Frontend: 200m CPU, 256Mi memory (request)
- Database: 250m CPU, 256Mi memory (request)
- Total: ~1150m CPU, ~1280Mi memory

### Secrets Management
- Never commit secrets to Git
- Use environment variables or Helm --set
- Base64 encode secrets in Kubernetes
- Example: `echo -n "value" | base64`

### Health Checks
- All services have liveness, readiness, and startup probes
- Backend: `/health` endpoint
- Frontend: `/` endpoint
- Database: `pg_isready` command

## Common Issues

### Issue: Images not found
**Solution**: Build images with `./scripts/build-images.sh`

### Issue: Pods stuck in Pending
**Solution**: Check resource availability with `kubectl describe pod`

### Issue: Service not accessible
**Solution**: Use `minikube service` or port-forward

### Issue: Database connection failed
**Solution**: Check database pod is running and secret is correct

## k9s Usage (FREE)

```bash
# Install
# Windows: choco install k9s
# macOS: brew install k9s
# Linux: sudo apt install k9s

# Launch
k9s -n todo-app-dev

# Common shortcuts:
# :pods - View pods
# :svc - View services
# :deploy - View deployments
# d - Describe resource
# l - View logs
# s - Shell into pod
# ? - Help
```

**Advantages:**
- ✅ Completely free ($0/month)
- ✅ No API keys required
- ✅ Works offline
- ✅ Fast and responsive
- ✅ No rate limits
- ✅ Open source

## Testing Checklist

- [ ] Minikube starts successfully
- [ ] Docker images build without errors
- [ ] Images load into Minikube
- [ ] Helm chart installs successfully
- [ ] All pods reach Running state
- [ ] Health checks pass
- [ ] Frontend accessible from browser
- [ ] Backend API responds
- [ ] Database persists data
- [ ] k9s connects to cluster
- [ ] k9s shows all resources

## Next Steps

1. Test complete deployment workflow
2. Verify all Phase 3 functionality works
3. Test kubectl-ai commands
4. Test kagent monitoring
5. Document any issues found
6. Optimize resource usage
7. Prepare demo

## Support

- **Specifications**: See `specs/` for detailed requirements
- **README**: See `README.md` for comprehensive guide
- **Constitution**: See `constitution.md` for principles
- **Troubleshooting**: Check README troubleshooting section

## Success Criteria

Phase 4 is complete when:
- ✅ All services deploy to Minikube
- ✅ Application accessible from host
- ✅ All Phase 3 features work
- ✅ kubectl-ai functional
- ✅ kagent monitoring active
- ✅ Documentation complete
- ✅ Demo ready

---

**Status**: Implementation Complete, Ready for Testing
**Last Updated**: 2026-02-04
