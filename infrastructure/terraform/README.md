# AWS Cost Optimization Platform - Terraform

This directory contains Terraform configuration for deploying the Cost Optimization Platform infrastructure using Infrastructure as Code (IaC).

## 📋 Overview

The Terraform configuration creates a complete serverless infrastructure using AWS free tier resources:

- **VPC**: Basic networking with public subnets (Free)
- **S3 Bucket**: Cost data storage (5GB Free Tier)
- **DynamoDB**: Cost tracking database (25GB Free Tier)
- **Lambda Functions**: Cost processing, budget alerts, optimization (1M requests Free Tier)
- **API Gateway**: RESTful API (1M requests Free Tier)

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │   Lambda        │
│   (React)       │───▶│   (REST API)     │───▶│   Functions     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   S3 Bucket      │    │   DynamoDB      │
                       │   (Raw Data)     │◀───│   (Cost Data)   │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Deployment

### Prerequisites

1. **Terraform installed** (>= 1.0):
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
   unzip terraform_1.6.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

2. **AWS CLI installed and configured**:
   ```bash
   aws configure
   ```

3. **Required AWS permissions**:
   - VPC, S3, DynamoDB, Lambda, API Gateway, IAM permissions

### Deploy

```bash
# Navigate to Terraform directory
cd infrastructure/terraform

# Copy and customize variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your preferences

# Make deploy script executable
chmod +x deploy.sh

# Deploy the infrastructure
./deploy.sh deploy
```

### Alternative: Manual Deployment

```bash
# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

## 📁 File Structure

```
infrastructure/terraform/
├── main.tf                    # Main infrastructure configuration
├── variables.tf               # Variable definitions
├── outputs.tf                 # Output definitions
├── versions.tf                # Provider version constraints
├── terraform.tfvars.example  # Example variables file
├── deploy.sh                  # Deployment script
├── README.md                  # This file
└── lambda_packages/           # Generated Lambda ZIP files
```

## 🔧 Configuration Variables

### Core Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `aws_region` | AWS region for deployment | `us-east-1` | No |
| `environment` | Environment name | `prod` | No |
| `project_name` | Project name for resources | `cost-optimization` | No |
| `vpc_cidr` | VPC CIDR block | `10.0.0.0/16` | No |

### Lambda Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `lambda_runtime` | Python runtime version | `python3.11` |
| `lambda_memory_size` | Memory allocation (MB) | `128` |
| `lambda_timeout` | Timeout in seconds | `120` |

### Storage Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `dynamodb_billing_mode` | DynamoDB billing mode | `PAY_PER_REQUEST` |
| `s3_versioning_enabled` | Enable S3 versioning | `true` |
| `s3_lifecycle_days` | Days to keep old versions | `7` |

## 📊 Outputs

After deployment, Terraform provides these outputs:

### Network Outputs
- `vpc_id`: VPC identifier
- `public_subnet_ids`: Public subnet identifiers
- `internet_gateway_id`: Internet Gateway identifier

### Storage Outputs
- `s3_bucket_name`: Cost data bucket name
- `dynamodb_table_name`: Cost tracking table name

### Compute Outputs
- `api_gateway_url`: API Gateway endpoint URL
- Lambda function ARNs for all functions

### Management Outputs
- `estimated_monthly_cost`: Cost breakdown
- `configuration_summary`: Deployment configuration
- `next_steps`: Post-deployment tasks
- `resource_urls`: AWS Console URLs

## 🔧 Management Commands

The deployment script provides several commands:

```bash
# Initialize Terraform
./deploy.sh init

# Create execution plan
./deploy.sh plan

# Apply changes
./deploy.sh apply

# Full deployment with confirmation
./deploy.sh deploy

# Show outputs
./deploy.sh output

# Validate configuration
./deploy.sh validate

# Format Terraform files
./deploy.sh format

# Destroy infrastructure
./deploy.sh destroy
```

## 💰 Cost Breakdown

| Resource | Free Tier Limit | Monthly Cost |
|----------|-----------------|--------------|
| VPC | Always free | $0.00 |
| S3 Standard | 5GB | $0.00 |
| DynamoDB | 25GB storage, 25 RCU/WCU | $0.00 |
| Lambda | 1M requests, 400K GB-seconds | $0.00 |
| API Gateway | 1M REST API calls | $0.00 |
| CloudWatch Logs | 5GB ingestion | $0.00 |
| **Total** | | **~$0.50/month** |

## 🔄 Key Features

### 1. **Reuses Existing Lambda Code**
- Uses actual Lambda implementations from `../cdk/lambda/`
- No duplicate code maintenance
- Consistent functionality across deployment methods

### 2. **Free Tier Optimized**
- All resources designed for AWS free tier
- Minimal memory and timeout configurations
- Pay-per-request billing modes

### 3. **Production Ready**
- Proper IAM roles with least privilege
- VPC with public subnets
- S3 encryption and lifecycle policies
- DynamoDB with appropriate billing mode

### 4. **Comprehensive Monitoring**
- CloudWatch integration
- Detailed outputs for monitoring setup
- Cost estimation and tracking

## 🔍 Terraform vs CDK vs CloudFormation

### **Terraform Advantages:**
- ✅ **Multi-cloud support**: Can extend to Azure, GCP
- ✅ **HCL syntax**: More readable than JSON/YAML
- ✅ **State management**: Explicit state tracking
- ✅ **Plan/Apply workflow**: Preview changes before applying
- ✅ **Module ecosystem**: Rich community modules
- ✅ **Variable validation**: Built-in input validation

### **When to Use Terraform:**
- Multi-cloud deployments
- Team prefers HCL over Python
- Need explicit state management
- Want to leverage Terraform modules
- Standardizing on Terraform across organization

### **When to Use CDK:**
- AWS-only deployment
- Team prefers Python/TypeScript
- Want type safety and IDE support
- Need complex logic in infrastructure code

## 🛠️ Troubleshooting

### Common Issues

1. **Terraform initialization fails**:
   ```bash
   # Clear cache and reinitialize
   rm -rf .terraform
   terraform init
   ```

2. **Lambda deployment fails**:
   ```bash
   # Check if Lambda code exists
   ls -la ../cdk/lambda/
   
   # Manually create ZIP files
   terraform plan  # This triggers archive creation
   ```

3. **AWS credentials issues**:
   ```bash
   # Verify credentials
   aws sts get-caller-identity
   
   # Check region
   aws configure get region
   ```

4. **State file conflicts**:
   ```bash
   # For development only - removes state
   rm terraform.tfstate*
   terraform import [resource] [id]  # Re-import existing resources
   ```

### Debug Commands

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform plan

# Validate configuration
terraform validate

# Check formatting
terraform fmt -check

# Show current state
terraform show

# List resources
terraform state list
```

## 🔐 Security Considerations

### IAM Roles
- Lambda execution role with minimal permissions
- Separate policies for DynamoDB, S3, and Cost Explorer
- No wildcard permissions except where required (Cost Explorer)

### Network Security
- VPC with public subnets only (no private subnets to avoid NAT costs)
- Security groups with minimal required access
- S3 bucket with public access blocked

### Data Encryption
- S3 server-side encryption (AES256)
- DynamoDB encryption at rest (AWS managed)
- Lambda environment variables (no sensitive data)

## 📚 Next Steps

After successful deployment:

1. **Test Infrastructure**:
   ```bash
   # Test API Gateway
   curl $(terraform output -raw api_gateway_url)/health
   
   # Check Lambda functions
   aws lambda list-functions --query 'Functions[?contains(FunctionName, `cost-optimization`)]'
   ```

2. **Configure Monitoring**:
   ```bash
   # Create CloudWatch dashboard
   # Set up cost budgets
   # Configure SNS notifications
   ```

3. **Deploy Frontend**:
   ```bash
   # Update frontend API URL
   export REACT_APP_API_URL=$(terraform output -raw api_gateway_url)
   
   # Build and deploy frontend
   cd ../../frontend/cost-dashboard
   npm run build
   ```

4. **Set Up Automation**:
   ```bash
   # Configure EventBridge rules
   # Set up automated cost processing
   # Configure budget alerts
   ```

## 🔗 Related Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

---

**Note**: This Terraform configuration reuses the existing Lambda function code from the CDK implementation, ensuring consistency across deployment methods while providing the flexibility and features of Terraform's Infrastructure as Code approach.
