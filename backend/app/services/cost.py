"""
Cost data service with business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
# import pandas as pd  # Skip for now due to Python 3.13 compatibility

from ..models import CostData

class CostService:
    """Service for cost data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_cost_data(self, days: int = 7, service: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get cost data for the specified period"""
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Build query
        query = self.db.query(CostData).filter(
            CostData.timestamp >= start_date.strftime("%Y-%m-%d"),
            CostData.timestamp <= end_date.strftime("%Y-%m-%d")
        )
        
        # Filter by service if specified
        if service:
            query = query.filter(CostData.service == service)
        
        # Execute query
        results = query.order_by(desc(CostData.timestamp)).all()
        
        # Convert to dictionary format
        data = []
        for record in results:
            data.append({
                "id": record.id,
                "account_id": record.account_id,
                "timestamp": record.timestamp,
                "service": record.service,
                "cost": record.cost,
                "total_daily_cost": record.total_daily_cost,
                "processed_at": record.processed_at,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })
        
        return data
    
    async def get_cost_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get cost summary for the specified period"""
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get total cost
        total_cost = self.db.query(func.sum(CostData.cost)).filter(
            CostData.timestamp >= start_date.strftime("%Y-%m-%d"),
            CostData.timestamp <= end_date.strftime("%Y-%m-%d")
        ).scalar() or 0
        
        # Get daily average
        daily_avg = total_cost / days if days > 0 else 0
        
        # Get service breakdown
        service_breakdown = self.db.query(
            CostData.service,
            func.sum(CostData.cost).label('total_cost')
        ).filter(
            CostData.timestamp >= start_date.strftime("%Y-%m-%d"),
            CostData.timestamp <= end_date.strftime("%Y-%m-%d")
        ).group_by(CostData.service).all()
        
        # Get trend data (last 7 days vs previous 7 days)
        if days >= 14:
            recent_start = end_date - timedelta(days=7)
            previous_start = recent_start - timedelta(days=7)
            
            recent_cost = self.db.query(func.sum(CostData.cost)).filter(
                CostData.timestamp >= recent_start.strftime("%Y-%m-%d"),
                CostData.timestamp <= end_date.strftime("%Y-%m-%d")
            ).scalar() or 0
            
            previous_cost = self.db.query(func.sum(CostData.cost)).filter(
                CostData.timestamp >= previous_start.strftime("%Y-%m-%d"),
                CostData.timestamp < recent_start.strftime("%Y-%m-%d")
            ).scalar() or 0
            
            trend_percentage = ((recent_cost - previous_cost) / previous_cost * 100) if previous_cost > 0 else 0
        else:
            trend_percentage = 0
        
        return {
            "total_cost": round(total_cost, 2),
            "daily_average": round(daily_avg, 2),
            "period_days": days,
            "trend_percentage": round(trend_percentage, 2),
            "service_breakdown": [
                {
                    "service": item.service,
                    "total_cost": round(item.total_cost, 2),
                    "percentage": round((item.total_cost / total_cost * 100) if total_cost > 0 else 0, 2)
                }
                for item in service_breakdown
            ]
        }
    
    async def get_cost_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get cost trends and analysis"""
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get daily costs
        daily_costs = self.db.query(
            CostData.timestamp,
            func.sum(CostData.cost).label('daily_cost')
        ).filter(
            CostData.timestamp >= start_date.strftime("%Y-%m-%d"),
            CostData.timestamp <= end_date.strftime("%Y-%m-%d")
        ).group_by(CostData.timestamp).order_by(CostData.timestamp).all()
        
        # Convert to list for easier processing
        daily_data = [
            {
                "date": item.timestamp,
                "cost": round(item.daily_cost, 2)
            }
            for item in daily_costs
        ]
        
        # Calculate trend analysis
        if len(daily_data) >= 7:
            recent_week = daily_data[-7:]
            previous_week = daily_data[-14:-7] if len(daily_data) >= 14 else daily_data[:-7]
            
            recent_avg = sum(day["cost"] for day in recent_week) / len(recent_week)
            previous_avg = sum(day["cost"] for day in previous_week) / len(previous_week)
            
            trend_direction = "increasing" if recent_avg > previous_avg else "decreasing"
            trend_percentage = abs((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
        else:
            trend_direction = "insufficient_data"
            trend_percentage = 0
        
        return {
            "daily_costs": daily_data,
            "trend_direction": trend_direction,
            "trend_percentage": round(trend_percentage, 2),
            "period_days": days
        }
    
    async def get_services_breakdown(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get cost breakdown by service"""
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get service costs
        service_costs = self.db.query(
            CostData.service,
            func.sum(CostData.cost).label('total_cost'),
            func.avg(CostData.cost).label('avg_cost'),
            func.count(CostData.id).label('record_count')
        ).filter(
            CostData.timestamp >= start_date.strftime("%Y-%m-%d"),
            CostData.timestamp <= end_date.strftime("%Y-%m-%d")
        ).group_by(CostData.service).order_by(desc('total_cost')).all()
        
        # Calculate total for percentage calculation
        total_cost = sum(item.total_cost for item in service_costs)
        
        return [
            {
                "service": item.service,
                "total_cost": round(item.total_cost, 2),
                "average_cost": round(item.avg_cost, 2),
                "record_count": item.record_count,
                "percentage": round((item.total_cost / total_cost * 100) if total_cost > 0 else 0, 2)
            }
            for item in service_costs
        ]
