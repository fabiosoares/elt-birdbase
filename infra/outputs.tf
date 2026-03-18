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

output "storage_bucket_database" {
  description = "Nome do bucket GCS para dados do birdbase."
  value       = google_storage_bucket.database.name
}

output "storage_bucket_birds_of_the_world" {
  description = "Nome do bucket GCS para dados do Birds of the World."
  value       = google_storage_bucket.birds_of_the_world.name
}

output "dbt_job_name" {
  description = "Nome do Cloud Run Job do dbt."
  value       = google_cloud_run_v2_job.dbt.name
}

output "workflow_name" {
  description = "Nome do Cloud Workflow."
  value       = google_workflows_workflow.birdbase_pipeline.name
}

output "scheduler_name" {
  description = "Nome do Cloud Scheduler Job."
  value       = google_cloud_scheduler_job.birdbase_daily.name
}
