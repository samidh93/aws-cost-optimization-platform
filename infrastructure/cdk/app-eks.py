#!/usr/bin/env python3
"""
AWS CDK App for EKS-based Cost Optimization Platform
Phase 3: Kubernetes Workloads
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    Duration,
    CfnOutput
)
from constructs import Construct


class CostOptimizationEKSStack(Stack):
    """EKS-based Cost Optimization Platform Stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC for EKS cluster
        self.vpc = self._create_vpc()
        
        # Create ECR repositories
        self.ecr_repos = self._create_ecr_repositories()
        
        # Create EKS cluster
        self.eks_cluster = self._create_eks_cluster()
        
        # Create IAM roles for service accounts
        self._create_iam_roles()
        
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
        """Create EKS cluster with managed node group"""
        
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
        
        # Create EKS cluster
        cluster = eks.Cluster(
            self, "CostOptimizationCluster",
            cluster_name="cost-optimization-cluster",
            version=eks.KubernetesVersion.V1_25,
            vpc=self.vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
            masters_role=cluster_admin_role,
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            default_capacity=0,  # We'll add managed node group separately
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
                eks.ClusterLoggingTypes.SCHEDULER
            ]
        )
        
        # Add managed node group
        cluster.add_nodegroup_capacity(
            "ManagedNodeGroup",
            instance_types=[ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO)],
            min_size=1,
            max_size=3,
            desired_size=2,
            disk_size=20,
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            capacity_type=eks.CapacityType.ON_DEMAND,
            labels={
                "node-type": "general",
                "environment": "production"
            }
        )
        
        # Add AWS Load Balancer Controller
        cluster.add_helm_chart(
            "AWSLoadBalancerController",
            chart="aws-load-balancer-controller",
            repository="https://aws.github.io/eks-charts",
            namespace="kube-system",
            values={
                "clusterName": cluster.cluster_name,
                "serviceAccount": {
                    "create": False,
                    "name": "aws-load-balancer-controller"
                }
            }
        )
        
        return cluster

    def _create_iam_roles(self):
        """Create IAM roles for service accounts"""
        
        # AWS Load Balancer Controller role
        alb_controller_role = iam.Role(
            self, "AWSLoadBalancerControllerRole",
            assumed_by=iam.FederatedPrincipal(
                f"arn:aws:iam::{self.account}:oidc-provider/"
                f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}",
                {
                    "StringEquals": {
                        f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}:sub": 
                        "system:serviceaccount:kube-system:aws-load-balancer-controller",
                        f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}:aud": 
                        "sts.amazonaws.com"
                    }
                },
                "sts:AssumeRoleWithWebIdentity"
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSLoadBalancerControllerPolicy")
            ]
        )
        
        # Backend service role
        backend_role = iam.Role(
            self, "BackendServiceRole",
            assumed_by=iam.FederatedPrincipal(
                f"arn:aws:iam::{self.account}:oidc-provider/"
                f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}",
                {
                    "StringEquals": {
                        f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}:sub": 
                        "system:serviceaccount:default:backend-service-account",
                        f"{self.eks_cluster.open_id_connect_provider.open_id_connect_provider_issuer}:aud": 
                        "sts.amazonaws.com"
                    }
                },
                "sts:AssumeRoleWithWebIdentity"
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

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
CostOptimizationEKSStack(app, "CostOptimizationEKS")
app.synth()
