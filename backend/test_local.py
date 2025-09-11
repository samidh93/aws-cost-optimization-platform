#!/usr/bin/env python3
"""
Test script for local development
Tests all API endpoints locally before deploying to AWS
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoints():
    """Test health check endpoints"""
    print("🏥 Testing Health Endpoints...")
    
    # Basic health check
    response = requests.get(f"{BASE_URL}/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✅ Basic health check passed")
    
    # Detailed health check
    response = requests.get(f"{BASE_URL}/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    print("✅ Detailed health check passed")
    print(f"   Database: {data['database']}")
    print(f"   Cost records: {data['data_counts']['cost_records']}")
    print(f"   Budget alerts: {data['data_counts']['budget_alerts']}")
    print(f"   Recommendations: {data['data_counts']['optimization_recommendations']}")

def test_cost_endpoints():
    """Test cost data endpoints"""
    print("\n💰 Testing Cost Endpoints...")
    
    # Get cost data
    response = requests.get(f"{BASE_URL}/api/v1/cost/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Cost data endpoint passed - {len(data['data'])} records")
    
    # Get cost summary
    response = requests.get(f"{BASE_URL}/api/v1/cost/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Cost summary endpoint passed - Total: ${data['summary']['total_cost']}")
    
    # Get cost trends
    response = requests.get(f"{BASE_URL}/api/v1/cost/trends")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Cost trends endpoint passed - {len(data['trends']['daily_costs'])} days")
    
    # Get services breakdown
    response = requests.get(f"{BASE_URL}/api/v1/cost/services")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Services breakdown endpoint passed - {len(data['services'])} services")

def test_budget_endpoints():
    """Test budget management endpoints"""
    print("\n📊 Testing Budget Endpoints...")
    
    # Get budget alerts
    response = requests.get(f"{BASE_URL}/api/v1/budget/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Budget alerts endpoint passed - {data['count']} alerts")
    
    # Get budget summary
    response = requests.get(f"{BASE_URL}/api/v1/budget/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Budget summary endpoint passed - {data['summary']['total_alerts']} total alerts")

def test_optimization_endpoints():
    """Test optimization recommendations endpoints"""
    print("\n🎯 Testing Optimization Endpoints...")
    
    # Get optimization recommendations
    response = requests.get(f"{BASE_URL}/api/v1/optimization/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Optimization recommendations endpoint passed - {data['count']} recommendations")
    
    # Get optimization summary
    response = requests.get(f"{BASE_URL}/api/v1/optimization/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Optimization summary endpoint passed - {data['summary']['total_recommendations']} total recommendations")

def test_api_documentation():
    """Test API documentation endpoints"""
    print("\n📚 Testing API Documentation...")
    
    # Test Swagger UI
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
    print("✅ Swagger UI accessible")
    
    # Test ReDoc
    response = requests.get(f"{BASE_URL}/redoc")
    assert response.status_code == 200
    print("✅ ReDoc accessible")

def main():
    """Run all tests"""
    print("🧪 Cost Optimization Platform - Local Testing")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Test all endpoints
        test_health_endpoints()
        test_cost_endpoints()
        test_budget_endpoints()
        test_optimization_endpoints()
        test_api_documentation()
        
        print("\n🎉 All tests passed! Local development setup is working correctly.")
        print("\n📋 Next steps:")
        print("1. Open http://localhost:8000/docs to explore the API")
        print("2. Test the frontend integration")
        print("3. Deploy to AWS when ready")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Make sure the server is running on http://localhost:8000")
        sys.exit(1)

if __name__ == "__main__":
    main()
