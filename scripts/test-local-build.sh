#!/bin/bash
# Test local Docker builds without pushing to ECR

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 Testing local Docker builds${NC}"

# Test backend build
echo -e "${YELLOW}🔨 Testing backend build...${NC}"
cd backend
docker build -t cost-optimization-backend:test .
echo -e "${GREEN}✅ Backend build successful${NC}"
cd ..

# Test frontend build
echo -e "${YELLOW}🔨 Testing frontend build...${NC}"
cd frontend/cost-dashboard
docker build -t cost-optimization-frontend:test .
echo -e "${GREEN}✅ Frontend build successful${NC}"
cd ../..

# Test database build
echo -e "${YELLOW}🔨 Testing database build...${NC}"
cd database
docker build -t cost-optimization-database:test .
echo -e "${GREEN}✅ Database build successful${NC}"
cd ..

echo -e "${GREEN}🎉 All local builds successful!${NC}"
echo -e "${YELLOW}📋 Built images:${NC}"
echo -e "  Backend:  cost-optimization-backend:test"
echo -e "  Frontend: cost-optimization-frontend:test"
echo -e "  Database: cost-optimization-database:test"

# Clean up test images
echo -e "${YELLOW}🧹 Cleaning up test images...${NC}"
docker rmi cost-optimization-backend:test cost-optimization-frontend:test cost-optimization-database:test
echo -e "${GREEN}✅ Cleanup complete${NC}"
