#!/bin/bash

# Python 3.11 Setup Script for Cost Optimization Platform
# This script sets up the project with Python 3.11 for better compatibility

set -e

echo "🐍 Setting up Cost Optimization Platform with Python 3.11"
echo "========================================================="

# Check if we're in the right directory
if [ ! -f "backend/run_local.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Set up pyenv if not already done
if ! command -v pyenv &> /dev/null; then
    echo "📦 Setting up pyenv..."
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# Set Python 3.11 for this project
echo "🔧 Setting Python 3.11 for this project..."
pyenv local 3.11.9

# Verify Python version
echo "✅ Python version: $(python --version)"

# Remove old virtual environment if it exists
if [ -d "backend/venv" ]; then
    echo "🗑️  Removing old virtual environment..."
    rm -rf backend/venv
fi

# Create new virtual environment with Python 3.11
echo "📦 Creating Python 3.11 virtual environment..."
cd backend
python -m venv venv
cd ..

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source backend/venv/bin/activate

# Verify we're using the right Python
echo "✅ Virtual environment Python: $(python --version)"

# Install dependencies
echo "📥 Installing dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Create environment file
echo "⚙️  Creating environment configuration..."
if [ ! -f "backend/.env" ]; then
    cp backend/env.example backend/.env
    echo "✅ Created .env file from template"
fi

# Create database directory
echo "🗄️  Setting up local database..."
mkdir -p backend/data

# Test the setup
echo "🧪 Testing local setup..."
cd backend
python run_local.py &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Run tests
echo "🔍 Running local tests..."
python test_local.py

# Stop the server
echo "🛑 Stopping test server..."
kill $SERVER_PID

cd ..

echo ""
echo "🎉 Setup complete with Python 3.11!"
echo ""
echo "📋 To start local development:"
echo "1. cd backend"
echo "2. source venv/bin/activate"
echo "3. python run_local.py"
echo ""
echo "🌐 Then visit:"
echo "   - http://localhost:8000 (Main page)"
echo "   - http://localhost:8000/docs (API Documentation)"
echo "   - http://localhost:8000/redoc (Alternative Documentation)"
echo ""
echo "🧪 To run tests:"
echo "   python test_local.py"
echo ""
echo "🐍 Python version management:"
echo "   - pyenv versions (list all Python versions)"
echo "   - pyenv local 3.11.9 (set Python 3.11 for this project)"
echo "   - pyenv global 3.13.6 (set Python 3.13 as default)"
