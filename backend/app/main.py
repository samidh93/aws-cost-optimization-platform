"""
Cost Optimization Platform - Main FastAPI Application
This is the main backend application that can run locally or in AWS
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import os
from typing import List, Dict, Any

from .database import get_database, init_database
from .models import CostData, BudgetAlert, OptimizationRecommendation
from .services import CostService, BudgetService, OptimizationService
from .routers import cost, budget, optimization, health

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Create FastAPI application
app = FastAPI(
    title="Cost Optimization Platform",
    description="A comprehensive platform for AWS cost monitoring and optimization",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🚀 Starting Cost Optimization Platform...")
    await init_database()
    print("✅ Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("🛑 Shutting down Cost Optimization Platform...")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if DEBUG else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(cost.router, prefix="/api/v1/cost", tags=["cost"])
app.include_router(budget.router, prefix="/api/v1/budget", tags=["budget"])
app.include_router(optimization.router, prefix="/api/v1/optimization", tags=["optimization"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API documentation"""
    return """
    <html>
        <head>
            <title>Cost Optimization Platform</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .method { color: #007bff; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Cost Optimization Platform</h1>
                <p>Welcome to the Cost Optimization Platform API!</p>
                
                <h2>📚 API Endpoints</h2>
                <div class="endpoint">
                    <span class="method">GET</span> /health - Health check
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> /api/v1/cost - Get cost data
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> /api/v1/budget - Get budget alerts
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> /api/v1/optimization - Get optimization recommendations
                </div>
                
                <h2>📖 Documentation</h2>
                <p><a href="/docs">Interactive API Documentation (Swagger UI)</a></p>
                <p><a href="/redoc">Alternative API Documentation (ReDoc)</a></p>
                
                <h2>🔧 Development</h2>
                <p>Environment: <strong>{}</strong></p>
                <p>Debug Mode: <strong>{}</strong></p>
            </div>
        </body>
    </html>
    """.format(ENVIRONMENT, DEBUG)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
        log_level="info"
    )
