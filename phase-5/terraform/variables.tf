variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Name of the DOKS cluster"
  type        = string
  default     = "todo-app-prod"
}

variable "region" {
  description = "DigitalOcean region for cluster deployment"
  type        = string
  default     = "nyc1"

  validation {
    condition     = contains(["nyc1", "nyc3", "sfo3", "lon1", "fra1", "sgp1", "tor1", "blr1"], var.region)
    error_message = "Region must be a valid DigitalOcean region."
  }
}

variable "kubernetes_version" {
  description = "Kubernetes version for DOKS cluster"
  type        = string
  default     = "1.28.2-do.0"
  # Check latest versions: doctl kubernetes options versions
}

variable "node_size" {
  description = "Droplet size for worker nodes"
  type        = string
  default     = "s-2vcpu-4gb"  # $24/month per node

  validation {
    condition     = contains(["s-2vcpu-2gb", "s-2vcpu-4gb", "s-4vcpu-8gb", "s-8vcpu-16gb"], var.node_size)
    error_message = "Node size must be a valid DigitalOcean droplet size."
  }
}

variable "node_count" {
  description = "Initial number of worker nodes"
  type        = number
  default     = 3

  validation {
    condition     = var.node_count >= 1 && var.node_count <= 10
    error_message = "Node count must be between 1 and 10."
  }
}

variable "min_nodes" {
  description = "Minimum nodes for autoscaling"
  type        = number
  default     = 2

  validation {
    condition     = var.min_nodes >= 1 && var.min_nodes <= var.node_count
    error_message = "Min nodes must be at least 1 and not exceed initial node count."
  }
}

variable "max_nodes" {
  description = "Maximum nodes for autoscaling"
  type        = number
  default     = 5

  validation {
    condition     = var.max_nodes >= var.node_count && var.max_nodes <= 20
    error_message = "Max nodes must be at least the initial node count and not exceed 20."
  }
}

variable "registry_name" {
  description = "Container registry name (must be globally unique)"
  type        = string
  default     = "todo-app-registry"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.registry_name))
    error_message = "Registry name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = list(string)
  default     = ["todo-app", "production", "phase-5"]
}
