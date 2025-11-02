import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

users = User.objects.all()
print(f'Total users in database: {users.count()}')
print('\nAll users:')
for u in users[:10]:  # Show first 10
    print(f'  - {u.email} ({u.username}) - is_student: {u.is_student}, is_active: {u.is_active}')
    
# Check for test users
test_users = User.objects.filter(email__icontains='teststudent')
print(f'\nTest users found: {test_users.count()}')
for u in test_users:
    print(f'  - {u.email}')
