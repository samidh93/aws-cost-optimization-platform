#!/usr/bin/env python3
"""
Test the deployed Lambda functions via API Gateway
"""

import requests
import json

# API Gateway URL
API_URL = "https://o4jbkndjo2.execute-api.us-east-1.amazonaws.com/prod"

def test_api_endpoints():
    """Test the deployed API endpoints"""
    print("🧪 Testing Deployed Lambda Functions via API Gateway")
    print("=" * 60)
    
    # Test endpoints
    endpoints = [
        "/health",
        "/api/v1/cost/summary",
        "/api/v1/budget/summary",
        "/api/v1/optimization/summary"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{API_URL}{endpoint}"
            print(f"\n🔍 Testing: {url}")
            
            response = requests.get(url, timeout=10)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Success: {response.json()}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_lambda_functions_directly():
    """Test Lambda functions directly"""
    print("\n🧪 Testing Lambda Functions Directly")
    print("=" * 60)
    
    import boto3
    lambda_client = boto3.client('lambda')
    
    # List functions
    functions = lambda_client.list_functions()
    cost_functions = [f for f in functions['Functions'] if 'Cost' in f['FunctionName'] or 'Budget' in f['FunctionName']]
    
    for func in cost_functions:
        print(f"\n🔍 Testing: {func['FunctionName']}")
        
        try:
            response = lambda_client.invoke(
                FunctionName=func['FunctionName'],
                Payload='{}'
            )
            
            result = json.loads(response['Payload'].read())
            print(f"Status: {response['StatusCode']}")
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
    test_lambda_functions_directly()
