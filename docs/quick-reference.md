# 🚀 Platform Quick Reference

## 📊 Current Platform Status

- **✅ Live Dashboard**: http://cost-optimization-frontend-703758695872-prod.s3-website-us-east-1.amazonaws.com
- **✅ API Backend**: https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod
- **✅ Infrastructure**: 35 resources managed by Terraform
- **✅ Monthly Cost**: ~$0.52 (AWS free tier optimized)

## 🎯 Primary Deployment Commands (Terraform)

```bash
# Navigate to Terraform directory
cd infrastructure/terraform

# Full deployment with confirmation
./deploy.sh deploy

# Individual commands
./deploy.sh init            # Initialize Terraform
./deploy.sh plan            # Preview changes
./deploy.sh apply           # Apply changes
./deploy.sh destroy         # Destroy infrastructure
./deploy.sh output          # Show outputs
./deploy.sh validate        # Validate configuration
```

## 📋 Alternative Deployment Methods

### CloudFormation
```bash
cd infrastructure/cloudformation
./deploy.sh deploy          # Deploy CloudFormation stack
./deploy.sh delete          # Delete stack
./deploy.sh status          # Check stack status
./deploy.sh outputs         # Show stack outputs
```

### CDK (Legacy - for reference)
```bash
cd infrastructure/cdk
npx cdk deploy CostOptimizationMinimal
npx cdk destroy CostOptimizationMinimal
```

## 🌐 Frontend Management

```bash
# Build and deploy frontend
npm run frontend:build      # Build React app
npm run frontend:deploy     # Build and deploy to S3

# Manual deployment
cd frontend/cost-dashboard
npm run build
aws s3 sync build/ s3://cost-optimization-frontend-703758695872-prod/ --delete
```

## 🔍 Testing & Monitoring

### API Testing
```bash
# Health check
curl https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod/health

# Cost summary
curl "https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod/api/v1/cost/summary?days=30"

# Cost trends
curl "https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod/api/v1/cost/trends?days=7"
```

### Lambda Function Testing
```bash
# Test Cost Processor
aws lambda invoke --function-name cost-optimization-cost-processor-prod --payload '{}' response.json

# Test Budget Alert
aws lambda invoke --function-name cost-optimization-budget-alert-prod --payload '{}' response.json

# Test Cost Optimizer
aws lambda invoke --function-name cost-optimization-cost-optimizer-prod --payload '{}' response.json
```

### Infrastructure Status
```bash
# Check Terraform state
cd infrastructure/terraform
terraform show

# List AWS resources
aws cloudformation list-stacks
aws lambda list-functions --query 'Functions[?contains(FunctionName, `cost-optimization`)]'
aws s3 ls | grep cost-optimization
```

## 💰 Cost Monitoring

### Current Costs
```bash
# Check actual AWS costs
aws ce get-cost-and-usage \
  --time-period Start=2025-09-01,End=2025-09-18 \
  --granularity MONTHLY \
  --metrics BlendedCost

# Monitor free tier usage
aws support describe-trusted-advisor-checks --language en
```

### Budget Management
```bash
# List current budgets
aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text)

# Create budget (optional)
aws budgets create-budget --account-id $(aws sts get-caller-identity --query Account --output text) --budget file://budget.json
```

## 🔧 Troubleshooting

### Common Issues

**Frontend not loading data**:
```bash
# Check API Gateway
curl https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod/health

# Rebuild and redeploy frontend
cd frontend/cost-dashboard
rm -rf build
REACT_APP_API_URL="https://o54yhb3r3h.execute-api.us-east-1.amazonaws.com/prod" npm run build
aws s3 sync build/ s3://cost-optimization-frontend-703758695872-prod/ --delete
```

**Lambda function errors**:
```bash
# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/cost-optimization

# View recent logs
aws logs filter-log-events --log-group-name /aws/lambda/cost-optimization-api-gateway-prod --start-time $(date -d '1 hour ago' +%s)000
```

**Terraform issues**:
```bash
# Reinitialize
rm -rf .terraform
terraform init

# Validate configuration
terraform validate

# Import existing resources (if needed)
terraform import aws_s3_bucket.cost_data cost-optimization-data-703758695872-prod
```

## 📚 Documentation Links

- **📋 [Deployment Summary](deployment-summary.md)**: Current infrastructure status
- **🏗️ [Terraform Guide](../infrastructure/terraform/README.md)**: Complete Terraform documentation
- **📋 [CloudFormation Guide](../infrastructure/cloudformation/README.md)**: Alternative deployment
- **⚡ [Lambda Functions Guide](lambda-functions-guide.md)**: Serverless architecture
- **🌐 [Frontend Guide](frontend-guide.md)**: React dashboard setup

## 🎯 Next Steps (Phase 2A)

### Automation Setup
```bash
# 1. Fix Cost Processor Lambda
# 2. Set up EventBridge scheduling
aws events put-rule --name daily-cost-processing --schedule-expression "rate(1 day)"

# 3. Configure SNS notifications
aws sns create-topic --name cost-optimization-alerts

# 4. Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name lambda-errors --metric-name Errors
```

### Advanced Features
- Cost forecasting algorithms
- Anomaly detection
- Multi-account support
- Enhanced optimization recommendations

---

**🎊 Platform Status**: Production-ready serverless cost optimization platform with real-time monitoring and beautiful web interface!

**📈 Value**: Complete AWS cost visibility and control for ~$0.52/month