# Phase 5: Advanced Cloud Deployment with Kafka, Dapr, and DOKS

Production-grade deployment of the Todo application on DigitalOcean Kubernetes with event-driven architecture, distributed tracing, and comprehensive monitoring.

## 🎯 Overview

Phase 5 transforms the todo application into a cloud-native, event-driven system deployed on production infrastructure:

- **Cloud Platform**: DigitalOcean Kubernetes (DOKS)
- **Event Streaming**: Apache Kafka via Strimzi Operator
- **Service Mesh**: Dapr for distributed application runtime
- **Monitoring**: Prometheus, Grafana, Jaeger
- **CI/CD**: GitHub Actions for automated deployments
- **Autoscaling**: Horizontal Pod Autoscaler (HPA)

## 📋 Prerequisites

### Required Tools

- **doctl** (DigitalOcean CLI): [Install Guide](https://docs.digitalocean.com/reference/doctl/how-to/install/)
- **kubectl** (Kubernetes CLI): [Install Guide](https://kubernetes.io/docs/tasks/tools/)
- **helm** (Package Manager): [Install Guide](https://helm.sh/docs/intro/install/)
- **docker** (Container Runtime): [Install Guide](https://docs.docker.com/get-docker/)
- **terraform** (Optional, for IaC): [Install Guide](https://developer.hashicorp.com/terraform/install)

### DigitalOcean Account

- Active DigitalOcean account
- API token with read/write permissions
- Sufficient quota for:
  - 3-5 Kubernetes nodes (s-2vcpu-4gb droplets)
  - 1 Load Balancer
  - Container Registry (free tier)

### Cost Estimate

**Monthly costs (approximate):**
- DOKS Cluster (3 nodes): ~$72/month
- Load Balancer: ~$12/month
- Container Registry: Free (up to 500MB)
- **Total**: ~$84/month

⚠️ **Important**: Remember to destroy resources after demo to avoid charges!

## 🚀 Quick Start

### 1. Setup DigitalOcean Authentication

```bash
# Initialize doctl
doctl auth init

# Verify authentication
doctl account get
```

### 2. Create DOKS Cluster

```bash
cd phase-5

# Option A: Using automated script
./scripts/setup-doks.sh

# Option B: Using Terraform
cd terraform
terraform init
terraform apply
cd ..
```

This creates:
- DOKS cluster with 3 nodes
- Cluster autoscaling (min: 2, max: 5)
- Container registry
- kubectl configuration

### 3. Install Infrastructure Components

```bash
# Install Kafka (Strimzi operator + cluster)
./scripts/install-kafka.sh

# Install Dapr (distributed application runtime)
./scripts/install-dapr.sh

# Install Monitoring (Prometheus, Grafana, Jaeger)
./scripts/setup-monitoring.sh
```

### 4. Build and Push Docker Images

```bash
# Authenticate Docker with registry
doctl registry login

# Build backend image
cd ../phase-3/backend
docker build -t registry.digitalocean.com/todo-app-registry/todo-backend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-backend:latest

# Build frontend image
cd ../frontend
docker build -t registry.digitalocean.com/todo-app-registry/todo-frontend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-frontend:latest

# Build event service image
cd ../../phase-5/backend-event-service
docker build -t registry.digitalocean.com/todo-app-registry/event-service:latest .
docker push registry.digitalocean.com/todo-app-registry/event-service:latest
```

### 5. Configure Secrets

```bash
# Copy secrets template
cp kubernetes/doks/secrets.yaml.example kubernetes/doks/secrets.yaml

# Edit with real values
# - Database URL (Neon PostgreSQL)
# - OpenAI API key
# - Redis password
nano kubernetes/doks/secrets.yaml

# IMPORTANT: Never commit secrets.yaml to git!
```

### 6. Deploy Application

```bash
./scripts/deploy-production.sh
```

This deploys:
- Backend API (3 replicas with Dapr sidecar)
- Frontend (3 replicas)
- Event Service (2 replicas with Dapr sidecar)
- Redis (for Dapr state store)
- Ingress controller with Load Balancer

### 7. Access Application

```bash
# Get load balancer IP
kubectl get svc ingress-nginx-controller -n ingress-nginx

# Access application
# Frontend: http://<LOAD_BALANCER_IP>
# Backend API: http://<LOAD_BALANCER_IP>/api
```

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  DigitalOcean Cloud                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         DigitalOcean Load Balancer                   │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              DOKS Cluster                            │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  Ingress-Nginx Controller                      │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  todo-app-prod namespace                       │ │  │
│  │  │                                                │ │  │
│  │  │  Backend (3 pods) + Dapr Sidecars             │ │  │
│  │  │  Frontend (3 pods)                             │ │  │
│  │  │  Event Service (2 pods) + Dapr Sidecars       │ │  │
│  │  │  Redis (state store)                           │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  kafka namespace                               │ │  │
│  │  │  Kafka Cluster (3 brokers)                     │ │  │
│  │  │  Zookeeper (3 nodes)                           │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  monitoring namespace                          │ │  │
│  │  │  Prometheus, Grafana, Jaeger                   │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Event Flow

```
User → Frontend → Backend API → Database
                      ↓
                 Publish Event (Dapr)
                      ↓
                 Kafka Topic
                      ↓
              Event Service (Dapr)
                      ↓
         Analytics / Audit / Notifications
```

## 📊 Monitoring

### Access Monitoring Tools

```bash
# Grafana (dashboards)
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000 (admin/admin)

# Prometheus (metrics)
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090

# Jaeger (distributed tracing)
kubectl port-forward -n monitoring svc/jaeger-query 16686:16686
# Open: http://localhost:16686
```

### Key Metrics

- **API Request Rate**: Requests per second
- **API Latency**: p50, p95, p99 response times
- **Error Rate**: 4xx and 5xx responses
- **Task Operations**: Create, update, delete rates
- **Event Publishing**: Events published per second
- **Kafka Consumer Lag**: Event processing backlog
- **Pod Resources**: CPU and memory usage

### Alerts

Configured alerts for:
- High error rate (>5%)
- High API latency (p95 >1s)
- Pod crash looping
- High Kafka consumer lag (>1000 messages)
- Node memory pressure
- Pod memory usage high (>90%)

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

**Build and Push** (`.github/workflows/build-push.yml`):
- Triggers on push to main branch
- Builds Docker images for backend, frontend, event service
- Pushes to DigitalOcean Container Registry
- Tags with git commit SHA and 'latest'

**Deploy to DOKS** (`.github/workflows/deploy-doks.yml`):
- Triggers after successful build
- Deploys using Helm
- Runs smoke tests
- Notifies on success/failure

### Setup GitHub Actions

1. Add secrets to GitHub repository:
   - `DIGITALOCEAN_ACCESS_TOKEN`: Your DO API token

2. Push code to trigger pipeline:
```bash
git add .
git commit -m "Deploy Phase 5"
git push origin main
```

## 📈 Autoscaling

### Horizontal Pod Autoscaler (HPA)

Configured for all services:

**Backend:**
- Min replicas: 2
- Max replicas: 10
- Target CPU: 70%
- Target Memory: 80%

**Frontend:**
- Min replicas: 2
- Max replicas: 8
- Target CPU: 70%

**Event Service:**
- Min replicas: 1
- Max replicas: 5
- Target CPU: 70%

### Test Autoscaling

```bash
# Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
# Inside pod:
while true; do wget -q -O- http://todo-backend.todo-app-prod.svc.cluster.local:8000/api/tasks; done

# Watch HPA scale up
kubectl get hpa -n todo-app-prod -w
```

## 🔧 Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo-app-prod
kubectl describe pod <pod-name> -n todo-app-prod
kubectl logs <pod-name> -n todo-app-prod
```

### Check Dapr Sidecar

```bash
# View Dapr sidecar logs
kubectl logs <pod-name> -c daprd -n todo-app-prod

# Check Dapr components
kubectl get components -n todo-app-prod
```

### Check Kafka

```bash
# Kafka cluster status
kubectl get kafka -n kafka

# Kafka topics
kubectl get kafkatopics -n kafka

# Kafka broker logs
kubectl logs -n kafka todo-kafka-kafka-0
```

### Check Events

```bash
# View events in namespace
kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'
```

### Common Issues

**Pods not starting:**
- Check image pull errors: `kubectl describe pod <pod-name>`
- Verify registry authentication: `doctl registry login`

**Dapr sidecar not injecting:**
- Verify Dapr is installed: `dapr status -k`
- Check annotations in deployment

**Events not flowing:**
- Check Kafka cluster: `kubectl get kafka -n kafka`
- Check Dapr pub/sub component: `kubectl get component kafka-pubsub -n todo-app-prod`
- View event service logs: `kubectl logs -l app=event-service -n todo-app-prod`

## 🧹 Cleanup

### Destroy All Resources

```bash
# Run cleanup script
./scripts/cleanup-cloud.sh

# Verify in DigitalOcean console:
# - Cluster deleted
# - Load balancer deleted
# - Volumes deleted
# - Registry deleted
```

**⚠️ Important**: Always verify in the DigitalOcean console that all resources are deleted to avoid unexpected charges!

## 📁 Project Structure

```
phase-5/
├── constitution.md              # Production cloud principles
├── specs/                       # Feature specifications
│   ├── 01-event-driven-architecture.md
│   ├── 02-kafka-integration.md
│   ├── 03-dapr-setup.md
│   ├── 04-doks-deployment.md
│   └── 05-monitoring-scaling.md
├── scripts/                     # Deployment scripts
│   ├── setup-doks.sh
│   ├── install-kafka.sh
│   ├── install-dapr.sh
│   ├── setup-monitoring.sh
│   ├── deploy-production.sh
│   └── cleanup-cloud.sh
├── kubernetes/                  # Kubernetes manifests
│   ├── doks/
│   │   ├── namespace.yaml
│   │   ├── kafka-cluster.yaml
│   │   ├── kafka-metrics-config.yaml
│   │   ├── ingress.yaml
│   │   └── secrets.yaml.example
│   └── monitoring/
│       ├── prometheus-rules.yaml
│       ├── grafana-dashboard.yaml
│       └── backend-servicemonitor.yaml
├── dapr/                        # Dapr configuration
│   ├── components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   └── secretstore.yaml
│   └── configuration/
│       └── tracing.yaml
├── kafka/                       # Kafka topics
│   └── topics.yaml
├── helm/                        # Helm charts
│   └── todo-app-prod/
│       ├── Chart.yaml
│       ├── values-production.yaml
│       └── templates/
│           ├── backend.yaml
│           ├── frontend.yaml
│           ├── event-service.yaml
│           ├── hpa.yaml
│           └── ingress.yaml
├── backend-event-service/       # Event consumer service
│   ├── src/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── terraform/                   # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ci-cd/                       # CI/CD workflows
│   └── .github/
│       └── workflows/
│           ├── build-push.yml
│           └── deploy-doks.yml
└── README.md                    # This file
```

## 🎓 Learning Resources

- [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/)
- [Strimzi Kafka Operator](https://strimzi.io/docs/operators/latest/overview.html)
- [Dapr Documentation](https://docs.dapr.io/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Helm Charts](https://helm.sh/docs/topics/charts/)

## 🏆 Hackathon Bonus Opportunities

- ✅ **Event-Driven Architecture**: Kafka + Dapr pub/sub
- ✅ **Production Cloud Deployment**: DOKS with HA
- ✅ **Comprehensive Monitoring**: Prometheus + Grafana + Jaeger
- ✅ **Autoscaling**: HPA for all services
- ✅ **CI/CD Pipeline**: GitHub Actions
- ✅ **Infrastructure as Code**: Terraform + Helm
- 🎯 **Reusable Intelligence**: Claude Code Subagents (+200 points)
- 🎯 **Cloud-Native Blueprints**: Agent Skills (+200 points)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

---

**Built with ❤️ for the Evolution of Todo Hackathon**
