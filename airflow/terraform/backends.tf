terraform {
  backend "gcs" {
    bucket  = "tf-state-case-boticario"
    prefix  = "terraform/state"
  }
  required_providers {
    google = ">= 3.53"
  }
}