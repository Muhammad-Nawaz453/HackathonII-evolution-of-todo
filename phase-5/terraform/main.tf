terraform {
  required_version = ">= 1.6.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.34"
    }
  }

  # Optional: Store state in DigitalOcean Spaces (S3-compatible)
  # Uncomment and configure for production use
  # backend "s3" {
  #   endpoint                    = "nyc3.digitaloceanspaces.com"
  #   key                         = "terraform/todo-app-phase5.tfstate"
  #   bucket                      = "my-terraform-state"
  #   region                      = "us-east-1"
  #   skip_credentials_validation = true
  #   skip_metadata_api_check     = true
  #   skip_requesting_account_id  = true
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
    tags       = ["todo-app", "production", "phase-5"]
  }

  tags = ["todo-app", "production", "phase-5"]
}

# Container Registry
resource "digitalocean_container_registry" "todo_app" {
  name                   = var.registry_name
  subscription_tier_slug = "basic"  # Free tier (500MB)
  region                 = var.region
}

# VPC for private networking (optional but recommended)
resource "digitalocean_vpc" "todo_app" {
  name     = "${var.cluster_name}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"
}

# Output kubeconfig to file
resource "local_file" "kubeconfig" {
  content  = digitalocean_kubernetes_cluster.todo_app.kube_config[0].raw_config
  filename = "${path.module}/kubeconfig.yaml"
  file_permission = "0600"
}

# Output cluster info
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

output "registry_name" {
  description = "Container registry name"
  value       = digitalocean_container_registry.todo_app.name
}

output "kubeconfig_path" {
  description = "Path to kubeconfig file"
  value       = local_file.kubeconfig.filename
}

output "vpc_id" {
  description = "VPC ID"
  value       = digitalocean_vpc.todo_app.id
}
