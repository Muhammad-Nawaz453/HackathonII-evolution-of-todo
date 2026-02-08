# Specification: Helm Charts for Package Management

**Feature ID**: PHASE4-03
**Status**: Draft
**Created**: 2026-02-04
**Dependencies**: Phase 4 Spec 02 (Kubernetes Design)

## Purpose

Create a comprehensive Helm chart for the AI-powered todo application that enables declarative, version-controlled, and repeatable deployments to Kubernetes. The Helm chart will template all Kubernetes resources and provide flexible configuration through values files for different environments (development, staging, production).

## User Stories

**As a DevOps engineer**, I want to:
1. Deploy the entire application with a single Helm command
2. Manage different configurations for dev/staging/prod environments
3. Upgrade deployments without downtime
4. Roll back to previous versions easily
5. Version control infrastructure changes
6. Share deployment packages with team members

**As a developer**, I want to:
1. Override default configurations for local testing
2. Understand what will be deployed before applying changes
3. Test Helm charts with dry-run mode
4. Debug deployment issues using Helm tools

## Acceptance Criteria

### AC1: Chart Structure
- [ ] Chart.yaml with metadata
- [ ] values.yaml with default values
- [ ] values-dev.yaml for development overrides
- [ ] values-prod.yaml for production overrides
- [ ] templates/ directory with all K8s resources
- [ ] helpers.tpl with reusable template functions
- [ ] NOTES.txt with post-installation instructions

### AC2: Chart Metadata
- [ ] Name: todo-app
- [ ] Version: 1.0.0 (chart version)
- [ ] AppVersion: 1.0.0 (application version)
- [ ] Description: AI-Powered Todo Application
- [ ] Keywords and maintainers defined
- [ ] Dependencies declared (if any)

### AC3: Templated Resources
- [ ] All Deployments templated
- [ ] All Services templated
- [ ] All ConfigMaps templated
- [ ] All Secrets templated
- [ ] StatefulSet templated
- [ ] Ingress templated
- [ ] Use {{ .Values.* }} for configuration
- [ ] Use {{ include "todo-app.labels" . }} for labels

### AC4: Values Configuration
- [ ] Image tags configurable
- [ ] Replica counts configurable
- [ ] Resource limits configurable
- [ ] Environment variables configurable
- [ ] Service types configurable
- [ ] Ingress configuration
- [ ] Storage configuration

### AC5: Helper Templates
- [ ] Common labels helper
- [ ] Selector labels helper
- [ ] Chart name helper
- [ ] Full name helper
- [ ] Service account name helper

### AC6: Environment-Specific Values
- [ ] values-dev.yaml: Lower resources, debug logging
- [ ] values-prod.yaml: Higher resources, production settings
- [ ] Easy to switch between environments

### AC7: Installation & Upgrade
- [ ] `helm install` works successfully
- [ ] `helm upgrade` works without downtime
- [ ] `helm rollback` works correctly
- [ ] `helm uninstall` cleans up resources

### AC8: Validation
- [ ] `helm lint` passes
- [ ] `helm template` generates valid YAML
- [ ] `helm install --dry-run` succeeds
- [ ] All required values validated

## Technical Design

### Chart Structure

```
helm/todo-app/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default values
├── values-dev.yaml            # Development overrides
├── values-prod.yaml           # Production overrides
├── templates/
│   ├── NOTES.txt              # Post-install instructions
│   ├── _helpers.tpl           # Template helpers
│   ├── namespace.yaml         # Namespace definition
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── backend-configmap.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── frontend-configmap.yaml
│   ├── database-statefulset.yaml
│   ├── database-service.yaml
│   ├── database-configmap.yaml
│   ├── secrets.yaml
│   ├── pvc.yaml
│   └── ingress.yaml
└── .helmignore                # Files to ignore
```

### Chart.yaml

**File**: `helm/todo-app/Chart.yaml`

```yaml
apiVersion: v2
name: todo-app
description: AI-Powered Todo Application with OpenAI ChatKit and Agents SDK
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - ai
  - chatbot
  - openai
  - kubernetes
maintainers:
  - name: Todo App Team
    email: team@todo-app.com
home: https://github.com/your-org/todo-app
sources:
  - https://github.com/your-org/todo-app
icon: https://todo-app.com/icon.png
```

### values.yaml (Default Values)

**File**: `helm/todo-app/values.yaml`

```yaml
# Default values for todo-app
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# Global settings
global:
  namespace: todo-app-dev
  environment: development

# Backend configuration
backend:
  enabled: true
  replicaCount: 2

  image:
    repository: todo-backend
    tag: latest
    pullPolicy: Never  # Use local images in Minikube

  service:
    type: ClusterIP
    port: 8000

  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 70

  config:
    openaiModel: "gpt-4-turbo-preview"
    corsOrigins: "http://localhost:3000,http://todo-frontend:3000"
    logLevel: "INFO"
    agentTemperature: "0.7"
    agentMaxTokens: "500"
    agentMaxHistory: "10"

  secrets:
    # These should be provided via --set or external secret management
    databaseUrl: ""
    openaiApiKey: ""

  probes:
    liveness:
      enabled: true
      path: /health
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    readiness:
      enabled: true
      path: /health
      initialDelaySeconds: 10
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    startup:
      enabled: true
      path: /health
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 30

# Frontend configuration
frontend:
  enabled: true
  replicaCount: 2

  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never

  service:
    type: NodePort
    port: 3000
    nodePort: 30000

  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 400m
      memory: 512Mi

  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 70

  config:
    apiUrl: "http://todo-backend:8000"
    chatEndpoint: "http://todo-backend:8000/api/chat"

  probes:
    liveness:
      enabled: true
      path: /
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    readiness:
      enabled: true
      path: /
      initialDelaySeconds: 10
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    startup:
      enabled: true
      path: /
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 30

# Database configuration
database:
  enabled: true

  image:
    repository: postgres
    tag: "16-alpine"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 5432

  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

  persistence:
    enabled: true
    storageClass: "standard"
    accessMode: ReadWriteOnce
    size: 5Gi

  config:
    databaseName: "todo_db"

  secrets:
    # These should be provided via --set or external secret management
    username: "todo_user"
    password: "todo_password"

  probes:
    liveness:
      enabled: true
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    readiness:
      enabled: true
      initialDelaySeconds: 10
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
  tls: []
    # - secretName: todo-tls
    #   hosts:
    #     - todo.local

# Security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL

# Pod disruption budget
podDisruptionBudget:
  enabled: false
  minAvailable: 1

# Network policy
networkPolicy:
  enabled: false

# Service account
serviceAccount:
  create: true
  annotations: {}
  name: ""

# Resource quotas
resourceQuota:
  enabled: true
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    persistentvolumeclaims: "5"
```

### values-dev.yaml (Development Overrides)

**File**: `helm/todo-app/values-dev.yaml`

```yaml
# Development environment overrides

global:
  environment: development

backend:
  replicaCount: 1  # Single replica for dev

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

  config:
    logLevel: "DEBUG"

  autoscaling:
    enabled: false

frontend:
  replicaCount: 1

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

  autoscaling:
    enabled: false

database:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

  persistence:
    size: 2Gi  # Smaller storage for dev

ingress:
  enabled: false

podDisruptionBudget:
  enabled: false

resourceQuota:
  enabled: false
```

### values-prod.yaml (Production Overrides)

**File**: `helm/todo-app/values-prod.yaml`

```yaml
# Production environment overrides

global:
  environment: production

backend:
  replicaCount: 3  # More replicas for prod

  image:
    pullPolicy: IfNotPresent

  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

  config:
    logLevel: "WARNING"

  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

frontend:
  replicaCount: 3

  image:
    pullPolicy: IfNotPresent

  service:
    type: LoadBalancer  # Use LoadBalancer in prod

  resources:
    requests:
      cpu: 400m
      memory: 512Mi
    limits:
      cpu: 800m
      memory: 1Gi

  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

database:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

  persistence:
    size: 20Gi  # Larger storage for prod

ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com

podDisruptionBudget:
  enabled: true
  minAvailable: 1

networkPolicy:
  enabled: true
```

### Helper Templates

**File**: `helm/todo-app/templates/_helpers.tpl`

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
environment: {{ .Values.global.environment }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-app.backend.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-app.frontend.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Database labels
*/}}
{{- define "todo-app.database.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: database
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "todo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "todo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Backend full name
*/}}
{{- define "todo-app.backend.fullname" -}}
{{- printf "%s-backend" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend full name
*/}}
{{- define "todo-app.frontend.fullname" -}}
{{- printf "%s-frontend" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Database full name
*/}}
{{- define "todo-app.database.fullname" -}}
{{- printf "%s-database" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### Example Templated Deployment

**File**: `helm/todo-app/templates/backend-deployment.yaml`

```yaml
{{- if .Values.backend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.backend.fullname" . }}
  namespace: {{ .Values.global.namespace }}
  labels:
    {{- include "todo-app.backend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:
        {{- include "todo-app.backend.labels" . | nindent 8 }}
    spec:
      {{- with .Values.securityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}

      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z {{ include "todo-app.database.fullname" . }} {{ .Values.database.service.port }}; do echo waiting for database; sleep 2; done;']

      containers:
      - name: backend
        image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
        imagePullPolicy: {{ .Values.backend.image.pullPolicy }}

        ports:
        - name: http
          containerPort: {{ .Values.backend.service.port }}
          protocol: TCP

        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: openai-api-key
        - name: OPENAI_MODEL
          value: {{ .Values.backend.config.openaiModel | quote }}
        - name: CORS_ORIGINS
          value: {{ .Values.backend.config.corsOrigins | quote }}
        - name: LOG_LEVEL
          value: {{ .Values.backend.config.logLevel | quote }}

        resources:
          {{- toYaml .Values.backend.resources | nindent 10 }}

        {{- if .Values.backend.probes.liveness.enabled }}
        livenessProbe:
          httpGet:
            path: {{ .Values.backend.probes.liveness.path }}
            port: http
          initialDelaySeconds: {{ .Values.backend.probes.liveness.initialDelaySeconds }}
          periodSeconds: {{ .Values.backend.probes.liveness.periodSeconds }}
          timeoutSeconds: {{ .Values.backend.probes.liveness.timeoutSeconds }}
          failureThreshold: {{ .Values.backend.probes.liveness.failureThreshold }}
        {{- end }}

        {{- if .Values.backend.probes.readiness.enabled }}
        readinessProbe:
          httpGet:
            path: {{ .Values.backend.probes.readiness.path }}
            port: http
          initialDelaySeconds: {{ .Values.backend.probes.readiness.initialDelaySeconds }}
          periodSeconds: {{ .Values.backend.probes.readiness.periodSeconds }}
          timeoutSeconds: {{ .Values.backend.probes.readiness.timeoutSeconds }}
          failureThreshold: {{ .Values.backend.probes.readiness.failureThreshold }}
        {{- end }}

        {{- if .Values.backend.probes.startup.enabled }}
        startupProbe:
          httpGet:
            path: {{ .Values.backend.probes.startup.path }}
            port: http
          initialDelaySeconds: {{ .Values.backend.probes.startup.initialDelaySeconds }}
          periodSeconds: {{ .Values.backend.probes.startup.periodSeconds }}
          timeoutSeconds: {{ .Values.backend.probes.startup.timeoutSeconds }}
          failureThreshold: {{ .Values.backend.probes.startup.failureThreshold }}
        {{- end }}
{{- end }}
```

### NOTES.txt (Post-Installation Instructions)

**File**: `helm/todo-app/templates/NOTES.txt`

```
🎉 Todo App has been deployed!

Chart: {{ .Chart.Name }}-{{ .Chart.Version }}
Release: {{ .Release.Name }}
Namespace: {{ .Values.global.namespace }}
Environment: {{ .Values.global.environment }}

📋 Deployment Summary:
- Backend replicas: {{ .Values.backend.replicaCount }}
- Frontend replicas: {{ .Values.frontend.replicaCount }}
- Database enabled: {{ .Values.database.enabled }}

🔍 Check deployment status:
  kubectl get pods -n {{ .Values.global.namespace }}
  kubectl get services -n {{ .Values.global.namespace }}

📊 View logs:
  kubectl logs -f deployment/{{ include "todo-app.backend.fullname" . }} -n {{ .Values.global.namespace }}
  kubectl logs -f deployment/{{ include "todo-app.frontend.fullname" . }} -n {{ .Values.global.namespace }}

🌐 Access the application:
{{- if eq .Values.frontend.service.type "NodePort" }}
  minikube service {{ include "todo-app.frontend.fullname" . }} -n {{ .Values.global.namespace }} --url
{{- else if eq .Values.frontend.service.type "LoadBalancer" }}
  kubectl get svc {{ include "todo-app.frontend.fullname" . }} -n {{ .Values.global.namespace }}
{{- end }}

{{- if .Values.ingress.enabled }}
🔗 Ingress configured:
{{- range .Values.ingress.hosts }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ .host }}
{{- end }}
{{- end }}

⚙️  Useful commands:
  # Upgrade deployment
  helm upgrade {{ .Release.Name }} ./helm/todo-app -n {{ .Values.global.namespace }}

  # Rollback to previous version
  helm rollback {{ .Release.Name }} -n {{ .Values.global.namespace }}

  # View release history
  helm history {{ .Release.Name }} -n {{ .Values.global.namespace }}

  # Uninstall
  helm uninstall {{ .Release.Name }} -n {{ .Values.global.namespace }}

📚 Documentation: https://github.com/your-org/todo-app/tree/main/phase-4

Happy task managing! 🚀
```

## Helm Commands

### Installation

```bash
# Install with default values
helm install todo-app ./helm/todo-app -n todo-app-dev --create-namespace

# Install with development values
helm install todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml -n todo-app-dev --create-namespace

# Install with custom values
helm install todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --set backend.secrets.openaiApiKey="sk-proj-..." \
  -n todo-app-dev --create-namespace

# Dry-run to see what will be deployed
helm install todo-app ./helm/todo-app --dry-run --debug -n todo-app-dev
```

### Upgrade

```bash
# Upgrade with new values
helm upgrade todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml -n todo-app-dev

# Upgrade with specific values
helm upgrade todo-app ./helm/todo-app \
  --set backend.image.tag=v1.1.0 \
  -n todo-app-dev

# Upgrade with wait for rollout
helm upgrade todo-app ./helm/todo-app -n todo-app-dev --wait --timeout 5m
```

### Rollback

```bash
# View release history
helm history todo-app -n todo-app-dev

# Rollback to previous version
helm rollback todo-app -n todo-app-dev

# Rollback to specific revision
helm rollback todo-app 2 -n todo-app-dev
```

### Uninstall

```bash
# Uninstall release
helm uninstall todo-app -n todo-app-dev

# Uninstall and keep history
helm uninstall todo-app -n todo-app-dev --keep-history
```

### Validation

```bash
# Lint chart
helm lint ./helm/todo-app

# Template chart (generate YAML)
helm template todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml

# Validate generated manifests
helm template todo-app ./helm/todo-app | kubectl apply --dry-run=client -f -
```

## Testing Strategy

### Chart Testing

```bash
# Install chart-testing tool
brew install chart-testing

# Lint chart
ct lint --charts helm/todo-app

# Test chart installation
ct install --charts helm/todo-app
```

### Integration Testing

```bash
# Install and verify
helm install todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml -n todo-app-dev --create-namespace --wait

# Check pod status
kubectl get pods -n todo-app-dev

# Test services
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app-dev
curl http://localhost:3000

# Uninstall
helm uninstall todo-app -n todo-app-dev
```

## Best Practices

### Values Organization

1. **Hierarchical Structure**: Group related values together
2. **Sensible Defaults**: Provide working defaults in values.yaml
3. **Environment Overrides**: Use separate files for different environments
4. **Documentation**: Comment all values explaining their purpose

### Template Best Practices

1. **Use Helpers**: Define reusable templates in _helpers.tpl
2. **Conditional Resources**: Use `{{- if .Values.component.enabled }}`
3. **Proper Indentation**: Use `| nindent` for correct YAML formatting
4. **Quote Strings**: Use `| quote` for string values
5. **Validate Required Values**: Use `required` function for mandatory values

### Security Best Practices

1. **No Secrets in Values**: Never commit secrets to values files
2. **External Secrets**: Use `--set` or external secret management
3. **RBAC**: Define proper service accounts and roles
4. **Security Context**: Always define security context

## Edge Cases and Error Handling

### Edge Case 1: Missing Required Values
**Scenario**: User forgets to provide required secrets
**Handling**:
```yaml
{{- if not .Values.backend.secrets.openaiApiKey }}
{{- fail "backend.secrets.openaiApiKey is required" }}
{{- end }}
```

### Edge Case 2: Invalid Configuration
**Scenario**: User provides invalid replica count
**Handling**:
```yaml
{{- if lt (.Values.backend.replicaCount | int) 1 }}
{{- fail "backend.replicaCount must be at least 1" }}
{{- end }}
```

### Edge Case 3: Conflicting Values
**Scenario**: User enables autoscaling but sets fixed replicas
**Handling**: Document that autoscaling overrides replicaCount

## Dependencies

### External Dependencies
- Helm 3.13+
- kubectl 1.28+
- Kubernetes cluster (Minikube)

### Internal Dependencies
- Phase 4 Spec 01: Docker images
- Phase 4 Spec 02: Kubernetes manifests

## Documentation Requirements

- [ ] Chart README with usage instructions
- [ ] Values documentation (inline comments)
- [ ] Example values files
- [ ] Upgrade guide
- [ ] Troubleshooting guide

## Success Metrics

- Chart passes `helm lint`
- Chart installs successfully
- All pods reach Ready state
- Services are accessible
- Upgrade works without downtime
- Rollback works correctly
- Values files work for different environments

## Future Enhancements (Out of Scope for Phase 4)

- Chart repository (ChartMuseum, Harbor)
- Chart signing and verification
- Helm hooks for pre/post install actions
- Subchart dependencies
- Chart testing with ct (chart-testing)
- Automated chart releases

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: Medium-High
**Implementation Order**: 3 of 5 (implement after Kubernetes manifests)
