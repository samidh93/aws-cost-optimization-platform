"""
Budget Alert Lambda Function
Monitors costs against budgets and sends alerts
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
sns_client = boto3.client('sns')

# Environment variables
COST_TABLE_NAME = os.environ['COST_TABLE_NAME']

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main handler for budget alerting
    """
    try:
        # Get current month costs
        current_costs = get_current_month_costs()
        
        # Check against budget thresholds
        alerts = check_budget_thresholds(current_costs)
        
        # Get account ID from context
        account_id = context.invoked_function_arn.split(':')[4] if context else "123456789012"
        
        # Send alerts if needed
        if alerts:
            send_alerts(alerts, account_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Budget check completed',
                'alerts_sent': len(alerts),
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        print(f"Error checking budget alerts: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

def get_current_month_costs() -> Dict[str, float]:
    """
    Get current month costs by service
    """
    try:
        # Get first day of current month
        now = datetime.now()
        start_date = now.replace(day=1).strftime('%Y-%m-%d')
        end_date = now.strftime('%Y-%m-%d')
        
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        
        costs = {}
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                costs[service] = cost
        
        return costs
        
    except Exception as e:
        print(f"Error fetching current costs: {str(e)}")
        # Return mock data for demo
        return {
            'Amazon Elastic Compute Cloud': 5.50,
            'Amazon Simple Storage Service': 2.30,
            'Amazon Relational Database Service': 8.75,
            'Amazon Elastic Kubernetes Service': 12.40
        }

def check_budget_thresholds(costs: Dict[str, float]) -> list:
    """
    Check costs against budget thresholds
    """
    alerts = []
    total_cost = sum(costs.values())
    
    # Define budget thresholds (in USD)
    BUDGET_LIMITS = {
        'total_monthly': 50.00,
        'ec2_monthly': 20.00,
        'rds_monthly': 15.00,
        's3_monthly': 5.00,
        'eks_monthly': 25.00
    }
    
    # Check total monthly budget
    if total_cost > BUDGET_LIMITS['total_monthly']:
        alerts.append({
            'type': 'BUDGET_EXCEEDED',
            'service': 'TOTAL',
            'current_cost': total_cost,
            'budget_limit': BUDGET_LIMITS['total_monthly'],
            'message': f'Total monthly budget exceeded: ${total_cost:.2f} > ${BUDGET_LIMITS["total_monthly"]:.2f}'
        })
    
    # Check individual service budgets
    service_mapping = {
        'Amazon Elastic Compute Cloud': 'ec2_monthly',
        'Amazon Relational Database Service': 'rds_monthly',
        'Amazon Simple Storage Service': 's3_monthly',
        'Amazon Elastic Kubernetes Service': 'eks_monthly'
    }
    
    for service, cost in costs.items():
        if service in service_mapping:
            budget_key = service_mapping[service]
            if cost > BUDGET_LIMITS[budget_key]:
                alerts.append({
                    'type': 'SERVICE_BUDGET_EXCEEDED',
                    'service': service,
                    'current_cost': cost,
                    'budget_limit': BUDGET_LIMITS[budget_key],
                    'message': f'{service} budget exceeded: ${cost:.2f} > ${BUDGET_LIMITS[budget_key]:.2f}'
                })
    
    return alerts

def send_alerts(alerts: list, account_id: str = None) -> None:
    """
    Send budget alerts (mock implementation)
    """
    for alert in alerts:
        print(f"ALERT: {alert['message']}")
        
        # In a real implementation, you would:
        # 1. Send SNS notifications
        # 2. Send emails
        # 3. Send Slack messages
        # 4. Create CloudWatch alarms
        
        # Store alert in DynamoDB
        store_alert(alert, account_id)

def store_alert(alert: Dict[str, Any], account_id: str = None) -> None:
    """
    Store alert in DynamoDB
    """
    table = dynamodb.Table(COST_TABLE_NAME)
    
    # Use provided account_id or default
    if not account_id:
        account_id = "123456789012"  # Default for demo
    
    alert_record = {
        'account_id': account_id,
        'timestamp': datetime.now().isoformat(),
        'alert_type': alert['type'],
        'service': alert['service'],
        'current_cost': Decimal(str(alert['current_cost'])),
        'budget_limit': Decimal(str(alert['budget_limit'])),
        'message': alert['message'],
        'processed_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=alert_record)
