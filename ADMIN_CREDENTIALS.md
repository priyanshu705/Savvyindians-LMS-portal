# 🔐 Admin Access Information

## Default Superuser Credentials

The application automatically creates a superuser during deployment.

### Login Details:

**Admin Panel URL:** https://savvyindians-lms-portal-2.onrender.com/admin/

**Default Credentials:**
- **Username:** `SavvyIndians`
- **Email:** `gy068644@gmail.com`
- **Password:** `Savvy@2024#Admin`

---

## 🔒 Security Note

⚠️ **IMPORTANT:** After first login, please change the password immediately!

### To Change Password:
1. Login to admin panel
2. Go to Users section
3. Click on your username
4. Change password
5. Save

---

## 🎨 Admin Panel Features

The admin panel now has a custom **Black & Gold Theme** matching the SavvyIndians branding:
- Gold (#FFD700) accents
- Black (#000000) background
- White input fields for better visibility
- Responsive design
- Professional look and feel

---

## 📝 Custom Environment Variables (Optional)

You can override the default superuser credentials by setting these environment variables in Render:

```
DJANGO_SUPERUSER_USERNAME=your_username
DJANGO_SUPERUSER_EMAIL=your_email@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

---

## 🚀 How It Works

The superuser is automatically created during deployment by the `ensure_superuser` management command. This command:

1. Checks if a superuser already exists
2. If not, creates one with the credentials above
3. Runs during every deployment (but won't duplicate)
4. No manual intervention needed!

---

## 📞 Support

If you have any issues accessing the admin panel, please check:
1. The deployment logs on Render
2. That the database migrations ran successfully
3. The admin URL is correct

---

**Last Updated:** October 30, 2025
