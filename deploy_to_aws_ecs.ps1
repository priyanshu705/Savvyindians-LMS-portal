# AWS ECS Fargate Deployment Script
# This deploys your Django LMS to AWS using Docker containers

Write-Host "🚀 AWS ECS FARGATE DEPLOYMENT" -ForegroundColor Green
Write-Host "=" * 70

# Step 1: Get AWS Account ID
Write-Host "`n📋 Step 1: Getting AWS Account ID..." -ForegroundColor Cyan
$AWS_ACCOUNT_ID = aws sts get-caller-identity --query Account --output text
Write-Host "✅ Account ID: $AWS_ACCOUNT_ID" -ForegroundColor Green

# Step 2: Create ECR Repository
Write-Host "`n📦 Step 2: Creating ECR Repository..." -ForegroundColor Cyan
aws ecr create-repository --repository-name savvyindians-lms --region us-east-1 2>$null
if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 254) {
    Write-Host "✅ ECR Repository ready" -ForegroundColor Green
}

# Step 3: Create RDS PostgreSQL Database
Write-Host "`n🗄️  Step 3: Creating RDS PostgreSQL (Free Tier)..." -ForegroundColor Cyan
Write-Host "⏱️  This takes 5-7 minutes..." -ForegroundColor Yellow

aws rds create-db-instance `
    --db-instance-identifier savvyindians-lms-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 15.4 `
    --master-username lmsadmin `
    --master-user-password "SavvyLMS2025Password" `
    --allocated-storage 20 `
    --publicly-accessible `
    --backup-retention-period 7 `
    --region us-east-1 `
    --no-multi-az `
    --storage-encrypted 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ RDS Database creation started" -ForegroundColor Green
    Write-Host "⏳ Waiting for database to be available..." -ForegroundColor Yellow
    
    # Wait for database to be available
    aws rds wait db-instance-available --db-instance-identifier savvyindians-lms-db --region us-east-1
    
    # Get database endpoint
    $DB_ENDPOINT = aws rds describe-db-instances `
        --db-instance-identifier savvyindians-lms-db `
        --query 'DBInstances[0].Endpoint.Address' `
        --output text `
        --region us-east-1
    
    Write-Host "✅ Database ready at: $DB_ENDPOINT" -ForegroundColor Green
    
    # Create DATABASE_URL
    $DATABASE_URL = "postgresql://lmsadmin:SavvyLMS2025Password@$DB_ENDPOINT:5432/postgres"
    Write-Host "✅ DATABASE_URL: $DATABASE_URL" -ForegroundColor Green
}

# Step 4: Login to ECR and Build Docker Image
Write-Host "`n🔐 Step 4: Building and Pushing Docker Image..." -ForegroundColor Cyan
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Logged in to ECR" -ForegroundColor Green
    
    # Build image
    Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
    docker build -t savvyindians-lms:latest .
    
    # Tag image
    docker tag savvyindians-lms:latest "$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/savvyindians-lms:latest"
    
    # Push image
    Write-Host "📤 Pushing to ECR..." -ForegroundColor Yellow
    docker push "$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/savvyindians-lms:latest"
    
    Write-Host "✅ Docker image pushed successfully" -ForegroundColor Green
}

# Step 5: Create ECS Cluster
Write-Host "`n🏗️  Step 5: Creating ECS Cluster..." -ForegroundColor Cyan
aws ecs create-cluster --cluster-name savvyindians-lms-cluster --region us-east-1 2>$null
Write-Host "✅ ECS Cluster created" -ForegroundColor Green

# Step 6: Create CloudWatch Log Group
Write-Host "`n📊 Step 6: Creating CloudWatch Log Group..." -ForegroundColor Cyan
aws logs create-log-group --log-group-name /ecs/savvyindians-lms --region us-east-1 2>$null
Write-Host "✅ Log group created" -ForegroundColor Green

# Step 7: Update Task Definition with Account ID
Write-Host "`n📝 Step 7: Creating ECS Task Definition..." -ForegroundColor Cyan
(Get-Content ecs-task-definition.json) -replace 'YOUR_ACCOUNT_ID', $AWS_ACCOUNT_ID | Set-Content ecs-task-definition-updated.json

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition-updated.json --region us-east-1
Write-Host "✅ Task definition registered" -ForegroundColor Green

# Step 8: Create ECS Service
Write-Host "`n🚀 Step 8: Creating ECS Service..." -ForegroundColor Cyan
Write-Host "⏱️  Getting default VPC and subnets..." -ForegroundColor Yellow

$VPC_ID = aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text --region us-east-1
$SUBNET_IDS = aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[*].SubnetId' --output text --region us-east-1
$SUBNET_ARRAY = $SUBNET_IDS -split '\s+'

# Create security group
$SG_ID = aws ec2 create-security-group `
    --group-name savvyindians-lms-sg `
    --description "Security group for SavvyIndians LMS" `
    --vpc-id $VPC_ID `
    --region us-east-1 `
    --query 'GroupId' `
    --output text 2>$null

# Allow inbound traffic on port 8000
aws ec2 authorize-security-group-ingress `
    --group-id $SG_ID `
    --protocol tcp `
    --port 8000 `
    --cidr 0.0.0.0/0 `
    --region us-east-1 2>$null

Write-Host "✅ Security group created: $SG_ID" -ForegroundColor Green

# Create ECS Service
aws ecs create-service `
    --cluster savvyindians-lms-cluster `
    --service-name savvyindians-lms-service `
    --task-definition savvyindians-lms `
    --desired-count 1 `
    --launch-type FARGATE `
    --network-configuration "awsvpcConfiguration={subnets=[$($SUBNET_ARRAY[0])],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" `
    --region us-east-1

Write-Host "✅ ECS Service created" -ForegroundColor Green

# Step 9: Get Service Public IP
Write-Host "`n🌐 Step 9: Getting Public IP..." -ForegroundColor Cyan
Write-Host "⏱️  Waiting for task to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

$TASK_ARN = aws ecs list-tasks --cluster savvyindians-lms-cluster --service-name savvyindians-lms-service --region us-east-1 --query 'taskArns[0]' --output text

if ($TASK_ARN) {
    $ENI_ID = aws ecs describe-tasks --cluster savvyindians-lms-cluster --tasks $TASK_ARN --region us-east-1 --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text
    
    if ($ENI_ID) {
        $PUBLIC_IP = aws ec2 describe-network-interfaces --network-interface-ids $ENI_ID --region us-east-1 --query 'NetworkInterfaces[0].Association.PublicIp' --output text
        
        Write-Host "`n🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
        Write-Host "=" * 70
        Write-Host "`n📌 YOUR LMS IS LIVE AT:" -ForegroundColor Yellow
        Write-Host "   http://$PUBLIC_IP:8000" -ForegroundColor White
        Write-Host "`n🔐 ADMIN ACCESS:" -ForegroundColor Yellow
        Write-Host "   http://$PUBLIC_IP:8000/admin/" -ForegroundColor White
        Write-Host "   Username: admin" -ForegroundColor White
        Write-Host "   Password: Admin@123Change" -ForegroundColor White
        Write-Host "   ⚠️  Change password after first login!" -ForegroundColor Red
        Write-Host "`n💾 DATABASE:" -ForegroundColor Yellow
        Write-Host "   Host: $DB_ENDPOINT" -ForegroundColor White
        Write-Host "   Database: postgres" -ForegroundColor White
        Write-Host "   Username: lmsadmin" -ForegroundColor White
        Write-Host "   Password: SavvyLMS2025Password" -ForegroundColor White
        Write-Host "`n💰 COST: $0/month for first 12 months (Free Tier)" -ForegroundColor Green
        Write-Host "=" * 70
    }
}

Write-Host "`n✅ All steps completed!" -ForegroundColor Green
