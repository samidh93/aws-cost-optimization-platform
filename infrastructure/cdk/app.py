#!/usr/bin/env python3
"""
AWS Cost Optimization Platform - CDK App
This app deploys the core infrastructure using only free tier resources.
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_rds as rds,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class CostOptimizationStack(Stack):
    """Main stack for the Cost Optimization Platform"""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create VPC for the platform
        self.vpc = self._create_vpc()
        
        # Create S3 bucket for cost data storage
        self.cost_data_bucket = self._create_s3_bucket()
        
        # Create DynamoDB table for cost tracking
        self.cost_table = self._create_dynamodb_table()
        
        # Create RDS instance for metadata storage
        self.rds_instance = self._create_rds_instance()
        
        # Create Lambda functions
        self.lambda_functions = self._create_lambda_functions()
        
        # Create API Gateway
        self.api_gateway = self._create_api_gateway()
        
        # Create EKS cluster
        self.eks_cluster = self._create_eks_cluster()
        
        # Create CloudWatch dashboards
        self._create_cloudwatch_dashboard()
        
        # Output important values
        self._create_outputs()
    
    def _create_vpc(self) -> ec2.Vpc:
        """Create VPC with public and private subnets"""
        return ec2.Vpc(
            self, "CostOptimizationVPC",
            max_azs=2,  # Use only 2 AZs to stay within free tier
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ],
            nat_gateways=1  # Only 1 NAT gateway to minimize costs
        )
    
    def _create_s3_bucket(self) -> s3.Bucket:
        """Create S3 bucket for cost data storage"""
        return s3.Bucket(
            self, "CostDataBucket",
            bucket_name=f"cost-optimization-data-{self.account}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,  # For demo purposes
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteOldVersions",
                    enabled=True,
                    noncurrent_version_expiration=Duration.days(30)
                )
            ]
        )
    
    def _create_dynamodb_table(self) -> dynamodb.Table:
        """Create DynamoDB table for cost tracking"""
        return dynamodb.Table(
            self, "CostTrackingTable",
            table_name="cost-tracking",
            partition_key=dynamodb.Attribute(
                name="account_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For demo purposes
            point_in_time_recovery=True
        )
    
    def _create_rds_instance(self) -> rds.DatabaseInstance:
        """Create RDS instance for metadata storage"""
        # Create security group for RDS
        rds_security_group = ec2.SecurityGroup(
            self, "RDSSecurityGroup",
            vpc=self.vpc,
            description="Security group for RDS instance"
        )
        
        # Allow access from VPC
        rds_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(self.vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="PostgreSQL access from VPC"
        )
        
        return rds.DatabaseInstance(
            self, "CostOptimizationDB",
            database_name="cost_optimization",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15_4
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2,
                ec2.InstanceSize.MICRO  # Free tier eligible
            ),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            security_groups=[rds_security_group],
            removal_policy=RemovalPolicy.DESTROY,  # For demo purposes
            deletion_protection=False,
            backup_retention=Duration.days(1),  # Minimal backup
            delete_automated_backups=True
        )
    
    def _create_lambda_functions(self) -> dict:
        """Create Lambda functions for cost processing"""
        functions = {}
        
        # Cost data processor
        functions['cost_processor'] = lambda_.Function(
            self, "CostProcessor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="cost_processor.handler",
            code=lambda_.Code.from_asset("lambda/cost_processor"),
            timeout=Duration.minutes(5),
            memory_size=128,  # Free tier eligible
            environment={
                "COST_TABLE_NAME": "cost-tracking",
                "S3_BUCKET": f"cost-optimization-data-{self.account}",
                "RDS_ENDPOINT": "placeholder"  # Will be updated after RDS creation
            },
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            )
        )
        
        # Budget alert handler
        functions['budget_alert'] = lambda_.Function(
            self, "BudgetAlert",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="budget_alert.handler",
            code=lambda_.Code.from_asset("lambda/budget_alert"),
            timeout=Duration.minutes(2),
            memory_size=128,  # Free tier eligible
            environment={
                "COST_TABLE_NAME": "cost-tracking"
            }
        )
        
        # Cost optimizer
        functions['cost_optimizer'] = lambda_.Function(
            self, "CostOptimizer",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="cost_optimizer.handler",
            code=lambda_.Code.from_asset("lambda/cost_optimizer"),
            timeout=Duration.minutes(10),
            memory_size=256,  # Free tier eligible
            environment={
                "COST_TABLE_NAME": "cost-tracking",
                "S3_BUCKET": f"cost-optimization-data-{self.account}"
            }
        )
        
        # Grant permissions
        self.cost_table.grant_read_write_data(functions['cost_processor'])
        self.cost_table.grant_read_write_data(functions['budget_alert'])
        self.cost_table.grant_read_write_data(functions['cost_optimizer'])
        
        self.cost_data_bucket.grant_read_write(functions['cost_processor'])
        self.cost_data_bucket.grant_read_write(functions['cost_optimizer'])
        
        return functions
    
    def _create_api_gateway(self) -> apigateway.RestApi:
        """Create API Gateway for the platform"""
        api = apigateway.RestApi(
            self, "CostOptimizationAPI",
            rest_api_name="Cost Optimization Platform",
            description="API for cost optimization platform",
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            )
        )
        
        # Add CORS - using Options method instead
        api.root.add_method(
            "OPTIONS",
            apigateway.MockIntegration(
                integration_responses=[{
                    'statusCode': '200',
                    'response_parameters': {
                        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'"
                    }
                }],
                passthrough_behavior=apigateway.PassthroughBehavior.WHEN_NO_MATCH,
                request_templates={"application/json": '{"statusCode": 200}'}
            ),
            method_responses=[{
                'statusCode': '200',
                'response_parameters': {
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Origin': True,
                    'method.response.header.Access-Control-Allow-Methods': True
                }
            }]
        )
        
        # Cost data endpoint
        cost_resource = api.root.add_resource("cost")
        cost_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(self.lambda_functions['cost_processor'])
        )
        
        # Budget alerts endpoint
        budget_resource = api.root.add_resource("budget")
        budget_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(self.lambda_functions['budget_alert'])
        )
        
        # Optimization recommendations endpoint
        optimization_resource = api.root.add_resource("optimization")
        optimization_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(self.lambda_functions['cost_optimizer'])
        )
        
        return api
    
    def _create_eks_cluster(self) -> eks.Cluster:
        """Create EKS cluster for containerized workloads"""
        # Create cluster without node group initially
        cluster = eks.Cluster(
            self, "CostOptimizationCluster",
            version=eks.KubernetesVersion.V1_25,
            vpc=self.vpc,
            vpc_subnets=[ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            )],
            endpoint_access=eks.EndpointAccess.PRIVATE,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
                eks.ClusterLoggingTypes.SCHEDULER
            ]
        )
        
        # Add managed node group with t3.micro instances
        cluster.add_nodegroup_capacity(
            "CostOptimizationNodes",
            instance_types=[ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.MICRO
            )],
            min_size=1,
            max_size=3,
            desired_size=1,
            disk_size=20,  # GB
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            capacity_type=eks.CapacityType.ON_DEMAND
        )
        
        return cluster
    
    def _create_cloudwatch_dashboard(self) -> cloudwatch.Dashboard:
        """Create CloudWatch dashboard for monitoring"""
        dashboard = cloudwatch.Dashboard(
            self, "CostOptimizationDashboard",
            dashboard_name="CostOptimizationPlatform"
        )
        
        # Add widgets for cost monitoring
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Lambda Invocations",
                left=[self.lambda_functions['cost_processor'].metric_invocations()],
                width=12,
                height=6
            ),
            cloudwatch.GraphWidget(
                title="DynamoDB Read/Write Capacity",
                left=[self.cost_table.metric_consumed_read_capacity_units()],
                right=[self.cost_table.metric_consumed_write_capacity_units()],
                width=12,
                height=6
            )
        )
        
        return dashboard
    
    def _create_outputs(self):
        """Create CloudFormation outputs"""
        CfnOutput(
            self, "VPCId",
            value=self.vpc.vpc_id,
            description="VPC ID for the cost optimization platform"
        )
        
        CfnOutput(
            self, "S3BucketName",
            value=self.cost_data_bucket.bucket_name,
            description="S3 bucket for cost data storage"
        )
        
        CfnOutput(
            self, "DynamoDBTableName",
            value=self.cost_table.table_name,
            description="DynamoDB table for cost tracking"
        )
        
        CfnOutput(
            self, "RDSEndpoint",
            value=self.rds_instance.instance_endpoint.hostname,
            description="RDS instance endpoint"
        )
        
        CfnOutput(
            self, "APIGatewayURL",
            value=self.api_gateway.url,
            description="API Gateway URL"
        )
        
        CfnOutput(
            self, "EKSClusterName",
            value=self.eks_cluster.cluster_name,
            description="EKS cluster name"
        )

# CDK App
app = cdk.App()

# Create the main stack
CostOptimizationStack(
    app, "CostOptimizationPlatform",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    )
)

app.synth()
