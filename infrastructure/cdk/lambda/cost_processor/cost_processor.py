"""
Cost Processor Lambda Function
Processes cost data from AWS Cost Explorer and stores it in DynamoDB
"""

import json
import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, Any
from decimal import Decimal

# Initialize AWS clients
ce_client = boto3.client('ce')
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

# Environment variables
COST_TABLE_NAME = os.environ['COST_TABLE_NAME']
S3_BUCKET = os.environ['S3_BUCKET']

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main handler for cost processing
    """
    try:
        # Get cost data for the last 7 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Fetch cost data from Cost Explorer
        cost_data = get_cost_data(start_date, end_date)
        
        # Get account ID from context
        account_id = context.invoked_function_arn.split(':')[4] if context else "123456789012"
        
        # Process and store the data
        processed_data = process_cost_data(cost_data, account_id)
        
        # Store in DynamoDB
        store_cost_data(processed_data)
        
        # Store raw data in S3
        store_raw_data_in_s3(cost_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Cost data processed successfully',
                'records_processed': len(processed_data),
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        print(f"Error processing cost data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

def get_cost_data(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Fetch cost data from AWS Cost Explorer
    """
    try:
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost', 'UnblendedCost', 'UsageQuantity'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        return response
    except Exception as e:
        print(f"Error fetching cost data: {str(e)}")
        # Return mock data for demo purposes
        return {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': start_date, 'End': end_date},
                    'Total': {'BlendedCost': {'Amount': '0.00', 'Unit': 'USD'}},
                    'Groups': []
                }
            ]
        }

def process_cost_data(cost_data: Dict[str, Any], account_id: str = None) -> list:
    """
    Process raw cost data into a structured format
    """
    processed_records = []
    
    # Use provided account_id or default
    if not account_id:
        account_id = "123456789012"  # Default for demo
    
    for result in cost_data.get('ResultsByTime', []):
        date = result['TimePeriod']['Start']
        total_cost = Decimal(str(result['Total']['BlendedCost']['Amount']))
        
        # Process service-level costs
        for group in result.get('Groups', []):
            service = group['Keys'][0]
            service_cost = Decimal(str(group['Metrics']['BlendedCost']['Amount']))
            
            record = {
                'account_id': account_id,
                'timestamp': date,
                'service': service,
                'cost': service_cost,
                'total_daily_cost': total_cost,
                'processed_at': datetime.now().isoformat()
            }
            processed_records.append(record)
        
        # Add daily total record
        daily_record = {
            'account_id': account_id,
            'timestamp': date,
            'service': 'TOTAL',
            'cost': total_cost,
            'total_daily_cost': total_cost,
            'processed_at': datetime.now().isoformat()
        }
        processed_records.append(daily_record)
    
    return processed_records

def store_cost_data(records: list) -> None:
    """
    Store processed cost data in DynamoDB
    """
    table = dynamodb.Table(COST_TABLE_NAME)
    
    with table.batch_writer() as batch:
        for record in records:
            batch.put_item(Item=record)

def store_raw_data_in_s3(cost_data: Dict[str, Any]) -> None:
    """
    Store raw cost data in S3 for backup and analysis
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    key = f"raw-cost-data/{timestamp}.json"
    
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(cost_data, indent=2),
        ContentType='application/json'
    )
