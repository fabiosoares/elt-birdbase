output "cloud_run_url" {
  description = "URL do serviço Cloud Run."
  value       = google_cloud_run_v2_service.app.uri
}

output "artifact_repo" {
  description = "Nome do Artifact Registry."
  value       = google_artifact_registry_repository.app.repository_id
}

output "deployer_service_account" {
  description = "Service Account usada no GitHub Actions."
  value       = google_service_account.deployer.email
}

output "wif_provider" {
  description = "Nome completo do Workload Identity Provider."
  value       = google_iam_workload_identity_pool_provider.github.name
}
