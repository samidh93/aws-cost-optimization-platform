#!/bin/bash

# Cost Optimization Platform - Simple Setup Script
# This script sets up the entire project with Python 3.11

set -e

echo "🚀 Cost Optimization Platform - Setup"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "backend/run_local.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
if ! python --version | grep -q "Python 3.11"; then
    echo "❌ Python 3.11 is required but not found"
    echo "📋 Please install Python 3.11 using pyenv:"
    echo "   1. brew install pyenv"
    echo "   2. pyenv install 3.11.9"
    echo "   3. pyenv local 3.11.9"
    echo "   4. Run this script again"
    exit 1
fi

echo "✅ Python 3.11 found: $(python --version)"

# Set up backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
echo "⚙️  Creating environment configuration..."
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Created .env file from template"
fi

cd ..

# Test the setup
echo "🧪 Testing setup..."
cd backend
python run_local.py &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Run tests
echo "🔍 Running tests..."
python test_local.py

# Stop the server
echo "🛑 Stopping test server..."
kill $SERVER_PID

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 To start development:"
echo "1. cd backend"
echo "2. source venv/bin/activate"
echo "3. python run_local.py"
echo ""
echo "🌐 Then visit:"
echo "   - http://localhost:8000 (Main page)"
echo "   - http://localhost:8000/docs (API Documentation)"
echo ""
echo "📚 For more information, see README.md"