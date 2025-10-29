# 🔐 Deployment Security Checklist

## ⚠️ CRITICAL: Before Deploying to Render

### 1. Environment Variables (Render Dashboard)

**Navigate to**: Render Dashboard → Your Service → Environment

**Required Variables**:

```bash
# Django Core (CRITICAL)
SECRET_KEY=<leave blank - Render auto-generates>
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings_minimal

# Database (Auto-set by Render)
DATABASE_URL=<automatically set when you add PostgreSQL>

# Google OAuth (if using social login)
GOOGLE_OAUTH2_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret

# Email (optional - for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## ✅ render.yaml Configuration

Your `render.yaml` should have:

```yaml
services:
  - type: web
    name: savvyindians-lms-portal
    runtime: python
    plan: free
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings_minimal
      - key: SECRET_KEY
        generateValue: true  # ← Render auto-generates secure key
      - key: DEBUG
        value: False  # ← MUST be False in production
      - key: DATABASE_URL
        sync: false  # ← Use value from PostgreSQL database

databases:
  - name: savvyindians-lms-db
    databaseName: lmsdb
    plan: free
```

---

## 🔍 Pre-Deployment Security Checks

Run these checks before deploying:

### Check 1: No Hardcoded Secrets
```bash
# Search for potential secrets in code
grep -r "password" config/ --include="*.py" | grep -v "PASSWORD"
grep -r "secret" config/ --include="*.py" | grep -v "SECRET"
grep -r "api_key" config/ --include="*.py"
```

**Expected**: No hardcoded passwords or API keys found ✅

### Check 2: DEBUG is False
```bash
# Check settings file
grep "DEBUG" config/settings_minimal.py
```

**Expected**: Should default to `False` ✅

### Check 3: ALLOWED_HOSTS Configured
```bash
# Check allowed hosts
grep "ALLOWED_HOSTS" config/settings_minimal.py
```

**Expected**: Specific domains only, no `"*"` wildcard in production ✅

### Check 4: Git Status Clean
```bash
git status
```

**Expected**: All security fixes committed ✅

---

## 🚀 Deployment Steps

### Step 1: Commit Security Fixes
```bash
git add config/render_env.py config/settings_minimal.py
git commit -m "SECURITY: Fix critical vulnerabilities - remove hardcoded credentials"
git push origin main
```

### Step 2: Verify Render Configuration
1. Go to Render Dashboard
2. Select your service
3. Check **Environment** tab:
   - `SECRET_KEY` should be auto-generated (lock icon 🔒)
   - `DEBUG` should be `False`
   - `DATABASE_URL` should show "Synced from database"

### Step 3: Deploy
- Render will automatically deploy from GitHub
- Or click **Manual Deploy** → **Deploy latest commit**

### Step 4: Monitor Deployment
Watch the logs for:
```
✓ DATABASE_URL found: postgresql:***@...
✓ Using database: django.db.backends.postgresql
🔄 Running migrations on Render startup...
✓ Migrations completed successfully!
🔄 Collecting static files...
✓ Static files collected!
```

---

## 🧪 Post-Deployment Testing

### Test 1: Homepage Loads
```bash
curl -I https://savvyindians-lms-portal-2.onrender.com
```
**Expected**: HTTP 200 OK ✅

### Test 2: Static Files Load
Open browser dev tools (F12) and check:
- CSS files load (no 404 errors)
- JavaScript files load
- Images display correctly

### Test 3: HTTPS Enforced
```bash
curl -I http://savvyindians-lms-portal-2.onrender.com
```
**Expected**: 301 redirect to HTTPS ✅

### Test 4: Security Headers Present
```bash
curl -I https://savvyindians-lms-portal-2.onrender.com
```
**Expected headers**:
- `Strict-Transport-Security: max-age=31536000`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`

### Test 5: Admin Login Works
1. Navigate to `/admin/`
2. Create superuser if needed:
   ```bash
   # In Render shell
   python manage.py createsuperuser
   ```
3. Login with credentials
4. Verify admin dashboard loads

---

## 🔥 CRITICAL: What NOT to Do

### ❌ DO NOT:
1. **Commit `.env` files** to Git
2. **Push database credentials** to GitHub
3. **Set `DEBUG=True`** in production
4. **Use `ALLOWED_HOSTS = ["*"]`** in production
5. **Hardcode API keys** or passwords in code
6. **Disable HTTPS** (`SECURE_SSL_REDIRECT`)
7. **Share `SECRET_KEY`** publicly
8. **Use weak passwords** for admin accounts

---

## 🆘 Troubleshooting

### Issue: App won't start
**Check**: Render logs for error messages
**Solution**: Verify `DATABASE_URL` and `SECRET_KEY` are set

### Issue: Static files not loading
**Check**: `staticfiles/` directory exists in repo
**Solution**: Ensure `.gitkeep` file is committed

### Issue: Database connection fails
**Check**: DATABASE_URL format is correct
**Solution**: Should be `postgresql://user:pass@host:port/dbname`

### Issue: HTTPS redirect loop
**Check**: `SECURE_PROXY_SSL_HEADER` is set
**Solution**: Should be `("HTTP_X_FORWARDED_PROTO", "https")`

---

## 📞 Emergency Contacts

If security issue detected:
1. **Immediately**: Suspend Render service
2. **Rotate**: Change all secrets (SECRET_KEY, database password)
3. **Review**: Check access logs for suspicious activity
4. **Fix**: Address vulnerability
5. **Redeploy**: With fixed code

---

## ✅ Deployment Approved

Once all checks pass:
- ✅ Security fixes applied
- ✅ Environment variables configured
- ✅ `render.yaml` updated
- ✅ All tests pass
- ✅ No hardcoded secrets
- ✅ DEBUG=False
- ✅ HTTPS enforced

**Status**: **READY FOR PRODUCTION DEPLOYMENT** 🚀

---

**Last Updated**: Current QA testing session  
**Next Review**: After deployment or when adding new features
