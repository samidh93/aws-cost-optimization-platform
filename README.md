# AWS Cost Optimization Platform

A comprehensive multi-cloud cost monitoring and optimization platform built with AWS CDK, Kubernetes, and modern web technologies. Features real-time cost tracking, budget alerts, optimization recommendations, and a beautiful React dashboard.

## 🚀 Technologies

- **Infrastructure**: AWS CDK, EKS, Lambda, DynamoDB, S3, ECR
- **Frontend**: React, Material-UI, Recharts
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **DevOps**: GitHub Actions, Docker, Kubernetes
- **Monitoring**: CloudWatch, Cost Explorer

## 💰 Cost Management Features

- **Real-time cost tracking** across AWS services
- **Intelligent budget alerts** and notifications
- **Automated optimization recommendations**
- **Multi-account cost aggregation**
- **Free tier compliant architecture**

## 🏗️ Architecture

### Frontend Dashboard ✅
- React-based cost visualization dashboard
- Material-UI components for modern UI
- Recharts for interactive charts and graphs
- Responsive design for all devices

### AWS Lambda Functions ✅
- Serverless cost processing functions
- Budget alert monitoring
- Optimization recommendation engine
- API Gateway integration

### Kubernetes Workloads 🚧
- Containerized microservices on EKS
- Auto-scaling based on demand
- High availability with multiple replicas
- Production-ready deployment patterns

### Infrastructure as Code (Planned)
- Multi-account infrastructure as code
- Centralized billing management
- Environment-specific deployments

### Configuration Management (Planned)
- Configuration management automation
- Security hardening
- Compliance automation

### CI/CD Pipeline (Planned)
- GitHub Actions for automated deployment
- Environment promotion
- Rollback capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended: use pyenv)
- Node.js 18+
- Docker
- AWS CLI configured
- kubectl (for Kubernetes)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/samidh93/aws-cost-optimization-platform.git
   cd aws-cost-optimization-platform
   ```

2. **Set up Python environment**
   ```bash
   # Install pyenv (if not installed)
   brew install pyenv
   
   # Install Python 3.11
   pyenv install 3.11.0
   pyenv local 3.11.0
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd frontend/cost-dashboard
   npm install
   npm start
   ```

4. **Start backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

### AWS Deployment

1. **Deploy ECR repositories**
   ```bash
   cd infrastructure/cdk
   npx cdk deploy CostOptimizationECR --app "python app-ecr-only.py"
   ```

2. **Build and push images** (via GitHub Actions)
   - Add AWS credentials as GitHub secrets
   - Push to main branch to trigger workflow

3. **Deploy to EKS** (coming soon)
   ```bash
   ./scripts/deploy-eks.sh
   ```

## 📊 Cost Analysis

### Free Tier Eligible Resources
- **EKS Cluster**: Management free (pay only for worker nodes)
- **t3.micro instances**: 750 hours/month free
- **ECR Storage**: 500 MB/month free
- **Lambda**: 1M requests/month free
- **DynamoDB**: 25 GB storage free
- **S3**: 5 GB storage free

### Expected Monthly Cost
- **Development**: $0-5 (minimal usage)
- **Production**: $10-50 (depending on usage)

## 🔧 Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/costdb
AWS_REGION=us-east-1
ENVIRONMENT=development

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

## 📈 Monitoring

### Health Checks
- **Backend**: `http://localhost:8000/health`
- **Frontend**: `http://localhost:3000`
- **Database**: Connection status in logs

### Logs
- **Backend**: Console output and CloudWatch
- **Frontend**: Browser console
- **Infrastructure**: CloudFormation events

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS CDK team for excellent infrastructure as code tools
- React and Material-UI communities
- FastAPI for the amazing Python web framework
- All open source contributors

## 📞 Contact

- **GitHub**: [@samidh93](https://github.com/samidh93)
- **Repository**: [aws-cost-optimization-platform](https://github.com/samidh93/aws-cost-optimization-platform)

---

**Built with ❤️ for the AWS community**