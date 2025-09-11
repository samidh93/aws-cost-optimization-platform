#!/bin/bash

# Emergency Shutdown Script for Cost Optimization Platform
# This script will immediately destroy all AWS resources to stop costs

set -e

echo "🚨 EMERGENCY SHUTDOWN - Cost Optimization Platform"
echo "=================================================="
echo "⚠️  This will DELETE ALL AWS resources immediately!"
echo ""

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured!"
    exit 1
fi

# Get current costs
echo "💰 Checking current costs..."
aws ce get-cost-and-usage \
    --time-period Start=$(date -d '1 day ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity DAILY \
    --metrics BlendedCost \
    --query 'ResultsByTime[0].Total.BlendedCost.Amount' \
    --output text 2>/dev/null || echo "Unable to fetch costs"

echo ""
echo "🗑️  Starting emergency shutdown..."

# Method 1: CDK Destroy (if in CDK directory)
if [ -f "cdk.json" ]; then
    echo "📦 Using CDK destroy..."
    cdk destroy --force --all
else
    echo "📦 Using CloudFormation delete..."
    aws cloudformation delete-stack --stack-name CostOptimizationPlatform
fi

echo ""
echo "⏳ Waiting for resources to be deleted..."
echo "   This may take 5-15 minutes for EKS and RDS"

# Wait for stack deletion
aws cloudformation wait stack-delete-complete --stack-name CostOptimizationPlatform

echo ""
echo "✅ Emergency shutdown completed!"
echo "💡 All resources have been deleted"
echo "💰 Costs should stop accumulating immediately"

# Check final costs
echo ""
echo "💰 Final cost check..."
aws ce get-cost-and-usage \
    --time-period Start=$(date -d '1 day ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity DAILY \
    --metrics BlendedCost \
    --query 'ResultsByTime[0].Total.BlendedCost.Amount' \
    --output text 2>/dev/null || echo "Unable to fetch costs"
