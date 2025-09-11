#!/bin/bash
# Build and push container images to ECR

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 Building and pushing container images to ECR${NC}"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"

echo -e "${YELLOW}📋 Account ID: ${ACCOUNT_ID}${NC}"
echo -e "${YELLOW}🌍 Region: ${REGION}${NC}"

# ECR repository URIs
BACKEND_REPO="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/cost-optimization-backend"
FRONTEND_REPO="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/cost-optimization-frontend"
DATABASE_REPO="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/cost-optimization-database"

# Login to ECR
echo -e "${YELLOW}🔐 Logging in to ECR...${NC}"
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

# Build and push backend image
echo -e "${YELLOW}🔨 Building backend image...${NC}"
cd backend
docker build -t cost-optimization-backend:latest .
docker tag cost-optimization-backend:latest ${BACKEND_REPO}:latest
docker push ${BACKEND_REPO}:latest
echo -e "${GREEN}✅ Backend image pushed successfully${NC}"
cd ..

# Build and push frontend image
echo -e "${YELLOW}🔨 Building frontend image...${NC}"
cd frontend/cost-dashboard
docker build -t cost-optimization-frontend:latest .
docker tag cost-optimization-frontend:latest ${FRONTEND_REPO}:latest
docker push ${FRONTEND_REPO}:latest
echo -e "${GREEN}✅ Frontend image pushed successfully${NC}"
cd ../..

# Build and push database image
echo -e "${YELLOW}🔨 Building database image...${NC}"
cd database
docker build -t cost-optimization-database:latest .
docker tag cost-optimization-database:latest ${DATABASE_REPO}:latest
docker push ${DATABASE_REPO}:latest
echo -e "${GREEN}✅ Database image pushed successfully${NC}"
cd ..

echo -e "${GREEN}🎉 All images built and pushed successfully!${NC}"
echo -e "${YELLOW}📋 Image URIs:${NC}"
echo -e "  Backend:  ${BACKEND_REPO}:latest"
echo -e "  Frontend: ${FRONTEND_REPO}:latest"
echo -e "  Database: ${DATABASE_REPO}:latest"
