# Kubernetes Deployment Guide

## 🎯 Overview

This guide covers the containerized microservices architecture running on Amazon EKS (Elastic Kubernetes Service). The platform demonstrates enterprise-grade cloud architecture and production-ready deployment patterns for cost optimization workloads.

## 🏗️ Architecture

### **Serverless Architecture**
```
┌─────────────────┐
│   Lambda        │
│   (Serverless)  │
│   API Gateway   │
└─────────────────┘
```

### **Containerized Architecture**
```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Pod)         │◄──►│   (Pod)         │
│   React App     │    │   FastAPI       │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   Database      │
         │              │   (Pod)         │
         │              │   PostgreSQL    │
         │              └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│   Lambda        │    │   Lambda        │
│   (Serverless)  │    │   (Serverless)  │
│   Cost Processor│    │   Budget Alert  │
└─────────────────┘    └─────────────────┘
```

## 🐳 Containerized Services

### **1. Backend API (FastAPI)**
- **Container**: `cost-optimization-backend:latest`
- **Port**: 8000
- **Replicas**: 3 (auto-scaling 2-10)
- **Database**: PostgreSQL (containerized)
- **Features**: Health checks, resource limits, IAM roles

### **2. Frontend App (React)**
- **Container**: `cost-optimization-frontend:latest`
- **Port**: 80 (Nginx)
- **Replicas**: 2 (auto-scaling 2-5)
- **Features**: Static file serving, API proxy, gzip compression

### **3. Database (PostgreSQL)**
- **Container**: `cost-optimization-database:latest`
- **Port**: 5432
- **Replicas**: 1
- **Features**: Persistent storage, initialization scripts, health checks

## 🚀 Deployment Process

### **Container Image Management**
```bash
# Build and push all container images to ECR
./scripts/build-and-push-images.sh
```

### **EKS Cluster Deployment**
```bash
# Deploy EKS cluster and containerized services
./scripts/deploy-eks.sh
```

### **Application Validation**
```bash
# Test the containerized application
./scripts/test-kubernetes.sh
```

## 📋 Kubernetes Manifests

### **Core Components**
- **Namespace**: `cost-optimization`
- **ConfigMap**: Application configuration
- **Secret**: Sensitive data (passwords, keys)
- **Deployments**: Application replicas
- **Services**: Internal networking
- **Ingress**: External access
- **HPA**: Auto-scaling

### **File Structure**
```
kubernetes/
├── namespace.yaml           # Namespace definition
├── configmap.yaml          # Application configuration
├── secret.yaml             # Sensitive data
├── database-deployment.yaml # PostgreSQL deployment
├── backend-deployment.yaml  # FastAPI deployment
├── frontend-deployment.yaml # React deployment
├── ingress.yaml            # External access
└── hpa.yaml               # Auto-scaling
```

## 🔧 Configuration

### **Environment Variables**
```yaml
# Backend Configuration
DATABASE_URL: "postgresql://cost_user:cost_password@postgres-service:5432/cost_optimization"
AWS_REGION: "us-east-1"
ENVIRONMENT: "production"
LOG_LEVEL: "INFO"

# Frontend Configuration
REACT_APP_API_URL: "http://backend-service:8000"
```

### **Resource Limits**
```yaml
# Backend Resources
requests:
  memory: "256Mi"
  cpu: "250m"
limits:
  memory: "512Mi"
  cpu: "500m"

# Frontend Resources
requests:
  memory: "128Mi"
  cpu: "100m"
limits:
  memory: "256Mi"
  cpu: "200m"
```

## 🌐 Networking

### **Service Discovery**
- **Frontend** → **Backend**: `http://backend-service:8000`
- **Backend** → **Database**: `postgres-service:5432`
- **External** → **Frontend**: `http://ingress-url/`

### **Load Balancing**
- **AWS Load Balancer Controller**: Manages ALB
- **Kubernetes Service**: Internal load balancing
- **Ingress**: External traffic routing

## 📊 Monitoring and Scaling

### **Auto-Scaling**
- **HPA**: CPU and memory-based scaling
- **Backend**: 2-10 replicas
- **Frontend**: 2-5 replicas

### **Health Checks**
- **Liveness Probe**: Container health
- **Readiness Probe**: Service readiness
- **Startup Probe**: Initial startup

### **Resource Management**
- **Requests**: Guaranteed resources
- **Limits**: Maximum resources
- **QoS**: Quality of Service classes

## 🔒 Security

### **IAM Roles for Service Accounts (IRSA)**
- **Backend Role**: DynamoDB, S3 access
- **Load Balancer Role**: ALB management
- **No hardcoded credentials**

### **Network Security**
- **Private Subnets**: Worker nodes
- **Security Groups**: Controlled access
- **VPC**: Isolated network

## 💰 Cost Optimization

### **Free Tier Eligible**
- **EKS Cluster**: Management free
- **t3.micro instances**: 750 hours/month
- **ALB**: Classic Load Balancer free

### **Resource Efficiency**
- **Right-sizing**: Appropriate resource limits
- **Auto-scaling**: Scale based on demand
- **Spot instances**: Optional for cost savings

## 🧪 Testing

### **Health Checks**
```bash
# Test health endpoint
curl http://ingress-url/health

# Test API endpoint
curl http://ingress-url/api/v1/cost/summary

# Test frontend
curl http://ingress-url/
```

### **Pod Status**
```bash
# Check pod status
kubectl get pods -n cost-optimization

# Check service status
kubectl get services -n cost-optimization

# Check ingress status
kubectl get ingress -n cost-optimization
```

## 🚀 Benefits

### **1. Scalability**
- **Horizontal scaling**: Add more pods
- **Auto-scaling**: Based on metrics
- **Load distribution**: Across multiple pods

### **2. Reliability**
- **High availability**: Multiple replicas
- **Health checks**: Automatic recovery
- **Rolling updates**: Zero downtime

### **3. Portability**
- **Container-based**: Run anywhere
- **Kubernetes**: Industry standard
- **Cloud agnostic**: Multi-cloud ready

### **4. Advanced Features**
- **Service mesh**: Advanced networking
- **Observability**: Comprehensive monitoring
- **GitOps**: Declarative deployment

## 🎯 Platform Capabilities

Upon completion, the platform provides:
- **Containerized microservices** running on EKS
- **Production-ready** deployment patterns
- **Enterprise Kubernetes** capabilities
- **Hybrid architecture** (containers + serverless)

**Next: Infrastructure as Code** or **CI/CD Pipeline** implementation! 🚀
