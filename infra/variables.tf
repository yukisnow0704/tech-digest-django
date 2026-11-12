variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-northeast1"
}

variable "image" {
  type        = string
  description = "Cloud Run で動かすコンテナイメージ"
}

variable "db_activation_policy" {
  type        = string
  default     = "ALWAYS"
  description = "Cloud SQL を動かすときは ALWAYS、止めるときは NEVER"
}

variable "github_repository" {
  type        = string
  description = "owner/repo の形式"
}
