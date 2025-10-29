# AWS Elastic Beanstalk Deployment Script
# Run this step by step in PowerShell

Write-Host "🚀 AWS Elastic Beanstalk Deployment" -ForegroundColor Green
Write-Host "=" * 60

# Step 1: Generate SECRET_KEY
Write-Host "`n📝 Step 1: Generating SECRET_KEY..." -ForegroundColor Cyan
$SECRET_KEY = & D:/django-lms-main/django-lms-main/django-backup/.venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(50))"
Write-Host "✅ SECRET_KEY generated: $SECRET_KEY" -ForegroundColor Green

# Step 2: Create environment
Write-Host "`n🔧 Step 2: Creating AWS Environment..." -ForegroundColor Cyan
Write-Host "⏱️  This takes 5-10 minutes. Please wait..." -ForegroundColor Yellow

$env:AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY_HERE"
$env:AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY_HERE"
$env:AWS_DEFAULT_REGION = "us-east-1"

# Create environment with RDS database
& D:/django-lms-main/django-lms-main/django-backup/.venv/Scripts/eb.exe create savvyindians-lms-env `
    --instance-type t2.micro `
    --database.engine postgres `
    --database.username lmsadmin `
    --database.password "SavvyLMS2025Password" `
    --envvars "DJANGO_SETTINGS_MODULE=config.settings_aws,DEBUG=False,SECRET_KEY=$SECRET_KEY" `
    --region us-east-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Environment created successfully!" -ForegroundColor Green
    
    # Step 3: Open the application
    Write-Host "`n🌐 Step 3: Opening your LMS..." -ForegroundColor Cyan
    & D:/django-lms-main/django-lms-main/django-backup/.venv/Scripts/eb.exe open
    
    Write-Host "`n🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
    Write-Host "=" * 60
    Write-Host "`n📌 ADMIN ACCESS:" -ForegroundColor Yellow
    Write-Host "   Username: admin" -ForegroundColor White
    Write-Host "   Password: Admin@123Change" -ForegroundColor White
    Write-Host "   ⚠️  Change password after first login!" -ForegroundColor Red
    
} else {
    Write-Host "`n❌ Deployment failed. Check errors above." -ForegroundColor Red
    Write-Host "Run: eb logs" -ForegroundColor Yellow
}
