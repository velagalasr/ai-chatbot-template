# Deploying to AWS

This guide covers multiple AWS deployment options.

## Option 1: AWS ECS (Elastic Container Service)

### Prerequisites

- AWS Account
- AWS CLI configured
- Docker installed
- ECR repository created

### Steps

#### 1. Build and Push Docker Image

```bash
# Build image
docker build -t chatbot:latest -f deployment/aws/Dockerfile .

# Tag for ECR
docker tag chatbot:latest <account-id>.dkr.ecr.<region>.amazonaws.com/chatbot:latest

# Login to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

# Push image
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/chatbot:latest
```

#### 2. Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name chatbot-cluster
```

#### 3. Create Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://deployment/aws/task-definition.json
```

#### 4. Create Service

```bash
aws ecs create-service \
  --cluster chatbot-cluster \
  --service-name chatbot-service \
  --task-definition chatbot-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

### Environment Variables

Set in task definition or use AWS Systems Manager Parameter Store:

```bash
aws ssm put-parameter --name /chatbot/openai-key --value "your-key" --type SecureString
```

## Option 2: AWS Lambda + API Gateway

For serverless deployment (suitable for lighter workloads).

### Steps

1. Package application with dependencies
2. Create Lambda function
3. Set up API Gateway
4. Configure environment variables
5. Deploy

**Note**: Lambda has 15-minute timeout and memory limitations.

## Option 3: AWS EC2

### Launch EC2 Instance

```bash
# Launch instance
aws ec2 run-instances \
  --image-id ami-xxxxx \
  --instance-type t3.medium \
  --key-name your-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx
```

### Setup on EC2

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@<instance-ip>

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# Clone repository
git clone <your-repo>
cd chatbot-template

# Setup .env
nano .env

# Run with Docker
docker build -t chatbot .
docker run -d -p 80:8501 --env-file .env chatbot
```

## Cost Optimization

1. **Use Spot Instances** for EC2
2. **Auto-scaling** with ECS
3. **Reserved Instances** for predictable workloads
4. **S3** for document storage
5. **CloudWatch** for monitoring and cost analysis

## Security Best Practices

1. **Secrets Manager** for API keys
2. **VPC** for network isolation
3. **IAM Roles** for permissions
4. **HTTPS** with ACM certificates
5. **WAF** for protection

## Monitoring

Use CloudWatch for:
- Application logs
- Performance metrics
- Alarms
- Dashboards

## Scaling

Configure ECS auto-scaling:

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/chatbot-cluster/chatbot-service \
  --min-capacity 1 \
  --max-capacity 10
```
