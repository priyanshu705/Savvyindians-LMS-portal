"""
Create default Programs for production
Run this on Render Shell: python create_programs.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Program

programs_data = [
    {
        'title': 'AI & Machine Learning Bootcamp',
        'summary': 'Master AI, ML, and Deep Learning with hands-on projects',
    },
    {
        'title': 'Full Stack Web Development',
        'summary': 'Learn MERN/MEAN stack development from scratch',
    },
    {
        'title': 'Data Science Masterclass',
        'summary': 'Python, Data Analysis, Visualization, and Big Data',
    },
    {
        'title': 'Cloud & DevOps Engineering',
        'summary': 'AWS, Azure, Docker, Kubernetes, and CI/CD pipelines',
    },
    {
        'title': 'Mobile App Development',
        'summary': 'Build Android & iOS apps with React Native/Flutter',
    },
]

print("\n" + "="*70)
print("📚 CREATING PROGRAMS FOR PRODUCTION")
print("="*70 + "\n")

created_count = 0
updated_count = 0

for program_data in programs_data:
    program, created = Program.objects.get_or_create(
        title=program_data['title'],
        defaults={'summary': program_data['summary']}
    )
    
    if created:
        print(f"✅ Created: {program.title}")
        created_count += 1
    else:
        print(f"⚠️  Already exists: {program.title}")
        updated_count += 1

print(f"\n" + "="*70)
print(f"✅ Total Programs: {Program.objects.count()}")
print(f"   • Created: {created_count}")
print(f"   • Existing: {updated_count}")
print("="*70 + "\n")
