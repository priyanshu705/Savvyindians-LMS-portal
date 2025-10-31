# 🚀 Supabase Setup Guide for SavvyIndians LMS

## ✅ Current Status
- Supabase PostgreSQL database created
- Connection string: `postgresql://postgres:Gaurav%237055@db.atifaphgpescrtmqvigd.supabase.co:5432/postgres`
- Code updated to support Supabase SSL configuration

---

## 📋 Steps to Complete Setup

### Step 1: Update Render Environment Variable

1. **Go to Render Dashboard:** https://dashboard.render.com
2. **Select your service:** `savvyindians-lms-portal-2`
3. Click on **"Environment"** tab (left sidebar)
4. Find the `DATABASE_URL` variable
5. Click **"Edit"** button
6. **Replace the old Render PostgreSQL URL with:**
   ```
   postgresql://postgres:Gaurav%237055@db.atifaphgpescrtmqvigd.supabase.co:5432/postgres
   ```
   
   **⚠️ IMPORTANT:** Use `%23` instead of `#` (URL encoding)
   
7. Click **"Save Changes"**
8. Service will automatically redeploy (wait 3-4 minutes)

---

### Step 2: Monitor Deployment

1. Go to **"Logs"** tab in Render Dashboard
2. Watch for these SUCCESS messages:
   ```
   Running migrations...
   Operations to perform: ...
   Running migrations:
     Applying ...
   ✅ Migrations completed
   🔍 Checking for superuser: SavvyIndians
   ✅ Superuser created successfully: SavvyIndians
   ```

3. If you see errors, check:
   - Database URL is correct
   - Password is properly URL-encoded (`%23` for `#`)
   - Supabase database is active

---

### Step 3: Test Admin Login

After deployment completes (3-4 minutes):

1. **Visit:** https://savvyindians-lms-portal-2.onrender.com/admin/login/
2. **Login with:**
   - Username: `SavvyIndians`
   - Password: `Savvy@2024#Admin`
3. Should redirect to admin dashboard ✅

**OR run automated test:**
```powershell
python test_admin_bootcamp.py
```

---

## 🔧 Local Testing (Optional)

If you want to test locally with Supabase:

```powershell
# Set DATABASE_URL
$env:DATABASE_URL="postgresql://postgres:Gaurav%237055@db.atifaphgpescrtmqvigd.supabase.co:5432/postgres"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py ensure_superuser

# Run test
python test_admin_bootcamp.py
```

---

## ✅ Why Supabase is Better

1. **Better SSL Support** - No SSL handshake errors
2. **Connection Pooling** - Built-in pgBouncer
3. **No Spin Down** - Always available (unlike Render free tier)
4. **Dashboard Access** - View/edit data directly
5. **Automatic Backups** - Free tier includes backups
6. **Better Performance** - Faster than Render free PostgreSQL

---

## 🎯 Next Steps After Login Success

1. **Change Default Password:**
   - Login to admin
   - Go to Users → SavvyIndians
   - Click "Change Password"
   - Set new secure password

2. **Test Bootcamp Creation:**
   - Navigate to Course → Programs
   - Click "Add Program"
   - Fill form and save

3. **Update README** with new database info

---

## 🆘 Troubleshooting

### Error: "connection timeout"
- Check Supabase project is running
- Verify connection string is correct
- Check firewall/network allows connections to Supabase

### Error: "authentication failed"
- Password must be URL-encoded: `#` = `%23`
- Check password in Supabase dashboard (Settings → Database)

### Error: "SSL error"
- Code updated to use `sslmode=prefer`
- Supabase handles SSL automatically

---

## 📊 Database Info

- **Provider:** Supabase
- **Region:** (Check your Supabase project)
- **Database:** postgres
- **Port:** 5432
- **SSL Mode:** prefer
- **Connection Pooling:** 10 minutes (CONN_MAX_AGE=600)

---

## 🔐 Security Notes

1. **Never commit DATABASE_URL to git**
2. Change default admin password immediately after first login
3. Supabase provides free SSL certificates
4. Enable Row Level Security (RLS) in Supabase if needed

---

**Created:** October 31, 2025  
**Status:** Ready for Render deployment  
**Next:** Update DATABASE_URL on Render Dashboard
