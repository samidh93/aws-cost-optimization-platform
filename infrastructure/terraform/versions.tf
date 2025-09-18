# AWS Cost Optimization Platform - Terraform Version Constraints

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }

  # Optional: Configure remote state backend
  # Uncomment and customize for production use
  #
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "cost-optimization/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-state-lock"
  #   encrypt        = true
  # }
}
