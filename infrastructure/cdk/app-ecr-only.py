#!/usr/bin/env python3
"""
AWS CDK App for ECR repositories only
Phase 3: Kubernetes Workloads - ECR Setup
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    CfnOutput
)
from constructs import Construct


class CostOptimizationECRStack(Stack):
    """ECR repositories for Cost Optimization Platform"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ECR repositories
        self.ecr_repos = self._create_ecr_repositories()
        
        # Output important values
        self._create_outputs()

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

    def _create_outputs(self):
        """Create CloudFormation outputs"""
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
CostOptimizationECRStack(app, "CostOptimizationECR")
app.synth()
