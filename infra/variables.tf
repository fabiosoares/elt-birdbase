variable "project_id" {
  type        = string
  description = "ID do projeto GCP (dev/prod)."
}

variable "region" {
  type        = string
  description = "Região GCP (ex: southamerica-east1)."
}

variable "env" {
  type        = string
  description = "Nome do ambiente (dev/prod)."
}

variable "service_name" {
  type        = string
  description = "Nome do serviço Cloud Run."
}

variable "artifact_repo" {
  type        = string
  description = "Nome do repositório Artifact Registry."
}

variable "image_name" {
  type        = string
  description = "Nome da imagem Docker."
  default     = "birdbase-api"
}

variable "image_tag" {
  type        = string
  description = "Tag da imagem Docker (ex: SHA do commit)."
  default     = "latest"
}

variable "cpu" {
  type        = string
  description = "CPU para o container."
  default     = "1"
}

variable "memory" {
  type        = string
  description = "Memória para o container."
  default     = "512Mi"
}

variable "min_instances" {
  type        = number
  description = "Mínimo de instâncias no Cloud Run."
  default     = 0
}

variable "max_instances" {
  type        = number
  description = "Máximo de instâncias no Cloud Run."
  default     = 3
}

variable "allow_unauthenticated" {
  type        = bool
  description = "Permite acesso público ao serviço Cloud Run."
  default     = true
}

variable "github_owner" {
  type        = string
  description = "Owner do repositório GitHub."
}

variable "github_repo" {
  type        = string
  description = "Nome do repositório GitHub."
}

variable "wif_pool_id" {
  type        = string
  description = "ID do Workload Identity Pool."
  default     = "github-pool"
}

variable "wif_provider_id" {
  type        = string
  description = "ID do Workload Identity Provider."
  default     = "github-provider"
}

variable "wif_deployer_sa_name" {
  type        = string
  description = "Nome da Service Account usada pelo GitHub Actions."
  default     = "github-actions-deployer"
}

variable "runtime_sa_name" {
  type        = string
  description = "Nome da Service Account do Cloud Run."
  default     = "cloud-run-runtime"
}

variable "bucket_database" {
  type        = string
  description = "Nome do bucket GCS para dados do birdbase."
}

variable "bucket_birds_of_the_world" {
  type        = string
  description = "Nome do bucket GCS para dados do Birds of the World."
}

variable "storage_location" {
  type        = string
  description = "Localização dos buckets GCS."
  default     = "US"
}
