"""
Quick Script to Create Superuser on Render.com
Run this command in Render Shell
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║          CREATE SUPERUSER ON RENDER.COM                          ║
╚══════════════════════════════════════════════════════════════════╝

📋 INSTRUCTIONS:
-----------------

1. Go to Render Dashboard:
   https://dashboard.render.com/

2. Select your service:
   "savvyindians-lms-portal-2"

3. Click "Shell" tab (top navigation)

4. Run this command:
   
   python manage.py createsuperuser

5. Enter details when prompted:
   - Username: admin
   - Email: admin@savvyindians.com
   - Password: [choose a strong password]
   - Password (again): [confirm]

6. You should see:
   "Superuser created successfully."

7. Now you can login at:
   https://savvyindians-lms-portal-2.onrender.com/admin/

═══════════════════════════════════════════════════════════════════

🔍 ALTERNATIVE - Check if superuser already exists:
---------------------------------------------------

In Render Shell, run:
python manage.py shell

Then run:
from accounts.models import User
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"Username: {admin.username}, Email: {admin.email}")
exit()

═══════════════════════════════════════════════════════════════════

💡 TIP: If you want to reset admin password:
-------------------------------------------

In Render Shell:
python manage.py changepassword admin

Enter new password when prompted.

═══════════════════════════════════════════════════════════════════
""")
