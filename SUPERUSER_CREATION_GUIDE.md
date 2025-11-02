# 🔐 Manual Superuser Creation Guide for Supabase

## Problem
Superuser wasn't created in Supabase database during deployment.

## Solution: Use Render Shell (RECOMMENDED)

### Step 1: Open Render Shell
1. Go to Render Dashboard: https://dashboard.render.com
2. Select service: `savvyindians-lms-portal-2`
3. Click **"Shell"** button (top right)
4. Wait for shell to connect

### Step 2: Run Management Command
In the Render shell, run:
```bash
python manage.py ensure_superuser
```

**Expected Output:**
```
🔍 Checking for superuser: SavvyIndians
✅ Superuser created successfully: SavvyIndians
   Email: gy068644@gmail.com
   ⚠️  Remember to change the default password!
```

### Step 3: Verify Superuser Created
Run this to check:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); admin = User.objects.get(username='SavvyIndians'); print(f'✅ Admin exists: {admin.username}, is_superuser={admin.is_superuser}, is_staff={admin.is_staff}')"
```

---

## Alternative: Force Redeploy

If Shell doesn't work, force a redeploy:

1. Render Dashboard → your service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. This will re-run all `startCommand` steps including `ensure_superuser`

---

## Superuser Credentials

Once created, login at: https://savvyindians-lms-portal-2.onrender.com/admin/

```
Username: SavvyIndians
Password: Savvy@2024#Admin
Email: gy068644@gmail.com
```

⚠️ **IMPORTANT:** Change password immediately after first login!

---

## Troubleshooting

### If `ensure_superuser` command not found:
```bash
python manage.py help
```
Check if `ensure_superuser` is listed under [accounts].

### If superuser exists but can't login:
Reset password:
```bash
python manage.py shell
```
Then:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username='SavvyIndians')
admin.set_password('Savvy@2024#Admin')
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("✅ Password reset!")
exit()
```

---

## Why This Happened

The `startCommand` in render.yaml includes `ensure_superuser`, but:
1. Command might have failed silently
2. Database connection might have timed out
3. Command might have run but didn't output logs

Manual execution via Shell ensures it runs successfully.

---

**Created:** 2025-10-31  
**Status:** Waiting for manual superuser creation via Render Shell
