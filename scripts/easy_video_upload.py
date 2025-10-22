"""
SavvyIndians Bootcamp - Easy YouTube Video Upload Script
Run with: python manage.py shell < scripts/easy_video_upload.py
"""

from course.models import Course, UploadVideo

def add_youtube_video():
    """
    Interactive script to add YouTube videos
    Modify the videos list below and run this script
    """
    
    # ==========================================
    # 📝 EDIT THIS SECTION - Add your videos here
    # ==========================================
    
    videos_to_add = [
        {
            'title': 'Introduction to AI - Welcome Video',
            'youtube_url': 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1',
            'course_code': 'AI101',  # Your course code from admin
            'summary': 'Welcome to the AI bootcamp. Overview of what you will learn.'
        },
        {
            'title': 'Python Basics - Variables and Data Types',
            'youtube_url': 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID_2',
            'course_code': 'PYTHON101',
            'summary': 'Learn Python variables, integers, strings, lists, and dictionaries.'
        },
        # Add more videos below:
        # {
        #     'title': 'Your Video Title',
        #     'youtube_url': 'https://www.youtube.com/watch?v=VIDEO_ID',
        #     'course_code': 'COURSE_CODE',
        #     'summary': 'Video description'
        # },
    ]
    
    # ==========================================
    # 🚀 Script Logic (Don't edit below)
    # ==========================================
    
    print("\n" + "="*60)
    print("🎥 SavvyIndians YouTube Video Upload Script")
    print("="*60 + "\n")
    
    success_count = 0
    error_count = 0
    
    for video_data in videos_to_add:
        try:
            # Validate required fields
            if not video_data.get('youtube_url') or 'YOUR_VIDEO_ID' in video_data.get('youtube_url', ''):
                print(f"⚠️  Skipped: {video_data.get('title', 'Unknown')} - Please update VIDEO_ID")
                error_count += 1
                continue
            
            # Get course
            course = Course.objects.get(code=video_data['course_code'])
            
            # Check if video already exists
            existing = UploadVideo.objects.filter(
                title=video_data['title'],
                course=course
            ).exists()
            
            if existing:
                print(f"ℹ️  Skipped: '{video_data['title']}' - Already exists")
                continue
            
            # Create video
            video = UploadVideo.objects.create(
                title=video_data['title'],
                youtube_url=video_data['youtube_url'],
                course=course,
                summary=video_data.get('summary', '')
            )
            
            print(f"✅ Added: '{video.title}'")
            print(f"   Course: {course.title}")
            print(f"   URL: {video.youtube_url}")
            print(f"   Video ID: {video.get_youtube_video_id()}")
            print()
            
            success_count += 1
            
        except Course.DoesNotExist:
            print(f"❌ Error: Course '{video_data.get('course_code')}' not found")
            print(f"   Create the course first in admin panel")
            print()
            error_count += 1
            
        except Exception as e:
            print(f"❌ Error adding '{video_data.get('title', 'Unknown')}': {str(e)}")
            print()
            error_count += 1
    
    # Summary
    print("="*60)
    print("📊 Upload Summary:")
    print(f"   ✅ Successfully added: {success_count} videos")
    print(f"   ❌ Errors/Skipped: {error_count} videos")
    print("="*60)
    print("\n💡 Next steps:")
    print("   1. Check admin panel: http://127.0.0.1:8000/admin/course/uploadvideo/")
    print("   2. Verify videos appear in your courses")
    print("   3. Test video playback on frontend")
    print("\n")

# Run the script
if __name__ == '__main__':
    add_youtube_video()
