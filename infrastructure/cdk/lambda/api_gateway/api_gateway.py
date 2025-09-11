"""
API Gateway Lambda Function
Provides REST API endpoints for the frontend dashboard
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main handler for API Gateway requests
    """
    try:
        # Get the HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Handle CORS preflight requests
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Route requests based on path
        if path == '/health':
            return handle_health()
        elif path == '/api/v1/cost/summary':
            return handle_cost_summary(event)
        elif path == '/api/v1/cost/trends':
            return handle_cost_trends(event)
        elif path == '/api/v1/cost/services':
            return handle_cost_services(event)
        elif path == '/api/v1/budget/summary':
            return handle_budget_summary(event)
        elif path == '/api/v1/budget/':
            return handle_budget_alerts(event)
        elif path == '/api/v1/optimization/summary':
            return handle_optimization_summary(event)
        elif path == '/api/v1/optimization/':
            return handle_optimization_recommendations(event)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_health() -> Dict[str, Any]:
    """Handle health check endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Cost Optimization Platform API'
        })
    }

def handle_cost_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle cost summary endpoint"""
    # Get query parameters
    query_params = event.get('queryStringParameters') or {}
    days = int(query_params.get('days', 30))
    
    # Generate mock data
    total_cost = 1250.75
    daily_average = total_cost / days
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'total_cost': total_cost,
            'daily_average': daily_average,
            'period_days': days,
            'currency': 'USD',
            'last_updated': datetime.now().isoformat()
        })
    }

def handle_cost_trends(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle cost trends endpoint"""
    query_params = event.get('queryStringParameters') or {}
    days = int(query_params.get('days', 30))
    
    # Generate mock trend data
    trends = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        cost = 25.50 + (i * 0.5) + (i % 7 * 2.0)  # Mock trend
        trends.append({
            'date': date,
            'cost': round(cost, 2)
        })
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'trends': trends,
            'period_days': days
        })
    }

def handle_cost_services(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle cost services breakdown endpoint"""
    query_params = event.get('queryStringParameters') or {}
    days = int(query_params.get('days', 30))
    
    # Generate mock service data
    services = [
        {'service': 'Amazon Elastic Compute Cloud', 'cost': 450.25, 'percentage': 36.0},
        {'service': 'Amazon Simple Storage Service', 'cost': 125.50, 'percentage': 10.0},
        {'service': 'Amazon Relational Database Service', 'cost': 300.00, 'percentage': 24.0},
        {'service': 'Amazon Lambda', 'cost': 75.25, 'percentage': 6.0},
        {'service': 'Amazon CloudWatch', 'cost': 50.00, 'percentage': 4.0},
        {'service': 'Other Services', 'cost': 249.75, 'percentage': 20.0}
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'services': services,
            'total_cost': sum(s['cost'] for s in services),
            'period_days': days
        })
    }

def handle_budget_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle budget summary endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'total_budgets': 3,
            'active_alerts': 1,
            'monthly_budget': 2000.00,
            'current_spending': 1250.75,
            'remaining_budget': 749.25,
            'utilization_percentage': 62.5
        })
    }

def handle_budget_alerts(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle budget alerts endpoint"""
    query_params = event.get('queryStringParameters') or {}
    limit = int(query_params.get('limit', 10))
    
    # Generate mock alert data
    alerts = [
        {
            'id': 1,
            'alert_type': 'BUDGET_THRESHOLD',
            'service': 'Amazon Elastic Compute Cloud',
            'current_cost': 450.25,
            'budget_limit': 400.00,
            'message': 'EC2 spending exceeded budget threshold',
            'created_at': (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            'id': 2,
            'alert_type': 'FORECAST_EXCEED',
            'service': 'Amazon Relational Database Service',
            'current_cost': 300.00,
            'budget_limit': 250.00,
            'message': 'RDS spending forecasted to exceed budget',
            'created_at': (datetime.now() - timedelta(hours=5)).isoformat()
        }
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'alerts': alerts[:limit],
            'total_count': len(alerts)
        })
    }

def handle_optimization_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle optimization summary endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'total_recommendations': 5,
            'high_priority': 2,
            'potential_savings': 450.75,
            'implementation_effort': 'Medium',
            'last_analysis': datetime.now().isoformat()
        })
    }

def handle_optimization_recommendations(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle optimization recommendations endpoint"""
    query_params = event.get('queryStringParameters') or {}
    limit = int(query_params.get('limit', 10))
    
    # Generate mock recommendation data
    recommendations = [
        {
            'id': 1,
            'service': 'Amazon Elastic Compute Cloud',
            'priority': 'HIGH',
            'category': 'Compute Optimization',
            'title': 'Resize EC2 Instances',
            'description': 'Consider resizing t3.medium instances to t3.small for non-production workloads',
            'potential_savings': 150.00,
            'action': 'Review instance utilization and resize accordingly',
            'impact': 'Medium',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'service': 'Amazon Simple Storage Service',
            'priority': 'MEDIUM',
            'category': 'Storage Optimization',
            'title': 'Enable S3 Lifecycle Policies',
            'description': 'Move old data to cheaper storage classes',
            'potential_savings': 75.50,
            'action': 'Configure lifecycle policies for S3 buckets',
            'impact': 'Low',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 3,
            'service': 'Amazon Relational Database Service',
            'priority': 'HIGH',
            'category': 'Database Optimization',
            'title': 'Optimize RDS Instance',
            'description': 'Consider using Aurora Serverless for variable workloads',
            'potential_savings': 225.25,
            'action': 'Evaluate Aurora Serverless migration',
            'impact': 'High',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'recommendations': recommendations[:limit],
            'total_count': len(recommendations)
        })
    }
