# Troubleshooting Guide - Phase 5

Common issues and their solutions for Phase 5 deployment.

## Table of Contents

1. [Prerequisites Issues](#prerequisites-issues)
2. [Cluster Creation Issues](#cluster-creation-issues)
3. [Pod Issues](#pod-issues)
4. [Dapr Issues](#dapr-issues)
5. [Kafka Issues](#kafka-issues)
6. [Event Flow Issues](#event-flow-issues)
7. [Monitoring Issues](#monitoring-issues)
8. [Networking Issues](#networking-issues)
9. [Performance Issues](#performance-issues)
10. [Cleanup Issues](#cleanup-issues)

---

## Prerequisites Issues

### doctl not authenticated

**Symptoms:**
```
Error: Unable to initialize DigitalOcean API client: access token is required
```

**Solution:**
```bash
doctl auth init
# Enter your API token when prompted

# Verify
doctl account get
```

### kubectl not configured

**Symptoms:**
```
The connection to the server localhost:8080 was refused
```

**Solution:**
```bash
# Configure kubectl for DOKS
doctl kubernetes cluster kubeconfig save todo-app-prod

# Verify
kubectl cluster-info
```

### Docker not authenticated with registry

**Symptoms:**
```
Error response from daemon: pull access denied
```

**Solution:**
```bash
doctl registry login

# Verify
docker info | grep Registry
```

---

## Cluster Creation Issues

### Insufficient quota

**Symptoms:**
```
Error: Unable to create cluster: you have reached your droplet limit
```

**Solution:**
1. Check your DigitalOcean account limits
2. Delete unused resources
3. Request quota increase from DigitalOcean support
4. Use smaller node size: `s-2vcpu-2gb` instead of `s-2vcpu-4gb`

### Cluster creation timeout

**Symptoms:**
```
Error: timeout waiting for cluster to be ready
```

**Solution:**
```bash
# Check cluster status in DigitalOcean console
# Or via CLI:
doctl kubernetes cluster list

# If cluster exists but not ready, wait longer
# If failed, delete and recreate:
doctl kubernetes cluster delete todo-app-prod --force
./scripts/setup-doks.sh
```

### Region not available

**Symptoms:**
```
Error: region not available for Kubernetes
```

**Solution:**
```bash
# List available regions
doctl kubernetes options regions

# Update region in script or Terraform
# Common regions: nyc1, nyc3, sfo3, lon1, fra1
```

---

## Pod Issues

### Pods stuck in "Pending"

**Symptoms:**
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-xxx                0/2     Pending   0          5m
```

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n todo-app-prod
```

**Common causes and solutions:**

1. **Insufficient resources:**
   ```
   Warning: FailedScheduling ... Insufficient cpu/memory
   ```
   **Solution:** Scale up cluster or reduce resource requests
   ```bash
   # Scale cluster
   doctl kubernetes cluster node-pool update <cluster-id> <pool-id> --count 4

   # Or reduce requests in values-production.yaml
   ```

2. **Image pull errors:**
   ```
   Warning: Failed to pull image ... unauthorized
   ```
   **Solution:** Re-authenticate with registry
   ```bash
   doctl registry login
   kubectl delete pod <pod-name> -n todo-app-prod  # Force recreate
   ```

3. **PVC not bound:**
   ```
   Warning: FailedMount ... PersistentVolumeClaim is not bound
   ```
   **Solution:** Check PVC status
   ```bash
   kubectl get pvc -n todo-app-prod
   kubectl describe pvc <pvc-name> -n todo-app-prod
   ```

### Pods in "CrashLoopBackOff"

**Symptoms:**
```
NAME                            READY   STATUS             RESTARTS   AGE
todo-backend-xxx                1/2     CrashLoopBackOff   5          10m
```

**Diagnosis:**
```bash
# Check logs
kubectl logs <pod-name> -n todo-app-prod
kubectl logs <pod-name> -c daprd -n todo-app-prod  # Dapr sidecar

# Check events
kubectl describe pod <pod-name> -n todo-app-prod
```

**Common causes and solutions:**

1. **Application error:**
   - Check logs for error messages
   - Verify environment variables
   - Check database connection

2. **Dapr sidecar not ready:**
   ```bash
   # Check Dapr status
   dapr status -k

   # Check Dapr components
   kubectl get components -n todo-app-prod
   ```

3. **Health check failing:**
   - Increase `initialDelaySeconds` in deployment
   - Check health endpoint manually:
   ```bash
   kubectl port-forward <pod-name> 8000:8000 -n todo-app-prod
   curl http://localhost:8000/health
   ```

### Pods not ready (0/2)

**Symptoms:**
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-xxx                0/2     Running   0          5m
```

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n todo-app-prod
# Look for readiness probe failures
```

**Solution:**
1. Check readiness probe endpoint
2. Increase `initialDelaySeconds` if app takes time to start
3. Check Dapr sidecar is ready:
   ```bash
   kubectl logs <pod-name> -c daprd -n todo-app-prod
   ```

---

## Dapr Issues

### Dapr sidecar not injected

**Symptoms:**
- Pod has only 1 container instead of 2
- No `daprd` container

**Diagnosis:**
```bash
kubectl get pods -n todo-app-prod
kubectl describe pod <pod-name> -n todo-app-prod
```

**Solution:**
1. Verify Dapr is installed:
   ```bash
   dapr status -k
   ```

2. Check deployment annotations:
   ```bash
   kubectl get deployment todo-backend -n todo-app-prod -o yaml | grep dapr.io
   ```

3. Ensure annotations are present:
   ```yaml
   annotations:
     dapr.io/enabled: "true"
     dapr.io/app-id: "todo-backend"
     dapr.io/app-port: "8000"
   ```

4. Restart deployment:
   ```bash
   kubectl rollout restart deployment/todo-backend -n todo-app-prod
   ```

### Dapr component not found

**Symptoms:**
```
Error: component kafka-pubsub not found
```

**Diagnosis:**
```bash
kubectl get components -n todo-app-prod
```

**Solution:**
```bash
# Apply Dapr components
kubectl apply -f dapr/components/

# Verify
kubectl get components -n todo-app-prod
kubectl describe component kafka-pubsub -n todo-app-prod
```

### Dapr pub/sub errors

**Symptoms:**
```
Error publishing event: connection refused
```

**Diagnosis:**
```bash
# Check Dapr component
kubectl get component kafka-pubsub -n todo-app-prod -o yaml

# Check Kafka is running
kubectl get kafka -n kafka

# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd -n todo-app-prod
```

**Solution:**
1. Verify Kafka bootstrap server address in component
2. Check Kafka cluster is ready:
   ```bash
   kubectl get kafka todo-kafka -n kafka
   ```
3. Test connectivity from pod:
   ```bash
   kubectl exec -it <pod-name> -n todo-app-prod -- curl -v telnet://todo-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092
   ```

---

## Kafka Issues

### Kafka cluster not ready

**Symptoms:**
```
NAME         DESIRED KAFKA REPLICAS   DESIRED ZK REPLICAS   READY
todo-kafka   3                        3                     False
```

**Diagnosis:**
```bash
kubectl get kafka -n kafka
kubectl describe kafka todo-kafka -n kafka
kubectl get pods -n kafka
```

**Solution:**
1. Check Strimzi operator logs:
   ```bash
   kubectl logs -n kafka -l name=strimzi-cluster-operator
   ```

2. Check Kafka broker logs:
   ```bash
   kubectl logs -n kafka todo-kafka-kafka-0
   ```

3. Check Zookeeper logs:
   ```bash
   kubectl logs -n kafka todo-kafka-zookeeper-0
   ```

4. Common issues:
   - Insufficient resources: Scale cluster
   - PVC issues: Check storage class
   - Network issues: Check pod networking

### Kafka topics not created

**Symptoms:**
```
Error: topic does not exist
```

**Diagnosis:**
```bash
kubectl get kafkatopics -n kafka
```

**Solution:**
```bash
# Apply topics
kubectl apply -f kafka/topics.yaml

# Verify
kubectl get kafkatopics -n kafka

# Check topic operator logs
kubectl logs -n kafka -l strimzi.io/name=todo-kafka-entity-operator
```

### High consumer lag

**Symptoms:**
- Events not being processed
- Consumer lag increasing

**Diagnosis:**
```bash
# Check consumer group
kubectl exec -n kafka todo-kafka-kafka-0 -- bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group todo-app

# Check event service logs
kubectl logs -l app=event-service -n todo-app-prod
```

**Solution:**
1. Scale event service:
   ```bash
   kubectl scale deployment event-service --replicas=5 -n todo-app-prod
   ```

2. Check for errors in event processing:
   ```bash
   kubectl logs -l app=event-service -n todo-app-prod | grep -i error
   ```

3. Restart event service:
   ```bash
   kubectl rollout restart deployment/event-service -n todo-app-prod
   ```

---

## Event Flow Issues

### Events not being published

**Symptoms:**
- No events in Kafka topics
- Event service not receiving events

**Diagnosis:**
```bash
# Check backend logs
kubectl logs -l app=todo-backend -n todo-app-prod | grep -i event

# Check Dapr pub/sub component
kubectl get component kafka-pubsub -n todo-app-prod -o yaml

# Check Kafka topics
kubectl get kafkatopics -n kafka
```

**Solution:**
1. Verify backend is publishing events:
   ```bash
   # Create a task and check logs
   kubectl logs -l app=todo-backend -n todo-app-prod --tail=50 | grep "Published event"
   ```

2. Check Dapr sidecar logs:
   ```bash
   kubectl logs <backend-pod> -c daprd -n todo-app-prod | grep pubsub
   ```

3. Test Kafka connectivity:
   ```bash
   kubectl exec -n kafka todo-kafka-kafka-0 -- bin/kafka-console-consumer.sh \
     --bootstrap-server localhost:9092 \
     --topic todo.tasks.created \
     --from-beginning
   ```

### Events not being consumed

**Symptoms:**
- Events in Kafka but not processed
- Event service logs show no activity

**Diagnosis:**
```bash
# Check event service logs
kubectl logs -l app=event-service -n todo-app-prod

# Check Dapr subscription
kubectl get subscription -n todo-app-prod

# Check event service /dapr/subscribe endpoint
kubectl port-forward <event-service-pod> 8001:8001 -n todo-app-prod
curl http://localhost:8001/dapr/subscribe
```

**Solution:**
1. Verify Dapr subscription configuration
2. Check event service is registered with Dapr:
   ```bash
   kubectl logs <event-service-pod> -c daprd -n todo-app-prod | grep subscribe
   ```

3. Restart event service:
   ```bash
   kubectl rollout restart deployment/event-service -n todo-app-prod
   ```

---

## Monitoring Issues

### Prometheus not scraping targets

**Symptoms:**
- No metrics in Grafana
- Targets down in Prometheus

**Diagnosis:**
```bash
# Port-forward Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Open http://localhost:9090/targets
# Check which targets are down
```

**Solution:**
1. Check ServiceMonitor:
   ```bash
   kubectl get servicemonitor -n todo-app-prod
   kubectl describe servicemonitor todo-backend -n todo-app-prod
   ```

2. Verify metrics endpoint:
   ```bash
   kubectl port-forward <pod-name> 8000:8000 -n todo-app-prod
   curl http://localhost:8000/metrics
   ```

3. Check pod annotations:
   ```bash
   kubectl get pod <pod-name> -n todo-app-prod -o yaml | grep prometheus
   ```

### Grafana dashboards not loading

**Symptoms:**
- Dashboards show "No data"
- Cannot connect to Prometheus

**Diagnosis:**
```bash
# Check Grafana logs
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana

# Check Prometheus data source in Grafana UI
```

**Solution:**
1. Verify Prometheus is running:
   ```bash
   kubectl get pods -n monitoring | grep prometheus
   ```

2. Check Grafana data source configuration
3. Restart Grafana:
   ```bash
   kubectl rollout restart deployment/prometheus-grafana -n monitoring
   ```

### Jaeger not showing traces

**Symptoms:**
- No traces in Jaeger UI
- Services not appearing

**Diagnosis:**
```bash
# Check Jaeger pods
kubectl get pods -n monitoring | grep jaeger

# Check Dapr tracing configuration
kubectl get configuration -n todo-app-prod -o yaml
```

**Solution:**
1. Verify Dapr tracing is enabled in configuration
2. Check Jaeger collector endpoint:
   ```bash
   kubectl get svc -n monitoring | grep jaeger
   ```

3. Check Dapr sidecar is sending traces:
   ```bash
   kubectl logs <pod-name> -c daprd -n todo-app-prod | grep -i trace
   ```

---

## Networking Issues

### Load balancer IP not assigned

**Symptoms:**
```
EXTERNAL-IP   <pending>
```

**Solution:**
1. Wait 2-5 minutes (DigitalOcean provisioning time)
2. Check load balancer in DigitalOcean console
3. Check ingress controller logs:
   ```bash
   kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
   ```

### Cannot access application

**Symptoms:**
- Load balancer has IP but application not accessible
- Connection timeout or refused

**Diagnosis:**
```bash
# Check ingress
kubectl get ingress -n todo-app-prod
kubectl describe ingress todo-app-ingress -n todo-app-prod

# Check services
kubectl get svc -n todo-app-prod

# Check pods
kubectl get pods -n todo-app-prod
```

**Solution:**
1. Verify ingress rules are correct
2. Check backend service is accessible:
   ```bash
   kubectl port-forward svc/todo-backend 8000:8000 -n todo-app-prod
   curl http://localhost:8000/health
   ```

3. Check ingress controller:
   ```bash
   kubectl get pods -n ingress-nginx
   kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
   ```

### DNS resolution issues

**Symptoms:**
```
Error: could not resolve host
```

**Solution:**
```bash
# Test DNS from pod
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup todo-backend.todo-app-prod.svc.cluster.local

# Check CoreDNS
kubectl get pods -n kube-system | grep coredns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

---

## Performance Issues

### High API latency

**Diagnosis:**
```bash
# Check metrics in Grafana
# Check pod resources
kubectl top pods -n todo-app-prod

# Check node resources
kubectl top nodes
```

**Solution:**
1. Scale up replicas:
   ```bash
   kubectl scale deployment todo-backend --replicas=5 -n todo-app-prod
   ```

2. Increase resource limits in Helm values
3. Check database performance (Neon dashboard)
4. Review traces in Jaeger for bottlenecks

### Pods being OOMKilled

**Symptoms:**
```
NAME                            READY   STATUS      RESTARTS   AGE
todo-backend-xxx                0/2     OOMKilled   3          10m
```

**Solution:**
1. Increase memory limits:
   ```yaml
   # In values-production.yaml
   resources:
     limits:
       memory: 2Gi  # Increase from 1Gi
   ```

2. Check for memory leaks in application
3. Redeploy with new limits:
   ```bash
   ./scripts/deploy-production.sh
   ```

### HPA not scaling

**Diagnosis:**
```bash
kubectl get hpa -n todo-app-prod
kubectl describe hpa todo-backend-hpa -n todo-app-prod
```

**Solution:**
1. Check metrics server:
   ```bash
   kubectl top nodes
   kubectl top pods -n todo-app-prod
   ```

2. Verify resource requests are set in deployment
3. Check HPA conditions:
   ```bash
   kubectl describe hpa todo-backend-hpa -n todo-app-prod
   ```

---

## Cleanup Issues

### Cluster won't delete

**Symptoms:**
```
Error: cluster has attached resources
```

**Solution:**
```bash
# Delete load balancers first
kubectl delete svc --all -n ingress-nginx

# Delete PVCs
kubectl delete pvc --all -n todo-app-prod
kubectl delete pvc --all -n kafka

# Wait a few minutes, then delete cluster
doctl kubernetes cluster delete todo-app-prod --force
```

### Resources still showing in console

**Solution:**
1. Check DigitalOcean console for:
   - Load balancers
   - Volumes
   - Snapshots

2. Delete manually if needed
3. Wait 5-10 minutes for cleanup to complete

---

## Getting More Help

### Collect diagnostic information

```bash
# Create diagnostic bundle
kubectl cluster-info dump --output-directory=./cluster-dump --namespaces todo-app-prod,kafka,monitoring,dapr-system

# Compress
tar -czf cluster-dump.tar.gz cluster-dump/
```

### Useful debugging commands

```bash
# Get all resources
kubectl get all -n todo-app-prod

# Describe everything
kubectl describe all -n todo-app-prod

# Get events
kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'

# Check resource usage
kubectl top nodes
kubectl top pods -n todo-app-prod

# Interactive debugging
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
```

### Contact support

- DigitalOcean Support: https://www.digitalocean.com/support
- Kubernetes Slack: https://kubernetes.slack.com
- Dapr Discord: https://discord.com/invite/ptHhX6jc34
- Strimzi Slack: https://slack.cncf.io (channel: #strimzi)

---

**Last Updated**: 2026-02-07
**Phase**: 5 - Production Cloud Deployment
