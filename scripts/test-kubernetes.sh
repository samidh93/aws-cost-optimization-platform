#!/bin/bash
# Test the containerized application on Kubernetes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 Testing containerized application on Kubernetes${NC}"

# Get ingress URL
INGRESS_URL=$(kubectl get ingress cost-optimization-ingress -n cost-optimization -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
if [ -z "$INGRESS_URL" ]; then
    echo -e "${RED}❌ Ingress URL not found. Please check if the ingress is ready.${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Testing URL: http://${INGRESS_URL}${NC}"

# Test endpoints
echo -e "${YELLOW}🔍 Testing endpoints...${NC}"

# Test health endpoint
echo -e "${YELLOW}1. Testing health endpoint...${NC}"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://${INGRESS_URL}/health)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Health endpoint: OK${NC}"
else
    echo -e "${RED}❌ Health endpoint: FAILED (HTTP ${HEALTH_RESPONSE})${NC}"
fi

# Test backend API
echo -e "${YELLOW}2. Testing backend API...${NC}"
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://${INGRESS_URL}/api/v1/cost/summary)
if [ "$API_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Backend API: OK${NC}"
else
    echo -e "${RED}❌ Backend API: FAILED (HTTP ${API_RESPONSE})${NC}"
fi

# Test frontend
echo -e "${YELLOW}3. Testing frontend...${NC}"
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://${INGRESS_URL}/)
if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend: OK${NC}"
else
    echo -e "${RED}❌ Frontend: FAILED (HTTP ${FRONTEND_RESPONSE})${NC}"
fi

# Test database connectivity
echo -e "${YELLOW}4. Testing database connectivity...${NC}"
DB_POD=$(kubectl get pods -n cost-optimization -l app=postgres -o jsonpath='{.items[0].metadata.name}')
if [ -n "$DB_POD" ]; then
    kubectl exec -n cost-optimization $DB_POD -- psql -U cost_user -d cost_optimization -c "SELECT COUNT(*) FROM cost_data;" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Database connectivity: OK${NC}"
    else
        echo -e "${RED}❌ Database connectivity: FAILED${NC}"
    fi
else
    echo -e "${RED}❌ Database pod not found${NC}"
fi

# Show pod status
echo -e "${YELLOW}📊 Pod Status:${NC}"
kubectl get pods -n cost-optimization

# Show service status
echo -e "${YELLOW}🔗 Service Status:${NC}"
kubectl get services -n cost-optimization

# Show ingress status
echo -e "${YELLOW}🌐 Ingress Status:${NC}"
kubectl get ingress -n cost-optimization

# Show HPA status
echo -e "${YELLOW}📈 HPA Status:${NC}"
kubectl get hpa -n cost-optimization

echo -e "${GREEN}🎉 Testing completed!${NC}"
echo -e "${YELLOW}📋 Access your application at: http://${INGRESS_URL}${NC}"
