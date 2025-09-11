#!/bin/bash
# Deploy EKS cluster and containerized services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying EKS cluster and containerized services${NC}"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"

echo -e "${YELLOW}📋 Account ID: ${ACCOUNT_ID}${NC}"
echo -e "${YELLOW}🌍 Region: ${REGION}${NC}"

# Deploy EKS stack
echo -e "${YELLOW}🏗️  Deploying EKS stack...${NC}"
cd infrastructure/cdk
npx cdk deploy CostOptimizationEKS --app app-eks.py --require-approval never
echo -e "${GREEN}✅ EKS stack deployed successfully${NC}"

# Get EKS cluster name
CLUSTER_NAME=$(aws eks list-clusters --region ${REGION} --query 'clusters[0]' --output text)
echo -e "${YELLOW}📋 EKS Cluster: ${CLUSTER_NAME}${NC}"

# Update kubeconfig
echo -e "${YELLOW}🔧 Updating kubeconfig...${NC}"
aws eks update-kubeconfig --region ${REGION} --name ${CLUSTER_NAME}
echo -e "${GREEN}✅ Kubeconfig updated${NC}"

# Verify cluster access
echo -e "${YELLOW}🔍 Verifying cluster access...${NC}"
kubectl get nodes
echo -e "${GREEN}✅ Cluster access verified${NC}"

# Update Kubernetes manifests with account ID
echo -e "${YELLOW}📝 Updating Kubernetes manifests...${NC}"
cd ../../kubernetes

# Replace placeholder account ID in manifests
sed -i.bak "s/YOUR_ACCOUNT_ID/${ACCOUNT_ID}/g" backend-deployment.yaml
sed -i.bak "s/YOUR_ACCOUNT_ID/${ACCOUNT_ID}/g" frontend-deployment.yaml

# Apply Kubernetes manifests
echo -e "${YELLOW}📦 Applying Kubernetes manifests...${NC}"

# Create namespace
kubectl apply -f namespace.yaml
echo -e "${GREEN}✅ Namespace created${NC}"

# Apply configuration
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
echo -e "${GREEN}✅ Configuration applied${NC}"

# Deploy database
kubectl apply -f database-deployment.yaml
echo -e "${GREEN}✅ Database deployed${NC}"

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/postgres -n cost-optimization
echo -e "${GREEN}✅ Database is ready${NC}"

# Deploy backend
kubectl apply -f backend-deployment.yaml
echo -e "${GREEN}✅ Backend deployed${NC}"

# Wait for backend to be ready
echo -e "${YELLOW}⏳ Waiting for backend to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/backend-api -n cost-optimization
echo -e "${GREEN}✅ Backend is ready${NC}"

# Deploy frontend
kubectl apply -f frontend-deployment.yaml
echo -e "${GREEN}✅ Frontend deployed${NC}"

# Wait for frontend to be ready
echo -e "${YELLOW}⏳ Waiting for frontend to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/frontend-app -n cost-optimization
echo -e "${GREEN}✅ Frontend is ready${NC}"

# Deploy ingress
kubectl apply -f ingress.yaml
echo -e "${GREEN}✅ Ingress deployed${NC}"

# Deploy HPA
kubectl apply -f hpa.yaml
echo -e "${GREEN}✅ HPA deployed${NC}"

# Get ingress URL
echo -e "${YELLOW}🔍 Getting ingress URL...${NC}"
INGRESS_URL=$(kubectl get ingress cost-optimization-ingress -n cost-optimization -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
if [ -z "$INGRESS_URL" ]; then
    echo -e "${YELLOW}⏳ Waiting for ingress URL...${NC}"
    sleep 30
    INGRESS_URL=$(kubectl get ingress cost-optimization-ingress -n cost-optimization -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
fi

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${YELLOW}📋 Access URLs:${NC}"
echo -e "  Frontend: http://${INGRESS_URL}"
echo -e "  Backend API: http://${INGRESS_URL}/api"
echo -e "  Health Check: http://${INGRESS_URL}/health"

# Show pod status
echo -e "${YELLOW}📊 Pod Status:${NC}"
kubectl get pods -n cost-optimization

# Show services
echo -e "${YELLOW}🔗 Services:${NC}"
kubectl get services -n cost-optimization

# Show ingress
echo -e "${YELLOW}🌐 Ingress:${NC}"
kubectl get ingress -n cost-optimization
