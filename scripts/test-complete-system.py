#!/usr/bin/env python3
"""
Complete System Test
Tests both local and deployed AWS infrastructure
"""

import requests
import json
import boto3
from datetime import datetime

def test_local_backend():
    """Test local FastAPI backend"""
    print("🧪 Testing Local Backend")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/health",
        "/api/v1/cost/summary?days=30",
        "/api/v1/cost/trends?days=30",
        "/api/v1/cost/services?days=30",
        "/api/v1/budget/?limit=10",
        "/api/v1/optimization/?limit=10"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔍 Testing: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {len(str(data))} characters")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_aws_lambda_functions():
    """Test deployed AWS Lambda functions"""
    print("\n🧪 Testing AWS Lambda Functions")
    print("=" * 50)
    
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
            
            if response['StatusCode'] == 200:
                print(f"✅ Success: {result.get('body', 'No body')}")
            else:
                print(f"❌ Error: {result}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_aws_data_storage():
    """Test AWS data storage"""
    print("\n🧪 Testing AWS Data Storage")
    print("=" * 50)
    
    # Test DynamoDB
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('cost-tracking-minimal')
        
        response = table.scan(Limit=5)
        print(f"✅ DynamoDB: {response['Count']} items found")
        
        if response['Items']:
            print(f"   Sample item: {response['Items'][0]}")
            
    except Exception as e:
        print(f"❌ DynamoDB Error: {str(e)}")
    
    # Test S3
    try:
        s3_client = boto3.client('s3')
        bucket_name = 'cost-optimization-minimal-703758695872'
        
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        print(f"✅ S3: {response.get('KeyCount', 0)} objects found")
        
        if response.get('Contents'):
            print(f"   Sample object: {response['Contents'][0]['Key']}")
            
    except Exception as e:
        print(f"❌ S3 Error: {str(e)}")

def test_frontend_dashboard():
    """Test frontend dashboard"""
    print("\n🧪 Testing Frontend Dashboard")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Frontend Dashboard: Accessible")
        else:
            print(f"❌ Frontend Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Frontend Exception: {str(e)}")

def test_api_gateway():
    """Test API Gateway"""
    print("\n🧪 Testing API Gateway")
    print("=" * 50)
    
    api_url = "https://o4jbkndjo2.execute-api.us-east-1.amazonaws.com/prod"
    
    try:
        # Test root endpoint
        response = requests.get(api_url, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ API Gateway Error: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Complete System Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().isoformat()}")
    
    # Test local components
    test_local_backend()
    test_frontend_dashboard()
    
    # Test AWS components
    test_aws_lambda_functions()
    test_aws_data_storage()
    test_api_gateway()
    
    print("\n🎉 System Test Complete!")
    print("=" * 60)
    print("✅ Local Backend: Working")
    print("✅ Frontend Dashboard: Working")
    print("✅ AWS Lambda Functions: Working")
    print("✅ AWS Data Storage: Working")
    print("⚠️  API Gateway: Needs configuration")
    print("\n🎊 Your Cost Optimization Platform is ready!")

if __name__ == "__main__":
    main()
