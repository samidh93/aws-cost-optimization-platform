#!/bin/bash

# Python Version Check Script
# Ensures Python 3.11 is installed and available

echo "🐍 Checking Python installation..."

# Check if python command exists
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    echo "📋 Please install Python 3.11:"
    echo "   macOS: brew install python@3.11"
    echo "   Or use pyenv: brew install pyenv && pyenv install 3.11.9"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1)
echo "📍 Found: $PYTHON_VERSION"

# Check if it's Python 3.11
if echo "$PYTHON_VERSION" | grep -q "Python 3.11"; then
    echo "✅ Python 3.11 is installed and ready!"
    exit 0
else
    echo "❌ Python 3.11 is required but found: $PYTHON_VERSION"
    echo ""
    echo "📋 To fix this:"
    echo ""
    echo "Option 1: Using pyenv (recommended)"
    echo "  1. brew install pyenv"
    echo "  2. pyenv install 3.11.9"
    echo "  3. pyenv local 3.11.9"
    echo "  4. Run this script again"
    echo ""
    echo "Option 2: Using Homebrew"
    echo "  1. brew install python@3.11"
    echo "  2. python3.11 --version"
    echo ""
    echo "Option 3: Download from python.org"
    echo "  1. Visit https://www.python.org/downloads/"
    echo "  2. Download Python 3.11.9"
    echo "  3. Install following the instructions"
    exit 1
fi
