"""
Budget management service
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models import BudgetAlert

class BudgetService:
    """Service for budget management operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_budget_alerts(self, limit: int = 50, alert_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get budget alerts"""
        query = self.db.query(BudgetAlert)
        
        if alert_type:
            query = query.filter(BudgetAlert.alert_type == alert_type)
        
        results = query.order_by(desc(BudgetAlert.created_at)).limit(limit).all()
        
        alerts = []
        for alert in results:
            alerts.append({
                "id": alert.id,
                "account_id": alert.account_id,
                "timestamp": alert.timestamp,
                "alert_type": alert.alert_type,
                "service": alert.service,
                "current_cost": alert.current_cost,
                "budget_limit": alert.budget_limit,
                "message": alert.message,
                "processed_at": alert.processed_at,
                "created_at": alert.created_at.isoformat() if alert.created_at else None
            })
        
        return alerts
    
    async def get_budget_summary(self) -> Dict[str, Any]:
        """Get budget summary and statistics"""
        # Get total alerts count
        total_alerts = self.db.query(BudgetAlert).count()
        
        # Get alerts by type
        alerts_by_type = self.db.query(
            BudgetAlert.alert_type,
            func.count(BudgetAlert.id).label('count')
        ).group_by(BudgetAlert.alert_type).all()
        
        # Get alerts by service
        alerts_by_service = self.db.query(
            BudgetAlert.service,
            func.count(BudgetAlert.id).label('count')
        ).group_by(BudgetAlert.service).order_by(desc('count')).all()
        
        # Get recent alerts (last 7 days)
        recent_alerts = self.db.query(BudgetAlert).filter(
            BudgetAlert.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        
        return {
            "total_alerts": total_alerts,
            "recent_alerts": recent_alerts,
            "alerts_by_type": [
                {"type": item.alert_type, "count": item.count}
                for item in alerts_by_type
            ],
            "alerts_by_service": [
                {"service": item.service, "count": item.count}
                for item in alerts_by_service
            ]
        }
