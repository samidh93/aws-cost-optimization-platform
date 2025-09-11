"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_database
from ..models import CostData, BudgetAlert, OptimizationRecommendation

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "cost-optimization-platform",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_database)):
    """Detailed health check with database connectivity"""
    try:
        # Test database connectivity
        cost_count = db.query(CostData).count()
        alert_count = db.query(BudgetAlert).count()
        rec_count = db.query(OptimizationRecommendation).count()
        
        return {
            "status": "healthy",
            "service": "cost-optimization-platform",
            "version": "1.0.0",
            "database": "connected",
            "data_counts": {
                "cost_records": cost_count,
                "budget_alerts": alert_count,
                "optimization_recommendations": rec_count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "cost-optimization-platform",
            "version": "1.0.0",
            "database": "disconnected",
            "error": str(e)
        }
