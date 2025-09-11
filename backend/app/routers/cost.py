"""
Cost data endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_database
from ..models import CostData
from ..services import CostService

router = APIRouter()

@router.get("/")
async def get_cost_data(
    days: int = Query(7, ge=1, le=365, description="Number of days to retrieve"),
    service: Optional[str] = Query(None, description="Filter by service name"),
    db: Session = Depends(get_database)
):
    """Get cost data for the specified period"""
    try:
        cost_service = CostService(db)
        data = await cost_service.get_cost_data(days=days, service=service)
        return {
            "success": True,
            "data": data,
            "period_days": days,
            "service_filter": service,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_cost_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days to summarize"),
    db: Session = Depends(get_database)
):
    """Get cost summary for the specified period"""
    try:
        cost_service = CostService(db)
        summary = await cost_service.get_cost_summary(days=days)
        return {
            "success": True,
            "summary": summary,
            "period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
async def get_cost_trends(
    days: int = Query(30, ge=7, le=365, description="Number of days for trend analysis"),
    db: Session = Depends(get_database)
):
    """Get cost trends and analysis"""
    try:
        cost_service = CostService(db)
        trends = await cost_service.get_cost_trends(days=days)
        return {
            "success": True,
            "trends": trends,
            "period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services")
async def get_services(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_database)
):
    """Get cost breakdown by service"""
    try:
        cost_service = CostService(db)
        services = await cost_service.get_services_breakdown(days=days)
        return {
            "success": True,
            "services": services,
            "period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
