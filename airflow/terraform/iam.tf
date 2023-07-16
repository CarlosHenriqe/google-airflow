module "composer-service-accounts" {
  source       = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/iam-service-account?ref=v18.0.0/"
  project_id   = var.project_id
  name         = "composer-default"
  generate_key = false
  # authoritative roles granted on the service accounts to other identities
  iam = {
  }
  # non-authoritative roles granted to the service accounts on other resources
  iam_project_roles = {
    "${var.project_id}" = [
      "roles/logging.logWriter",
      "roles/monitoring.metricWriter",
      "roles/composer.ServiceAgentV2Ext",
      "roles/composer.worker",
      "roles/composer.admin",
      "roles/dataflow.admin",
      "roles/iam.serviceAccountUser",
      "roles/compute.networkUser",
    ]
  }
}