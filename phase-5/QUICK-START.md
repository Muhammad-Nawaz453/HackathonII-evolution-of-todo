# Quick Start Guide - Phase 5

Get your Todo app running on DOKS in under 1 hour!

## Prerequisites (5 minutes)

1. **Install required tools:**
   ```bash
   # macOS
   brew install doctl kubectl helm docker

   # Linux
   # Follow installation guides for each tool

   # Windows
   # Use Chocolatey or download installers
   ```

2. **Authenticate with DigitalOcean:**
   ```bash
   doctl auth init
   # Enter your API token when prompted
   ```

3. **Verify setup:**
   ```bash
   cd phase-5
   ./scripts/verify-setup.sh
   ```

## Deployment (30-45 minutes)

### Step 1: Create Infrastructure (15-20 minutes)

```bash
# Create DOKS cluster
./scripts/setup-doks.sh
# ⏱️ Takes 5-10 minutes

# Install Kafka
./scripts/install-kafka.sh
# ⏱️ Takes 5-10 minutes

# Install Dapr
./scripts/install-dapr.sh
# ⏱️ Takes 2-3 minutes

# Setup monitoring
./scripts/setup-monitoring.sh
# ⏱️ Takes 3-5 minutes
```

**☕ Take a coffee break while infrastructure provisions!**

### Step 2: Build Images (10-15 minutes)

```bash
# Authenticate Docker
doctl registry login

# Build and push backend
cd ../phase-3/backend
docker build -t registry.digitalocean.com/todo-app-registry/todo-backend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-backend:latest

# Build and push frontend
cd ../frontend
docker build -t registry.digitalocean.com/todo-app-registry/todo-frontend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-frontend:latest

# Build and push event service
cd ../../phase-5/backend-event-service
docker build -t registry.digitalocean.com/todo-app-registry/event-service:latest .
docker push registry.digitalocean.com/todo-app-registry/event-service:latest

cd ..
```

### Step 3: Configure Secrets (2 minutes)

```bash
# Copy secrets template
cp kubernetes/doks/secrets.yaml.example kubernetes/doks/secrets.yaml

# Edit with your values
nano kubernetes/doks/secrets.yaml
```

**Required values:**
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key (starts with `sk-`)
- `REDIS_PASSWORD`: Choose a strong password

**Example:**
```yaml
stringData:
  url: "postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
  api-key: "sk-proj-xxxxxxxxxxxxx"
  password: "MyStr0ngP@ssw0rd!"
```

### Step 4: Deploy Application (5-10 minutes)

```bash
./scripts/deploy-production.sh
# ⏱️ Takes 5-10 minutes
```

**What happens:**
- Creates namespaces
- Deploys Redis
- Deploys backend (3 replicas)
- Deploys frontend (3 replicas)
- Deploys event service (2 replicas)
- Configures ingress
- Provisions load balancer

### Step 5: Access Your App (1 minute)

```bash
# Get load balancer IP
kubectl get svc ingress-nginx-controller -n ingress-nginx

# Wait for EXTERNAL-IP to appear (may take 2-5 minutes)
```

**Access your application:**
- Frontend: `http://<EXTERNAL-IP>`
- Backend API: `http://<EXTERNAL-IP>/api`
- Health check: `http://<EXTERNAL-IP>/api/health`

## Verification (5 minutes)

### Check Everything is Running

```bash
# Check pods
kubectl get pods -n todo-app-prod
# All should be "Running"

# Check services
kubectl get svc -n todo-app-prod

# Check HPA
kubectl get hpa -n todo-app-prod
```

### Test Event Flow

1. **Create a task** via the frontend or API:
   ```bash
   curl -X POST http://<EXTERNAL-IP>/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Test task","description":"Testing events"}'
   ```

2. **Check backend logs** for event publishing:
   ```bash
   kubectl logs -l app=todo-backend -n todo-app-prod | grep "Published event"
   ```

3. **Check event service logs** for consumption:
   ```bash
   kubectl logs -l app=event-service -n todo-app-prod | grep "Received"
   ```

### Access Monitoring

```bash
# Grafana (dashboards)
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000 (admin/admin)

# Jaeger (traces)
kubectl port-forward -n monitoring svc/jaeger-query 16686:16686
# Open: http://localhost:16686
```

## Common Issues & Solutions

### Issue: Pods stuck in "Pending"
**Solution:** Check node resources
```bash
kubectl describe pod <pod-name> -n todo-app-prod
kubectl get nodes
```

### Issue: Image pull errors
**Solution:** Re-authenticate with registry
```bash
doctl registry login
```

### Issue: Load balancer IP not assigned
**Solution:** Wait 2-5 minutes, then check again
```bash
kubectl get svc ingress-nginx-controller -n ingress-nginx -w
```

### Issue: Events not flowing
**Solution:** Check Kafka and Dapr
```bash
kubectl get kafka -n kafka
kubectl get components -n todo-app-prod
kubectl logs -l app=event-service -n todo-app-prod
```

## Next Steps

### Explore Your Deployment

1. **View metrics in Grafana:**
   - API request rate
   - Latency (p50, p95, p99)
   - Error rate
   - Task operations
   - Kafka consumer lag

2. **View traces in Jaeger:**
   - Search for traces
   - See end-to-end request flow
   - Identify performance bottlenecks

3. **Test autoscaling:**
   ```bash
   # Generate load
   kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
   # Inside pod:
   while true; do wget -q -O- http://todo-backend.todo-app-prod.svc.cluster.local:8000/api/tasks; done

   # Watch HPA scale up
   kubectl get hpa -n todo-app-prod -w
   ```

### Customize Your Deployment

1. **Adjust autoscaling:**
   - Edit `helm/todo-app-prod/values-production.yaml`
   - Change `minReplicas`, `maxReplicas`, `targetCPU`
   - Redeploy: `./scripts/deploy-production.sh`

2. **Add custom metrics:**
   - Modify backend to expose new metrics
   - Update Grafana dashboards

3. **Configure alerts:**
   - Edit `kubernetes/monitoring/prometheus-rules.yaml`
   - Add Slack/Discord notifications

## Cleanup (IMPORTANT!)

**⚠️ Don't forget to cleanup to avoid charges!**

```bash
./scripts/cleanup-cloud.sh
```

This will delete:
- DOKS cluster
- Container registry
- Load balancer
- All volumes

**Verify in DigitalOcean console that everything is deleted!**

## Cost Reminder

**Monthly costs if left running:**
- DOKS Cluster (3 nodes): ~$72/month
- Load Balancer: ~$12/month
- **Total**: ~$84/month

**Always cleanup after demos and testing!**

## Troubleshooting Commands

```bash
# View all resources
kubectl get all -n todo-app-prod

# Describe a pod
kubectl describe pod <pod-name> -n todo-app-prod

# View logs
kubectl logs <pod-name> -n todo-app-prod
kubectl logs <pod-name> -c daprd -n todo-app-prod  # Dapr sidecar

# View events
kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'

# Check Kafka
kubectl get kafka -n kafka
kubectl get kafkatopics -n kafka

# Check Dapr
dapr status -k
kubectl get components -n todo-app-prod

# Restart a deployment
kubectl rollout restart deployment/todo-backend -n todo-app-prod
```

## Getting Help

1. **Check documentation:**
   - `README.md` - Comprehensive guide
   - `DEPLOYMENT-CHECKLIST.md` - Step-by-step checklist
   - `CLAUDE.md` - Development guidelines
   - `specs/` - Detailed specifications

2. **Review logs:**
   ```bash
   kubectl logs -l app=todo-backend -n todo-app-prod --tail=100
   ```

3. **Check pod status:**
   ```bash
   kubectl get pods -n todo-app-prod
   kubectl describe pod <pod-name> -n todo-app-prod
   ```

## Success Checklist

- [ ] All pods running
- [ ] Application accessible via load balancer
- [ ] Tasks can be created/updated/deleted
- [ ] Events flowing through Kafka
- [ ] Traces visible in Jaeger
- [ ] Metrics in Grafana
- [ ] Autoscaling configured
- [ ] No errors in logs

## Congratulations! 🎉

You've successfully deployed a production-grade, event-driven application on Kubernetes!

**What you've built:**
- Cloud-native application on DOKS
- Event streaming with Kafka
- Service mesh with Dapr
- Comprehensive monitoring
- Horizontal autoscaling
- CI/CD ready

**Next:** Take screenshots, document your learnings, and don't forget to cleanup!

---

**Deployment Time**: 40-65 minutes
**Difficulty**: Intermediate
**Cost**: ~$84/month (cleanup after demo!)
