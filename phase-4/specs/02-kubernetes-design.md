# Specification: Kubernetes Architecture Design

**Feature ID**: PHASE4-02
**Status**: Draft
**Created**: 2026-02-04
**Dependencies**: Phase 4 Spec 01 (Docker Architecture)

## Purpose

Design a production-ready Kubernetes architecture for deploying the AI-powered todo application on Minikube. Define all Kubernetes resources including Deployments, Services, ConfigMaps, Secrets, StatefulSets, and Ingress to ensure high availability, scalability, and maintainability.

## User Stories

**As a DevOps engineer**, I want to:
1. Deploy the application to Kubernetes with high availability
2. Configure services for internal and external communication
3. Manage configuration and secrets securely
4. Ensure data persistence for the database
5. Implement health checks and auto-healing
6. Enable zero-downtime deployments

**As a developer**, I want to:
1. Access services running in Kubernetes from my local machine
2. Debug issues using Kubernetes logs and events
3. Scale services based on load
4. Roll back deployments if issues occur

## Acceptance Criteria

### AC1: Namespace
- [ ] Dedicated namespace: `todo-app-dev`
- [ ] Resource quotas defined
- [ ] Network policies configured
- [ ] Labels for organization

### AC2: Backend Deployment
- [ ] 2 replicas for high availability
- [ ] Resource requests and limits defined
- [ ] Environment variables from ConfigMap/Secret
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Rolling update strategy
- [ ] Pod anti-affinity for distribution

### AC3: Backend Service
- [ ] ClusterIP type (internal only)
- [ ] Port 8000 exposed
- [ ] Selector matches backend pods
- [ ] Session affinity configured

### AC4: Frontend Deployment
- [ ] 2 replicas for high availability
- [ ] Resource requests and limits
- [ ] Environment variables configured
- [ ] Health probes
- [ ] Rolling update strategy

### AC5: Frontend Service
- [ ] NodePort type for external access
- [ ] Port 3000 exposed
- [ ] Selector matches frontend pods

### AC6: Database StatefulSet
- [ ] 1 replica with stable identity
- [ ] Persistent Volume Claim
- [ ] PostgreSQL 16 image
- [ ] Init container for schema setup
- [ ] Resource limits
- [ ] Health probes

### AC7: Database Service
- [ ] Headless service for StatefulSet
- [ ] ClusterIP (internal only)
- [ ] Port 5432 exposed

### AC8: ConfigMaps
- [ ] Backend configuration
- [ ] Frontend configuration
- [ ] Database configuration
- [ ] No sensitive data

### AC9: Secrets
- [ ] Database credentials (base64 encoded)
- [ ] OpenAI API key
- [ ] Proper RBAC for access

### AC10: Ingress
- [ ] Route traffic to frontend
- [ ] Path-based routing
- [ ] Optional TLS configuration

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster (Minikube)                 │
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
│  │  └──────┬───────┘  └──────────────┘  └─────────────┘ │    │
│  │         │                                              │    │
│  │  ┌──────▼───────┐                                     │    │
│  │  │   Ingress    │                                     │    │
│  │  │  (Optional)  │                                     │    │
│  │  └──────────────┘                                     │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐                  │    │
│  │  │  ConfigMaps  │  │   Secrets    │                  │    │
│  │  └──────────────┘  └──────────────┘                  │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────┐    │    │
│  │  │  Persistent Volume (Database Storage)        │    │    │
│  │  └──────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Namespace Definition

**File**: `kubernetes/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app-dev
  labels:
    name: todo-app-dev
    environment: development
    app: todo-app
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: todo-app-quota
  namespace: todo-app-dev
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    persistentvolumeclaims: "5"
    services.nodeports: "2"
```

### Backend Deployment

**File**: `kubernetes/backend/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: backend
    version: v1
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: todo-app
      component: backend
  template:
    metadata:
      labels:
        app: todo-app
        component: backend
        version: v1
    spec:
      # Anti-affinity to spread pods across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: component
                  operator: In
                  values:
                  - backend
              topologyKey: kubernetes.io/hostname

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      # Init container to wait for database
      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z todo-database 5432; do echo waiting for database; sleep 2; done;']

      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: Never  # Use local image in Minikube

        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        # Environment variables from ConfigMap and Secret
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: openai-api-key
        - name: OPENAI_MODEL
          valueFrom:
            configMapKeyRef:
              name: todo-backend-config
              key: openai-model
        - name: CORS_ORIGINS
          valueFrom:
            configMapKeyRef:
              name: todo-backend-config
              key: cors-origins
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: todo-backend-config
              key: log-level

        # Resource limits
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi

        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe - remove from service if not ready
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # Startup probe - allow slow startup
        startupProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30

        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false  # FastAPI needs write access for temp files
          capabilities:
            drop:
            - ALL
```

### Backend Service

**File**: `kubernetes/backend/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: backend
spec:
  type: ClusterIP
  selector:
    app: todo-app
    component: backend
  ports:
  - name: http
    port: 8000
    targetPort: http
    protocol: TCP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### Backend ConfigMap

**File**: `kubernetes/backend/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-backend-config
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: backend
data:
  openai-model: "gpt-4-turbo-preview"
  cors-origins: "http://localhost:3000,http://todo-frontend:3000"
  log-level: "INFO"
  agent-temperature: "0.7"
  agent-max-tokens: "500"
  agent-max-history: "10"
```

### Backend Secret

**File**: `kubernetes/backend/secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app-dev
  labels:
    app: todo-app
type: Opaque
data:
  # Base64 encoded values
  # database-url: <base64 encoded DATABASE_URL>
  # openai-api-key: <base64 encoded OPENAI_API_KEY>
  #
  # To encode: echo -n "your-value" | base64
  # To decode: echo "encoded-value" | base64 -d

  # Example (replace with actual values):
  database-url: cG9zdGdyZXNxbDovL3RvZG9fdXNlcjp0b2RvX3Bhc3N3b3JkQHRvZG8tZGF0YWJhc2U6NTQzMi90b2RvX2Ri
  openai-api-key: c2stcHJvai15b3VyLWtleS1oZXJl
```

### Frontend Deployment

**File**: `kubernetes/frontend/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: frontend
    version: v1
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: todo-app
      component: frontend
  template:
    metadata:
      labels:
        app: todo-app
        component: frontend
        version: v1
    spec:
      # Anti-affinity
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: component
                  operator: In
                  values:
                  - frontend
              topologyKey: kubernetes.io/hostname

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: Never

        ports:
        - name: http
          containerPort: 3000
          protocol: TCP

        # Environment variables
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: todo-frontend-config
              key: api-url
        - name: NEXT_PUBLIC_CHAT_ENDPOINT
          valueFrom:
            configMapKeyRef:
              name: todo-frontend-config
              key: chat-endpoint
        - name: NODE_ENV
          value: "production"

        # Resource limits
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 400m
            memory: 512Mi

        # Liveness probe
        livenessProbe:
          httpGet:
            path: /
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          httpGet:
            path: /
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # Startup probe
        startupProbe:
          httpGet:
            path: /
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30

        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
          capabilities:
            drop:
            - ALL
```

### Frontend Service

**File**: `kubernetes/frontend/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: frontend
spec:
  type: NodePort
  selector:
    app: todo-app
    component: frontend
  ports:
  - name: http
    port: 3000
    targetPort: http
    nodePort: 30000  # Fixed NodePort for easy access
    protocol: TCP
```

### Frontend ConfigMap

**File**: `kubernetes/frontend/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-frontend-config
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: frontend
data:
  api-url: "http://todo-backend:8000"
  chat-endpoint: "http://todo-backend:8000/api/chat"
```

### Database StatefulSet

**File**: `kubernetes/database/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: todo-database
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: database
spec:
  serviceName: todo-database
  replicas: 1
  selector:
    matchLabels:
      app: todo-app
      component: database
  template:
    metadata:
      labels:
        app: todo-app
        component: database
    spec:
      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 999  # postgres user
        fsGroup: 999

      # Init container to set permissions
      initContainers:
      - name: init-permissions
        image: busybox:1.36
        command: ['sh', '-c', 'chown -R 999:999 /var/lib/postgresql/data']
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        securityContext:
          runAsUser: 0  # Need root to chown

      containers:
      - name: postgres
        image: postgres:16-alpine

        ports:
        - name: postgres
          containerPort: 5432
          protocol: TCP

        # Environment variables
        env:
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              name: todo-database-config
              key: database-name
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata

        # Resource limits
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi

        # Liveness probe
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # Volume mount
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data

        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL

  # Volume claim template
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
```

### Database Service

**File**: `kubernetes/database/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-database
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: database
spec:
  type: ClusterIP
  clusterIP: None  # Headless service for StatefulSet
  selector:
    app: todo-app
    component: database
  ports:
  - name: postgres
    port: 5432
    targetPort: postgres
    protocol: TCP
```

### Database ConfigMap

**File**: `kubernetes/database/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-database-config
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: database
data:
  database-name: "todo_db"
```

### Database Secret

**File**: `kubernetes/database/secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-database-secret
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: database
type: Opaque
data:
  # Base64 encoded values
  # To encode: echo -n "your-value" | base64
  database-user: dG9kb191c2Vy  # todo_user
  database-password: dG9kb19wYXNzd29yZA==  # todo_password
```

### Persistent Volume Claim

**File**: `kubernetes/database/pvc.yaml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: todo-app-dev
  labels:
    app: todo-app
    component: database
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard  # Minikube default storage class
```

### Ingress

**File**: `kubernetes/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app-dev
  labels:
    app: todo-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: todo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 8000
```

## Deployment Order

1. **Namespace**: Create namespace first
2. **ConfigMaps & Secrets**: Create configuration
3. **Database**: Deploy StatefulSet and Service
4. **Backend**: Deploy Deployment and Service
5. **Frontend**: Deploy Deployment and Service
6. **Ingress**: Configure routing (optional)

## Resource Requirements

### Total Cluster Resources

| Component | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|----------|-------------|-----------|----------------|--------------|
| Frontend  | 2        | 200m        | 400m      | 256Mi          | 512Mi        |
| Backend   | 2        | 250m        | 500m      | 256Mi          | 512Mi        |
| Database  | 1        | 250m        | 500m      | 256Mi          | 512Mi        |
| **Total** | **5**    | **1150m**   | **2300m** | **1280Mi**     | **2560Mi**   |

**Minikube Requirements**: 4GB RAM, 2 CPUs minimum

## Health Check Strategy

### Liveness Probe
- **Purpose**: Detect if container is alive
- **Action**: Restart container if fails
- **Configuration**: HTTP GET to `/health` endpoint

### Readiness Probe
- **Purpose**: Detect if container can serve traffic
- **Action**: Remove from service if fails
- **Configuration**: HTTP GET to `/health` endpoint

### Startup Probe
- **Purpose**: Allow slow-starting containers time to initialize
- **Action**: Delay liveness/readiness checks
- **Configuration**: HTTP GET to `/health` endpoint

## Scaling Strategy

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment todo-backend -n todo-app-dev --replicas=3

# Scale frontend
kubectl scale deployment todo-frontend -n todo-app-dev --replicas=3
```

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: todo-app-dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Security Considerations

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app-dev
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: todo-app-dev
spec:
  podSelector:
    matchLabels:
      component: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          component: frontend
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          component: database
    ports:
    - protocol: TCP
      port: 5432
```

## Monitoring and Observability

### Metrics Server

```bash
# Enable metrics-server in Minikube
minikube addons enable metrics-server

# View resource usage
kubectl top nodes
kubectl top pods -n todo-app-dev
```

### Logging

```bash
# View logs
kubectl logs -f deployment/todo-backend -n todo-app-dev
kubectl logs -f deployment/todo-frontend -n todo-app-dev
kubectl logs -f statefulset/todo-database -n todo-app-dev

# View logs from all replicas
kubectl logs -l component=backend -n todo-app-dev --all-containers=true
```

## Troubleshooting

### Common Issues

**Issue**: Pods stuck in Pending state
```bash
# Check events
kubectl describe pod <pod-name> -n todo-app-dev

# Check resource availability
kubectl top nodes
```

**Issue**: Pods crashing (CrashLoopBackOff)
```bash
# Check logs
kubectl logs <pod-name> -n todo-app-dev --previous

# Check events
kubectl get events -n todo-app-dev --sort-by='.lastTimestamp'
```

**Issue**: Service not accessible
```bash
# Check service endpoints
kubectl get endpoints -n todo-app-dev

# Test service connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -n todo-app-dev -- wget -O- http://todo-backend:8000/health
```

## Testing Strategy

### Deployment Testing

```bash
# Apply all manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/backend/
kubectl apply -f kubernetes/frontend/
kubectl apply -f kubernetes/database/

# Wait for rollout
kubectl rollout status deployment/todo-backend -n todo-app-dev
kubectl rollout status deployment/todo-frontend -n todo-app-dev
kubectl rollout status statefulset/todo-database -n todo-app-dev

# Check pod status
kubectl get pods -n todo-app-dev

# Test services
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app-dev
curl http://localhost:3000
```

## Success Metrics

- All pods running and ready
- Health checks passing
- Services accessible
- Database data persists across pod restarts
- Zero-downtime rolling updates
- Resource usage within limits
- Logs accessible and structured

## Future Enhancements (Out of Scope for Phase 4)

- Service Mesh (Istio/Linkerd)
- Advanced monitoring (Prometheus/Grafana)
- Distributed tracing (Jaeger)
- GitOps (ArgoCD/Flux)
- Multi-cluster deployment
- Blue-green deployments
- Canary deployments

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: High
**Implementation Order**: 2 of 5 (implement after Docker)
