"""
One-time script to create superuser in Supabase database
Run this locally to create admin user on production database
"""
import os
import django

# Set environment to use Supabase database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DATABASE_URL'] = 'postgresql://postgres.atifaphgpescrtmqvigd:Gaurav%237055@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres'

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Superuser credentials
username = 'SavvyIndians'
email = 'gy068644@gmail.com'
password = 'Savvy@2024#Admin'

print(f"🔍 Checking for superuser: {username}")

# Check if user exists
if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.is_superuser = True
    user.is_staff = True
    user.set_password(password)
    user.save()
    print(f"✅ Updated existing user '{username}' to superuser!")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
else:
    # Create new superuser
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Superuser created successfully!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")

print("\n🎉 You can now login at: https://savvyindians-lms-portal-2.onrender.com/admin/")
print(f"   Username: {username}")
print(f"   Password: {password}")
print("\n⚠️  Remember to change the password after first login!")
