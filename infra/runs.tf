locals {
  plain_env = {
    GOOGLE_CLOUD_PROJECT = var.project_id
    ALLOWED_HOSTS        = ".run.app,localhost"
    CSRF_TRUSTED_ORIGINS = "https://*.run.app"
  }

  secret_env = {
    DATABASE_URL = google_secret_manager_secret.database_url.secret_id
    SECRET_KEY   = google_secret_manager_secret.django_secret_key.secret_id
  }
}

resource "google_cloud_run_v2_service" "api" {
  name                = "tech-digest-api"
  location            = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.app.email

    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.main.connection_name]
      }
    }

    containers {
      image = var.image

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      dynamic "env" {
        for_each = local.plain_env
        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = local.secret_env
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
  }

  depends_on = [
    google_project_iam_member.app,
    google_secret_manager_secret_version.database_url,
    google_secret_manager_secret_version.django_secret_key,
  ]
}

resource "google_cloud_run_v2_job" "migrate" {
  name                = "tech-digest-migrate"
  location            = var.region
  deletion_protection = false

  template {
    template {
      service_account = google_service_account.app.email
      max_retries     = 0
      timeout         = "300s"

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.main.connection_name]
        }
      }

      containers {
        image   = var.image
        command = ["python", "manage.py"]
        args    = ["migrate", "--noinput"]

        dynamic "env" {
          for_each = local.plain_env
          content {
            name  = env.key
            value = env.value
          }
        }

        dynamic "env" {
          for_each = local.secret_env
          content {
            name = env.key
            value_source {
              secret_key_ref {
                secret  = env.value
                version = "latest"
              }
            }
          }
        }

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }
      }
    }
  }

  depends_on = [
    google_project_iam_member.app,
    google_secret_manager_secret_version.database_url,
    google_secret_manager_secret_version.django_secret_key,
  ]
}

resource "google_cloud_run_v2_job" "ingest" {
  name                = "tech-digest-ingest"
  location            = var.region
  deletion_protection = false

  template {
    template {
      service_account = google_service_account.app.email
      max_retries     = 0
      timeout         = "900s"

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.main.connection_name]
        }
      }

      containers {
        image   = var.image
        command = ["python", "manage.py"]
        args    = ["ingest", "--limit", "20"]

        dynamic "env" {
          for_each = local.plain_env
          content {
            name  = env.key
            value = env.value
          }
        }

        dynamic "env" {
          for_each = local.secret_env
          content {
            name = env.key
            value_source {
              secret_key_ref {
                secret  = env.value
                version = "latest"
              }
            }
          }
        }

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }
      }
    }
  }

  depends_on = [
    google_project_iam_member.app,
    google_secret_manager_secret_version.database_url,
    google_secret_manager_secret_version.django_secret_key,
  ]
}
