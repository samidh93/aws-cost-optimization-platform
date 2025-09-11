"""
Database configuration and connection management
Supports both local SQLite and production PostgreSQL
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sqlite3

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cost_optimization.db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create database engine
if ENVIRONMENT == "development":
    # Use SQLite for local development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True  # Log SQL queries in development
    )
else:
    # Use PostgreSQL for production
    engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Metadata for table creation
metadata = MetaData()

def get_database():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_database():
    """Initialize database tables"""
    try:
        # Import all models to ensure they're registered
        from .models import CostData, BudgetAlert, OptimizationRecommendation
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Insert sample data for development
        if ENVIRONMENT == "development":
            await insert_sample_data()
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise

async def insert_sample_data():
    """Insert sample data for local development"""
    from .models import CostData, BudgetAlert, OptimizationRecommendation
    from datetime import datetime, timedelta
    import random
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(CostData).first():
            print("📊 Sample data already exists")
            return
        
        print("📊 Inserting sample data...")
        
        # Insert sample cost data
        services = ["EC2", "RDS", "S3", "Lambda", "EKS"]
        for i in range(30):  # 30 days of data
            date = datetime.now() - timedelta(days=i)
            for service in services:
                cost_data = CostData(
                    account_id="123456789012",
                    timestamp=date.strftime("%Y-%m-%d"),
                    service=service,
                    cost=round(random.uniform(5, 50), 2),
                    total_daily_cost=round(random.uniform(100, 500), 2),
                    processed_at=datetime.now().isoformat()
                )
                db.add(cost_data)
        
        # Insert sample budget alerts
        alert_data = [
            {
                "account_id": "123456789012",
                "timestamp": datetime.now().isoformat(),
                "alert_type": "BUDGET_EXCEEDED",
                "service": "EC2",
                "current_cost": 125.50,
                "budget_limit": 100.00,
                "message": "EC2 budget exceeded: $125.50 > $100.00",
                "processed_at": datetime.now().isoformat()
            },
            {
                "account_id": "123456789012",
                "timestamp": datetime.now().isoformat(),
                "alert_type": "SERVICE_BUDGET_EXCEEDED",
                "service": "RDS",
                "current_cost": 85.75,
                "budget_limit": 75.00,
                "message": "RDS budget exceeded: $85.75 > $75.00",
                "processed_at": datetime.now().isoformat()
            }
        ]
        
        for alert in alert_data:
            budget_alert = BudgetAlert(**alert)
            db.add(budget_alert)
        
        # Insert sample optimization recommendations
        recommendations = [
            {
                "account_id": "123456789012",
                "timestamp": datetime.now().isoformat(),
                "recommendation_id": "rec-001",
                "service": "EC2",
                "priority": "HIGH",
                "category": "RIGHT_SIZING",
                "title": "Consider Right-Sizing EC2 Instances",
                "description": "EC2 costs are $125.50. Review instance types and consider downsizing.",
                "potential_savings": "$37.65",
                "action": "Review EC2 instances and consider t2.micro or t3.micro instances",
                "impact": "MEDIUM"
            },
            {
                "account_id": "123456789012",
                "timestamp": datetime.now().isoformat(),
                "recommendation_id": "rec-002",
                "service": "RDS",
                "priority": "MEDIUM",
                "category": "INSTANCE_OPTIMIZATION",
                "title": "Optimize RDS Instance Size",
                "description": "RDS costs are $85.75. Consider using db.t2.micro for development.",
                "potential_savings": "$34.30",
                "action": "Review RDS instance types and consider smaller instances",
                "impact": "MEDIUM"
            }
        ]
        
        for rec in recommendations:
            optimization_rec = OptimizationRecommendation(**rec)
            db.add(optimization_rec)
        
        db.commit()
        print("✅ Sample data inserted successfully")
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()
