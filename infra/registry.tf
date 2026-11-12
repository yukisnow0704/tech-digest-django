resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = "tech-digest"
  format        = "DOCKER"

  depends_on = [google_project_service.this]
}