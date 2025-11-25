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
}
