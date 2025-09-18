# AWS Cost Optimization Platform - Terraform Outputs

# ==========================================
# Network Outputs
# ==========================================

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

# ==========================================
# Storage Outputs
# ==========================================

output "s3_bucket_name" {
  description = "Name of the S3 bucket for cost data storage"
  value       = aws_s3_bucket.cost_data.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.cost_data.arn
}

output "s3_bucket_domain_name" {
  description = "Bucket domain name"
  value       = aws_s3_bucket.cost_data.bucket_domain_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table for cost tracking"
  value       = aws_dynamodb_table.cost_tracking.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.cost_tracking.arn
}

# ==========================================
# Lambda Function Outputs
# ==========================================

output "cost_processor_function_name" {
  description = "Name of the Cost Processor Lambda function"
  value       = aws_lambda_function.cost_processor.function_name
}

output "cost_processor_function_arn" {
  description = "ARN of the Cost Processor Lambda function"
  value       = aws_lambda_function.cost_processor.arn
}

output "budget_alert_function_name" {
  description = "Name of the Budget Alert Lambda function"
  value       = aws_lambda_function.budget_alert.function_name
}

output "budget_alert_function_arn" {
  description = "ARN of the Budget Alert Lambda function"
  value       = aws_lambda_function.budget_alert.arn
}

output "cost_optimizer_function_name" {
  description = "Name of the Cost Optimizer Lambda function"
  value       = aws_lambda_function.cost_optimizer.function_name
}

output "cost_optimizer_function_arn" {
  description = "ARN of the Cost Optimizer Lambda function"
  value       = aws_lambda_function.cost_optimizer.arn
}

output "api_gateway_function_name" {
  description = "Name of the API Gateway Lambda function"
  value       = aws_lambda_function.api_gateway.function_name
}

output "api_gateway_function_arn" {
  description = "ARN of the API Gateway Lambda function"
  value       = aws_lambda_function.api_gateway.arn
}

# ==========================================
# API Gateway Outputs
# ==========================================

output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_arn" {
  description = "ARN of the API Gateway"
  value       = aws_api_gateway_rest_api.main.arn
}

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
}

output "api_gateway_execution_arn" {
  description = "Execution ARN of the API Gateway"
  value       = aws_api_gateway_rest_api.main.execution_arn
}

# ==========================================
# IAM Outputs
# ==========================================

output "lambda_execution_role_name" {
  description = "Name of the Lambda execution role"
  value       = aws_iam_role.lambda_execution.name
}

output "lambda_execution_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_execution.arn
}

# ==========================================
# General Information Outputs
# ==========================================

output "aws_region" {
  description = "AWS region where resources are deployed"
  value       = var.aws_region
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

# ==========================================
# Cost Estimation Outputs
# ==========================================

output "estimated_monthly_cost" {
  description = "Estimated monthly cost breakdown"
  value = {
    vpc                = "$0.00 (Free)"
    s3_storage        = "$0.00 (5GB Free Tier)"
    dynamodb          = "$0.00 (25GB Free Tier)"
    lambda_requests   = "$0.00 (1M requests Free Tier)"
    api_gateway       = "$0.00 (1M requests Free Tier)"
    cloudwatch_logs   = "~$0.50 (5GB Free Tier)"
    total_estimated   = "~$0.50/month"
  }
}

# ==========================================
# Configuration Summary
# ==========================================

output "configuration_summary" {
  description = "Summary of deployed configuration"
  value = {
    vpc_cidr              = var.vpc_cidr
    lambda_runtime        = var.lambda_runtime
    lambda_memory_size    = var.lambda_memory_size
    lambda_timeout        = var.lambda_timeout
    dynamodb_billing_mode = var.dynamodb_billing_mode
    s3_versioning_enabled = var.s3_versioning_enabled
    environment           = var.environment
    deployment_timestamp  = timestamp()
  }
}

# ==========================================
# Next Steps Information
# ==========================================

output "next_steps" {
  description = "Next steps after deployment"
  value = [
    "1. Update Lambda function code with actual implementation",
    "2. Configure EventBridge rules for automated processing",
    "3. Set up CloudWatch alarms and notifications",
    "4. Test API endpoints: ${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}/health",
    "5. Deploy frontend application and connect to API Gateway",
    "6. Configure AWS Budgets with cost alerts"
  ]
}

# ==========================================
# Resource URLs for Testing
# ==========================================

output "resource_urls" {
  description = "URLs for testing and management"
  value = {
    api_gateway_url = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
    health_check    = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}/health"
    aws_console = {
      lambda      = "https://console.aws.amazon.com/lambda/home?region=${var.aws_region}"
      dynamodb    = "https://console.aws.amazon.com/dynamodb/home?region=${var.aws_region}"
      s3          = "https://console.aws.amazon.com/s3/home?region=${var.aws_region}"
      api_gateway = "https://console.aws.amazon.com/apigateway/home?region=${var.aws_region}"
      cloudwatch  = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}"
    }
  }
}
