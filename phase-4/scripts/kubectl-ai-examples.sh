#!/bin/bash

# kubectl-ai usage examples for Todo App

echo "=== kubectl-ai Examples for Todo App ==="

# Basic queries
echo -e "\n1. Show all pods in todo-app-dev namespace"
kubectl ai "show me all pods in todo-app-dev namespace"

echo -e "\n2. Check pod status"
kubectl ai "are there any failing pods in todo-app-dev?"

echo -e "\n3. Show resource usage"
kubectl ai "show resource usage for pods in todo-app-dev"

# Logs and debugging
echo -e "\n4. View backend logs"
kubectl ai "show logs from backend pods in todo-app-dev"

echo -e "\n5. Debug pod issues"
kubectl ai "why is the backend pod crashing?"

echo -e "\n6. Check recent events"
kubectl ai "show recent events in todo-app-dev namespace"

# Scaling
echo -e "\n7. Scale backend deployment"
kubectl ai "scale backend deployment to 3 replicas in todo-app-dev"

echo -e "\n8. Check current replica count"
kubectl ai "how many replicas does the backend deployment have?"

# Service and networking
echo -e "\n9. Describe frontend service"
kubectl ai "describe the frontend service in todo-app-dev"

echo -e "\n10. Check service endpoints"
kubectl ai "show endpoints for backend service in todo-app-dev"

# Troubleshooting
echo -e "\n11. Check deployment health"
kubectl ai "check if all deployments are healthy in todo-app-dev"

echo -e "\n12. Find resource-intensive pods"
kubectl ai "find pods using more than 400Mi memory in todo-app-dev"

echo -e "\n13. Optimize resources"
kubectl ai "suggest resource optimizations for todo-app-dev namespace"

# Advanced operations
echo -e "\n14. Restart deployment"
kubectl ai "restart the backend deployment in todo-app-dev"

echo -e "\n15. Check best practices"
kubectl ai "check if my backend deployment follows Kubernetes best practices"

echo -e "\n=== Examples Complete ==="
