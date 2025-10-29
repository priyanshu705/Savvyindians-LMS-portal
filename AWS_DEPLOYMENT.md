# 🚀 AWS ELASTIC BEANSTALK DEPLOYMENT GUIDE
**Django LMS - SavvyIndians Platform on AWS**

---

## ✅ PREREQUISITES COMPLETED
- ✅ AWS EB CLI installed
- ✅ Boto3 and django-storages installed
- ✅ AWS configuration files created
- ✅ Auto-superuser creation script added

---

## 📋 NEXT STEPS (Manual)

### **STEP 1: Create AWS Account** (5 minutes)
1. Go to: https://aws.amazon.com/free/
2. Click **"Create a Free Account"**
3. Enter email, password, account name
4. **Enter credit card** (required but won't be charged in Free Tier)
5. Verify phone number
6. Select **Free Support Plan**

### **STEP 2: Get AWS Access Keys** (3 minutes)
1. Login to AWS Console: https://console.aws.amazon.com/
2. Click your name (top right) → **Security Credentials**
3. Scroll to **"Access keys"**
4. Click **"Create access key"**
5. Choose **"Command Line Interface (CLI)"**
6. **Save these securely**:
   - Access Key ID (looks like: AKIAIOSFODNN7EXAMPLE)
   - Secret Access Key (looks like: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)

### **STEP 3: Configure AWS CLI** (2 minutes)
Run in PowerShell:
```powershell
eb init
```

**Answer the prompts**:
- **Select a default region**: Choose `us-east-1` (cheapest, part of Free Tier)
- **Enter your AWS Access Key ID**: [paste from Step 2]
- **Enter your AWS Secret Access Key**: [paste from Step 2]
- **Select an application**: Create new application
- **Application name**: `savvyindians-lms`
- **Platform**: Python
- **Platform version**: Python 3.11 (recommended for Free Tier)
- **Set up SSH**: Yes (optional but helpful)

### **STEP 4: Create Environment** (3 minutes)
```powershell
eb create savvyindians-lms-env --database.engine postgres --database.username lmsadmin --database.password YOUR_SECURE_PASSWORD --instance-type t2.micro --envvars "DJANGO_SETTINGS_MODULE=config.settings_aws,DEBUG=False,SECRET_KEY=YOUR_RANDOM_SECRET_KEY"
```

**What this does**:
- ✅ Creates t2.micro EC2 instance (FREE TIER)
- ✅ Creates RDS PostgreSQL db.t2.micro (FREE TIER)
- ✅ Sets up load balancer
- ✅ Configures environment variables
- ✅ Automatically deploys your code

**Wait 5-10 minutes** for environment creation...

### **STEP 5: Open Your App**
```powershell
eb open
```

This opens your deployed LMS in the browser! 🎉

---

## 🔐 ADMIN ACCESS

**After deployment completes**:

1. **Your admin is auto-created**:
   - Username: `admin`
   - Email: `admin@savvyindians.com`
   - Password: `Admin@123Change`

2. **Login at**:
   ```
   https://your-eb-domain.elasticbeanstalk.com/admin/
   ```

3. **⚠️ CHANGE PASSWORD IMMEDIATELY!**
   - Go to admin → Change password
   - Use strong password

---

## 💰 COST MONITORING

### **Set Up Billing Alerts** (IMPORTANT!)

1. Go to: https://console.aws.amazon.com/billing/
2. Click **"Billing Preferences"**
3. Enable:
   - ✅ Receive Free Tier Usage Alerts
   - ✅ Receive Billing Alerts
4. Enter your email
5. Go to **CloudWatch** → **Alarms** → **Billing**
6. Create alarm:
   - **Threshold**: $1 (you'll get alert if charges exceed $1)
   - **Email**: Your email

### **Monitor Usage**:
```
AWS Console → Billing Dashboard → Free Tier Usage
```

Check daily to ensure you're within Free Tier limits!

---

## 📊 AWS FREE TIER LIMITS

**What you get FREE for 12 months**:

| Resource | Free Tier | Your Usage | Status |
|----------|-----------|------------|--------|
| EC2 (t2.micro) | 750 hrs/mo | 24/7 = 720 hrs | ✅ Safe |
| RDS (db.t2.micro) | 750 hrs/mo | 24/7 = 720 hrs | ✅ Safe |
| RDS Storage | 20 GB | ~5 GB | ✅ Safe |
| Data Transfer | 15 GB/mo | Depends on traffic | ⚠️ Monitor |

**If you exceed**: You'll get charged (~$20-30/month)

---

## 🛠️ USEFUL COMMANDS

### **Deploy Updates**:
```powershell
git add .
git commit -m "Update"
eb deploy
```

### **View Logs**:
```powershell
eb logs
```

### **SSH to Server**:
```powershell
eb ssh
```

### **Check Status**:
```powershell
eb status
```

### **Open App**:
```powershell
eb open
```

### **Environment Info**:
```powershell
eb printenv
```

### **Set Environment Variable**:
```powershell
eb setenv KEY=value
```

### **Terminate (Delete Everything)**:
```powershell
eb terminate savvyindians-lms-env
```

---

## 🔧 CONFIGURATION FILES CREATED

### **`.ebextensions/01_django.config`**
- Runs migrations automatically
- Collects static files
- Creates superuser

### **`.ebextensions/02_https_redirect.config`**
- Forces HTTPS (secure)

### **`.ebextensions/03_packages.config`**
- Installs required system packages

### **`config/settings_aws.py`**
- AWS-specific Django settings
- RDS PostgreSQL configuration
- S3 storage setup (optional)

### **`accounts/management/commands/createsu.py`**
- Auto-creates admin on deployment

---

## 🚀 OPTIONAL: S3 STATIC FILES

**For better performance** (Free Tier: 5GB forever):

1. **Create S3 Bucket**:
   - Go to S3 Console
   - Create bucket: `savvyindians-lms-static`
   - Region: `us-east-1`
   - Uncheck "Block all public access"

2. **Set Environment Variables**:
   ```powershell
   eb setenv AWS_STORAGE_BUCKET_NAME=savvyindians-lms-static AWS_S3_REGION_NAME=us-east-1
   ```

3. **Deploy**:
   ```powershell
   eb deploy
   ```

Static files will now load from S3 (faster + Free Tier 5GB)!

---

## 🌍 CUSTOM DOMAIN (Optional)

**Connect savvyindians.com**:

1. Go to Route 53 (AWS DNS service)
2. Create hosted zone
3. Add A record pointing to EB environment
4. Update nameservers at your domain registrar

**Cost**: $0.50/month for hosted zone (after Free Tier)

---

## 📞 TROUBLESHOOTING

### **Deployment Failed**
```powershell
eb logs
```
Check logs for errors.

### **Database Connection Error**
Verify RDS credentials:
```powershell
eb printenv
```

### **Static Files Not Loading**
Collect static files:
```powershell
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py collectstatic --noinput
```

### **500 Internal Server Error**
Check Django logs:
```powershell
eb logs
```

### **Need to Reset Database**
```powershell
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py flush
python manage.py migrate
python manage.py createsu
```

---

## 🎯 SUMMARY

**To deploy**:
1. Create AWS account (5 min)
2. Get access keys (3 min)
3. Run `eb init` (2 min)
4. Run `eb create` (10 min)
5. Open app with `eb open`

**Total time**: ~20 minutes

**Cost**: $0 for 12 months (Free Tier)

**After 12 months**: ~$20-30/month

---

## ✅ CHECKLIST

Before running `eb create`:

- [ ] AWS account created
- [ ] Credit card added (for verification)
- [ ] Access keys obtained
- [ ] `eb init` completed successfully
- [ ] Billing alerts set up
- [ ] Strong database password ready
- [ ] Secret key generated (use: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)

---

**⚠️ IMPORTANT REMINDERS**:

1. **Change admin password** after first login
2. **Set up billing alerts** to avoid charges
3. **Monitor Free Tier usage** daily
4. **Use t2.micro** instances only (Free Tier)
5. **Back up database** regularly

---

**🎉 Your LMS is ready to deploy to AWS!**

**Run these commands when you have your AWS credentials**:
```powershell
eb init
eb create savvyindians-lms-env --database.engine postgres --database.username lmsadmin --instance-type t2.micro
eb open
```
