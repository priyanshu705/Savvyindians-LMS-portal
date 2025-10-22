import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from course.models import Program, Course, UploadVideo
from django.utils import timezone

# Use existing program or create one
program, _ = Program.objects.get_or_create(title="Computer Science", summary="Learn programming, algorithms, and software engineering.")

# Add new course named Python
python_course, _ = Course.objects.get_or_create(
    title="Python",
    code="PY202",
    credit=3,
    summary="A practical course on Python programming.",
    program=program,
    level="Bachelor",
    year=1,
    semester="First",
    is_elective=False,
)

# Add a YouTube video lesson
UploadVideo.objects.get_or_create(
    title="Python Crash Course",
    course=python_course,
    youtube_url="https://www.youtube.com/watch?v=jjw5dYBz2zU",
    summary="A complete Python crash course for beginners.",
    is_youtube_video=True,
    timestamp=timezone.now()
)

print("Python course and YouTube lesson added!")
