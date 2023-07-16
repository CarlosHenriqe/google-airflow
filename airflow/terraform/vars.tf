variable "project_id" {
    type = string 
    default = "default-case"
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
    default = "composer-1.20.10-airflow-2.4.3"
}