"""
Optimization recommendations endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_database
from ..models import OptimizationRecommendation
from ..services import OptimizationService

router = APIRouter()

@router.get("/")
async def get_optimization_recommendations(
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of recommendations to return"),
    service: Optional[str] = Query(None, description="Filter by service"),
    priority: Optional[str] = Query(None, description="Filter by priority (HIGH, MEDIUM, LOW)"),
    db: Session = Depends(get_database)
):
    """Get optimization recommendations"""
    try:
        optimization_service = OptimizationService(db)
        recommendations = await optimization_service.get_recommendations(
            limit=limit, 
            service=service, 
            priority=priority
        )
        return {
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations),
            "limit": limit,
            "service_filter": service,
            "priority_filter": priority
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_optimization_summary(db: Session = Depends(get_database)):
    """Get optimization summary and statistics"""
    try:
        optimization_service = OptimizationService(db)
        summary = await optimization_service.get_optimization_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
