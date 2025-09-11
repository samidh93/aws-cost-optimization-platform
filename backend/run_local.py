#!/usr/bin/env python3
"""
Local development server for Cost Optimization Platform
Run this to test the application locally before deploying to AWS
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set environment variables for local development
os.environ["ENVIRONMENT"] = "development"
os.environ["DATABASE_URL"] = "sqlite:///./cost_optimization.db"

def main():
    """Run the local development server"""
    print("🚀 Starting Cost Optimization Platform - Local Development")
    print("=" * 60)
    print("📍 Environment: Development")
    print("🗄️  Database: SQLite (local)")
    print("🌐 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("=" * 60)
    print()
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
