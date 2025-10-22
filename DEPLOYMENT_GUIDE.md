# PythonAnywhere Deployment Guide for Django LMS

## Step 1: Sign Up on PythonAnywhere
1. Go to: https://www.pythonanywhere.com/registration/register/beginner/
2. Create FREE account (no credit card needed)
3. Verify your email

## Step 2: Upload Your Project

### Option A: Via GitHub (Recommended)
```bash
# 1. Create GitHub repository and push your code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/django-lms.git
git push -u origin main
```

### Option B: Direct Upload
- Use "Files" tab on PythonAnywhere
- Upload as ZIP and extract

## Step 3: Setup on PythonAnywhere

### Open Bash Console (from Dashboard)
```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/django-lms.git
cd django-lms

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 lmsenv

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add your SECRET_KEY and other settings
# Press Ctrl+X, then Y, then Enter to save

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 4: Configure Web App

### Go to "Web" tab and click "Add a new web app"
1. Choose "Manual configuration"
2. Select Python 3.10
3. Click Next

### Configure WSGI file:
Click on WSGI configuration file link and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/django-lms'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Activate virtual environment
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Set Virtualenv path:
```
/home/YOUR_USERNAME/.virtualenvs/lmsenv
```

### Configure Static Files:
URL: `/static/`
Directory: `/home/YOUR_USERNAME/django-lms/staticfiles/`

URL: `/media/`
Directory: `/home/YOUR_USERNAME/django-lms/media/`

## Step 5: Update Django Settings

Add to ALLOWED_HOSTS:
```python
ALLOWED_HOSTS = ['YOUR_USERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']
```

## Step 6: Reload Web App
Click green "Reload" button on Web tab

## Step 7: Visit Your Site
https://YOUR_USERNAME.pythonanywhere.com

## Troubleshooting

### If you see errors:
1. Check error log (Web tab → Log files → Error log)
2. Check server log (Web tab → Log files → Server log)

### Common fixes:
```bash
# Fix permissions
chmod 755 /home/YOUR_USERNAME/django-lms

# Update dependencies
pip install --upgrade -r requirements.txt

# Re-run migrations
python manage.py migrate

# Collect static again
python manage.py collectstatic --noinput
```

## Daily Maintenance (Free Tier)
- Free accounts need manual reload every 24 hours
- Just click "Reload" button on Web tab

## Next Steps After Deployment
1. Test all features
2. Add custom domain (optional, paid)
3. Setup email (Gmail SMTP)
4. Add SSL certificate (included free)
5. Monitor error logs regularly

---
Your LMS will be live at: **https://YOUR_USERNAME.pythonanywhere.com**
