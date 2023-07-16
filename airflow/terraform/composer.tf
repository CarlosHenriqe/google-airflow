module "composer" {
  source = "terraform-google-modules/composer/google//modules/create_environment_v1"

  project_id        = var.project_id
  composer_env_name = var.composer_env_name
  region            = var.region
  zone              = "us-east1-c"
  machine_type      = "n1-standard-1"
  network           = var.vpc_name
  subnetwork        = var.subnetwork
  node_count        = "3"
  image_version     = var.image_version

  composer_service_account = replace(module.composer-service-accounts.iam_email, "serviceAccount:", "")

  depends_on = [
    module.project-services,
  ]
}

#module "composer" {
#  source                   = "terraform-google-modules/composer/google//modules/create_environment_v1"
#  project_id               = var.project_id
#  region                   = var.region
#  composer_env_name        = var.composer_env_name
#  network                  = var.vpc_name
#  subnetwork               = var.subnetwork
#  enable_private_endpoint  = false
#  composer_service_account = replace(module.composer-service-accounts.iam_email, "serviceAccount:", "")
#  image_version            = var.image_version
#  airflow_config_overrides = {
#  }
#
#  scheduler  = {
#    cpu        = 0.5
#    memory_gb  = 1.875
#    storage_gb = 1
#    count      = 1
#  }
#  web_server = {
#    cpu        = 0.5
#    memory_gb  = 1.875
#    storage_gb = 1
#  }
#  worker = {
#    cpu        = 0.5
#    memory_gb  = 1.875
#    storage_gb = 1
#    min_count  = 1
#    max_count  = 1
#  }
#
#  depends_on = [
#    module.project-services,
#  ]
#}