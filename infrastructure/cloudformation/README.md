# AWS Cost Optimization Platform - CloudFormation

This directory contains AWS CloudFormation templates for deploying the Cost Optimization Platform infrastructure.

## 📋 Overview

The CloudFormation template creates a complete serverless infrastructure using only AWS free tier resources:

- **VPC**: Basic networking (Free)
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

1. **AWS CLI installed and configured**:
   ```bash
   aws configure
   ```

2. **Required permissions**:
   - CloudFormation full access
   - IAM role creation
   - VPC, S3, DynamoDB, Lambda, API Gateway permissions

### Deploy

```bash
# Navigate to CloudFormation directory
cd infrastructure/cloudformation

# Make deploy script executable
chmod +x deploy.sh

# Deploy the stack
./deploy.sh deploy
```

### Alternative: Manual Deployment

```bash
aws cloudformation create-stack \
  --stack-name cost-optimization-platform \
  --template-body file://main-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=prod \
               ParameterKey=ProjectName,ParameterValue=cost-optimization \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

## 📊 Stack Outputs

After deployment, the stack provides these outputs:

| Output | Description | Example |
|--------|-------------|---------|
| `VpcId` | VPC identifier | `vpc-12345678` |
| `S3BucketName` | Cost data bucket | `cost-optimization-data-123456789-prod` |
| `DynamoDBTableName` | Cost tracking table | `cost-optimization-cost-tracking-prod` |
| `ApiGatewayUrl` | API endpoint | `https://abc123.execute-api.us-east-1.amazonaws.com/prod` |
| `CostProcessorFunctionArn` | Cost processor Lambda | `arn:aws:lambda:...` |

## 🔧 Management Commands

```bash
# Check stack status
./deploy.sh status

# View stack outputs
./deploy.sh outputs

# Update existing stack
./deploy.sh deploy

# Delete stack
./deploy.sh delete
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

## 📝 Template Structure

### Parameters

- `Environment`: Deployment environment (dev/staging/prod)
- `ProjectName`: Project name for resource naming

### Resources Created

1. **Networking**:
   - VPC with public subnets
   - Internet Gateway
   - Route tables

2. **Storage**:
   - S3 bucket with versioning and lifecycle rules
   - DynamoDB table with pay-per-request billing

3. **Compute**:
   - Cost Processor Lambda
   - Budget Alert Lambda
   - Cost Optimizer Lambda
   - API Gateway Lambda

4. **API**:
   - API Gateway with proxy integration
   - CORS configuration

5. **Security**:
   - IAM roles with least privilege access
   - S3 bucket policies
   - Lambda execution roles

## 🔄 Updates and Maintenance

### Updating Lambda Code

1. **Package your code**:
   ```bash
   cd ../../backend/lambda/cost_processor
   zip -r cost_processor.zip .
   ```

2. **Update function**:
   ```bash
   aws lambda update-function-code \
     --function-name cost-optimization-cost-processor-prod \
     --zip-file fileb://cost_processor.zip
   ```

### Scaling Considerations

The template is designed for free tier usage. For production scaling:

1. **DynamoDB**: Switch to provisioned billing mode
2. **Lambda**: Increase memory/timeout based on workload
3. **API Gateway**: Consider caching for frequently accessed endpoints
4. **S3**: Implement Intelligent Tiering for cost optimization

## 🔍 Monitoring

### CloudWatch Dashboards

After deployment, create custom dashboards to monitor:

- Lambda function invocations and errors
- DynamoDB read/write capacity
- API Gateway request count and latency
- S3 bucket size and requests

### Alarms

Set up CloudWatch alarms for:

- Lambda function errors > 5%
- DynamoDB throttling events
- API Gateway 4xx/5xx errors > 10%
- Unusual cost spikes

## 🛠️ Troubleshooting

### Common Issues

1. **Stack creation fails**:
   - Check AWS credentials and permissions
   - Verify region supports all services
   - Check CloudFormation events for specific errors

2. **Lambda functions fail**:
   - Check CloudWatch logs
   - Verify environment variables
   - Test function permissions

3. **API Gateway returns 500**:
   - Check Lambda function logs
   - Verify API Gateway integration
   - Test Lambda function directly

### Debug Commands

```bash
# Check stack events
aws cloudformation describe-stack-events \
  --stack-name cost-optimization-platform

# View Lambda logs
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/cost-optimization

# Test API Gateway
curl -X GET https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/health
```

## 📚 Next Steps

After successful deployment:

1. **Update Lambda Functions**: Replace placeholder code with actual implementation
2. **Configure EventBridge**: Set up scheduled cost processing
3. **Deploy Frontend**: Connect React app to API Gateway
4. **Set up Monitoring**: Create CloudWatch dashboards and alarms
5. **Configure Budgets**: Set up AWS Budgets with alerts

## 🔗 Related Resources

- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [AWS Free Tier](https://aws.amazon.com/free/)

---

**Note**: This CloudFormation template is designed for the minimal, free-tier version of the Cost Optimization Platform. For production deployments with higher scale requirements, consider the CDK version with additional features like VPC endpoints, enhanced monitoring, and auto-scaling capabilities.
