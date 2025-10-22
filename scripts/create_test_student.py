import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from accounts.models import User, Student
from course.models import Program, Course
from result.models import TakenCourse
from django.contrib.auth.hashers import make_password

# Create a test student user
username = "teststudent"
password = "testpass123"

# Check if student already exists
if User.objects.filter(username=username).exists():
    print(f"Student '{username}' already exists.")
    user = User.objects.get(username=username)
else:
    # Create user
    user = User.objects.create(
        username=username,
        email="teststudent@example.com",
        first_name="Test",
        last_name="Student",
        password=make_password(password),
        is_student=True,
        is_active=True
    )
    print(f"Created student user: {username}")

# Get or create student profile
program = Program.objects.first()
if program:
    student, created = Student.objects.get_or_create(
        student=user,
        defaults={
            'level': 'Bachelor',
            'program': program
        }
    )
    if created:
        print(f"Created student profile for {username}")
    else:
        print(f"Student profile already exists for {username}")
else:
    print("No programs available. Please create a program first.")
    exit()

# Enroll student in first available course
course = Course.objects.first()
if course:
    enrollment, created = TakenCourse.objects.get_or_create(
        student=student,
        course=course
    )
    if created:
        print(f"Enrolled {username} in course: {course.title}")
    else:
        print(f"{username} already enrolled in: {course.title}")
else:
    print("No courses available. Please create a course first.")

print("\n=== Test Student Details ===")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Login URL: http://127.0.0.1:8000/accounts/student/login/")
print(f"Course List URL: http://127.0.0.1:8000/course/user_course_list/")
