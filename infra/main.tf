locals {
  image_uri = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}/${var.image_name}:${var.image_tag}"
}

resource "google_project_service" "required" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "cloudbuild.googleapis.com",
    "workflows.googleapis.com",
    "cloudscheduler.googleapis.com"
  ])

  project = var.project_id
  service = each.value

  disable_on_destroy = false
}

resource "google_service_account" "runtime" {
  account_id   = var.runtime_sa_name
  display_name = "Cloud Run runtime (${var.env})"
}

resource "google_service_account" "deployer" {
  account_id   = var.wif_deployer_sa_name
  display_name = "GitHub Actions deployer (${var.env})"
}

resource "google_project_iam_member" "deployer_roles" {
  for_each = toset([
    "roles/run.admin",
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser",
    "roles/cloudbuild.builds.editor"
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = var.artifact_repo
  format        = "DOCKER"

  depends_on = [google_project_service.required]
}

resource "google_cloud_run_v2_service" "app" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = local.image_uri

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }
    }

    service_account = google_service_account.runtime.email
    timeout         = "3600s"

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }
  }

  depends_on = [google_project_service.required]
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  count    = var.allow_unauthenticated ? 1 : 0
  name     = google_cloud_run_v2_service.app.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = var.wif_pool_id
  display_name              = "GitHub Actions (${var.env})"

  depends_on = [google_project_service.required]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.wif_provider_id
  display_name                       = "GitHub Actions provider (${var.env})"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository == \"${var.github_owner}/${var.github_repo}\" || assertion.repository == \"${var.github_owner}/${var.github_repo_dbt}\""
}

resource "google_service_account_iam_member" "deployer_wif" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_owner}/${var.github_repo}"
}

resource "google_service_account_iam_member" "deployer_wif_dbt" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_owner}/${var.github_repo_dbt}"
}

# ── GCS Buckets ──────────────────────────────────────────────────────────────

resource "google_storage_bucket" "database" {
  name          = var.bucket_database
  location      = var.storage_location
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_storage_bucket" "birds_of_the_world" {
  name          = var.bucket_birds_of_the_world
  location      = var.storage_location
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Permissão para a SA do Cloud Run nos dois buckets
resource "google_storage_bucket_iam_member" "runtime_database" {
  bucket = google_storage_bucket.database.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_storage_bucket_iam_member" "runtime_birds_of_the_world" {
  bucket = google_storage_bucket.birds_of_the_world.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.runtime.email}"
}

# Permissões BigQuery para a SA runtime (API + dbt)
resource "google_project_iam_member" "runtime_bq_roles" {
  for_each = toset([
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.runtime.email}"
}

# ── Cloud Run Job (dbt) ─────────────────────────────────────────────────────

resource "google_cloud_run_v2_job" "dbt" {
  name     = var.dbt_job_name
  location = var.region

  template {
    template {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}/${var.dbt_image_name}:${var.dbt_image_tag}"

        resources {
          limits = {
            cpu    = "2"
            memory = "1Gi"
          }
        }
      }

      service_account = google_service_account.runtime.email
      timeout         = "1800s"
      max_retries     = 1
    }
  }

  depends_on = [google_project_service.required]
}

# ── Service Account para Workflows / Scheduler ──────────────────────────────

resource "google_service_account" "orchestrator" {
  account_id   = "birdbase-orchestrator"
  display_name = "Birdbase orchestrator (Workflows + Scheduler)"
}

resource "google_project_iam_member" "orchestrator_roles" {
  for_each = toset([
    "roles/run.invoker",
    "roles/run.developer",
    "roles/workflows.invoker",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.orchestrator.email}"
}

# ── Cloud Workflows ─────────────────────────────────────────────────────────

resource "google_workflows_workflow" "birdbase_pipeline" {
  name            = "birdbase-pipeline"
  region          = var.region
  description     = "Orquestra: ingestão (API) → transformação (dbt)"
  service_account = google_service_account.orchestrator.id

  source_contents = <<-YAML
    main:
      steps:
        - parallel_ingest:
            parallel:
              branches:
                - ingest_birdbase_branch:
                    steps:
                      - ingest_birdbase:
                          call: http.post
                          args:
                            url: ${google_cloud_run_v2_service.app.uri}/birds/birdbase
                            auth:
                              type: OIDC
                          result: ingest_birdbase_result
                      - log_ingest_birdbase:
                          call: sys.log
                          args:
                            text: $${"Ingestão birdbase concluída com status " + string(ingest_birdbase_result.code)}

                - ingest_names_branch:
                    steps:
                      - ingest_names:
                          call: http.post
                          args:
                            url: ${google_cloud_run_v2_service.app.uri}/birds/names
                            auth:
                              type: OIDC
                          result: ingest_names_result
                      - log_ingest_names:
                          call: sys.log
                          args:
                            text: $${"Ingestão nomes PT-BR concluída com status " + string(ingest_names_result.code)}

                - ingest_images_branch:
                    steps:
                      - ingest_images:
                          call: http.post
                          args:
                            url: ${google_cloud_run_v2_service.app.uri}/birds/images
                            auth:
                              type: OIDC
                            timeout: 1800
                          result: ingest_images_result
                      - log_ingest_images:
                          call: sys.log
                          args:
                            text: $${"Ingestão imagens concluída com status " + string(ingest_images_result.code)}

        - run_dbt:
            call: googleapis.run.v2.projects.locations.jobs.run
            args:
              name: projects/${var.project_id}/locations/${var.region}/jobs/${var.dbt_job_name}
            result: dbt_result

        - log_dbt:
            call: sys.log
            args:
              text: $${"dbt job concluído"}

        - return_result:
            return:
              dbt_status: "completed"
  YAML

  depends_on = [
    google_project_service.required,
    google_cloud_run_v2_service.app,
    google_cloud_run_v2_job.dbt
  ]
}

# ── Cloud Scheduler ─────────────────────────────────────────────────────────

resource "google_cloud_scheduler_job" "birdbase_daily" {
  name        = "birdbase-daily-pipeline"
  description = "Executa pipeline birdbase diariamente às 06:00 BRT"
  schedule    = var.scheduler_cron
  time_zone   = "America/Sao_Paulo"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/${google_workflows_workflow.birdbase_pipeline.id}/executions"

    oauth_token {
      service_account_email = google_service_account.orchestrator.email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }

  depends_on = [google_project_service.required]
}
