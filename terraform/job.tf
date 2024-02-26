resource "google_service_account" "main" {
  account_id   = "${var.app_name}-${var.env}"
  display_name = "${var.app_name} ${var.env}"
}

resource "google_service_account" "scheduler" {
  account_id   = "${var.app_name}-scheduler-${var.env}"
  display_name = "${var.app_name} Scheduler ${var.env}"
}

resource "google_cloud_run_v2_job" "main" {
  name         = "${var.app_name}-${var.env}"
  location     = var.region

  template {
    template {
      service_account = google_service_account.main.email
      timeout         = "120s"
      containers {
        image = "us-west1-docker.pkg.dev/tideswell/docker-default/exif-crawler:${var.image_tag}"
      }
    }
  }
}

resource "google_cloud_run_v2_job_iam_member" "scheduler" {
  name     = google_cloud_run_v2_job.main.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}

resource "google_cloud_scheduler_job" "schedule" {
  name             = "${var.app_name}-${var.env}"
  description      = "${var.app_name} ${var.env}"
  schedule         = var.cron_schedule
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "120s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/tideswell/jobs/${var.app_name}-${var.env}:run"
    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }
}
