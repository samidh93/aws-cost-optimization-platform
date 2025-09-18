#!/bin/bash

# AWS Cost Optimization Platform - CloudFormation Deployment Script
# This script deploys the infrastructure using AWS CloudFormation

set -e  # Exit on any error

# Configuration
STACK_NAME="cost-optimization-platform"
TEMPLATE_FILE="main-template.yaml"
REGION="us-east-1"
ENVIRONMENT="prod"
PROJECT_NAME="cost-optimization"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  AWS Cost Optimization Platform - CloudFormation${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_step() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Please run 'aws configure'."
        exit 1
    fi
    
    # Check if template exists
    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        print_error "Template file '$TEMPLATE_FILE' not found."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Validate CloudFormation template
validate_template() {
    print_step "Validating CloudFormation template..."
    
    if aws cloudformation validate-template \
        --template-body file://$TEMPLATE_FILE \
        --region $REGION > /dev/null; then
        print_success "Template validation passed"
    else
        print_error "Template validation failed"
        exit 1
    fi
}

# Check if stack exists
stack_exists() {
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION &> /dev/null
}

# Deploy stack
deploy_stack() {
    print_step "Deploying CloudFormation stack..."
    
    # Parameters
    PARAMETERS="ParameterKey=Environment,ParameterValue=$ENVIRONMENT"
    PARAMETERS="$PARAMETERS ParameterKey=ProjectName,ParameterValue=$PROJECT_NAME"
    
    if stack_exists; then
        print_info "Stack exists. Updating..."
        
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --parameters $PARAMETERS \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $REGION
        
        print_step "Waiting for stack update to complete..."
        aws cloudformation wait stack-update-complete \
            --stack-name $STACK_NAME \
            --region $REGION
            
        print_success "Stack updated successfully"
    else
        print_info "Creating new stack..."
        
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --parameters $PARAMETERS \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $REGION
        
        print_step "Waiting for stack creation to complete..."
        aws cloudformation wait stack-create-complete \
            --stack-name $STACK_NAME \
            --region $REGION
            
        print_success "Stack created successfully"
    fi
}

# Get stack outputs
get_outputs() {
    print_step "Retrieving stack outputs..."
    
    echo -e "\n${BLUE}📋 Stack Outputs:${NC}"
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
        --output table
}

# Get estimated costs
estimate_costs() {
    print_step "Cost estimation..."
    echo -e "\n${BLUE}💰 Estimated Monthly Costs:${NC}"
    echo "• VPC: $0.00 (Free)"
    echo "• S3 Bucket: $0.00 (5GB Free Tier)"
    echo "• DynamoDB: $0.00 (25GB Free Tier)"
    echo "• Lambda Functions: $0.00 (1M requests Free Tier)"
    echo "• API Gateway: $0.00 (1M requests Free Tier)"
    echo "• CloudWatch Logs: ~$0.50 (5GB Free Tier)"
    echo -e "${GREEN}Total Estimated Cost: ~$0.50/month${NC}"
}

# Main execution
main() {
    print_header
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    check_prerequisites
    validate_template
    deploy_stack
    get_outputs
    estimate_costs
    
    echo -e "\n${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${BLUE}📚 Next Steps:${NC}"
    echo "1. Update Lambda function code with actual implementation"
    echo "2. Configure EventBridge rules for automated processing"
    echo "3. Set up CloudWatch alarms and notifications"
    echo "4. Test the API endpoints"
    echo -e "\n${BLUE}🔗 API Gateway URL:${NC}"
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
        --output text
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "delete")
        print_header
        print_step "Deleting CloudFormation stack..."
        aws cloudformation delete-stack \
            --stack-name $STACK_NAME \
            --region $REGION
        print_step "Waiting for stack deletion to complete..."
        aws cloudformation wait stack-delete-complete \
            --stack-name $STACK_NAME \
            --region $REGION
        print_success "Stack deleted successfully"
        ;;
    "status")
        print_header
        print_step "Checking stack status..."
        aws cloudformation describe-stacks \
            --stack-name $STACK_NAME \
            --region $REGION \
            --query 'Stacks[0].[StackName,StackStatus]' \
            --output table
        ;;
    "outputs")
        print_header
        get_outputs
        ;;
    *)
        echo "Usage: $0 [deploy|delete|status|outputs]"
        echo "  deploy  - Deploy the CloudFormation stack (default)"
        echo "  delete  - Delete the CloudFormation stack"
        echo "  status  - Check stack status"
        echo "  outputs - Show stack outputs"
        exit 1
        ;;
esac
