# Phase 5: Advanced Cloud Deployment - Claude Code Instructions

## Project Context

**Phase**: Phase 5 - Production Cloud Deployment
**Status**: Implementation Ready
**Technology Stack**: DOKS, Kafka, Dapr, Prometheus, Grafana, Jaeger

This phase deploys the todo application to production cloud infrastructure with:
- Event-driven architecture using Apache Kafka
- Distributed application runtime with Dapr
- Comprehensive monitoring and observability
- Horizontal autoscaling
- CI/CD automation

## Architecture Overview

### Infrastructure Layers

1. **Cloud Platform**: DigitalOcean Kubernetes (DOKS)
   - 3-node cluster with autoscaling (2-5 nodes)
   - DigitalOcean Load Balancer
   - Container Registry (DOCR)
   - VPC networking

2. **Event Streaming**: Apache Kafka
   - Deployed via Strimzi Operator
   - 3 Kafka brokers for high availability
   - 3 Zookeeper nodes
   - 4 topics: task.created, task.updated, task.deleted, task.completed

3. **Service Mesh**: Dapr
   - Pub/Sub component (Kafka backend)
   - State store component (Redis backend)
   - Secret store component (Kubernetes secrets)
   - Distributed tracing (Jaeger)

4. **Application Services**:
   - Backend API (3 replicas + Dapr sidecars)
   - Frontend (3 replicas)
   - Event Service (2 replicas + Dapr sidecars)
   - Redis (state store)

5. **Observability**:
   - Prometheus (metrics collection)
   - Grafana (visualization)
   - Jaeger (distributed tracing)
   - Custom dashboards and alerts

## Development Workflow

### 1. Initial Setup

```bash
# Authenticate with DigitalOcean
doctl auth init

# Create DOKS cluster
cd phase-5
./scripts/setup-doks.sh

# Install infrastructure components
./scripts/install-kafka.sh
./scripts/install-dapr.sh
./scripts/setup-monitoring.sh
```

### 2. Build and Deploy

```bash
# Build and push images
doctl registry login
docker build -t registry.digitalocean.com/todo-app-registry/todo-backend:latest ../phase-3/backend
docker push registry.digitalocean.com/todo-app-registry/todo-backend:latest

# Deploy application
./scripts/deploy-production.sh
```

### 3. Verify Deployment

```bash
# Check pods
kubectl get pods -n todo-app-prod

# Check services
kubectl get svc -n todo-app-prod

# Get application URL
kubectl get ingress -n todo-app-prod
```

## Key Files and Their Purpose

### Specifications (specs/)
- `01-event-driven-architecture.md`: Event flow and schema design
- `02-kafka-integration.md`: Kafka cluster setup and configuration
- `03-dapr-setup.md`: Dapr components and integration
- `04-doks-deployment.md`: Kubernetes deployment strategy
- `05-monitoring-scaling.md`: Observability and autoscaling

### Infrastructure (kubernetes/)
- `doks/kafka-cluster.yaml`: Strimzi Kafka cluster definition
- `doks/ingress.yaml`: Ingress controller configuration
- `doks/namespace.yaml`: Namespace definitions
- `monitoring/prometheus-rules.yaml`: Alert rules
- `monitoring/grafana-dashboard.yaml`: Custom dashboards

### Dapr Configuration (dapr/)
- `components/pubsub.yaml`: Kafka pub/sub component
- `components/statestore.yaml`: Redis state store
- `components/secretstore.yaml`: Kubernetes secrets integration
- `configuration/tracing.yaml`: Jaeger tracing configuration

### Helm Chart (helm/todo-app-prod/)
- `Chart.yaml`: Chart metadata
- `values-production.yaml`: Production configuration
- `templates/backend.yaml`: Backend deployment with Dapr
- `templates/frontend.yaml`: Frontend deployment
- `templates/event-service.yaml`: Event consumer service
- `templates/hpa.yaml`: Horizontal Pod Autoscalers
- `templates/ingress.yaml`: Ingress resource

### Application Code (backend-event-service/)
- `src/main.py`: FastAPI event consumer with Dapr integration
- `Dockerfile`: Container image definition
- `requirements.txt`: Python dependencies

### CI/CD (ci-cd/.github/workflows/)
- `build-push.yml`: Build and push Docker images
- `deploy-doks.yml`: Deploy to DOKS with Helm

### Infrastructure as Code (terraform/)
- `main.tf`: DOKS cluster and registry provisioning
- `variables.tf`: Configurable parameters
- `outputs.tf`: Cluster information outputs

## Important Constraints

### Technical Constraints
1. **Cloud Deployment**: Must use DigitalOcean Kubernetes (DOKS)
2. **Event Streaming**: Must use Apache Kafka via Strimzi
3. **Service Mesh**: Must use Dapr for pub/sub and tracing
4. **Monitoring**: Must include Prometheus, Grafana, Jaeger
5. **Autoscaling**: Must configure HPA for all services
6. **High Availability**: Minimum 2 replicas for critical services

### Security Constraints
1. **No Hardcoded Secrets**: All secrets in Kubernetes Secrets
2. **Secret Management**: Use Dapr secret store component
3. **Image Security**: Scan images for vulnerabilities
4. **RBAC**: Proper service account permissions
5. **Network Policies**: Isolate namespaces (optional)

### Cost Constraints
1. **Resource Limits**: Set CPU/memory limits on all containers
2. **Autoscaling**: Scale down during low traffic
3. **Retention**: Limit Prometheus (7 days) and logs
4. **Cleanup**: Destroy resources after demo
5. **Monitoring**: Track costs in DigitalOcean dashboard

## Common Operations

### Viewing Logs

```bash
# Backend logs
kubectl logs -l app=todo-backend -n todo-app-prod -f

# Event service logs
kubectl logs -l app=event-service -n todo-app-prod -f

# Dapr sidecar logs
kubectl logs <pod-name> -c daprd -n todo-app-prod
```

### Scaling Services

```bash
# Manual scaling
kubectl scale deployment todo-backend --replicas=5 -n todo-app-prod

# Check HPA status
kubectl get hpa -n todo-app-prod
```

### Accessing Monitoring

```bash
# Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Jaeger
kubectl port-forward -n monitoring svc/jaeger-query 16686:16686
```

### Debugging Issues

```bash
# Describe pod
kubectl describe pod <pod-name> -n todo-app-prod

# Check events
kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'

# Check Dapr components
kubectl get components -n todo-app-prod

# Check Kafka topics
kubectl get kafkatopics -n kafka
```

## Testing Strategy

### Manual Testing
1. Access application via load balancer IP
2. Create tasks and verify events are published
3. Check event service logs for event processing
4. View traces in Jaeger
5. Monitor metrics in Grafana

### Load Testing
```bash
# Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
while true; do wget -q -O- http://todo-backend.todo-app-prod.svc.cluster.local:8000/api/tasks; done

# Watch autoscaling
kubectl get hpa -n todo-app-prod -w
```

### Smoke Tests
```bash
# Health checks
curl http://<LOAD_BALANCER_IP>/api/health
curl http://<LOAD_BALANCER_IP>/

# Create task
curl -X POST http://<LOAD_BALANCER_IP>/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Testing deployment"}'
```

## Troubleshooting Guide

### Pods Not Starting
- Check image pull errors: `kubectl describe pod <pod-name>`
- Verify registry authentication: `doctl registry login`
- Check resource limits and node capacity

### Dapr Sidecar Issues
- Verify Dapr is installed: `dapr status -k`
- Check Dapr operator logs: `kubectl logs -n dapr-system -l app=dapr-operator`
- Verify annotations in deployment

### Events Not Flowing
- Check Kafka cluster: `kubectl get kafka -n kafka`
- Verify topics exist: `kubectl get kafkatopics -n kafka`
- Check Dapr pub/sub component: `kubectl get component kafka-pubsub -n todo-app-prod`
- View event service logs for errors

### Monitoring Not Working
- Check Prometheus targets: Port-forward and visit /targets
- Verify ServiceMonitors: `kubectl get servicemonitor -n todo-app-prod`
- Check pod annotations for Prometheus scraping

## Cost Management

### Estimated Monthly Costs
- DOKS Cluster (3 nodes): ~$72/month
- Load Balancer: ~$12/month
- Container Registry: Free (up to 500MB)
- **Total**: ~$84/month

### Cost Optimization Tips
1. Use smallest viable node size (s-2vcpu-4gb)
2. Enable autoscaling to scale down during low traffic
3. Set appropriate resource requests/limits
4. Use Neon serverless database (pay-per-use)
5. Destroy cluster when not in use

### Cleanup Procedure
```bash
# Destroy all resources
./scripts/cleanup-cloud.sh

# Verify in DigitalOcean console:
# - Cluster deleted
# - Load balancer deleted
# - Volumes deleted
# - Registry deleted (optional)
```

## Success Criteria

Phase 5 is complete when:
- ✅ DOKS cluster running with 3 nodes
- ✅ Kafka cluster operational (3 brokers)
- ✅ Dapr sidecars injected into all services
- ✅ Application accessible via public URL
- ✅ Events flowing through Kafka
- ✅ Distributed traces visible in Jaeger
- ✅ Metrics displayed in Grafana
- ✅ Autoscaling working under load
- ✅ CI/CD pipeline deploying successfully
- ✅ All health checks passing

## Next Steps

After Phase 5 completion:
1. Document architecture with diagrams
2. Create runbooks for common operations
3. Set up alerting notifications (Slack, Discord)
4. Implement additional event consumers
5. Add more comprehensive monitoring dashboards
6. Consider multi-region deployment
7. Implement blue-green deployment strategy

## References

- [DOKS Documentation](https://docs.digitalocean.com/products/kubernetes/)
- [Strimzi Kafka Operator](https://strimzi.io/)
- [Dapr Documentation](https://docs.dapr.io/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Helm Documentation](https://helm.sh/docs/)

---

**Version**: 1.0.0
**Last Updated**: 2026-02-07
**Phase**: 5 - Production Cloud Deployment
