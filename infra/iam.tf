resource "google_service_account" "app" {
  account_id   = "tech-digest-app"
  display_name = "tech-digest Cloud Run"
}

locals {
  app_roles = [
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/aiplatform.user",
  ]
}

resource "google_project_iam_member" "app" {
  for_each = toset(local.app_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.app.email}"
}
