#!/bin/bash
set -e

echo "=========================================="
echo "  Installing Strimzi Kafka Operator"
echo "=========================================="
echo ""

# Create kafka namespace
echo "📦 Creating kafka namespace..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Add Strimzi Helm repository
echo "📦 Adding Strimzi Helm repository..."
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install Strimzi operator
echo "📦 Installing Strimzi Kafka Operator..."
helm upgrade --install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --version 0.38.0 \
  --set watchNamespaces="{kafka}" \
  --set logLevel=INFO \
  --wait \
  --timeout 10m

echo "✅ Strimzi operator installed"
echo ""

# Wait for operator to be ready
echo "⏳ Waiting for Strimzi operator to be ready..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

echo "✅ Strimzi operator is ready"
echo ""

# Deploy Kafka metrics ConfigMap
echo "📦 Deploying Kafka metrics configuration..."
kubectl apply -f ../kubernetes/doks/kafka-metrics-config.yaml

# Deploy Kafka cluster
echo "📦 Deploying Kafka cluster (this takes 5-10 minutes)..."
kubectl apply -f ../kubernetes/doks/kafka-cluster.yaml

echo "⏳ Waiting for Kafka cluster to be ready..."
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=600s -n kafka

echo "✅ Kafka cluster is ready"
echo ""

# Create Kafka topics
echo "📦 Creating Kafka topics..."
kubectl apply -f ../kafka/topics.yaml

echo "⏳ Waiting for topics to be created..."
sleep 10

# Verify topics
echo "🔍 Verifying Kafka topics..."
kubectl get kafkatopics -n kafka

echo ""
echo "=========================================="
echo "  ✅ Kafka Installation Complete!"
echo "=========================================="
echo ""
echo "Kafka Cluster:"
echo "  Name: todo-kafka"
echo "  Brokers: 3"
echo "  Zookeeper: 3 nodes"
echo "  Bootstrap: todo-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092"
echo ""
echo "Topics Created:"
echo "  - todo.tasks.created"
echo "  - todo.tasks.updated"
echo "  - todo.tasks.deleted"
echo "  - todo.tasks.completed"
echo ""
echo "Useful Commands:"
echo "  kubectl get kafka -n kafka"
echo "  kubectl get kafkatopics -n kafka"
echo "  kubectl logs -n kafka todo-kafka-kafka-0"
echo ""
