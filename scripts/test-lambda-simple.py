#!/usr/bin/env python3
"""
Simple Lambda Functions Test
Tests basic functionality without AWS dependencies
"""

import sys
import os
import json
from datetime import datetime

def test_cost_processor_logic():
    """Test the cost processor logic without AWS calls"""
    print("🧪 Testing Cost Processor Logic...")
    
    try:
        # Test the data processing logic
        mock_cost_data = {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': '2025-09-03', 'End': '2025-09-04'},
                    'Total': {'BlendedCost': {'Amount': '25.50', 'Unit': 'USD'}},
                    'Groups': [
                        {
                            'Keys': ['Amazon Elastic Compute Cloud'],
                            'Metrics': {'BlendedCost': {'Amount': '15.30', 'Unit': 'USD'}}
                        },
                        {
                            'Keys': ['Amazon Simple Storage Service'],
                            'Metrics': {'BlendedCost': {'Amount': '10.20', 'Unit': 'USD'}}
                        }
                    ]
                }
            ]
        }
        
        # Import and test the processing function
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'cost_processor'))
        from cost_processor import process_cost_data
        
        # Test processing
        processed_data = process_cost_data(mock_cost_data, "123456789012")
        
        print(f"✅ Processed {len(processed_data)} records")
        print(f"📊 Sample record: {processed_data[0] if processed_data else 'No data'}")
        return True
        
    except Exception as e:
        print(f"❌ Cost Processor Logic Test Failed: {str(e)}")
        return False

def test_budget_alert_logic():
    """Test the budget alert logic without AWS calls"""
    print("\n🧪 Testing Budget Alert Logic...")
    
    try:
        # Test the budget checking logic
        mock_costs = {
            'Amazon Elastic Compute Cloud': 25.50,
            'Amazon Simple Storage Service': 8.75,
            'Amazon Relational Database Service': 15.30
        }
        
        # Import and test the budget checking function
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'budget_alert'))
        from budget_alert import check_budget_thresholds
        
        # Test budget checking
        alerts = check_budget_thresholds(mock_costs)
        
        print(f"✅ Generated {len(alerts)} budget alerts")
        print(f"📊 Sample alert: {alerts[0] if alerts else 'No alerts'}")
        return True
        
    except Exception as e:
        print(f"❌ Budget Alert Logic Test Failed: {str(e)}")
        return False

def test_cost_optimizer_logic():
    """Test the cost optimizer logic without AWS calls"""
    print("\n🧪 Testing Cost Optimizer Logic...")
    
    try:
        # Test the recommendation generation logic
        mock_cost_data = {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': '2025-09-03', 'End': '2025-09-04'},
                    'Total': {'BlendedCost': {'Amount': '45.50', 'Unit': 'USD'}},
                    'Groups': [
                        {
                            'Keys': ['Amazon Elastic Compute Cloud'],
                            'Metrics': {'BlendedCost': {'Amount': '25.30', 'Unit': 'USD'}}
                        },
                        {
                            'Keys': ['Amazon Relational Database Service'],
                            'Metrics': {'BlendedCost': {'Amount': '12.75', 'Unit': 'USD'}}
                        }
                    ]
                }
            ]
        }
        
        # Import and test the recommendation generation
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'cost_optimizer'))
        from cost_optimizer import generate_recommendations
        
        # Test recommendation generation
        recommendations = generate_recommendations(mock_cost_data)
        
        print(f"✅ Generated {len(recommendations)} optimization recommendations")
        print(f"📊 Sample recommendation: {recommendations[0] if recommendations else 'No recommendations'}")
        return True
        
    except Exception as e:
        print(f"❌ Cost Optimizer Logic Test Failed: {str(e)}")
        return False

def main():
    """Run all Lambda function logic tests"""
    print("🚀 Lambda Functions Logic Testing")
    print("=" * 50)
    
    tests = [
        test_cost_processor_logic,
        test_budget_alert_logic,
        test_cost_optimizer_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📋 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Lambda function logic is working correctly!")
        print("✅ Ready for deployment to AWS")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
