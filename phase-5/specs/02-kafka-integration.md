# Specification: Kafka Integration

**Feature ID**: 02
**Feature Name**: Kafka Integration on DOKS
**Phase**: 5 - Production Cloud Deployment
**Status**: Draft
**Created**: 2026-02-07
**Last Updated**: 2026-02-07

## Purpose

Deploy a production-grade Apache Kafka cluster on DigitalOcean Kubernetes using the Strimzi operator. Provide reliable, scalable event streaming infrastructure for the event-driven architecture.

## User Stories

**As a platform engineer**, I want a Kubernetes-native Kafka deployment so that I can manage Kafka using standard Kubernetes tools and practices.

**As a developer**, I want a reliable Kafka cluster so that events are never lost and the system can handle high throughput.

**As an operations engineer**, I want Kafka monitoring and management tools so that I can troubleshoot issues and optimize performance.

## Acceptance Criteria

### Kafka Cluster Deployment

- [ ] Strimzi operator installed in `kafka` namespace
- [ ] Kafka cluster with 3 brokers deployed
- [ ] Zookeeper ensemble with 3 nodes deployed
- [ ] Kafka cluster is highly available (survives single node failure)
- [ ] Persistent storage configured for Kafka and Zookeeper
- [ ] Kafka accessible from within cluster via service endpoints

### Topic Configuration

- [ ] Topic `todo.tasks.created` created with 3 partitions, replication factor 3
- [ ] Topic `todo.tasks.updated` created with 3 partitions, replication factor 3
- [ ] Topic `todo.tasks.deleted` created with 3 partitions, replication factor 3
- [ ] Topic `todo.tasks.completed` created with 3 partitions, replication factor 3
- [ ] Topics have 7-day retention policy
- [ ] Topics have compression enabled (snappy or lz4)

### Monitoring

- [ ] Kafka metrics exposed for Prometheus scraping
- [ ] Kafka Exporter deployed for detailed metrics
- [ ] Grafana dashboard for Kafka metrics
- [ ] Alerts configured for broker failures, high lag, disk usage

### Management

- [ ] Kafka UI deployed for topic management (optional)
- [ ] Scripts for creating/deleting topics
- [ ] Scripts for viewing consumer groups and lag
- [ ] Documentation for common Kafka operations

## Architecture

### Strimzi Operator

Strimzi provides Kubernetes-native deployment and management of Kafka:

- **Custom Resources**: Kafka, KafkaTopic, KafkaUser, KafkaConnect
- **Operator Pattern**: Reconciles desired state with actual state
- **Rolling Updates**: Zero-downtime upgrades
- **Monitoring**: Built-in Prometheus metrics

### Kafka Cluster Topology

```
┌─────────────────────────────────────────────────┐
│              DOKS Cluster                       │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │         Kafka Namespace                  │  │
│  │                                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────┐ │  │
│  │  │ Kafka    │  │ Kafka    │  │ Kafka  │ │  │
│  │  │ Broker 0 │  │ Broker 1 │  │ Broker │ │  │
│  │  │          │  │          │  │   2    │ │  │
│  │  └──────────┘  └──────────┘  └────────┘ │  │
│  │                                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────┐ │  │
│  │  │Zookeeper │  │Zookeeper │  │Zookeep │ │  │
│  │  │    0     │  │    1     │  │  er 2  │ │  │
│  │  └──────────┘  └──────────┘  └────────┘ │  │
│  │                                          │  │
│  │  ┌──────────────────────────────────┐   │  │
│  │  │      Kafka Exporter              │   │  │
│  │  └──────────────────────────────────┘   │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Install Strimzi Operator

**File**: `scripts/install-kafka.sh`

```bash
#!/bin/bash
set -e

echo "Installing Strimzi Kafka Operator..."

# Create kafka namespace
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Install Strimzi operator using Helm
helm repo add strimzi https://strimzi.io/charts/
helm repo update

helm upgrade --install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --version 0.38.0 \
  --set watchNamespaces="{kafka}" \
  --wait

echo "Waiting for Strimzi operator to be ready..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

echo "Strimzi operator installed successfully!"
```

### 2. Kafka Cluster Configuration

**File**: `kubernetes/doks/kafka-cluster.yaml`

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.6"
      log.retention.hours: 168  # 7 days
      log.segment.bytes: 1073741824  # 1GB
      compression.type: snappy
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
      class: do-block-storage
    resources:
      requests:
        memory: 2Gi
        cpu: 1000m
      limits:
        memory: 4Gi
        cpu: 2000m
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
      class: do-block-storage
    resources:
      requests:
        memory: 1Gi
        cpu: 500m
      limits:
        memory: 2Gi
        cpu: 1000m
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: zookeeper-metrics-config.yml
  entityOperator:
    topicOperator:
      resources:
        requests:
          memory: 512Mi
          cpu: 200m
        limits:
          memory: 512Mi
          cpu: 500m
    userOperator:
      resources:
        requests:
          memory: 512Mi
          cpu: 200m
        limits:
          memory: 512Mi
          cpu: 500m
```

### 3. Kafka Metrics ConfigMap

**File**: `kubernetes/doks/kafka-metrics-config.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-metrics
  namespace: kafka
data:
  kafka-metrics-config.yml: |
    lowercaseOutputName: true
    rules:
    - pattern: kafka.server<type=(.+), name=(.+), clientId=(.+), topic=(.+), partition=(.*)><>Value
      name: kafka_server_$1_$2
      type: GAUGE
      labels:
        clientId: "$3"
        topic: "$4"
        partition: "$5"
    - pattern: kafka.server<type=(.+), name=(.+), clientId=(.+), brokerHost=(.+), brokerPort=(.+)><>Value
      name: kafka_server_$1_$2
      type: GAUGE
      labels:
        clientId: "$3"
        broker: "$4:$5"
  zookeeper-metrics-config.yml: |
    lowercaseOutputName: true
    rules:
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+)><>(\\w+)"
      name: "zookeeper_$2"
      type: GAUGE
```

### 4. Kafka Topics

**File**: `kafka/topics.yaml`

```yaml
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: todo.tasks.created
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    compression.type: snappy
    min.insync.replicas: 2
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: todo.tasks.updated
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    compression.type: snappy
    min.insync.replicas: 2
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: todo.tasks.deleted
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    compression.type: snappy
    min.insync.replicas: 2
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: todo.tasks.completed
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    compression.type: snappy
    min.insync.replicas: 2
```

### 5. Kafka Exporter for Metrics

**File**: `kubernetes/doks/kafka-exporter.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-exporter
  namespace: kafka
  labels:
    app: kafka-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-exporter
  template:
    metadata:
      labels:
        app: kafka-exporter
    spec:
      containers:
      - name: kafka-exporter
        image: danielqsj/kafka-exporter:v1.7.0
        args:
        - --kafka.server=todo-kafka-kafka-bootstrap:9092
        - --web.listen-address=:9308
        - --log.level=info
        ports:
        - containerPort: 9308
          name: metrics
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: kafka-exporter
  namespace: kafka
  labels:
    app: kafka-exporter
spec:
  selector:
    app: kafka-exporter
  ports:
  - port: 9308
    targetPort: 9308
    name: metrics
---
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: kafka-exporter
  namespace: kafka
  labels:
    app: kafka-exporter
spec:
  selector:
    matchLabels:
      app: kafka-exporter
  endpoints:
  - port: metrics
    interval: 30s
```

## Edge Cases and Error Handling

### Broker Failures

- **Scenario**: One Kafka broker fails
- **Handling**: Kafka cluster continues operating with 2 brokers
- **Recovery**: Kubernetes restarts failed pod automatically
- **Data Safety**: Replication factor 3 ensures no data loss

### Disk Space Exhaustion

- **Scenario**: Kafka broker runs out of disk space
- **Handling**: Alert triggers, manual intervention required
- **Prevention**: Monitor disk usage, set retention policies
- **Recovery**: Increase PVC size or reduce retention

### Zookeeper Quorum Loss

- **Scenario**: 2 out of 3 Zookeeper nodes fail
- **Handling**: Kafka cluster becomes unavailable
- **Recovery**: Restore Zookeeper quorum
- **Prevention**: Monitor Zookeeper health, ensure node anti-affinity

### Network Partitions

- **Scenario**: Network partition splits cluster
- **Handling**: Kafka uses min.insync.replicas to prevent split-brain
- **Recovery**: Automatic once network heals
- **Prevention**: Use DigitalOcean VPC for reliable networking

## Testing Strategy

### Deployment Tests

- [ ] Verify Strimzi operator is running
- [ ] Verify Kafka cluster is ready (3 brokers)
- [ ] Verify Zookeeper ensemble is ready (3 nodes)
- [ ] Verify topics are created
- [ ] Verify metrics are exposed

### Functional Tests

- [ ] Produce messages to topics
- [ ] Consume messages from topics
- [ ] Verify message ordering within partitions
- [ ] Verify replication across brokers
- [ ] Test consumer group management

### Resilience Tests

- [ ] Kill one Kafka broker, verify cluster continues
- [ ] Kill one Zookeeper node, verify cluster continues
- [ ] Simulate network latency, verify performance
- [ ] Fill disk to 90%, verify alerts trigger

## Monitoring and Metrics

### Key Metrics

**Broker Metrics:**
- `kafka_server_replicamanager_underreplicatedpartitions`: Under-replicated partitions
- `kafka_server_brokertopicmetrics_messagesinpersec`: Messages in per second
- `kafka_server_brokertopicmetrics_bytesinpersec`: Bytes in per second
- `kafka_controller_kafkacontroller_activecontrollercount`: Active controller count

**Topic Metrics:**
- `kafka_topic_partition_current_offset`: Current offset per partition
- `kafka_topic_partition_oldest_offset`: Oldest offset per partition
- `kafka_topic_partition_replicas`: Number of replicas per partition

**Consumer Metrics:**
- `kafka_consumergroup_lag`: Consumer group lag
- `kafka_consumergroup_current_offset`: Current consumer offset
- `kafka_consumergroup_lag_seconds`: Lag in seconds

### Alerts

```yaml
- alert: KafkaBrokerDown
  expr: kafka_server_replicamanager_leadercount == 0
  for: 5m
  annotations:
    summary: "Kafka broker is down"

- alert: KafkaUnderReplicatedPartitions
  expr: kafka_server_replicamanager_underreplicatedpartitions > 0
  for: 10m
  annotations:
    summary: "Kafka has under-replicated partitions"

- alert: KafkaConsumerLag
  expr: kafka_consumergroup_lag > 1000
  for: 5m
  annotations:
    summary: "Kafka consumer lag is high"

- alert: KafkaDiskUsageHigh
  expr: kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes > 0.85
  for: 10m
  annotations:
    summary: "Kafka disk usage is high"
```

## Performance Requirements

- Kafka cluster handles 10,000 messages/second
- Message latency p99 < 100ms
- Consumer lag stays below 1000 messages under normal load
- Cluster survives single broker failure with no data loss
- Topic creation completes within 30 seconds

## Security Considerations

- Kafka uses internal listeners only (not exposed externally)
- TLS encryption available on port 9093 (optional for demo)
- SASL authentication can be enabled (optional for demo)
- Network policies restrict access to Kafka namespace
- Persistent volumes encrypted at rest (DigitalOcean default)

## Cost Optimization

- Use DigitalOcean block storage (cheaper than SSD)
- Set appropriate retention policies (7 days)
- Enable compression (snappy) to reduce storage
- Right-size broker resources (2Gi memory, 1 CPU)
- Use single Kafka cluster for all environments (dev/staging/prod topics)

## Rollout Plan

1. Install Strimzi operator
2. Deploy Kafka metrics ConfigMap
3. Deploy Kafka cluster (wait for ready)
4. Create topics
5. Deploy Kafka exporter
6. Verify metrics in Prometheus
7. Create Grafana dashboard
8. Configure alerts

## Success Metrics

- Kafka cluster deployed with 3 brokers
- All 4 topics created successfully
- Metrics exposed and scraped by Prometheus
- Grafana dashboard showing Kafka metrics
- Alerts configured and firing correctly
- Test messages produced and consumed successfully
- Cluster survives broker failure test

## Troubleshooting Guide

### Kafka Broker Not Starting

```bash
# Check broker logs
kubectl logs -n kafka todo-kafka-kafka-0

# Check persistent volume claims
kubectl get pvc -n kafka

# Check Strimzi operator logs
kubectl logs -n kafka -l name=strimzi-cluster-operator
```

### Topics Not Created

```bash
# Check topic operator logs
kubectl logs -n kafka -l strimzi.io/name=todo-kafka-entity-operator

# Manually create topic
kubectl apply -f kafka/topics.yaml

# List topics
kubectl get kafkatopics -n kafka
```

### High Consumer Lag

```bash
# Check consumer group status
kubectl exec -n kafka todo-kafka-kafka-0 -- bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group event-service

# Check event service logs
kubectl logs -n todo-app-prod -l app=event-service
```

## Dependencies

- DigitalOcean Kubernetes cluster (DOKS)
- Strimzi operator 0.38+
- Persistent storage (DigitalOcean block storage)
- Prometheus for metrics collection

## Future Enhancements

- Schema Registry for Avro schema management
- Kafka Connect for integrations
- Kafka Streams for real-time processing
- Multi-region replication (MirrorMaker 2)
- SASL/SCRAM authentication
- TLS encryption for all traffic

---

**Specification Version**: 1.0
**Approved By**: [Pending]
**Implementation Status**: Not Started
