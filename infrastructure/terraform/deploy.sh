#!/bin/bash

# AWS Cost Optimization Platform - Terraform Deployment Script
# This script deploys the infrastructure using Terraform

set -e  # Exit on any error

# Configuration
ENVIRONMENT="prod"
PROJECT_NAME="cost-optimization"
AWS_REGION="us-east-1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  AWS Cost Optimization Platform - Terraform${NC}"
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
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed. Please install it first."
        print_info "Visit: https://www.terraform.io/downloads.html"
        exit 1
    fi
    
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
    
    # Check if terraform.tfvars exists
    if [[ ! -f "terraform.tfvars" ]]; then
        print_info "terraform.tfvars not found. Creating from example..."
        cp terraform.tfvars.example terraform.tfvars
        print_info "Please review and customize terraform.tfvars before proceeding."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Initialize Terraform
init_terraform() {
    print_step "Initializing Terraform..."
    
    terraform init
    
    print_success "Terraform initialized"
}

# Validate Terraform configuration
validate_terraform() {
    print_step "Validating Terraform configuration..."
    
    terraform validate
    
    print_success "Terraform configuration is valid"
}

# Format Terraform files
format_terraform() {
    print_step "Formatting Terraform files..."
    
    terraform fmt -recursive
    
    print_success "Terraform files formatted"
}

# Plan Terraform deployment
plan_terraform() {
    print_step "Planning Terraform deployment..."
    
    terraform plan -out=tfplan
    
    print_success "Terraform plan created"
}

# Apply Terraform deployment
apply_terraform() {
    print_step "Applying Terraform deployment..."
    
    terraform apply tfplan
    
    print_success "Terraform deployment completed"
}

# Show Terraform outputs
show_outputs() {
    print_step "Retrieving Terraform outputs..."
    
    echo -e "\n${BLUE}📋 Terraform Outputs:${NC}"
    terraform output
}

# Get estimated costs
estimate_costs() {
    print_step "Cost estimation..."
    echo -e "\n${BLUE}💰 Estimated Monthly Costs:${NC}"
    terraform output estimated_monthly_cost
}

# Destroy infrastructure
destroy_terraform() {
    print_step "Destroying Terraform infrastructure..."
    
    echo -e "${RED}⚠️  This will destroy ALL infrastructure!${NC}"
    read -p "Are you sure? Type 'yes' to confirm: " confirm
    
    if [[ $confirm == "yes" ]]; then
        terraform destroy -auto-approve
        print_success "Infrastructure destroyed"
    else
        print_info "Destruction cancelled"
    fi
}

# Main execution
main() {
    print_header
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    check_prerequisites
    init_terraform
    validate_terraform
    format_terraform
    plan_terraform
    
    # Ask for confirmation before applying
    echo -e "\n${YELLOW}📋 Review the plan above${NC}"
    read -p "Do you want to apply this plan? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        apply_terraform
        show_outputs
        estimate_costs
        
        echo -e "\n${GREEN}🎉 Deployment completed successfully!${NC}"
        echo -e "${BLUE}📚 Next Steps:${NC}"
        echo "1. Test the API endpoints"
        echo "2. Configure EventBridge rules for automated processing"
        echo "3. Set up CloudWatch alarms and notifications"
        echo "4. Deploy frontend application"
        
        echo -e "\n${BLUE}🔗 API Gateway URL:${NC}"
        terraform output -raw api_gateway_url
        echo ""
    else
        print_info "Deployment cancelled"
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "init")
        print_header
        cd "$(dirname "$0")"
        init_terraform
        ;;
    "plan")
        print_header
        cd "$(dirname "$0")"
        check_prerequisites
        init_terraform
        validate_terraform
        format_terraform
        plan_terraform
        ;;
    "apply")
        print_header
        cd "$(dirname "$0")"
        check_prerequisites
        init_terraform
        validate_terraform
        format_terraform
        apply_terraform
        show_outputs
        ;;
    "deploy")
        main
        ;;
    "destroy")
        print_header
        cd "$(dirname "$0")"
        destroy_terraform
        ;;
    "output")
        print_header
        cd "$(dirname "$0")"
        show_outputs
        ;;
    "validate")
        print_header
        cd "$(dirname "$0")"
        validate_terraform
        ;;
    "format")
        print_header
        cd "$(dirname "$0")"
        format_terraform
        ;;
    *)
        echo "Usage: $0 [init|plan|apply|deploy|destroy|output|validate|format]"
        echo ""
        echo "Commands:"
        echo "  init     - Initialize Terraform"
        echo "  plan     - Create execution plan"
        echo "  apply    - Apply the execution plan"
        echo "  deploy   - Full deployment (plan + apply with confirmation)"
        echo "  destroy  - Destroy infrastructure"
        echo "  output   - Show outputs"
        echo "  validate - Validate configuration"
        echo "  format   - Format Terraform files"
        exit 1
        ;;
esac
