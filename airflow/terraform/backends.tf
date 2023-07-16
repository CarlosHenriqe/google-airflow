terraform {
  backend "gcs" {
    bucket  = "state-case-tf"
    prefix  = "terraform/state"
  }
  required_providers {
    google = ">= 3.53"
  }
}