"""
Quick database connection test
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from accounts.models import User, Student
from course.models import Course
import requests

print("\n" + "="*70)
print("📊 DATABASE CONNECTION TEST")
print("="*70)

# Test 1: Local Database
print("\n1️⃣ LOCAL DATABASE (SQLite):")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   ✅ Connected: {connection.settings_dict['NAME']}")
        print(f"   📋 Total tables: {len(tables)}")
        
        # Show key tables
        key_tables = [t[0] for t in tables if any(x in t[0] for x in ['auth_user', 'accounts', 'course', 'quiz'])]
        if key_tables:
            print(f"   🔑 Key tables: {', '.join(key_tables[:5])}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Query data
print("\n2️⃣ DATA QUERY TEST:")
try:
    user_count = User.objects.count()
    student_count = User.objects.filter(is_student=True).count()
    admin_count = User.objects.filter(is_superuser=True).count()
    course_count = Course.objects.count()
    
    print(f"   ✅ Total Users: {user_count}")
    print(f"   👨‍🎓 Students: {student_count}")
    print(f"   👑 Admins: {admin_count}")
    print(f"   📚 Courses: {course_count}")
    
    # Show recent users
    if user_count > 0:
        print("\n   📋 Recent Users:")
        for user in User.objects.all()[:5]:
            role = "Admin" if user.is_superuser else "Student" if user.is_student else "User"
            print(f"      • {user.email or user.username} ({role})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Production site
print("\n3️⃣ PRODUCTION SITE (Render PostgreSQL):")
try:
    resp = requests.get('https://savvyindians-lms-portal-2.onrender.com/admin/login/', timeout=30)
    print(f"   ✅ Site Status: {resp.status_code}")
    print(f"   📄 Response Size: {len(resp.text)} bytes")
    print(f"   🔑 Login page accessible: {'id_username' in resp.text}")
    
    # Test student login page
    resp2 = requests.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/login/', timeout=30)
    print(f"\n   📝 Student Login Status: {resp2.status_code}")
    print(f"   🎨 Modern theme loaded: {'form-modern' in resp2.text}")
    print(f"   🖼️  Logo present: {'savvyindians-logo.png' in resp2.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ Database check complete!")
print("="*70 + "\n")
