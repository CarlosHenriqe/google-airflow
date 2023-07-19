resource "google_cloudbuild_trigger" "trigger-build-dags" {
  location = "global"
  project  = var.project_id
  name     = "build-dags"

  github {
    name  = "google-airflow"
    owner = "CarlosHenriqe"

    push {
      branch       = "main"
      invert_regex = false
    }
  }

  #trigger_template {
  #  branch_name = "main"
  #  project_id  = var.project_id
  #  repo_name   = "CarlosHenriqe/google-airflow"
  #}

  substitutions = {
    _COMPOSER_DAG_BUCKET = "gs://us-east1-airflow-gcp-54adddd8-bucket/dags"
  }
  filename = "./cloudbuild.yaml"

  included_files = [
    "airflow/dags/**"
  ]
}