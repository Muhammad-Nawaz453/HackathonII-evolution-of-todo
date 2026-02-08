# Phase 5 Deployment Checklist

Use this checklist to deploy the Todo application to production on DOKS.

## Prerequisites ✓

- [ ] DigitalOcean account created
- [ ] DigitalOcean API token generated
- [ ] `doctl` CLI installed and authenticated
- [ ] `kubectl` CLI installed
- [ ] `helm` CLI installed (v3.x)
- [ ] `docker` CLI installed
- [ ] Git repository cloned

## Phase 1: Infrastructure Setup

### 1.1 Verify Prerequisites
```bash
cd phase-5
./scripts/verify-setup.sh
```
- [ ] All required tools installed
- [ ] DigitalOcean authentication working

### 1.2 Create DOKS Cluster
```bash
./scripts/setup-doks.sh
```
- [ ] DOKS cluster created (3 nodes)
- [ ] Autoscaling enabled (2-5 nodes)
- [ ] Container registry created
- [ ] kubectl configured
- [ ] Cluster accessible

**Expected time**: 5-10 minutes

### 1.3 Install Kafka
```bash
./scripts/install-kafka.sh
```
- [ ] Strimzi operator installed
- [ ] Kafka cluster deployed (3 brokers)
- [ ] Zookeeper ensemble deployed (3 nodes)
- [ ] Kafka topics created (4 topics)
- [ ] Kafka cluster ready

**Expected time**: 5-10 minutes

### 1.4 Install Dapr
```bash
./scripts/install-dapr.sh
```
- [ ] Dapr control plane installed
- [ ] Dapr operator running
- [ ] Dapr sidecar injector running
- [ ] Dapr dashboard accessible

**Expected time**: 2-3 minutes

### 1.5 Setup Monitoring
```bash
./scripts/setup-monitoring.sh
```
- [ ] Prometheus installed
- [ ] Grafana installed
- [ ] Jaeger installed
- [ ] Alert rules configured
- [ ] Dashboards created

**Expected time**: 3-5 minutes

## Phase 2: Application Deployment

### 2.1 Build Docker Images

**Backend:**
```bash
cd ../phase-3/backend
docker build -t registry.digitalocean.com/todo-app-registry/todo-backend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-backend:latest
```
- [ ] Backend image built
- [ ] Backend image pushed to DOCR

**Frontend:**
```bash
cd ../frontend
docker build -t registry.digitalocean.com/todo-app-registry/todo-frontend:latest .
docker push registry.digitalocean.com/todo-app-registry/todo-frontend:latest
```
- [ ] Frontend image built
- [ ] Frontend image pushed to DOCR

**Event Service:**
```bash
cd ../../phase-5/backend-event-service
docker build -t registry.digitalocean.com/todo-app-registry/event-service:latest .
docker push registry.digitalocean.com/todo-app-registry/event-service:latest
```
- [ ] Event service image built
- [ ] Event service image pushed to DOCR

**Expected time**: 5-10 minutes (depending on internet speed)

### 2.2 Configure Secrets

```bash
cd ../
cp kubernetes/doks/secrets.yaml.example kubernetes/doks/secrets.yaml
nano kubernetes/doks/secrets.yaml
```

Update with real values:
- [ ] Database URL (Neon PostgreSQL connection string)
- [ ] OpenAI API key
- [ ] Redis password

**⚠️ IMPORTANT**: Never commit `secrets.yaml` to git!

### 2.3 Deploy Application

```bash
./scripts/deploy-production.sh
```

- [ ] Namespaces created
- [ ] Secrets applied
- [ ] Dapr components deployed
- [ ] Redis deployed
- [ ] Backend deployed (3 replicas)
- [ ] Frontend deployed (3 replicas)
- [ ] Event service deployed (2 replicas)
- [ ] Ingress controller installed
- [ ] Load balancer provisioned
- [ ] All pods running

**Expected time**: 5-10 minutes

### 2.4 Verify Deployment

```bash
# Check pods
kubectl get pods -n todo-app-prod

# Check services
kubectl get svc -n todo-app-prod

# Check ingress
kubectl get ingress -n todo-app-prod

# Get load balancer IP
kubectl get svc ingress-nginx-controller -n ingress-nginx
```

- [ ] All pods in Running state
- [ ] All services created
- [ ] Ingress configured
- [ ] Load balancer has external IP

## Phase 3: Verification

### 3.1 Access Application

```bash
# Get load balancer IP
LOAD_BALANCER_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Application URL: http://$LOAD_BALANCER_IP"
```

- [ ] Frontend accessible at `http://<LOAD_BALANCER_IP>`
- [ ] Backend API accessible at `http://<LOAD_BALANCER_IP>/api`
- [ ] Health endpoint responds: `http://<LOAD_BALANCER_IP>/api/health`

### 3.2 Test Event Flow

1. Create a task via frontend or API
2. Check backend logs for event publishing:
   ```bash
   kubectl logs -l app=todo-backend -n todo-app-prod | grep "Published event"
   ```
3. Check event service logs for event consumption:
   ```bash
   kubectl logs -l app=event-service -n todo-app-prod | grep "Received"
   ```

- [ ] Tasks can be created
- [ ] Events are published to Kafka
- [ ] Events are consumed by event service
- [ ] No errors in logs

### 3.3 Verify Monitoring

**Grafana:**
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000 (admin/admin)
```
- [ ] Grafana accessible
- [ ] Prometheus data source connected
- [ ] Todo App dashboard visible
- [ ] Metrics displaying

**Prometheus:**
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090
```
- [ ] Prometheus accessible
- [ ] All targets up and healthy
- [ ] Metrics being scraped

**Jaeger:**
```bash
kubectl port-forward -n monitoring svc/jaeger-query 16686:16686
# Open: http://localhost:16686
```
- [ ] Jaeger accessible
- [ ] Traces visible
- [ ] End-to-end traces showing (backend → Kafka → event service)

### 3.4 Test Autoscaling

```bash
# Check HPA status
kubectl get hpa -n todo-app-prod

# Generate load (optional)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
# Inside pod: while true; do wget -q -O- http://todo-backend.todo-app-prod.svc.cluster.local:8000/api/tasks; done

# Watch HPA scale up
kubectl get hpa -n todo-app-prod -w
```

- [ ] HPA configured for all services
- [ ] HPA responds to load (optional test)
- [ ] Pods scale up under load (optional test)
- [ ] Pods scale down after load decreases (optional test)

## Phase 4: CI/CD Setup (Optional)

### 4.1 Configure GitHub Actions

1. Add secrets to GitHub repository:
   - `DIGITALOCEAN_ACCESS_TOKEN`: Your DO API token

2. Copy workflows to repository root:
   ```bash
   cp -r ci-cd/.github ../../.github
   ```

3. Push to trigger pipeline:
   ```bash
   git add .
   git commit -m "Add Phase 5 deployment"
   git push origin main
   ```

- [ ] GitHub secrets configured
- [ ] Workflows copied to repository
- [ ] Build workflow runs successfully
- [ ] Deploy workflow runs successfully

## Phase 5: Documentation

- [ ] Review README.md for usage instructions
- [ ] Review CLAUDE.md for development guidelines
- [ ] Review specifications in specs/ directory
- [ ] Document any custom configurations
- [ ] Take screenshots of:
  - Application running
  - Grafana dashboards
  - Jaeger traces
  - Kubernetes dashboard

## Phase 6: Cleanup (After Demo)

**⚠️ IMPORTANT**: Run cleanup to avoid ongoing charges!

```bash
./scripts/cleanup-cloud.sh
```

- [ ] DOKS cluster deleted
- [ ] Container registry deleted (optional)
- [ ] Load balancer deleted
- [ ] Volumes deleted
- [ ] Verified in DigitalOcean console

## Troubleshooting

### Pods Not Starting
```bash
kubectl describe pod <pod-name> -n todo-app-prod
kubectl logs <pod-name> -n todo-app-prod
```

### Dapr Issues
```bash
dapr status -k
kubectl logs -n dapr-system -l app=dapr-operator
kubectl get components -n todo-app-prod
```

### Kafka Issues
```bash
kubectl get kafka -n kafka
kubectl get kafkatopics -n kafka
kubectl logs -n kafka todo-kafka-kafka-0
```

### Events Not Flowing
```bash
kubectl logs -l app=todo-backend -n todo-app-prod | grep -i event
kubectl logs -l app=event-service -n todo-app-prod
kubectl get component kafka-pubsub -n todo-app-prod -o yaml
```

## Success Criteria

Phase 5 is complete when ALL of the following are true:

- ✅ DOKS cluster running with 3 nodes
- ✅ Kafka cluster operational (3 brokers, 3 Zookeeper nodes)
- ✅ Dapr sidecars injected into backend and event service
- ✅ Application accessible via public load balancer IP
- ✅ Tasks can be created, updated, and deleted
- ✅ Events published to Kafka for all task operations
- ✅ Event service consuming and processing events
- ✅ Distributed traces visible in Jaeger
- ✅ Metrics displayed in Grafana dashboards
- ✅ Prometheus scraping all targets
- ✅ HPA configured and functional
- ✅ All pods healthy and running
- ✅ No errors in application logs

## Estimated Total Time

- Infrastructure setup: 15-25 minutes
- Application deployment: 15-25 minutes
- Verification: 10-15 minutes
- **Total**: 40-65 minutes

## Cost Reminder

**Monthly costs**: ~$84/month
- DOKS Cluster (3 nodes): ~$72/month
- Load Balancer: ~$12/month
- Container Registry: Free (up to 500MB)

**Remember to run cleanup script after demo!**

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs: `kubectl logs <pod-name> -n todo-app-prod`
3. Check events: `kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'`
4. Review specifications in `specs/` directory
5. Consult CLAUDE.md for development guidelines

---

**Last Updated**: 2026-02-07
**Phase**: 5 - Production Cloud Deployment
**Status**: Ready for Deployment
