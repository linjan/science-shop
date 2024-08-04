from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, Lambda
from diagrams.aws.mobile import Amplify
from diagrams.aws.database import RDS, ElastiCache, Dynamodb
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.security import Cognito, SecretsManager
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import Kinesis, EMR, Glue, Redshift
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch, Config
from diagrams.aws.devtools import XRay
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service

with Diagram("Life Science Shop Platform", show=False, direction="TB", filename="architecture"):
    cf = CloudFront("CloudFront CDN")
    
    with Cluster("VPC"):
        alb = ELB("Application Load Balancer")

        # EKS cluster w/ Karpenter
        # Also great way to use Spot instances        
        with Cluster("EKS Cluster"):
            eks = EKS("EKS")
            
            with Cluster("Karpenter"):
                karpenter = Pod("Karpenter")
            
            # Amplify help us easier develop mobile/desktop app
            with Cluster("Web Frontend"):
                web = Amplify("Amplify Web App")
            
            with Cluster("API Backend"):
                api = Deployment("API Service")
            
            with Cluster("Authentication"):
                auth = Deployment("Auth Service")
            
            karpenter >> [web, api, auth]
        
        rds = RDS("RDS (PostgreSQL)")
        cache = ElastiCache("ElastiCache (Redis)")
        ddb = Dynamodb("DynamoDB")
        
        cognito = Cognito("Cognito")
        secrets = SecretsManager("Secrets Manager")
        
        # Event processing
        with Cluster("Real-time Data Processing"):
            kinesis = Kinesis("Kinesis Data Streams")
            lambda_fn = Lambda("Lambda")
            emr = EMR("EMR")
            glue = Glue("Glue")
            redshift = Redshift("Redshift")
        
        s3 = S3("S3 Data Lake")
        sqs = SQS("SQS")
        
        cloudwatch = Cloudwatch("CloudWatch")
        config = Config("Config")
        xray = XRay("X-Ray")
