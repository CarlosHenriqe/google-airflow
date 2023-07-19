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

  pypi_packages = {
    pendulum   = ">=2.1.2"
    pandas     = ">=0.24.2"
    pyarrow    = ">=3.0.0"
    gcsfs      = ">=2023.6.0"
    pandas-gbq = ">=0.17.0"
    google-auth-oauthlib = ">=0.4.1,<0.5"
    tensorboard = ">=2.8.0"
    apache-airflow-providers-google=">=2.3.0"
  }

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