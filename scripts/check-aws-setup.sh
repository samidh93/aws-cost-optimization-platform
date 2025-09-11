#!/bin/bash

# AWS Free Tier Setup Checker
# This script checks if your AWS environment is ready for free tier development

echo "🚀 AWS Free Tier Setup Checker"
echo "================================"

# Check if AWS CLI is installed
if command -v aws &> /dev/null; then
    echo "✅ AWS CLI is installed"
    aws --version
else
    echo "❌ AWS CLI is not installed"
    echo "   Please install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if AWS credentials are configured
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ AWS credentials are configured"
    echo "   Account ID: $(aws sts get-caller-identity --query Account --output text)"
    echo "   User ARN: $(aws sts get-caller-identity --query Arn --output text)"
else
    echo "❌ AWS credentials not configured"
    echo "   Please run: aws configure"
    exit 1
fi

# Check if required tools are installed
echo ""
echo "🔧 Checking Required Tools..."

tools=("python3" "pip" "node" "npm" "docker" "kubectl" "cdk" "terraform" "ansible")

for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool is installed"
    else
        echo "❌ $tool is not installed"
    fi
done

# Check AWS region
echo ""
echo "🌍 AWS Configuration:"
echo "   Region: $(aws configure get region)"
echo "   Output: $(aws configure get output)"

# Check if we're in a good region for free tier
region=$(aws configure get region)
if [[ "$region" =~ ^(us-east-1|us-west-2|eu-west-1|ap-southeast-1)$ ]]; then
    echo "✅ Good region for free tier development"
else
    echo "⚠️  Consider using us-east-1, us-west-2, eu-west-1, or ap-southeast-1 for better free tier support"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Run: python3 scripts/check-free-tier.py"
echo "2. If all checks pass, run: ./scripts/setup.sh"
echo "3. Deploy with: ./scripts/deploy.sh"
echo "4. Always cleanup with: ./scripts/cleanup.sh"
