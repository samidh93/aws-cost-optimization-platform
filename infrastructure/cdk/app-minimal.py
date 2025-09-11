#!/usr/bin/env python3
"""
AWS Cost Optimization Platform - MINIMAL VERSION
This version uses ONLY free tier resources to minimize costs
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_apigateway as apigateway,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class CostOptimizationMinimalStack(Stack):
    """Minimal stack using ONLY free tier resources"""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create VPC (free)
        self.vpc = self._create_vpc()
        
        # Create S3 bucket (5GB free)
        self.s3_bucket = self._create_s3_bucket()
        
        # Create DynamoDB table (25GB free)
        self.dynamodb_table = self._create_dynamodb_table()
        
        # Create Lambda functions (1M requests free)
        self.lambda_functions = self._create_lambda_functions()
        
        # Create API Gateway Lambda function
        self.api_gateway_lambda = self._create_api_gateway_lambda()
        
        # Create API Gateway (1M requests free)
        self.api_gateway = self._create_api_gateway()
        
        # Output important values
        self._create_outputs()
    
    def _create_vpc(self) -> ec2.Vpc:
        """Create minimal VPC - NO NAT Gateway to avoid costs"""
        return ec2.Vpc(
            self, "MinimalVPC",
            max_azs=2,
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ],
            # NO NAT Gateway - saves $45/month!
            nat_gateways=0
        )
    
    def _create_s3_bucket(self) -> s3.Bucket:
        """Create S3 bucket for cost data storage"""
        return s3.Bucket(
            self, "CostDataBucket",
            bucket_name=f"cost-optimization-minimal-{self.account}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteOldVersions",
                    enabled=True,
                    noncurrent_version_expiration=Duration.days(7)  # Shorter retention
                )
            ]
        )
    
    def _create_dynamodb_table(self) -> dynamodb.Table:
        """Create DynamoDB table for cost tracking"""
        return dynamodb.Table(
            self, "CostTrackingTable",
            table_name="cost-tracking-minimal",
            partition_key=dynamodb.Attribute(
                name="account_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=False  # Disable to save costs
        )
    
    def _create_lambda_functions(self) -> dict:
        """Create Lambda functions for cost processing"""
        functions = {}
        
        # Cost processor (simplified)
        functions['cost_processor'] = lambda_.Function(
            self, "CostProcessor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="cost_processor.handler",
            code=lambda_.Code.from_asset("lambda/cost_processor"),
            timeout=Duration.minutes(2),  # Shorter timeout
            memory_size=128,  # Minimum memory
            environment={
                "COST_TABLE_NAME": "cost-tracking-minimal",
                "S3_BUCKET": f"cost-optimization-minimal-{self.account}"
            }
            # NO VPC - saves on NAT Gateway costs
        )
        
        # Budget alert (simplified)
        functions['budget_alert'] = lambda_.Function(
            self, "BudgetAlert",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="budget_alert.handler",
            code=lambda_.Code.from_asset("lambda/budget_alert"),
            timeout=Duration.minutes(1),  # Shorter timeout
            memory_size=128,  # Minimum memory
            environment={
                "COST_TABLE_NAME": "cost-tracking-minimal"
            }
        )
        
        # Grant permissions
        self.dynamodb_table.grant_read_write_data(functions['cost_processor'])
        self.dynamodb_table.grant_read_write_data(functions['budget_alert'])
        
        self.s3_bucket.grant_read_write(functions['cost_processor'])
        
        return functions
    
    def _create_api_gateway_lambda(self) -> lambda_.Function:
        """Create API Gateway Lambda function"""
        return lambda_.Function(
            self, "APIGatewayLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="api_gateway.handler",
            code=lambda_.Code.from_asset("lambda/api_gateway"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                'COST_TABLE_NAME': self.dynamodb_table.table_name,
                'S3_BUCKET': self.s3_bucket.bucket_name
            },
            description="API Gateway Lambda function for frontend dashboard"
        )
    
    def _create_api_gateway(self) -> apigateway.RestApi:
        """Create API Gateway for the platform"""
        api = apigateway.RestApi(
            self, "CostOptimizationAPI",
            rest_api_name="Cost Optimization Platform (Minimal)",
            description="Minimal cost optimization platform",
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            )
        )
        
        # Create Lambda integration with proxy
        lambda_integration = apigateway.LambdaIntegration(
            self.api_gateway_lambda,
            proxy=True
        )
        
        # Add CORS support
        api.root.add_cors_preflight(
            allow_origins=["*"],
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"]
        )
        
        # Health check endpoint
        health_resource = api.root.add_resource("health")
        health_resource.add_method("GET", lambda_integration)
        
        # API v1 endpoints
        api_v1 = api.root.add_resource("api").add_resource("v1")
        
        # Cost endpoints
        cost_resource = api_v1.add_resource("cost")
        cost_resource.add_method("GET", lambda_integration)
        
        cost_summary = cost_resource.add_resource("summary")
        cost_summary.add_method("GET", lambda_integration)
        
        cost_trends = cost_resource.add_resource("trends")
        cost_trends.add_method("GET", lambda_integration)
        
        cost_services = cost_resource.add_resource("services")
        cost_services.add_method("GET", lambda_integration)
        
        # Budget endpoints
        budget_resource = api_v1.add_resource("budget")
        budget_resource.add_method("GET", lambda_integration)
        
        budget_summary = budget_resource.add_resource("summary")
        budget_summary.add_method("GET", lambda_integration)
        
        # Optimization endpoints
        optimization_resource = api_v1.add_resource("optimization")
        optimization_resource.add_method("GET", lambda_integration)
        
        optimization_summary = optimization_resource.add_resource("summary")
        optimization_summary.add_method("GET", lambda_integration)
        
        return api
    
    def _create_outputs(self):
        """Create CloudFormation outputs"""
        CfnOutput(
            self, "APIGatewayURL",
            value=self.api_gateway.url,
            description="API Gateway URL for the minimal platform"
        )
        
        CfnOutput(
            self, "S3BucketName",
            value=self.s3_bucket.bucket_name,
            description="S3 bucket for cost data storage"
        )
        
        CfnOutput(
            self, "DynamoDBTableName",
            value=self.dynamodb_table.table_name,
            description="DynamoDB table for cost tracking"
        )

# CDK App
app = cdk.App()

# Create the minimal stack
CostOptimizationMinimalStack(
    app, "CostOptimizationMinimal",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    )
)

app.synth()
