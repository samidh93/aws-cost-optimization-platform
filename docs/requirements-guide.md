# 📦 Dependency Management Guide

This document outlines the dependency management strategy for the AWS Cost Optimization Platform, including Python package requirements and environment configuration.

## 📁 Requirements Files Overview

| File | Purpose | Python Version | Used For |
|------|---------|----------------|----------|
| `backend/requirements.txt` | **Backend Dependencies** | Python 3.11 | FastAPI, Database, Business Logic |
| `infrastructure/cdk/requirements.txt` | **CDK Dependencies** | Python 3.11 | AWS CDK, Infrastructure as Code |

## 🔧 Backend Requirements (`backend/requirements.txt`)

**Purpose**: Python dependencies for the FastAPI backend application

**Key Dependencies**:
- **FastAPI** - Web framework for building APIs
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Pandas/NumPy** - Data analysis and processing
- **Boto3** - AWS SDK for Python
- **Pytest** - Testing framework

**Installation**:
```bash
cd backend
pip install -r requirements.txt
```

## 🏗️ Infrastructure Requirements (`infrastructure/cdk/requirements.txt`)

**Purpose**: Python dependencies for AWS CDK infrastructure

**Key Dependencies**:
- **aws-cdk-lib** - AWS CDK core library
- **constructs** - CDK constructs
- **boto3** - AWS SDK for infrastructure management

**Installation**:
```bash
cd infrastructure/cdk
pip install -r requirements.txt
```

## 🚫 Removed Files

The following files were removed to reduce confusion:

- `requirements.txt` (root) - ❌ Removed
- `requirements-minimal.txt` - ❌ Removed  
- `backend/requirements-dev.txt` - ❌ Removed
- `backend/requirements-minimal-dev.txt` - ❌ Removed
- `backend/requirements-python311.txt` - ❌ Renamed to `requirements.txt`

## 🐍 Python Version Requirements

**All requirements files require Python 3.11**

### Why Python 3.11?

- **Compatibility**: All dependencies work reliably with Python 3.11
- **Performance**: Better performance than older versions
- **Features**: Modern Python features and syntax
- **Stability**: Well-tested and stable version

### Setting Up Python 3.11

```bash
# Using pyenv (recommended)
pyenv install 3.11.9
pyenv local 3.11.9

# Verify version
python --version  # Should show Python 3.11.9
```

## 🛠️ Development Workflow

### 1. Backend Development

```bash
# Set up Python 3.11
pyenv local 3.11.9

# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_local.py
```

### 2. Infrastructure Development

```bash
# Set up Python 3.11
pyenv local 3.11.9

# Create virtual environment
cd infrastructure/cdk
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deploy infrastructure
npx cdk deploy
```

## 🔍 Troubleshooting

### Python Version Issues

```bash
# Check current version
python --version

# If not 3.11, set it
pyenv local 3.11.9

# Or use specific Python version
python3.11 -m venv venv
```

### Dependency Conflicts

```bash
# Create fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Missing Dependencies

```bash
# Update pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

## 📝 Adding New Dependencies

### Backend Dependencies

```bash
# Add to backend/requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt

# Install
pip install -r requirements.txt
```

### CDK Dependencies

```bash
# Add to infrastructure/cdk/requirements.txt
echo "new-cdk-package==1.0.0" >> infrastructure/cdk/requirements.txt

# Install
pip install -r requirements.txt
```

## ✅ Best Practices

1. **Always use Python 3.11** for this project
2. **Use virtual environments** to isolate dependencies
3. **Pin dependency versions** to ensure reproducibility
4. **Test after adding dependencies** to ensure compatibility
5. **Keep requirements files minimal** - only include what's needed
6. **Document any special requirements** in the README
