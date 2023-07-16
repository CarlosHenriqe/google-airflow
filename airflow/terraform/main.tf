data "google_project" "project" {
  project_id = var.project_id
}

module "project-services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  project_id                  = var.project_id
  enable_apis                 = true
  disable_services_on_destroy = true
  activate_apis = [
    "sourcerepo.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "pubsub.googleapis.com",
    "composer.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
    "servicenetworking.googleapis.com",
    "bigquery.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
  ]
}