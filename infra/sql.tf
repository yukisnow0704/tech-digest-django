resource "google_sql_database_instance" "main" {
  name                = "tech-digest"
  database_version    = "POSTGRES_17"
  region              = var.region
  deletion_protection = false

  settings {
    edition           = "ENTERPRISE"
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    activation_policy = var.db_activation_policy
    disk_size         = 10
    disk_autoresize   = false

    backup_configuration {
      enabled = false
    }

    ip_configuration {
      ipv4_enabled = true
    }
  }

  depends_on = [google_project_service.this]
}

resource "google_sql_database" "digest" {
  name     = "digest"
  instance = google_sql_database_instance.main.name
}

resource "random_password" "db" {
  length  = 32
  special = false
}

resource "google_sql_user" "digest" {
  name     = "digest"
  instance = google_sql_database_instance.main.name
  password = random_password.db.result
}
