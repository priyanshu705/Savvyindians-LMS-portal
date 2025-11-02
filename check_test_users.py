"""
Quick script to check if test user exists in database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DATABASE_URL'] = 'postgresql://postgres.atifaphgpescrtmqvigd:Gaurav%237055@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres'

django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Student

User = get_user_model()

# Check recent test users
test_emails = [
    "teststudent_ljjvpn@test.com",
    "teststudent_ao4lzf@test.com",
    "teststudent_ivl2b7@test.com",
]

print("🔍 Checking test user accounts in Supabase database...\n")
print("="*60)

for email in test_emails:
    print(f"\n📧 Checking: {email}")
    try:
        user = User.objects.filter(email__iexact=email).first()
        if user:
            print(f"   ✅ User EXISTS!")
            print(f"   👤 Username: {user.username}")
            print(f"   📛 Name: {user.first_name} {user.last_name}")
            print(f"   📞 Phone: {user.phone}")
            print(f"   🎓 Is Student: {user.is_student}")
            print(f"   ✓ Is Active: {user.is_active}")
            print(f"   🔐 Has usable password: {user.has_usable_password()}")
            
            # Check Student profile
            student_profile = Student.objects.filter(student=user).first()
            if student_profile:
                print(f"   👨‍🎓 Student profile: EXISTS")
                print(f"   📚 Level: {student_profile.level}")
                print(f"   🎯 Program: {student_profile.program}")
            else:
                print(f"   ⚠️  Student profile: MISSING")
        else:
            print(f"   ❌ User NOT FOUND")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("\n✅ Database check complete!")
