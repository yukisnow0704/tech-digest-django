resource "google_service_account" "scheduler" {
  account_id   = "tech-digest-scheduler"
  display_name = "tech-digest Cloud Scheduler"
}

resource "google_cloud_run_v2_job_iam_member" "scheduler_ingest" {
  name     = google_cloud_run_v2_job.ingest.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}

resource "google_cloud_scheduler_job" "ingest" {
  name      = "tech-digest-ingest"
  region    = var.region
  schedule  = "0 8,19 * * *"
  time_zone = "Asia/Tokyo"
  paused    = var.db_activation_policy != "ALWAYS"

  retry_config {
    retry_count = 0
  }

  http_target {
    http_method = "POST"
    uri         = "https://run.googleapis.com/v2/${google_cloud_run_v2_job.ingest.id}:run"

    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }

  depends_on = [
    google_project_service.this,
    google_cloud_run_v2_job_iam_member.scheduler_ingest,
  ]
}
