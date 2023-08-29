provider "google" {
  project = "generative-ai-386501"
  region  = "us-central1"
}

resource "google_cloud_run_service" "default" {
  name     = "myapp"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/generative-ai-386501/myapp"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

output "url" {
  value = google_cloud_run_service.default.status[0].url
}
