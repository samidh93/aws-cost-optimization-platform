# AWS Cost Optimization Platform - Terraform Configuration
# This configuration deploys the infrastructure using only AWS free tier resources

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
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
}

# ==========================================
# VPC Infrastructure (Free)
# ==========================================

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc-${var.environment}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw-${var.environment}"
  }
}

# Public subnets (2 AZs for high availability)
resource "aws_subnet" "public" {
  count = 2

  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index + 1}-${var.environment}"
    Type = "Public"
  }
}

# Route table for public subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-routes-${var.environment}"
  }
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# ==========================================
# S3 Bucket for Cost Data Storage (5GB Free)
# ==========================================

resource "aws_s3_bucket" "cost_data" {
  bucket        = "${var.project_name}-data-${data.aws_caller_identity.current.account_id}-${var.environment}"
  force_destroy = true

  tags = {
    Name = "${var.project_name}-cost-data-${var.environment}"
  }
}

resource "aws_s3_bucket_versioning" "cost_data" {
  bucket = aws_s3_bucket.cost_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "cost_data" {
  bucket = aws_s3_bucket.cost_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "cost_data" {
  bucket = aws_s3_bucket.cost_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "cost_data" {
  bucket = aws_s3_bucket.cost_data.id

  rule {
    id     = "delete_old_versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 7
    }
  }
}

# ==========================================
# DynamoDB Table for Cost Tracking (25GB Free)
# ==========================================

resource "aws_dynamodb_table" "cost_tracking" {
  name           = "${var.project_name}-cost-tracking-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "account_id"
  range_key      = "timestamp"

  attribute {
    name = "account_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  point_in_time_recovery {
    enabled = false  # Disabled to save costs
  }

  tags = {
    Name = "${var.project_name}-cost-tracking-${var.environment}"
  }
}

# ==========================================
# IAM Roles for Lambda Functions
# ==========================================

# Lambda execution role
resource "aws_iam_role" "lambda_execution" {
  name = "${var.project_name}-lambda-execution-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-lambda-role-${var.environment}"
  }
}

# Basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# DynamoDB access policy
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "${var.project_name}-lambda-dynamodb-${var.environment}"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.cost_tracking.arn
      }
    ]
  })
}

# S3 access policy
resource "aws_iam_role_policy" "lambda_s3" {
  name = "${var.project_name}-lambda-s3-${var.environment}"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.cost_data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.cost_data.arn
      }
    ]
  })
}

# Cost Explorer access policy
resource "aws_iam_role_policy" "lambda_cost_explorer" {
  name = "${var.project_name}-lambda-cost-explorer-${var.environment}"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ce:GetCostAndUsage",
          "ce:GetDimensionValues",
          "ce:GetReservationCoverage",
          "ce:GetReservationPurchaseRecommendation",
          "ce:GetReservationUtilization",
          "ce:GetUsageReport"
        ]
        Resource = "*"
      }
    ]
  })
}

# ==========================================
# Lambda Function Code Archives
# ==========================================

# Create ZIP files for Lambda functions using existing CDK code
data "archive_file" "cost_processor" {
  type        = "zip"
  output_path = "${path.module}/lambda_packages/cost_processor.zip"
  source_dir  = "${path.root}/../cdk/lambda/cost_processor"
}

data "archive_file" "budget_alert" {
  type        = "zip"
  output_path = "${path.module}/lambda_packages/budget_alert.zip"
  source_dir  = "${path.root}/../cdk/lambda/budget_alert"
}

data "archive_file" "cost_optimizer" {
  type        = "zip"
  output_path = "${path.module}/lambda_packages/cost_optimizer.zip"
  source_dir  = "${path.root}/../cdk/lambda/cost_optimizer"
}

data "archive_file" "api_gateway" {
  type        = "zip"
  output_path = "${path.module}/lambda_packages/api_gateway.zip"
  source_dir  = "${path.root}/../cdk/lambda/api_gateway"
}

# ==========================================
# Lambda Functions (1M Requests Free)
# ==========================================

resource "aws_lambda_function" "cost_processor" {
  filename         = data.archive_file.cost_processor.output_path
  function_name    = "${var.project_name}-cost-processor-${var.environment}"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "cost_processor.handler"
  runtime         = "python3.11"
  timeout         = 120
  memory_size     = 128
  source_code_hash = data.archive_file.cost_processor.output_base64sha256

  environment {
    variables = {
      COST_TABLE_NAME = aws_dynamodb_table.cost_tracking.name
      S3_BUCKET      = aws_s3_bucket.cost_data.bucket
      ENVIRONMENT    = var.environment
    }
  }

  tags = {
    Name = "${var.project_name}-cost-processor-${var.environment}"
  }
}

resource "aws_lambda_function" "budget_alert" {
  filename         = data.archive_file.budget_alert.output_path
  function_name    = "${var.project_name}-budget-alert-${var.environment}"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "budget_alert.handler"
  runtime         = "python3.11"
  timeout         = 60
  memory_size     = 128
  source_code_hash = data.archive_file.budget_alert.output_base64sha256

  environment {
    variables = {
      COST_TABLE_NAME = aws_dynamodb_table.cost_tracking.name
      ENVIRONMENT    = var.environment
    }
  }

  tags = {
    Name = "${var.project_name}-budget-alert-${var.environment}"
  }
}

resource "aws_lambda_function" "cost_optimizer" {
  filename         = data.archive_file.cost_optimizer.output_path
  function_name    = "${var.project_name}-cost-optimizer-${var.environment}"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "cost_optimizer.handler"
  runtime         = "python3.11"
  timeout         = 120
  memory_size     = 128
  source_code_hash = data.archive_file.cost_optimizer.output_base64sha256

  environment {
    variables = {
      COST_TABLE_NAME = aws_dynamodb_table.cost_tracking.name
      S3_BUCKET      = aws_s3_bucket.cost_data.bucket
      ENVIRONMENT    = var.environment
    }
  }

  tags = {
    Name = "${var.project_name}-cost-optimizer-${var.environment}"
  }
}

resource "aws_lambda_function" "api_gateway" {
  filename         = data.archive_file.api_gateway.output_path
  function_name    = "${var.project_name}-api-gateway-${var.environment}"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "api_gateway.handler"
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 128
  source_code_hash = data.archive_file.api_gateway.output_base64sha256

  environment {
    variables = {
      COST_TABLE_NAME = aws_dynamodb_table.cost_tracking.name
      S3_BUCKET      = aws_s3_bucket.cost_data.bucket
      ENVIRONMENT    = var.environment
    }
  }

  tags = {
    Name = "${var.project_name}-api-gateway-${var.environment}"
  }
}

# ==========================================
# API Gateway (1M Requests Free)
# ==========================================

resource "aws_api_gateway_rest_api" "main" {
  name        = "${var.project_name}-api-${var.environment}"
  description = "Cost Optimization Platform API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "${var.project_name}-api-${var.environment}"
  }
}

# API Gateway Lambda permission
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_gateway.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

# Proxy resource (catch-all)
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "{proxy+}"
}

# ANY method for proxy resource
resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# OPTIONS method for CORS
resource "aws_api_gateway_method" "proxy_options" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# Integration for ANY method
resource "aws_api_gateway_integration" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.api_gateway.invoke_arn
}

# Integration for OPTIONS method
resource "aws_api_gateway_integration" "proxy_options" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.proxy_options.resource_id
  http_method = aws_api_gateway_method.proxy_options.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.api_gateway.invoke_arn
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_method.proxy,
    aws_api_gateway_integration.proxy,
    aws_api_gateway_method.proxy_options,
    aws_api_gateway_integration.proxy_options,
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = var.environment

  lifecycle {
    create_before_destroy = true
  }
}
