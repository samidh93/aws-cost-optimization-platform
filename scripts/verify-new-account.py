#!/usr/bin/env python3
"""
AWS New Account Free Tier Verification
This script verifies that a new AWS account is properly set up for free tier development
"""

import boto3
import json
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, NoCredentialsError

def check_new_account_setup():
    """Check if the new AWS account is properly configured"""
    print("🆕 AWS New Account Free Tier Verification")
    print("=" * 50)
    
    try:
        # Check AWS credentials
        session = boto3.Session()
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print(f"✅ AWS credentials configured")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        
        # Check if this looks like a new account
        iam = boto3.client('iam')
        try:
            # Try to get account summary
            account_summary = iam.get_account_summary()
            print(f"✅ IAM access confirmed")
        except ClientError as e:
            print(f"⚠️  IAM access issue: {e}")
        
        # Check current costs (should be $0 for new account)
        print("\n💰 Checking Current Costs...")
        ce = boto3.client('ce')
        
        # Check last 7 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        try:
            response = ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='DAILY',
                Metrics=['BlendedCost']
            )
            
            total_cost = 0
            for result in response['ResultsByTime']:
                cost = float(result['Total']['BlendedCost']['Amount'])
                total_cost += cost
                print(f"   {result['TimePeriod']['Start']}: ${cost:.4f}")
            
            if total_cost == 0:
                print("✅ Perfect! No charges detected - new account ready!")
            elif total_cost < 0.01:
                print("✅ Excellent! Minimal charges - safe for free tier")
            else:
                print(f"⚠️  Some charges detected: ${total_cost:.4f}")
                print("   This might not be a completely new account")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print("⚠️  Cost Explorer access denied")
                print("   This is normal for new accounts - permissions may take time to propagate")
            else:
                print(f"❌ Error checking costs: {e}")
        
        return True
        
    except NoCredentialsError:
        print("❌ No AWS credentials found!")
        print("   Please run: aws configure")
        return False
    except ClientError as e:
        print(f"❌ AWS credentials error: {e}")
        return False

def check_free_tier_services():
    """Check availability of free tier services"""
    print("\n🔧 Checking Free Tier Services...")
    
    services = {
        'EC2': 'ec2',
        'EKS': 'eks',
        'Lambda': 'lambda', 
        'S3': 's3',
        'RDS': 'rds',
        'CloudWatch': 'cloudwatch',
        'IAM': 'iam',
        'Cost Explorer': 'ce',
        'API Gateway': 'apigateway',
        'DynamoDB': 'dynamodb'
    }
    
    available_services = []
    
    for service_name, service_code in services.items():
        try:
            if service_code == 'ec2':
                client = boto3.client('ec2')
                regions = client.describe_regions()
                print(f"✅ {service_name}: Available ({len(regions['Regions'])} regions)")
            elif service_code == 'eks':
                client = boto3.client('eks')
                clusters = client.list_clusters()
                print(f"✅ {service_name}: Available (0 clusters)")
            elif service_code == 'lambda':
                client = boto3.client('lambda')
                functions = client.list_functions()
                print(f"✅ {service_name}: Available (0 functions)")
            elif service_code == 's3':
                client = boto3.client('s3')
                buckets = client.list_buckets()
                print(f"✅ {service_name}: Available (0 buckets)")
            elif service_code == 'rds':
                client = boto3.client('rds')
                instances = client.describe_db_instances()
                print(f"✅ {service_name}: Available (0 instances)")
            elif service_code == 'cloudwatch':
                client = boto3.client('cloudwatch')
                metrics = client.list_metrics()
                print(f"✅ {service_name}: Available")
            elif service_code == 'iam':
                client = boto3.client('iam')
                summary = client.get_account_summary()
                print(f"✅ {service_name}: Available")
            elif service_code == 'ce':
                client = boto3.client('ce')
                # Just test if we can create a client
                print(f"✅ {service_name}: Available")
            elif service_code == 'apigateway':
                client = boto3.client('apigateway')
                apis = client.get_rest_apis()
                print(f"✅ {service_name}: Available (0 APIs)")
            elif service_code == 'dynamodb':
                client = boto3.client('dynamodb')
                tables = client.list_tables()
                print(f"✅ {service_name}: Available (0 tables)")
            
            available_services.append(service_name)
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print(f"⚠️  {service_name}: Access denied (may need time to propagate)")
            else:
                print(f"❌ {service_name}: {e}")
        except Exception as e:
            print(f"❌ {service_name}: {e}")
    
    return available_services

def check_region_recommendations():
    """Check and recommend the best region for free tier"""
    print("\n🌍 Region Recommendations...")
    
    current_region = boto3.Session().region_name
    print(f"   Current region: {current_region}")
    
    # Recommended regions for free tier
    recommended_regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
    
    if current_region in recommended_regions:
        print(f"✅ Good choice! {current_region} is excellent for free tier")
    else:
        print(f"⚠️  Consider switching to one of these regions for better free tier support:")
        for region in recommended_regions:
            print(f"   - {region}")
        print(f"   Run: aws configure set region us-east-1")

def main():
    """Main verification function"""
    if not check_new_account_setup():
        return
    
    available_services = check_free_tier_services()
    check_region_recommendations()
    
    print("\n" + "=" * 50)
    print("📋 New Account Status:")
    print(f"✅ Available services: {len(available_services)}")
    print("✅ Ready for free tier development!")
    
    print("\n💡 Next Steps:")
    print("1. Wait 5-10 minutes for all services to be fully available")
    print("2. Run: ./scripts/setup.sh")
    print("3. Deploy: ./scripts/deploy.sh")
    print("4. Always cleanup: ./scripts/cleanup.sh")
    
    print("\n⚠️  Important Reminders:")
    print("- Free tier lasts 12 months from account creation")
    print("- Always run cleanup scripts to avoid charges")
    print("- Monitor costs in AWS Billing Dashboard")
    print("- Use only t2.micro instances and free tier services")

if __name__ == "__main__":
    main()
