# AWS Cost Optimization Platform - Terraform Variables Example
# Copy this file to terraform.tfvars and customize the values

# AWS Configuration
aws_region = "us-east-1"
environment = "prod"
project_name = "cost-optimization"

# Network Configuration
vpc_cidr = "10.0.0.0/16"

# Lambda Configuration
lambda_runtime = "python3.11"
lambda_memory_size = 128
lambda_timeout = 120

# DynamoDB Configuration
dynamodb_billing_mode = "PAY_PER_REQUEST"
enable_point_in_time_recovery = false

# S3 Configuration
s3_versioning_enabled = true
s3_lifecycle_days = 7

# API Gateway Configuration
api_gateway_stage_name = "prod"

# Monitoring Configuration
enable_detailed_monitoring = false
log_retention_days = 7

# Cost Management
enable_cost_anomaly_detection = false
cost_budget_limit = 10.0

# Tags
additional_tags = {
  Owner = "sami"
  Team = "platform"
  CostCenter = "engineering"
}

cost_center = "engineering"
owner = "sami"

# Feature Flags
enable_api_gateway_caching = false
enable_lambda_reserved_concurrency = false
lambda_reserved_concurrency = 10
