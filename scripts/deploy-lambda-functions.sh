#!/bin/bash

# Lambda Functions Deployment Script
# Deploys the Lambda functions to AWS using CDK

set -e

echo "🚀 Deploying Lambda Functions to AWS"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "infrastructure/cdk/app.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured"
    echo "📋 Please run: aws configure"
    exit 1
fi

echo "✅ AWS CLI is configured"

# Check if CDK is available
if ! command -v npx &> /dev/null; then
    echo "❌ npx is not available"
    echo "📋 Please install Node.js and npm"
    exit 1
fi

echo "✅ npx is available"

# Navigate to CDK directory
cd infrastructure/cdk

# Install CDK dependencies
echo "📦 Installing CDK dependencies..."
npm install

# Bootstrap CDK (if needed)
echo "🔧 Bootstrapping CDK..."
npx cdk bootstrap

# Deploy the stack
echo "🚀 Deploying Lambda functions..."
npx cdk deploy --require-approval never

echo ""
echo "🎉 Lambda functions deployed successfully!"
echo ""
echo "📋 What was deployed:"
echo "  ✅ Cost Processor Lambda - Fetches cost data from Cost Explorer"
echo "  ✅ Budget Alert Lambda - Monitors costs against budgets"
echo "  ✅ Cost Optimizer Lambda - Generates optimization recommendations"
echo "  ✅ DynamoDB Tables - Store cost data, alerts, and recommendations"
echo "  ✅ S3 Bucket - Store raw cost data"
echo "  ✅ EventBridge Rules - Schedule daily cost processing"
echo ""
echo "🔧 Next steps:"
echo "  1. Check AWS Console for deployed resources"
echo "  2. Test Lambda functions manually"
echo "  3. Set up EventBridge schedules"
echo "  4. Update frontend to use Lambda API endpoints"
echo ""
echo "💰 Cost monitoring:"
echo "  - Lambda functions run on-demand (pay-per-use)"
echo "  - DynamoDB has free tier (25 GB, 25 RCU/WCU)"
echo "  - S3 has free tier (5 GB storage)"
echo "  - EventBridge has free tier (1M events/month)"
echo ""
echo "🌐 Access your resources:"
echo "  - AWS Console: https://console.aws.amazon.com/"
echo "  - Lambda Functions: https://console.aws.amazon.com/lambda/"
echo "  - DynamoDB: https://console.aws.amazon.com/dynamodb/"
echo "  - S3: https://console.aws.amazon.com/s3/"
