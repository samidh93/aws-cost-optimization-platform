#!/usr/bin/env python3
"""
Local Testing Script for Lambda Functions
Tests the Lambda functions locally before deployment
"""

import sys
import os
import json
from datetime import datetime

# Add the lambda directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'cost_processor'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'budget_alert'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'cdk', 'lambda', 'cost_optimizer'))

def test_cost_processor():
    """Test the cost processor Lambda function"""
    print("🧪 Testing Cost Processor Lambda...")
    
    try:
        from cost_processor import handler
        
        # Mock event and context
        event = {}
        context = type('Context', (), {
            'invoked_function_arn': 'arn:aws:lambda:us-east-1:123456789012:function:cost-processor'
        })()
        
        # Set environment variables
        os.environ['COST_TABLE_NAME'] = 'cost-data-table'
        os.environ['S3_BUCKET'] = 'cost-optimization-bucket'
        
        # Test the handler
        result = handler(event, context)
        
        print(f"✅ Cost Processor Test Result: {result['statusCode']}")
        print(f"📊 Response: {json.loads(result['body'])}")
        return True
        
    except Exception as e:
        print(f"❌ Cost Processor Test Failed: {str(e)}")
        return False

def test_budget_alert():
    """Test the budget alert Lambda function"""
    print("\n🧪 Testing Budget Alert Lambda...")
    
    try:
        from budget_alert import handler
        
        # Mock event and context
        event = {}
        context = type('Context', (), {
            'invoked_function_arn': 'arn:aws:lambda:us-east-1:123456789012:function:budget-alert'
        })()
        
        # Set environment variables
        os.environ['COST_TABLE_NAME'] = 'cost-data-table'
        
        # Test the handler
        result = handler(event, context)
        
        print(f"✅ Budget Alert Test Result: {result['statusCode']}")
        print(f"📊 Response: {json.loads(result['body'])}")
        return True
        
    except Exception as e:
        print(f"❌ Budget Alert Test Failed: {str(e)}")
        return False

def test_cost_optimizer():
    """Test the cost optimizer Lambda function"""
    print("\n🧪 Testing Cost Optimizer Lambda...")
    
    try:
        from cost_optimizer import handler
        
        # Mock event and context
        event = {}
        context = type('Context', (), {
            'invoked_function_arn': 'arn:aws:lambda:us-east-1:123456789012:function:cost-optimizer'
        })()
        
        # Set environment variables
        os.environ['COST_TABLE_NAME'] = 'cost-data-table'
        os.environ['S3_BUCKET'] = 'cost-optimization-bucket'
        
        # Test the handler
        result = handler(event, context)
        
        print(f"✅ Cost Optimizer Test Result: {result['statusCode']}")
        print(f"📊 Response: {json.loads(result['body'])}")
        return True
        
    except Exception as e:
        print(f"❌ Cost Optimizer Test Failed: {str(e)}")
        return False

def main():
    """Run all Lambda function tests"""
    print("🚀 Lambda Functions Local Testing")
    print("=" * 50)
    
    tests = [
        test_cost_processor,
        test_budget_alert,
        test_cost_optimizer
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📋 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Lambda functions are working correctly!")
        print("✅ Ready for deployment to AWS")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
