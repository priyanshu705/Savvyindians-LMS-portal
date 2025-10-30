# Railway Deployment Guide for SavvyIndians LMS

## 🚂 Railway.app - Easiest Free Deployment with Database

Railway provides **FREE** hosting with PostgreSQL database included. No complex setup needed!

---

## 📋 Quick Deployment Steps

### 1. Create Railway Account
- Go to: https://railway.app
- Sign up with GitHub (one-click signup)
- ✅ **$5 free credits monthly** (enough for small projects)

### 2. Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: `Savvyindians-LMS-portal`
4. Railway will automatically detect it's a Django project

### 3. Add PostgreSQL Database
1. In your project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Database will be created automatically
3. Railway will automatically set `DATABASE_URL` environment variable

### 4. Configure Environment Variables
In Railway dashboard → **Variables** tab, add:

```env
DJANGO_SETTINGS_MODULE=config.settings_minimal
SECRET_KEY=bFp3Us&2LTCD+x9M_dC68sSnD41&SRl$7!)om!!1Zr_tV_hs2e
DEBUG=False
PYTHON_VERSION=3.10.12

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=gy068644@gmail.com
EMAIL_HOST_PASSWORD=ynttunin qzmgehoq
EMAIL_FROM_ADDRESS=gy068644@gmail.com

# Optional
STUDENT_ID_PREFIX=STD
LECTURER_ID_PREFIX=LECT
```

**Note:** `DATABASE_URL` is automatically set by Railway PostgreSQL!

### 5. Deploy!
- Railway will automatically deploy from GitHub
- Every push to `main` branch = automatic deployment
- View logs in Railway dashboard

---

## 🎯 Alternative: Render.com (Already Configured)

You already have Render configured! Just need to:

1. Go to: https://dashboard.render.com
2. Your service: `savvyindians-lms`
3. **Environment** tab
4. Set `DATABASE_URL`:
```
postgresql://neondb_owner:npg_snWe2DkE4QGR@ep-noisy-frost-adlq3kiy-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```
5. **Manual Deploy** or push to GitHub

---

## ⚡ Other Free Options

### **Fly.io** (Free PostgreSQL included)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly postgres create
fly postgres attach
fly deploy
```

### **Koyeb** (Heroku alternative)
- https://www.koyeb.com
- Connect GitHub
- Auto-deploy
- Free PostgreSQL

---

## 📊 Comparison

| Platform | Database | Free Tier | Auto-Deploy | Ease |
|----------|----------|-----------|-------------|------|
| **Railway** | PostgreSQL (Free) | $5/month credit | ✅ | ⭐⭐⭐⭐⭐ |
| **Render** | External (Neon) | 750 hrs/month | ✅ | ⭐⭐⭐⭐ |
| **Fly.io** | PostgreSQL (Free) | 3GB storage | ✅ | ⭐⭐⭐ |
| **PythonAnywhere** | MySQL (Free) | 1 app | ❌ | ⭐⭐ |

---

## ✅ Recommended: Railway

**Why Railway?**
- 🚀 Fastest setup (5 minutes)
- 💾 PostgreSQL included (no external setup)
- 🔄 Auto-deploy from GitHub
- 📊 Beautiful dashboard
- 🆓 $5 free credits monthly

**Steps:**
1. Go to https://railway.app
2. Login with GitHub
3. "New Project" → "Deploy from GitHub"
4. Select repository
5. Add PostgreSQL database (one click)
6. Add environment variables
7. ✅ Done! Your site is live!

---

## 🔧 Files Already Configured

Your project has these files ready:
- ✅ `railway.json` - Railway configuration
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version

---

## 🎯 Next Steps

1. Choose a platform (Railway recommended)
2. Sign up & connect GitHub
3. Deploy in 5 minutes
4. Your LMS is live! 🚀

---

## 💡 Pro Tips

- Railway gives $5/month free (enough for small projects)
- Render gives 750 hours/month free
- Use Neon for free PostgreSQL (if needed separately)
- Always use environment variables for secrets
- Enable auto-deploy from GitHub

---

## 📞 Need Help?

If you face any issues:
1. Check deployment logs in platform dashboard
2. Verify environment variables are set
3. Ensure `DATABASE_URL` is configured
4. Check Python version matches `runtime.txt`

**Happy Deploying! 🚀**
