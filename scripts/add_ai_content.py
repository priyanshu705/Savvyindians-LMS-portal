import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.utils import timezone  # noqa: E402

from course.models import Course, Program, UploadVideo  # noqa: E402

# Create AI program
ai_program, _ = Program.objects.get_or_create(
    title="Artificial Intelligence",
    summary="Explore AI, machine learning, and deep learning.",
)

# Create AI course
ai_course, _ = Course.objects.get_or_create(
    title="Introduction to Artificial Intelligence",
    code="AI101",
    credit=4,
    summary="Fundamentals of AI, ML, and neural networks.",
    program=ai_program,
    level="Bachelor",
    year=1,
    semester="First",
    is_elective=False,
)

# Add 5 AI YouTube video lessons
ai_videos = [
    {
        "title": "What is Artificial Intelligence?",
        "youtube_url": "https://www.youtube.com/watch?v=JMUxmLyrhSk",
        "summary": "Overview of AI concepts and history.",
    },
    {
        "title": "Machine Learning Basics",
        "youtube_url": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
        "summary": "Introduction to machine learning and algorithms.",
    },
    {
        "title": "Deep Learning Explained",
        "youtube_url": "https://www.youtube.com/watch?v=aircAruvnKk",
        "summary": "Understanding deep learning and neural networks.",
    },
    {
        "title": "Natural Language Processing (NLP)",
        "youtube_url": "https://www.youtube.com/watch?v=8rXD5-xhemo",
        "summary": "Basics of NLP and language models.",
    },
    {
        "title": "AI in Real Life: Applications",
        "youtube_url": "https://www.youtube.com/watch?v=2ePf9rue1Ao",
        "summary": "How AI is used in industry and daily life.",
    },
]

for v in ai_videos:
    UploadVideo.objects.get_or_create(
        title=v["title"],
        course=ai_course,
        youtube_url=v["youtube_url"],
        summary=v["summary"],
        is_youtube_video=True,
        timestamp=timezone.now(),
    )

print("AI program, course, and 5 YouTube lessons added!")
