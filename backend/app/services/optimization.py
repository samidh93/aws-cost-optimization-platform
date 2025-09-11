"""
Optimization recommendations service
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models import OptimizationRecommendation

class OptimizationService:
    """Service for optimization recommendations operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_recommendations(
        self, 
        limit: int = 50, 
        service: Optional[str] = None, 
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get optimization recommendations"""
        query = self.db.query(OptimizationRecommendation)
        
        if service:
            query = query.filter(OptimizationRecommendation.service == service)
        
        if priority:
            query = query.filter(OptimizationRecommendation.priority == priority)
        
        results = query.order_by(desc(OptimizationRecommendation.created_at)).limit(limit).all()
        
        recommendations = []
        for rec in results:
            recommendations.append({
                "id": rec.id,
                "account_id": rec.account_id,
                "timestamp": rec.timestamp,
                "recommendation_id": rec.recommendation_id,
                "service": rec.service,
                "priority": rec.priority,
                "category": rec.category,
                "title": rec.title,
                "description": rec.description,
                "potential_savings": rec.potential_savings,
                "action": rec.action,
                "impact": rec.impact,
                "created_at": rec.created_at.isoformat() if rec.created_at else None
            })
        
        return recommendations
    
    async def get_optimization_summary(self) -> Dict[str, Any]:
        """Get optimization summary and statistics"""
        # Get total recommendations count
        total_recommendations = self.db.query(OptimizationRecommendation).count()
        
        # Get recommendations by priority
        recommendations_by_priority = self.db.query(
            OptimizationRecommendation.priority,
            func.count(OptimizationRecommendation.id).label('count')
        ).group_by(OptimizationRecommendation.priority).all()
        
        # Get recommendations by service
        recommendations_by_service = self.db.query(
            OptimizationRecommendation.service,
            func.count(OptimizationRecommendation.id).label('count')
        ).group_by(OptimizationRecommendation.service).order_by(desc('count')).all()
        
        # Get recommendations by category
        recommendations_by_category = self.db.query(
            OptimizationRecommendation.category,
            func.count(OptimizationRecommendation.id).label('count')
        ).group_by(OptimizationRecommendation.category).order_by(desc('count')).all()
        
        # Calculate total potential savings
        total_savings = 0
        for rec in self.db.query(OptimizationRecommendation).all():
            try:
                # Extract numeric value from potential_savings string
                savings_str = rec.potential_savings.replace('$', '').replace(',', '')
                total_savings += float(savings_str)
            except (ValueError, AttributeError):
                continue
        
        return {
            "total_recommendations": total_recommendations,
            "total_potential_savings": f"${total_savings:.2f}",
            "recommendations_by_priority": [
                {"priority": item.priority, "count": item.count}
                for item in recommendations_by_priority
            ],
            "recommendations_by_service": [
                {"service": item.service, "count": item.count}
                for item in recommendations_by_service
            ],
            "recommendations_by_category": [
                {"category": item.category, "count": item.count}
                for item in recommendations_by_category
            ]
        }
