# 🚀 Platform Quick Reference

## 📦 Requirements Files

| File | Purpose |
|------|---------|
| `backend/requirements.txt` | **Backend Python dependencies** |
| `infrastructure/cdk/requirements.txt` | **CDK Python dependencies** |

## 🐍 Python Setup

```bash
# Check Python version
./scripts/check-python.sh

# Install Python 3.11 (if needed)
brew install pyenv
pyenv install 3.11.9
pyenv local 3.11.9
```

## 🚀 Quick Start

```bash
# One-command setup
./scripts/setup.sh

# Or manual setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_local.py
```

## 🌐 API Endpoints

- **Main**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health/
- **Cost**: http://localhost:8000/api/v1/cost/
- **Budget**: http://localhost:8000/api/v1/budget/
- **Optimization**: http://localhost:8000/api/v1/optimization/

## 🧪 Testing

```bash
# Run all tests
cd backend && python test_local.py

# Test specific endpoint
curl http://localhost:8000/health/
```

## 🔧 Troubleshooting

```bash
# Python version issues
pyenv local 3.11.9

# Database issues
rm backend/cost_optimization.db

# Port conflicts
lsof -ti:8000 | xargs kill -9
```
