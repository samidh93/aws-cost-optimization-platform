#!/bin/bash

# Local Development Setup Script
# This script sets up the local development environment for testing

set -e

echo "🚀 Setting up Local Development Environment"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "backend/run_local.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source backend/venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
cd backend
pip install -r requirements-ultra-minimal.txt
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
echo "✅ Local development environment setup complete!"
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
