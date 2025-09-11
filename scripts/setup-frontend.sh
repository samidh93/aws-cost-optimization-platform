#!/bin/bash

# Frontend Setup Script
# Sets up the React dashboard for the Cost Optimization Platform

set -e

echo "🎨 Setting up React Frontend Dashboard"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "frontend/cost-dashboard/package.json" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "📋 Please install Node.js:"
    echo "   macOS: brew install node"
    echo "   Or download from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ npm found: $(npm --version)"

# Navigate to frontend directory
cd frontend/cost-dashboard

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Create environment file
echo "⚙️  Creating environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Frontend Environment Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=1.0.0
REACT_APP_NAME=Cost Optimization Platform
EOF
    echo "✅ Created .env file"
fi

# Build the project to check for errors
echo "🔨 Building project to check for errors..."
npm run build

echo ""
echo "🎉 Frontend setup complete!"
echo ""
echo "📋 To start the frontend:"
echo "1. Make sure the backend is running:"
echo "   cd backend && python run_local.py"
echo ""
echo "2. Start the frontend:"
echo "   cd frontend/cost-dashboard && npm start"
echo ""
echo "🌐 Then visit:"
echo "   - http://localhost:3000 (Frontend Dashboard)"
echo "   - http://localhost:8000 (Backend API)"
echo ""
echo "📚 For development:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000/docs"
