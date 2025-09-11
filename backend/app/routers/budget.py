"""
Budget management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_database
from ..models import BudgetAlert
from ..services import BudgetService

router = APIRouter()

@router.get("/")
async def get_budget_alerts(
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of alerts to return"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type"),
    db: Session = Depends(get_database)
):
    """Get budget alerts"""
    try:
        budget_service = BudgetService(db)
        alerts = await budget_service.get_budget_alerts(limit=limit, alert_type=alert_type)
        return {
            "success": True,
            "alerts": alerts,
            "count": len(alerts),
            "limit": limit,
            "alert_type_filter": alert_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_budget_summary(db: Session = Depends(get_database)):
    """Get budget summary and statistics"""
    try:
        budget_service = BudgetService(db)
        summary = await budget_service.get_budget_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
