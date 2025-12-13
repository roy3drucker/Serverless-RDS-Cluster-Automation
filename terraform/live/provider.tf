provider "aws" {
  # Region is picked up from AWS_DEFAULT_REGION env var
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket = "terraform-state-rds-provisioner"

    region = "us-east-1"
  }
}
