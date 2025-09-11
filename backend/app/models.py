"""
Database models for the Cost Optimization Platform
"""

from sqlalchemy import Column, String, Float, DateTime, Text, Integer
from sqlalchemy.sql import func
from .database import Base

class CostData(Base):
    """Model for storing cost data"""
    __tablename__ = "cost_data"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD format
    service = Column(String(100), nullable=False, index=True)
    cost = Column(Float, nullable=False)
    total_daily_cost = Column(Float, nullable=False)
    processed_at = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CostData(account_id='{self.account_id}', service='{self.service}', cost={self.cost})>"

class BudgetAlert(Base):
    """Model for storing budget alerts"""
    __tablename__ = "budget_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(String(50), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False, index=True)
    service = Column(String(100), nullable=False, index=True)
    current_cost = Column(Float, nullable=False)
    budget_limit = Column(Float, nullable=False)
    message = Column(Text, nullable=False)
    processed_at = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<BudgetAlert(account_id='{self.account_id}', service='{self.service}', alert_type='{self.alert_type}')>"

class OptimizationRecommendation(Base):
    """Model for storing optimization recommendations"""
    __tablename__ = "optimization_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(String(50), nullable=False, index=True)
    recommendation_id = Column(String(100), nullable=False, index=True)
    service = Column(String(100), nullable=False, index=True)
    priority = Column(String(20), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    potential_savings = Column(String(20), nullable=False)
    action = Column(Text, nullable=False)
    impact = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<OptimizationRecommendation(service='{self.service}', priority='{self.priority}', title='{self.title}')>"
