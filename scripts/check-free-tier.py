#!/usr/bin/env python3
"""
AWS Free Tier Eligibility Checker
This script checks if your AWS account is eligible for free tier services
and provides recommendations for cost-free development.
"""

import boto3
import json
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, NoCredentialsError

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            print("❌ No AWS credentials found!")
            print("Please configure AWS CLI: aws configure")
            return False
        
        # Test credentials by calling STS
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS credentials configured")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return True
    except NoCredentialsError:
        print("❌ AWS credentials not found!")
        print("Please run: aws configure")
        return False
    except ClientError as e:
        print(f"❌ Error with AWS credentials: {e}")
        return False

def check_free_tier_eligibility():
    """Check free tier eligibility and current usage"""
    try:
        # Check if account is new (less than 12 months old)
        iam = boto3.client('iam')
        account_summary = iam.get_account_summary()
        
        # Check account creation date (approximate)
        print("\n🔍 Checking Free Tier Eligibility...")
        
        # Check current month costs
        ce = boto3.client('ce')
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        try:
            # Get cost and usage data
            response = ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            total_cost = 0
            for result in response['ResultsByTime']:
                cost = float(result['Total']['BlendedCost']['Amount'])
                total_cost += cost
            
            print(f"💰 Current month cost: ${total_cost:.2f}")
            
            if total_cost == 0:
                print("✅ No charges detected - perfect for free tier development!")
            elif total_cost < 1.00:
                print("✅ Very low costs - safe for free tier development")
            else:
                print("⚠️  Some costs detected - review your usage")
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print("⚠️  Cost Explorer access denied - cannot check current costs")
                print("   This is normal for new accounts or restricted permissions")
            else:
                print(f"⚠️  Could not check costs: {e}")
        
        return True
        
    except ClientError as e:
        print(f"❌ Error checking free tier: {e}")
        return False

def check_required_services():
    """Check if required AWS services are available"""
    print("\n🔧 Checking Required AWS Services...")
    
    services = {
        'EC2': 'ec2',
        'EKS': 'eks', 
        'Lambda': 'lambda',
        'S3': 's3',
        'RDS': 'rds',
        'CloudWatch': 'cloudwatch',
        'IAM': 'iam',
        'Cost Explorer': 'ce'
    }
    
    available_services = []
    
    for service_name, service_code in services.items():
        try:
            if service_code == 'ec2':
                client = boto3.client('ec2')
                client.describe_regions()
            elif service_code == 'eks':
                client = boto3.client('eks')
                client.list_clusters()
            elif service_code == 'lambda':
                client = boto3.client('lambda')
                client.list_functions()
            elif service_code == 's3':
                client = boto3.client('s3')
                client.list_buckets()
            elif service_code == 'rds':
                client = boto3.client('rds')
                client.describe_db_instances()
            elif service_code == 'cloudwatch':
                client = boto3.client('cloudwatch')
                client.list_metrics()
            elif service_code == 'iam':
                client = boto3.client('iam')
                client.get_account_summary()
            elif service_code == 'ce':
                client = boto3.client('ce')
                client.get_cost_and_usage(
                    TimePeriod={
                        'Start': '2024-01-01',
                        'End': '2024-01-02'
                    },
                    Granularity='MONTHLY',
                    Metrics=['BlendedCost']
                )
            
            print(f"✅ {service_name}: Available")
            available_services.append(service_name)
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print(f"⚠️  {service_name}: Access denied (may need permissions)")
            else:
                print(f"❌ {service_name}: {e}")
        except Exception as e:
            print(f"❌ {service_name}: {e}")
    
    return available_services

def check_free_tier_limits():
    """Check current usage against free tier limits"""
    print("\n📊 Checking Free Tier Usage...")
    
    try:
        # Check EC2 instances
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()
        
        running_instances = 0
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running':
                    running_instances += 1
        
        print(f"🖥️  Running EC2 instances: {running_instances}/750 hours (free tier)")
        
        # Check S3 buckets
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        print(f"🪣  S3 buckets: {len(buckets['Buckets'])}")
        
        # Check Lambda functions
        lambda_client = boto3.client('lambda')
        functions = lambda_client.list_functions()
        print(f"⚡ Lambda functions: {len(functions['Functions'])}/1M requests (free tier)")
        
        # Check RDS instances
        rds = boto3.client('rds')
        db_instances = rds.describe_db_instances()
        print(f"🗄️  RDS instances: {len(db_instances['DBInstances'])}/750 hours (free tier)")
        
    except ClientError as e:
        print(f"⚠️  Could not check current usage: {e}")

def main():
    """Main function to run all checks"""
    print("🚀 AWS Free Tier Eligibility Checker")
    print("=" * 50)
    
    # Check credentials
    if not check_aws_credentials():
        return
    
    # Check free tier eligibility
    check_free_tier_eligibility()
    
    # Check required services
    available_services = check_required_services()
    
    # Check current usage
    check_free_tier_limits()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"✅ Available services: {len(available_services)}")
    print("✅ Ready for free tier development!")
    print("\n💡 Recommendations:")
    print("   - Use t2.micro instances for EC2")
    print("   - Use EKS with managed node groups")
    print("   - Use Lambda for serverless functions")
    print("   - Use S3 for storage (5GB free)")
    print("   - Use RDS db.t2.micro for database")
    print("   - Always run cleanup scripts after testing")

if __name__ == "__main__":
    main()
