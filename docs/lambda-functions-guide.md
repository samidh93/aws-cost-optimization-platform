# AWS Lambda Functions Guide

## ⚡ **Serverless Cost Processing**

This guide covers the **serverless Lambda functions** that connect to AWS Cost Explorer API and process real-time cost data for the optimization platform.

## 🎯 **What We Built**

### **1. Cost Data Fetcher Lambda** 📊
**Purpose**: Fetch real cost data from AWS Cost Explorer API

**Features**:
- Calls AWS Cost Explorer API daily
- Fetches cost data by service, region, time period
- Stores processed data in DynamoDB
- Backs up raw data to S3
- Handles empty data gracefully (perfect for new AWS accounts)

**Input**: EventBridge schedule (daily at 6 AM)
**Output**: Cost data stored in DynamoDB

### **2. Budget Alert Processor Lambda** 🚨
**Purpose**: Monitor costs against budgets and generate alerts

**Features**:
- Reads cost data from DynamoDB
- Compares against configurable budget thresholds
- Generates alerts for budget violations
- Stores alerts in DynamoDB
- Ready for SNS/email/Slack notifications

**Input**: Cost data from DynamoDB
**Output**: Budget alerts stored in DynamoDB

### **3. Optimization Recommendation Engine Lambda** 💡
**Purpose**: Analyze cost patterns and generate optimization suggestions

**Features**:
- Analyzes historical cost data
- Identifies cost optimization opportunities
- Generates actionable recommendations
- Calculates potential savings
- Covers EC2, RDS, S3, EKS optimization

**Input**: Historical cost data
**Output**: Optimization recommendations stored in DynamoDB

## 🔧 **Technical Architecture**

### **Current State** (Local):
```
Frontend (React) → Backend (FastAPI) → SQLite Database
```

### **Phase 2 State** (Serverless):
```
Frontend (React) → API Gateway → Lambda Functions → DynamoDB
                                    ↓
                              AWS Cost Explorer API
```

## 📋 **Lambda Functions Details**

### **Cost Processor Lambda**
- **File**: `infrastructure/cdk/lambda/cost_processor/cost_processor.py`
- **Dependencies**: `boto3`, `botocore`
- **Environment Variables**: `COST_TABLE_NAME`, `S3_BUCKET`
- **Permissions**: Cost Explorer read, DynamoDB write, S3 write

### **Budget Alert Lambda**
- **File**: `infrastructure/cdk/lambda/budget_alert/budget_alert.py`
- **Dependencies**: `boto3`, `botocore`
- **Environment Variables**: `COST_TABLE_NAME`
- **Permissions**: Cost Explorer read, DynamoDB write

### **Cost Optimizer Lambda**
- **File**: `infrastructure/cdk/lambda/cost_optimizer/cost_optimizer.py`
- **Dependencies**: `boto3`, `botocore`
- **Environment Variables**: `COST_TABLE_NAME`, `S3_BUCKET`
- **Permissions**: Cost Explorer read, DynamoDB write

## 🚀 **Deployment Process**

### **1. Local Testing**
```bash
# Test Lambda function logic
COST_TABLE_NAME=test-table S3_BUCKET=test-bucket python scripts/test-lambda-simple.py
```

### **2. Deploy to AWS**
```bash
# Deploy Lambda functions
./scripts/deploy-lambda-functions.sh
```

### **3. Verify Deployment**
- Check AWS Console for deployed resources
- Test Lambda functions manually
- Verify DynamoDB tables created
- Confirm S3 bucket exists

## 💰 **Cost Benefits**

### **Serverless Advantages**:
- **Pay-per-use**: Only pay when functions execute
- **No server management**: AWS handles scaling
- **Automatic scaling**: Handles traffic spikes
- **Free tier**: 1M requests/month free

### **AWS Free Tier Limits**:
- **Lambda**: 1M requests/month, 400,000 GB-seconds
- **DynamoDB**: 25 GB storage, 25 RCU/WCU
- **API Gateway**: 1M API calls/month
- **EventBridge**: 1M events/month

## 🔄 **Data Flow**

### **Daily Process**:
1. **EventBridge** triggers Cost Fetcher Lambda (6 AM)
2. **Cost Fetcher** calls Cost Explorer API
3. **Data stored** in DynamoDB
4. **Budget Processor** analyzes data
5. **Alerts generated** if budgets exceeded
6. **Optimization Engine** runs analysis
7. **Recommendations** stored in DynamoDB
8. **Frontend** displays real-time data

## 🎯 **Real AWS Integration**

### **AWS Cost Explorer API Calls**:
- **GetCostAndUsage**: Daily cost data by service
- **GetDimensionValues**: Available services/regions
- **GetReservationCoverage**: Reserved instance usage
- **GetReservationUtilization**: RI utilization rates

### **AWS Budgets API**:
- **DescribeBudgets**: Get budget configurations
- **DescribeBudgetPerformanceHistory**: Budget vs actual costs
- **CreateBudget**: Set up new budgets
- **UpdateBudget**: Modify budget thresholds

## 📊 **Expected Results**

After Phase 2, your dashboard will show:
- **Real AWS costs** instead of sample data
- **Actual budget alerts** from your AWS account
- **Genuine optimization recommendations** based on your usage
- **Live cost trends** from Cost Explorer

## 🎯 **Perfect for New AWS Accounts**

### **Empty Data Handling**:
- **Graceful degradation**: Dashboard shows empty states
- **No errors**: Functions handle empty responses
- **Ready for data**: Same code works with real data
- **Safe testing**: No unexpected costs

### **Gradual Data Population**:
- **Start with empty data** (current state)
- **Add test services** (EC2, S3, etc.)
- **Watch data populate** in real-time
- **See dashboard come alive** with real data

## 🚀 **Next Steps**

### **Phase 3: Kubernetes Deployment**
- Containerize the backend
- Deploy to EKS cluster
- Helm charts for management

### **Phase 4: Full AWS Deployment**
- Deploy CDK infrastructure to AWS
- Set up RDS PostgreSQL
- Configure API Gateway

### **Phase 5: Advanced Features**
- Terraform modules for multi-account
- Ansible playbooks
- CI/CD pipeline

## 📚 **Development Commands**

```bash
# Test Lambda functions locally
COST_TABLE_NAME=test-table S3_BUCKET=test-bucket python scripts/test-lambda-simple.py

# Deploy to AWS
./scripts/deploy-lambda-functions.sh

# Check deployment status
aws lambda list-functions
aws dynamodb list-tables
aws s3 ls
```

## 🌐 **AWS Console Links**

- **Lambda Functions**: https://console.aws.amazon.com/lambda/
- **DynamoDB**: https://console.aws.amazon.com/dynamodb/
- **S3**: https://console.aws.amazon.com/s3/
- **EventBridge**: https://console.aws.amazon.com/events/
- **Cost Explorer**: https://console.aws.amazon.com/cost-management/home

Phase 2 transforms your demo into a real AWS cost optimization platform with serverless architecture and actual AWS integration! 🎉
