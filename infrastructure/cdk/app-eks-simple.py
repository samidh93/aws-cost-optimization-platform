#!/usr/bin/env python3
"""
Simplified AWS CDK App for EKS-based Cost Optimization Platform
Phase 3: Kubernetes Workloads - Simplified Version
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    aws_ecr as ecr,
    Duration,
    CfnOutput
)
from constructs import Construct


class CostOptimizationEKSSimpleStack(Stack):
    """Simplified EKS-based Cost Optimization Platform Stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC for EKS cluster
        self.vpc = self._create_vpc()
        
        # Create ECR repositories
        self.ecr_repos = self._create_ecr_repositories()
        
        # Create EKS cluster (simplified)
        self.eks_cluster = self._create_eks_cluster()
        
        # Output important values
        self._create_outputs()

    def _create_vpc(self) -> ec2.Vpc:
        """Create VPC for EKS cluster"""
        return ec2.Vpc(
            self, "EKSVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            nat_gateways=1,  # Single NAT gateway for cost optimization
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
            ]
        )

    def _create_ecr_repositories(self) -> dict:
        """Create ECR repositories for container images"""
        repos = {}
        
        # Backend repository
        repos['backend'] = ecr.Repository(
            self, "BackendRepository",
            repository_name="cost-optimization-backend",
            image_scan_on_push=True,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10,
                    rule_priority=1
                )
            ]
        )
        
        # Frontend repository
        repos['frontend'] = ecr.Repository(
            self, "FrontendRepository",
            repository_name="cost-optimization-frontend",
            image_scan_on_push=True,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10,
                    rule_priority=1
                )
            ]
        )
        
        # Database repository
        repos['database'] = ecr.Repository(
            self, "DatabaseRepository",
            repository_name="cost-optimization-database",
            image_scan_on_push=True,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=5,
                    rule_priority=1
                )
            ]
        )
        
        return repos

    def _create_eks_cluster(self) -> eks.Cluster:
        """Create simplified EKS cluster"""
        
        # Create cluster admin role
        cluster_admin_role = iam.Role(
            self, "EKSClusterAdminRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("eks.amazonaws.com"),
                iam.AccountRootPrincipal()
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy")
            ]
        )
        
        # Create EKS cluster with default capacity (simplified)
        cluster = eks.Cluster(
            self, "CostOptimizationCluster",
            cluster_name="cost-optimization-cluster",
            version=eks.KubernetesVersion.V1_25,
            vpc=self.vpc,
            masters_role=cluster_admin_role,
            default_capacity=2,  # Use default capacity instead of managed node group
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO)
        )
        
        return cluster

    def _create_outputs(self):
        """Create CloudFormation outputs"""
        CfnOutput(
            self, "EKSClusterName",
            value=self.eks_cluster.cluster_name,
            description="EKS Cluster Name"
        )
        
        CfnOutput(
            self, "EKSClusterEndpoint",
            value=self.eks_cluster.cluster_endpoint,
            description="EKS Cluster Endpoint"
        )
        
        CfnOutput(
            self, "EKSClusterArn",
            value=self.eks_cluster.cluster_arn,
            description="EKS Cluster ARN"
        )
        
        CfnOutput(
            self, "BackendRepositoryURI",
            value=self.ecr_repos['backend'].repository_uri,
            description="Backend ECR Repository URI"
        )
        
        CfnOutput(
            self, "FrontendRepositoryURI",
            value=self.ecr_repos['frontend'].repository_uri,
            description="Frontend ECR Repository URI"
        )
        
        CfnOutput(
            self, "DatabaseRepositoryURI",
            value=self.ecr_repos['database'].repository_uri,
            description="Database ECR Repository URI"
        )


app = cdk.App()
CostOptimizationEKSSimpleStack(app, "CostOptimizationEKSSimple")
app.synth()
