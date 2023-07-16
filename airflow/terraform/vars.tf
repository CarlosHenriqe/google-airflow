variable "project_id" {
    type = string 
    default = "my-first-case-393014"
}

variable "region" {
    type = string 
    default = "us-east1"
}

variable "composer_env_name" {
    type = string 
    default = "airflow-gcp"
}

variable "vpc_name" {
    type = string 
    default = "default"
}

variable "subnetwork" {
    type = string 
    default = "default"
}

variable "image_version" {
    type = string 
    default = "composer-2.0.32-airflow-2.3.4"
}