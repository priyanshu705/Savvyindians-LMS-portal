"""
Production Database Check - Query via Django ORM using production settings
"""
import os
import sys

# Use production settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_minimal'
os.environ['DEBUG'] = 'False'

import django
django.setup()

from accounts.models import User, Student
from course.models import Course, Program
from quiz.models import Quiz
import requests

print("\n" + "="*70)
print("🌐 PRODUCTION DATABASE CHECK (Render PostgreSQL)")
print("="*70)

# Check if DATABASE_URL is set (production)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    print(f"\n✅ DATABASE_URL is set")
    print(f"   Database: PostgreSQL (Production)")
else:
    print(f"\n⚠️  DATABASE_URL not set - using SQLite")

# Test production site connectivity
print("\n1️⃣ PRODUCTION SITE STATUS:")
try:
    resp = requests.get('https://savvyindians-lms-portal-2.onrender.com/', timeout=30)
    print(f"   ✅ Site Status: {resp.status_code}")
    print(f"   📄 Homepage Size: {len(resp.text)} bytes")
    
    # Check login page
    resp2 = requests.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/login/', timeout=30)
    print(f"   ✅ Login Page: {resp2.status_code}")
    print(f"   🎨 Modern Theme: {'form-modern' in resp2.text}")
    
    # Check admin
    resp3 = requests.get('https://savvyindians-lms-portal-2.onrender.com/admin/', timeout=30)
    print(f"   ✅ Admin Panel: {resp3.status_code}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Query production data via API
print("\n2️⃣ CHECKING PRODUCTION DATA:")
print("   Note: Cannot query production DB directly from local")
print("   Need to check via Render logs or admin panel")

# Show what we CAN check
print("\n3️⃣ WHAT YOU NEED TO CHECK ON RENDER:")
print("   1. Go to Render Dashboard → Your service")
print("   2. Click 'Shell' tab")
print("   3. Run these commands:")
print("      python manage.py shell")
print("      >>> from accounts.models import User")
print("      >>> print(f'Users: {User.objects.count()}')")
print("      >>> from course.models import Program")
print("      >>> print(f'Programs: {Program.objects.count()}')")
print("      >>> [print(p.title) for p in Program.objects.all()]")

print("\n4️⃣ OR CHECK VIA ADMIN PANEL:")
print("   https://savvyindians-lms-portal-2.onrender.com/admin/")
print("   Login with admin credentials")
print("   Check: Users, Programs, Courses")

print("\n" + "="*70)
print("💡 TIP: For production DB access, use Render Shell or Admin Panel")
print("="*70 + "\n")
