# Specification: DOKS Deployment

**Feature ID**: 04
**Feature Name**: DigitalOcean Kubernetes Deployment
**Phase**: 5 - Production Cloud Deployment
**Status**: Draft
**Created**: 2026-02-07
**Last Updated**: 2026-02-07

## Purpose

Deploy the todo application to DigitalOcean Kubernetes (DOKS) with production-grade configuration including high availability, autoscaling, ingress, and proper resource management. Provide Infrastructure as Code (Terraform) for reproducible cluster provisioning.

## User Stories

**As a platform engineer**, I want Infrastructure as Code so that I can provision and manage the DOKS cluster reproducibly.

**As a developer**, I want automated deployment scripts so that I can deploy the application to production with a single command.

**As an operations engineer**, I want high availability so that the application survives node failures without downtime.

**As a product manager**, I want the application accessible via a public URL so that users can access it from anywhere.

## Acceptance Criteria

### DOKS Cluster Provisioning

- [ ] DOKS cluster created with 3 nodes (s-2vcpu-4gb droplets)
- [ ] Cluster autoscaling enabled (min: 2, max: 5 nodes)
- [ ] Cluster deployed in a DigitalOcean region (e.g., nyc1, sfo3)
- [ ] Kubernetes version 1.28 or later
- [ ] VPC networking configured for private communication
- [ ] kubectl configured to access the cluster

### Container Registry

- [ ] DigitalOcean Container Registry (DOCR) created
- [ ] Docker authenticated with DOCR
- [ ] Backend image built and pushed to DOCR
- [ ] Frontend image built and pushed to DOCR
- [ ] Event service image built and pushed to DOCR
- [ ] Kubernetes configured to pull from DOCR

### Namespace Configuration

- [ ] `todo-app-prod` namespace created for application
- [ ] `kafka` namespace created for Kafka cluster
- [ ] `dapr-system` namespace created for Dapr control plane
- [ ] `monitoring` namespace created for observability stack
- [ ] `ingress-nginx` namespace created for ingress controller

### Ingress and Load Balancer

- [ ] Ingress-nginx controller deployed
- [ ] DigitalOcean Load Balancer provisioned automatically
- [ ] Ingress resource configured for frontend and backend
- [ ] Public URL accessible (e.g., http://<load-balancer-ip>)
- [ ] Optional: SSL/TLS certificate configured with cert-manager

### Application Deployment

- [ ] Backend deployed with 3 replicas
- [ ] Frontend deployed with 3 replicas
- [ ] Event service deployed with 2 replicas
- [ ] All pods have resource requests and limits
- [ ] All pods have liveness and readiness probes
- [ ] Horizontal Pod Autoscaler (HPA) configured for all services

### Secrets Management

- [ ] Database credentials stored in Kubernetes Secret
- [ ] OpenAI API key stored in Kubernetes Secret
- [ ] Redis password stored in Kubernetes Secret
- [ ] Secrets not committed to version control
- [ ] Documentation for creating secrets

## Architecture

### DOKS Cluster Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  DigitalOcean Cloud                         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              DigitalOcean Load Balancer               │ │
│  │         (Provisioned by Ingress Controller)           │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────▼──────────────────────────────┐ │
│  │              DOKS Cluster (3 nodes)                   │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │         Ingress-Nginx Controller                │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │      todo-app-prod namespace                    │ │ │
│  │  │                                                 │ │ │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │ │ │
│  │  │  │ Backend  │  │ Backend  │  │ Backend  │     │ │ │
│  │  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │     │ │ │
│  │  │  └──────────┘  └──────────┘  └──────────┘     │ │ │
│  │  │                                                 │ │ │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │ │ │
│  │  │  │Frontend  │  │Frontend  │  │Frontend  │     │ │ │
│  │  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │     │ │ │
│  │  │  └──────────┘  └──────────┘  └──────────┘     │ │ │
│  │  │                                                 │ │ │
│  │  │  ┌──────────┐  ┌──────────┐                   │ │ │
│  │  │  │  Event   │  │  Event   │                   │ │ │
│  │  │  │Service 1 │  │Service 2 │                   │ │ │
│  │  │  └──────────┘  └──────────┘                   │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │         kafka namespace                         │ │ │
│  │  │  (Kafka cluster with 3 brokers)                 │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │         dapr-system namespace                   │ │ │
│  │  │  (Dapr control plane)                           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │         monitoring namespace                    │ │ │
│  │  │  (Prometheus, Grafana, Jaeger)                  │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │      DigitalOcean Container Registry (DOCR)           │ │
│  │  - todo-backend:latest                                │ │
│  │  - todo-frontend:latest                               │ │
│  │  - event-service:latest                               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Terraform Configuration

**File**: `terraform/main.tf`

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.34"
    }
  }

  # Optional: Store state in DigitalOcean Spaces
  # backend "s3" {
  #   endpoint                    = "nyc3.digitaloceanspaces.com"
  #   key                         = "terraform/todo-app.tfstate"
  #   bucket                      = "my-terraform-state"
  #   region                      = "us-east-1"
  #   skip_credentials_validation = true
  #   skip_metadata_api_check     = true
  # }
}

provider "digitalocean" {
  token = var.do_token
}

# DOKS Cluster
resource "digitalocean_kubernetes_cluster" "todo_app" {
  name    = var.cluster_name
  region  = var.region
  version = var.kubernetes_version

  node_pool {
    name       = "worker-pool"
    size       = var.node_size
    node_count = var.node_count
    auto_scale = true
    min_nodes  = var.min_nodes
    max_nodes  = var.max_nodes
    tags       = ["todo-app", "production"]
  }

  tags = ["todo-app", "production"]
}

# Container Registry
resource "digitalocean_container_registry" "todo_app" {
  name                   = var.registry_name
  subscription_tier_slug = "basic"  # Free tier
  region                 = var.region
}

# VPC (optional, for network isolation)
resource "digitalocean_vpc" "todo_app" {
  name     = "${var.cluster_name}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"
}

# Output kubeconfig
resource "local_file" "kubeconfig" {
  content  = digitalocean_kubernetes_cluster.todo_app.kube_config[0].raw_config
  filename = "${path.module}/kubeconfig.yaml"
}
```

**File**: `terraform/variables.tf`

```hcl
variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Name of the DOKS cluster"
  type        = string
  default     = "todo-app-prod"
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "nyc1"  # Options: nyc1, nyc3, sfo3, lon1, fra1, sgp1, etc.
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28.2-do.0"  # Check latest: doctl kubernetes options versions
}

variable "node_size" {
  description = "Droplet size for worker nodes"
  type        = string
  default     = "s-2vcpu-4gb"  # $24/month per node
}

variable "node_count" {
  description = "Initial number of worker nodes"
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Minimum nodes for autoscaling"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum nodes for autoscaling"
  type        = number
  default     = 5
}

variable "registry_name" {
  description = "Container registry name"
  type        = string
  default     = "todo-app-registry"
}
```

**File**: `terraform/outputs.tf`

```hcl
output "cluster_id" {
  description = "DOKS cluster ID"
  value       = digitalocean_kubernetes_cluster.todo_app.id
}

output "cluster_endpoint" {
  description = "DOKS cluster endpoint"
  value       = digitalocean_kubernetes_cluster.todo_app.endpoint
}

output "cluster_name" {
  description = "DOKS cluster name"
  value       = digitalocean_kubernetes_cluster.todo_app.name
}

output "registry_endpoint" {
  description = "Container registry endpoint"
  value       = digitalocean_container_registry.todo_app.endpoint
}

output "kubeconfig_path" {
  description = "Path to kubeconfig file"
  value       = local_file.kubeconfig.filename
}
```

### 2. Setup Script (Alternative to Terraform)

**File**: `scripts/setup-doks.sh`

```bash
#!/bin/bash
set -e

# Configuration
CLUSTER_NAME="${CLUSTER_NAME:-todo-app-prod}"
REGION="${REGION:-nyc1}"
NODE_SIZE="${NODE_SIZE:-s-2vcpu-4gb}"
NODE_COUNT="${NODE_COUNT:-3}"
REGISTRY_NAME="${REGISTRY_NAME:-todo-app-registry}"

echo "Creating DOKS cluster: $CLUSTER_NAME"
echo "Region: $REGION"
echo "Node size: $NODE_SIZE"
echo "Node count: $NODE_COUNT"
echo ""

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "Error: doctl is not installed"
    echo "Install: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if authenticated
if ! doctl account get &> /dev/null; then
    echo "Error: Not authenticated with DigitalOcean"
    echo "Run: doctl auth init"
    exit 1
fi

# Create DOKS cluster
echo "Creating DOKS cluster (this takes 5-10 minutes)..."
doctl kubernetes cluster create "$CLUSTER_NAME" \
  --region "$REGION" \
  --version latest \
  --size "$NODE_SIZE" \
  --count "$NODE_COUNT" \
  --auto-upgrade=true \
  --surge-upgrade=true \
  --maintenance-window "saturday=02:00" \
  --tag "todo-app,production" \
  --wait

# Enable autoscaling
echo "Enabling cluster autoscaling..."
CLUSTER_ID=$(doctl kubernetes cluster get "$CLUSTER_NAME" --format ID --no-header)
NODE_POOL_ID=$(doctl kubernetes cluster node-pool list "$CLUSTER_ID" --format ID --no-header)

doctl kubernetes cluster node-pool update "$CLUSTER_ID" "$NODE_POOL_ID" \
  --auto-scale \
  --min-nodes 2 \
  --max-nodes 5

# Configure kubectl
echo "Configuring kubectl..."
doctl kubernetes cluster kubeconfig save "$CLUSTER_NAME"

# Verify cluster access
echo "Verifying cluster access..."
kubectl cluster-info
kubectl get nodes

# Create container registry
echo "Creating container registry..."
doctl registry create "$REGISTRY_NAME" --subscription-tier basic --region "$REGION" || true

# Configure Docker to use registry
echo "Configuring Docker authentication..."
doctl registry login

echo ""
echo "✅ DOKS cluster created successfully!"
echo ""
echo "Cluster name: $CLUSTER_NAME"
echo "Cluster ID: $CLUSTER_ID"
echo "Registry: registry.digitalocean.com/$REGISTRY_NAME"
echo ""
echo "Next steps:"
echo "  1. Install Kafka: ./scripts/install-kafka.sh"
echo "  2. Install Dapr: ./scripts/install-dapr.sh"
echo "  3. Deploy application: ./scripts/deploy-production.sh"
```

### 3. Ingress-Nginx Installation

**File**: `kubernetes/doks/ingress-nginx.yaml`

```yaml
# Install using Helm (recommended)
# helm upgrade --install ingress-nginx ingress-nginx \
#   --repo https://kubernetes.github.io/ingress-nginx \
#   --namespace ingress-nginx --create-namespace \
#   --set controller.service.type=LoadBalancer \
#   --set controller.metrics.enabled=true \
#   --set controller.podAnnotations."prometheus\.io/scrape"=true \
#   --set controller.podAnnotations."prometheus\.io/port"=10254

# Or use this manifest for basic setup
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
---
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx-controller
  namespace: ingress-nginx
  annotations:
    service.beta.kubernetes.io/do-loadbalancer-name: "todo-app-lb"
    service.beta.kubernetes.io/do-loadbalancer-protocol: "http"
    service.beta.kubernetes.io/do-loadbalancer-healthcheck-path: "/healthz"
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/component: controller
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
```

### 4. Application Ingress

**File**: `kubernetes/doks/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  namespace: todo-app-prod
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 80
```

### 5. Namespace Configuration

**File**: `kubernetes/doks/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app-prod
  labels:
    name: todo-app-prod
    environment: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: kafka
  labels:
    name: kafka
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
  labels:
    name: monitoring
```

### 6. Secrets Configuration

**File**: `kubernetes/doks/secrets.yaml.example`

```yaml
# DO NOT COMMIT THIS FILE WITH REAL VALUES!
# Copy to secrets.yaml and fill in real values
# Add secrets.yaml to .gitignore

apiVersion: v1
kind: Secret
metadata:
  name: database-secret
  namespace: todo-app-prod
type: Opaque
stringData:
  url: "postgresql://user:password@host:5432/dbname"
---
apiVersion: v1
kind: Secret
metadata:
  name: openai-secret
  namespace: todo-app-prod
type: Opaque
stringData:
  api-key: "sk-..."
---
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: todo-app-prod
type: Opaque
stringData:
  password: "changeme"
```

### 7. Deployment Script

**File**: `scripts/deploy-production.sh`

```bash
#!/bin/bash
set -e

NAMESPACE="todo-app-prod"
REGISTRY="registry.digitalocean.com/todo-app-registry"
VERSION="${VERSION:-latest}"

echo "Deploying Todo App to DOKS..."
echo "Namespace: $NAMESPACE"
echo "Registry: $REGISTRY"
echo "Version: $VERSION"
echo ""

# Verify cluster access
if ! kubectl cluster-info &> /dev/null; then
    echo "Error: Cannot access Kubernetes cluster"
    echo "Run: doctl kubernetes cluster kubeconfig save <cluster-name>"
    exit 1
fi

# Create namespace
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Apply secrets (must exist!)
if [ ! -f kubernetes/doks/secrets.yaml ]; then
    echo "Error: kubernetes/doks/secrets.yaml not found"
    echo "Copy secrets.yaml.example and fill in real values"
    exit 1
fi
kubectl apply -f kubernetes/doks/secrets.yaml

# Deploy using Helm
echo "Deploying with Helm..."
helm upgrade --install todo-app ./helm/todo-app-prod \
  --namespace "$NAMESPACE" \
  --values ./helm/todo-app-prod/values-production.yaml \
  --set backend.image="$REGISTRY/todo-backend:$VERSION" \
  --set frontend.image="$REGISTRY/todo-frontend:$VERSION" \
  --set eventService.image="$REGISTRY/event-service:$VERSION" \
  --wait \
  --timeout 10m

# Wait for rollout
echo "Waiting for deployments to be ready..."
kubectl rollout status deployment/todo-backend -n "$NAMESPACE" --timeout=5m
kubectl rollout status deployment/todo-frontend -n "$NAMESPACE" --timeout=5m
kubectl rollout status deployment/event-service -n "$NAMESPACE" --timeout=5m

# Get ingress URL
echo ""
echo "✅ Deployment successful!"
echo ""
echo "Getting application URL..."
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [ -n "$INGRESS_IP" ]; then
    echo "Application URL: http://$INGRESS_IP"
    echo "Backend API: http://$INGRESS_IP/api"
    echo "Frontend: http://$INGRESS_IP"
else
    echo "Load balancer IP not yet assigned. Check with:"
    echo "  kubectl get svc ingress-nginx-controller -n ingress-nginx"
fi

echo ""
echo "Check deployment status:"
echo "  kubectl get pods -n $NAMESPACE"
echo "  kubectl get svc -n $NAMESPACE"
echo "  kubectl get ingress -n $NAMESPACE"
```

## Edge Cases and Error Handling

### Cluster Creation Failures

- **Scenario**: DOKS cluster creation fails
- **Handling**: Check DigitalOcean account limits and quotas
- **Recovery**: Delete failed cluster and retry
- **Prevention**: Verify account has sufficient resources

### Node Failures

- **Scenario**: Worker node becomes unhealthy
- **Handling**: Kubernetes reschedules pods to healthy nodes
- **Recovery**: DigitalOcean replaces unhealthy node automatically
- **Monitoring**: Alert on node NotReady status

### Load Balancer Provisioning Delays

- **Scenario**: Load balancer takes time to provision
- **Handling**: Wait for external IP assignment (can take 2-5 minutes)
- **Recovery**: Check DigitalOcean console for load balancer status
- **Verification**: `kubectl get svc -n ingress-nginx -w`

### Image Pull Failures

- **Scenario**: Pods fail to pull images from DOCR
- **Handling**: Verify Docker authentication and image tags
- **Recovery**: Re-authenticate with `doctl registry login`
- **Prevention**: Use imagePullSecrets in deployments

## Testing Strategy

### Infrastructure Tests

- [ ] Verify cluster is created with correct node count
- [ ] Verify autoscaling is enabled
- [ ] Verify kubectl can access cluster
- [ ] Verify container registry is accessible

### Deployment Tests

- [ ] Verify all namespaces are created
- [ ] Verify all pods are running
- [ ] Verify services are created with correct ports
- [ ] Verify ingress is configured correctly
- [ ] Verify load balancer has external IP

### Smoke Tests

- [ ] Access frontend via load balancer IP
- [ ] Access backend API via load balancer IP
- [ ] Create a task via API
- [ ] Verify task appears in frontend
- [ ] Check pod logs for errors

## Monitoring and Metrics

### Cluster Metrics

- Node CPU and memory usage
- Pod count per namespace
- Persistent volume usage
- Network traffic

### Application Metrics

- Pod restart count
- Container CPU and memory usage
- HTTP request rate and latency
- Error rate (4xx, 5xx)

### Alerts

```yaml
- alert: NodeNotReady
  expr: kube_node_status_condition{condition="Ready",status="true"} == 0
  for: 5m

- alert: PodCrashLooping
  expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
  for: 5m

- alert: HighMemoryUsage
  expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
  for: 5m
```

## Performance Requirements

- Cluster provisioning completes within 10 minutes
- Application deployment completes within 5 minutes
- Load balancer provisioning completes within 5 minutes
- All pods start within 2 minutes
- Application responds to requests within 1 second

## Security Considerations

- Use private networking (VPC) for inter-node communication
- Enable RBAC for Kubernetes access control
- Store secrets in Kubernetes Secrets (encrypted at rest)
- Use imagePullSecrets for private registry access
- Enable network policies for pod isolation (optional)
- Regularly update Kubernetes version

## Cost Optimization

- Start with 3 nodes (s-2vcpu-4gb) = ~$72/month
- Enable autoscaling to scale down during low traffic
- Use free tier container registry (up to 500MB)
- Set resource limits to prevent over-provisioning
- Monitor costs in DigitalOcean dashboard
- Destroy cluster when not needed (demo/testing)

## Rollout Plan

1. Provision DOKS cluster (Terraform or doctl)
2. Configure kubectl access
3. Create container registry
4. Build and push Docker images
5. Install ingress-nginx controller
6. Create namespaces
7. Create secrets
8. Deploy application with Helm
9. Verify deployment
10. Test application via load balancer

## Success Metrics

- DOKS cluster running with 3 nodes
- All namespaces created
- All pods running and healthy
- Ingress controller deployed with external IP
- Application accessible via public URL
- All health checks passing
- No pod restarts or errors

## Cleanup Procedure

**File**: `scripts/cleanup-cloud.sh`

```bash
#!/bin/bash
set -e

CLUSTER_NAME="${CLUSTER_NAME:-todo-app-prod}"
REGISTRY_NAME="${REGISTRY_NAME:-todo-app-registry}"

echo "⚠️  WARNING: This will destroy all cloud resources!"
echo "Cluster: $CLUSTER_NAME"
echo "Registry: $REGISTRY_NAME"
echo ""
read -p "Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo "Deleting DOKS cluster..."
doctl kubernetes cluster delete "$CLUSTER_NAME" --force

echo "Deleting container registry..."
doctl registry delete "$REGISTRY_NAME" --force

echo "Cleaning up local kubeconfig..."
kubectl config delete-context "do-$CLUSTER_NAME" || true
kubectl config delete-cluster "do-$CLUSTER_NAME" || true

echo ""
echo "✅ All resources deleted!"
echo "Verify in DigitalOcean console that load balancers are also deleted."
```

## Dependencies

- DigitalOcean account with API token
- doctl CLI or Terraform
- kubectl CLI
- Docker CLI
- Helm CLI

## Future Enhancements

- Multi-region deployment for global availability
- Blue-green deployment strategy
- Canary deployments with traffic splitting
- GitOps with ArgoCD or Flux
- Infrastructure testing with Terratest
- Disaster recovery procedures

---

**Specification Version**: 1.0
**Approved By**: [Pending]
**Implementation Status**: Not Started
