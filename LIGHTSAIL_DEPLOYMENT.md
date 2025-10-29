# 🚀 AWS LIGHTSAIL DEPLOYMENT (EASIEST & CHEAPEST!)
**Django LMS - SavvyIndians Platform**

---

## ✅ WHY LIGHTSAIL?

**Lightsail is AWS's simplest option**:
- ✅ **$3.50/month** (first 3 months FREE with trial)
- ✅ **One-click setup** - No complex configuration
- ✅ **Includes everything**: Server + Database + Storage
- ✅ **Fixed pricing** - No surprise bills
- ✅ **Perfect for startups** - Easy to scale later

---

## 📋 DEPLOYMENT STEPS (15 MINUTES)

### **STEP 1: Create Lightsail Instance** (5 min)

1. **Go to Lightsail Console**:
   ```
   https://lightsail.aws.amazon.com/
   ```

2. **Click "Create instance"**

3. **Select**:
   - **Location**: `us-east-1` (Virginia)
   - **Platform**: Linux/Unix
   - **Blueprint**: OS Only → **Ubuntu 22.04 LTS**
   - **Instance Plan**: **$5/month** (1GB RAM, 40GB SSD)
   - **Instance name**: `savvyindians-lms`

4. **Click "Create instance"**
   - Wait 2-3 minutes for it to start

---

### **STEP 2: Connect to Instance** (1 min)

1. **Click your instance** → Click **"Connect using SSH"**
2. **Browser SSH terminal opens**

---

### **STEP 3: Setup Script** (10 min)

**Copy and paste this entire script** into the SSH terminal:

```bash
#!/bin/bash
# SavvyIndians LMS Automated Setup

echo "🚀 Starting SavvyIndians LMS Setup..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git

# Create database
sudo -u postgres psql << EOF
CREATE DATABASE lmsdb;
CREATE USER lmsadmin WITH PASSWORD 'SavvyLMS2025Password';
ALTER ROLE lmsadmin SET client_encoding TO 'utf8';
ALTER ROLE lmsadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE lmsadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lmsdb TO lmsadmin;
\q
EOF

# Clone repository
cd /home/ubuntu
git clone https://github.com/priyanshu705/Savvyindians-LMS-portal.git
cd Savvyindians-LMS-portal

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create .env file
cat > .env << 'ENV'
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=False
DATABASE_URL=postgresql://lmsadmin:SavvyLMS2025Password@localhost:5432/lmsdb
ALLOWED_HOSTS=*
ENV

# Run migrations
python manage.py migrate

# Create superuser
python manage.py shell << PYEOF
from accounts.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@savvyindians.com', 'Admin@123Change')
    print('Superuser created!')
PYEOF

# Collect static files
python manage.py collectstatic --noinput

# Create Gunicorn systemd service
sudo cat > /etc/systemd/system/gunicorn.service << 'SERVICE'
[Unit]
Description=gunicorn daemon for Django LMS
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Savvyindians-LMS-portal
ExecStart=/home/ubuntu/Savvyindians-LMS-portal/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/ubuntu/Savvyindians-LMS-portal/gunicorn.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
SERVICE

# Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configure Nginx
sudo cat > /etc/nginx/sites-available/lms << 'NGINX'
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/Savvyindians-LMS-portal/staticfiles/;
    }
    
    location /media/ {
        alias /home/ubuntu/Savvyindians-LMS-portal/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Savvyindians-LMS-portal/gunicorn.sock;
    }
}
NGINX

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "✅ Setup Complete!"
echo "🌐 Access your LMS at: http://$(curl -s ifconfig.me)"
echo "🔐 Admin: http://$(curl -s ifconfig.me)/admin/"
echo "   Username: admin"
echo "   Password: Admin@123Change"
```

**Press Enter** and wait 10 minutes for installation.

---

### **STEP 4: Get Your URL** (1 min)

After installation completes, you'll see:
```
✅ Setup Complete!
🌐 Access your LMS at: http://YOUR_IP_ADDRESS
```

**Open that URL in your browser!** 🎉

---

## 🔐 ADMIN ACCESS

1. **Go to**: `http://YOUR_IP_ADDRESS/admin/`
2. **Login**:
   - Username: `admin`
   - Password: `Admin@123Change`
3. **⚠️ Change password immediately!**

---

## 💰 PRICING

| Plan | Price | RAM | CPU | Storage | Transfer |
|------|-------|-----|-----|---------|----------|
| **First 3 months** | **FREE** | 1GB | 1 core | 40GB | 2TB |
| **After trial** | **$5/mo** | 1GB | 1 core | 40GB | 2TB |

**Total Cost Year 1**: ~$50 ($0 first 3 months + $5 x 9 months)

---

## 🌐 CUSTOM DOMAIN (Optional)

### **Connect your domain**:

1. **Go to Lightsail** → Your instance → **Networking** tab
2. **Create Static IP** (FREE)
3. **Attach it** to your instance
4. **Add DNS Zone**:
   - Type: A Record
   - Name: @ (or www)
   - Value: Your Static IP

5. **Update domain nameservers** at your registrar to Lightsail nameservers

---

## 🔧 USEFUL COMMANDS

### **SSH to Server**:
```bash
# From Lightsail console, click "Connect using SSH"
```

### **Check Status**:
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### **View Logs**:
```bash
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
```

### **Restart Services**:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### **Update Code**:
```bash
cd /home/ubuntu/Savvyindians-LMS-portal
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### **Database Access**:
```bash
sudo -u postgres psql lmsdb
```

---

## 📊 MONITORING

### **Check Resource Usage**:
```bash
# CPU and Memory
htop

# Disk Space
df -h

# Database Size
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('lmsdb'));"
```

---

## 🚀 SCALING OPTIONS

When you outgrow $5/month plan:

### **Option 1: Upgrade Lightsail Plan**
- $10/mo: 2GB RAM, 2 cores
- $20/mo: 4GB RAM, 2 cores
- $40/mo: 8GB RAM, 2 cores

### **Option 2: Move to EC2**
- Snapshot Lightsail instance
- Export to EC2
- Use Auto Scaling

---

## 🔒 SECURITY HARDENING

### **Setup Firewall**:
```bash
# In Lightsail console, go to Networking
# Add rule: Allow HTTP (port 80)
# Add rule: Allow HTTPS (port 443)
```

### **Enable HTTPS** (Free SSL):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **Auto-renew SSL**:
```bash
sudo systemctl enable certbot.timer
```

---

## 📞 TROUBLESHOOTING

### **Can't access website**:
```bash
# Check Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn --no-pager | tail -50

# Check Nginx
sudo nginx -t
sudo systemctl status nginx
```

### **Static files not loading**:
```bash
cd /home/ubuntu/Savvyindians-LMS-portal
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### **Database errors**:
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Check connection
sudo -u postgres psql lmsdb -c "SELECT 1;"
```

---

## ✅ CHECKLIST

- [ ] Lightsail instance created ($5/month)
- [ ] Setup script executed successfully
- [ ] Website accessible at public IP
- [ ] Admin panel working (/admin/)
- [ ] Static files loading
- [ ] Database connected
- [ ] Admin password changed

---

## 🎯 SUMMARY

**Lightsail vs Elastic Beanstalk**:

| Feature | Lightsail | Elastic Beanstalk |
|---------|-----------|-------------------|
| **Ease** | ⭐⭐⭐⭐⭐ One-click | ⭐⭐⭐ Complex |
| **Cost** | $5/mo fixed | $20-40/mo variable |
| **Setup** | 15 minutes | 1-2 hours |
| **Free Tier** | 3 months | 12 months |
| **Scaling** | Manual upgrade | Auto-scaling |
| **Best For** | Startups | Enterprise |

---

## 💡 RECOMMENDATION

**Start with Lightsail** because:
1. ✅ Simple setup (15 min vs 2 hours)
2. ✅ Fixed pricing ($5/mo)
3. ✅ No surprise bills
4. ✅ Can export to EC2 later
5. ✅ Perfect for MVP/testing

**When to switch to EB/ECS**:
- Traffic > 10,000 users/month
- Need auto-scaling
- Complex microservices
- Enterprise requirements

---

**🎉 Ready to deploy? Follow Step 1 above!**

**Questions?**
- Lightsail Docs: https://lightsail.aws.amazon.com/ls/docs/
- AWS Support: https://console.aws.amazon.com/support/
