variable "app_name" {
  type    = string
  default = "exif-crawler"
}

variable "region" {
  type        = string
  default     = "us-west1"
  description = "Google Cloud region for deployment"
}

variable "env" {
  type        = string
  description = "Environment (dev or prod)"
}

variable "cron_schedule" {
  type    = string
  default = "0 8 * * 2"
}

variable "image_tag" {
  type        = string
  description = "Container image tag for job"
}
