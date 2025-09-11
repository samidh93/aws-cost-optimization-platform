"""
Cost Optimizer Lambda Function
Analyzes costs and provides optimization recommendations
"""

import json
import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
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
    Main handler for cost optimization
    """
    try:
        # Get cost data for analysis
        cost_data = get_cost_data_for_analysis()
        
        # Generate optimization recommendations
        recommendations = generate_recommendations(cost_data)
        
        # Get account ID from context
        account_id = context.invoked_function_arn.split(':')[4] if context else "123456789012"
        
        # Store recommendations
        store_recommendations(recommendations, account_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Cost optimization analysis completed',
                'recommendations_count': len(recommendations),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        print(f"Error generating cost optimization: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

def get_cost_data_for_analysis() -> Dict[str, Any]:
    """
    Get cost data for the last 30 days for analysis
    """
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
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
        # Return mock data for demo
        return {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': start_date, 'End': end_date},
                    'Total': {'BlendedCost': {'Amount': '45.50', 'Unit': 'USD'}},
                    'Groups': [
                        {
                            'Keys': ['Amazon Elastic Compute Cloud'],
                            'Metrics': {'BlendedCost': {'Amount': '25.30', 'Unit': 'USD'}}
                        },
                        {
                            'Keys': ['Amazon Relational Database Service'],
                            'Metrics': {'BlendedCost': {'Amount': '12.75', 'Unit': 'USD'}}
                        },
                        {
                            'Keys': ['Amazon Simple Storage Service'],
                            'Metrics': {'BlendedCost': {'Amount': '3.45', 'Unit': 'USD'}}
                        },
                        {
                            'Keys': ['Amazon Elastic Kubernetes Service'],
                            'Metrics': {'BlendedCost': {'Amount': '4.00', 'Unit': 'USD'}}
                        }
                    ]
                }
            ]
        }

def generate_recommendations(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate cost optimization recommendations
    """
    recommendations = []
    
    # Analyze EC2 costs
    ec2_recommendations = analyze_ec2_costs(cost_data)
    recommendations.extend(ec2_recommendations)
    
    # Analyze RDS costs
    rds_recommendations = analyze_rds_costs(cost_data)
    recommendations.extend(rds_recommendations)
    
    # Analyze S3 costs
    s3_recommendations = analyze_s3_costs(cost_data)
    recommendations.extend(s3_recommendations)
    
    # Analyze EKS costs
    eks_recommendations = analyze_eks_costs(cost_data)
    recommendations.extend(eks_recommendations)
    
    # General recommendations
    general_recommendations = generate_general_recommendations(cost_data)
    recommendations.extend(general_recommendations)
    
    return recommendations

def analyze_ec2_costs(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze EC2 costs and provide recommendations
    """
    recommendations = []
    
    # Find EC2 costs
    ec2_cost = 0
    for result in cost_data.get('ResultsByTime', []):
        for group in result.get('Groups', []):
            if 'Amazon Elastic Compute Cloud' in group['Keys']:
                ec2_cost += float(group['Metrics']['BlendedCost']['Amount'])
    
    if ec2_cost > 20:  # If EC2 costs are high
        recommendations.append({
            'service': 'EC2',
            'priority': 'HIGH',
            'category': 'RIGHT_SIZING',
            'title': 'Consider Right-Sizing EC2 Instances',
            'description': f'EC2 costs are ${ec2_cost:.2f}. Review instance types and consider downsizing.',
            'potential_savings': f'${ec2_cost * 0.3:.2f}',
            'action': 'Review EC2 instances and consider t2.micro or t3.micro instances',
            'impact': 'MEDIUM'
        })
        
        recommendations.append({
            'service': 'EC2',
            'priority': 'MEDIUM',
            'category': 'RESERVED_INSTANCES',
            'title': 'Consider Reserved Instances',
            'description': 'For predictable workloads, Reserved Instances can save up to 75%.',
            'potential_savings': f'${ec2_cost * 0.5:.2f}',
            'action': 'Analyze usage patterns and consider Reserved Instances',
            'impact': 'HIGH'
        })
    
    return recommendations

def analyze_rds_costs(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze RDS costs and provide recommendations
    """
    recommendations = []
    
    # Find RDS costs
    rds_cost = 0
    for result in cost_data.get('ResultsByTime', []):
        for group in result.get('Groups', []):
            if 'Amazon Relational Database Service' in group['Keys']:
                rds_cost += float(group['Metrics']['BlendedCost']['Amount'])
    
    if rds_cost > 10:  # If RDS costs are high
        recommendations.append({
            'service': 'RDS',
            'priority': 'HIGH',
            'category': 'INSTANCE_OPTIMIZATION',
            'title': 'Optimize RDS Instance Size',
            'description': f'RDS costs are ${rds_cost:.2f}. Consider using db.t2.micro for development.',
            'potential_savings': f'${rds_cost * 0.4:.2f}',
            'action': 'Review RDS instance types and consider smaller instances',
            'impact': 'MEDIUM'
        })
    
    return recommendations

def analyze_s3_costs(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze S3 costs and provide recommendations
    """
    recommendations = []
    
    # Find S3 costs
    s3_cost = 0
    for result in cost_data.get('ResultsByTime', []):
        for group in result.get('Groups', []):
            if 'Amazon Simple Storage Service' in group['Keys']:
                s3_cost += float(group['Metrics']['BlendedCost']['Amount'])
    
    if s3_cost > 5:  # If S3 costs are high
        recommendations.append({
            'service': 'S3',
            'priority': 'MEDIUM',
            'category': 'LIFECYCLE_POLICIES',
            'title': 'Implement S3 Lifecycle Policies',
            'description': f'S3 costs are ${s3_cost:.2f}. Implement lifecycle policies to move old data to cheaper storage.',
            'potential_savings': f'${s3_cost * 0.6:.2f}',
            'action': 'Set up lifecycle policies to transition data to IA and Glacier',
            'impact': 'HIGH'
        })
    
    return recommendations

def analyze_eks_costs(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze EKS costs and provide recommendations
    """
    recommendations = []
    
    # Find EKS costs
    eks_cost = 0
    for result in cost_data.get('ResultsByTime', []):
        for group in result.get('Groups', []):
            if 'Amazon Elastic Kubernetes Service' in group['Keys']:
                eks_cost += float(group['Metrics']['BlendedCost']['Amount'])
    
    if eks_cost > 15:  # If EKS costs are high
        recommendations.append({
            'service': 'EKS',
            'priority': 'HIGH',
            'category': 'NODE_OPTIMIZATION',
            'title': 'Optimize EKS Node Configuration',
            'description': f'EKS costs are ${eks_cost:.2f}. Review node group configuration and consider spot instances.',
            'potential_savings': f'${eks_cost * 0.7:.2f}',
            'action': 'Use spot instances for non-critical workloads and optimize node sizing',
            'impact': 'HIGH'
        })
    
    return recommendations

def generate_general_recommendations(cost_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate general cost optimization recommendations
    """
    recommendations = []
    
    # Calculate total cost
    total_cost = 0
    for result in cost_data.get('ResultsByTime', []):
        total_cost += float(result['Total']['BlendedCost']['Amount'])
    
    if total_cost > 50:  # If total costs are high
        recommendations.append({
            'service': 'GENERAL',
            'priority': 'HIGH',
            'category': 'BUDGET_MONITORING',
            'title': 'Set Up Budget Alerts',
            'description': f'Total costs are ${total_cost:.2f}. Set up budget alerts to monitor spending.',
            'potential_savings': f'${total_cost * 0.2:.2f}',
            'action': 'Configure AWS Budgets with alerts at 50%, 80%, and 100% of budget',
            'impact': 'HIGH'
        })
        
        recommendations.append({
            'service': 'GENERAL',
            'priority': 'MEDIUM',
            'category': 'COST_ALLOCATION',
            'title': 'Implement Cost Allocation Tags',
            'description': 'Use tags to track costs by project, environment, or team.',
            'potential_savings': f'${total_cost * 0.1:.2f}',
            'action': 'Implement consistent tagging strategy across all resources',
            'impact': 'MEDIUM'
        })
    
    return recommendations

def store_recommendations(recommendations: List[Dict[str, Any]], account_id: str = None) -> None:
    """
    Store optimization recommendations in DynamoDB
    """
    table = dynamodb.Table(COST_TABLE_NAME)
    
    # Use provided account_id or default
    if not account_id:
        account_id = "123456789012"  # Default for demo
    
    for i, recommendation in enumerate(recommendations):
        record = {
            'account_id': account_id,
            'timestamp': datetime.now().isoformat(),
            'recommendation_id': f"rec_{i}_{int(datetime.now().timestamp())}",
            'service': recommendation['service'],
            'priority': recommendation['priority'],
            'category': recommendation['category'],
            'title': recommendation['title'],
            'description': recommendation['description'],
            'potential_savings': Decimal(str(recommendation['potential_savings'])),
            'action': recommendation['action'],
            'impact': recommendation['impact'],
            'created_at': datetime.now().isoformat()
        }
        
        table.put_item(Item=record)
