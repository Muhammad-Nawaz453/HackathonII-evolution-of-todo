output "cluster_id" {
  description = "The ID of the DOKS cluster"
  value       = digitalocean_kubernetes_cluster.todo_app.id
}

output "cluster_endpoint" {
  description = "The endpoint for the DOKS cluster API server"
  value       = digitalocean_kubernetes_cluster.todo_app.endpoint
}

output "cluster_name" {
  description = "The name of the DOKS cluster"
  value       = digitalocean_kubernetes_cluster.todo_app.name
}

output "cluster_region" {
  description = "The region where the cluster is deployed"
  value       = digitalocean_kubernetes_cluster.todo_app.region
}

output "cluster_version" {
  description = "The Kubernetes version of the cluster"
  value       = digitalocean_kubernetes_cluster.todo_app.version
}

output "registry_endpoint" {
  description = "The endpoint for the container registry"
  value       = digitalocean_container_registry.todo_app.endpoint
}

output "registry_name" {
  description = "The name of the container registry"
  value       = digitalocean_container_registry.todo_app.name
}

output "registry_server_url" {
  description = "The full server URL for the container registry"
  value       = digitalocean_container_registry.todo_app.server_url
}

output "kubeconfig_path" {
  description = "Path to the generated kubeconfig file"
  value       = local_file.kubeconfig.filename
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = digitalocean_vpc.todo_app.id
}

output "vpc_ip_range" {
  description = "The IP range of the VPC"
  value       = digitalocean_vpc.todo_app.ip_range
}

output "kubectl_config_command" {
  description = "Command to configure kubectl"
  value       = "doctl kubernetes cluster kubeconfig save ${digitalocean_kubernetes_cluster.todo_app.name}"
}

output "docker_login_command" {
  description = "Command to authenticate Docker with the registry"
  value       = "doctl registry login"
}

output "estimated_monthly_cost" {
  description = "Estimated monthly cost in USD"
  value       = "~$${var.node_count * 24 + 12} (${var.node_count} nodes + load balancer)"
}
