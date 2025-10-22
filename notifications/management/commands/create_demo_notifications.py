"""
Django management command to create demo notifications for testing the notification system.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from notifications.models import Notification, NotificationPreference
from course.models import Course, UploadVideo
from quiz.models import Quiz
from core.models import Session, Semester

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo notifications for testing the notification system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of random users to create notifications for (default: 5)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Total number of notifications to create (default: 50)',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear all existing notifications before creating new ones',
        )

    def handle(self, *args, **options):
        users_count = options['users']
        notifications_count = options['count']
        clear_existing = options['clear_existing']

        self.stdout.write(
            self.style.SUCCESS(f'Creating {notifications_count} demo notifications for {users_count} users...')
        )

        # Clear existing notifications if requested
        if clear_existing:
            deleted_count = Notification.objects.all().count()
            Notification.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Cleared {deleted_count} existing notifications')
            )

        # Get users (preferably students)
        users = list(User.objects.filter(is_student=True)[:users_count])
        if len(users) < users_count:
            # If not enough student users, get any users
            additional_users = User.objects.exclude(
                id__in=[u.id for u in users]
            )[:users_count - len(users)]
            users.extend(additional_users)

        if not users:
            self.stdout.write(
                self.style.ERROR('No users found. Please create some users first.')
            )
            return

        # Get some courses and videos for related content
        courses = list(Course.objects.all()[:10])
        videos = list(UploadVideo.objects.all()[:20])
        quizzes = list(Quiz.objects.all()[:10])

        # Notification templates for each type
        notification_templates = {
            'progress_update': [
                {
                    'title': 'Course Progress Update',
                    'message': 'You have completed {progress}% of the course "{course}". Keep up the great work!',
                    'color': 'primary',
                    'priority': 'medium',
                },
                {
                    'title': 'Learning Milestone Reached',
                    'message': 'Congratulations! You have watched {count} videos in "{course}". You\'re making excellent progress.',
                    'color': 'info',
                    'priority': 'medium',
                },
                {
                    'title': 'Weekly Progress Summary',
                    'message': 'This week you completed {hours} hours of learning across {courses} courses. Fantastic dedication!',
                    'color': 'primary',
                    'priority': 'low',
                },
            ],
            'course_completion': [
                {
                    'title': 'Course Completed! 🎉',
                    'message': 'Congratulations! You have successfully completed "{course}". Your certificate is now available.',
                    'color': 'success',
                    'priority': 'high',
                },
                {
                    'title': 'Course Module Finished',
                    'message': 'You have completed all modules in "{course}". Time to celebrate your achievement!',
                    'color': 'success',
                    'priority': 'medium',
                },
            ],
            'video_completion': [
                {
                    'title': 'Video Completed',
                    'message': 'You finished watching "{video}" in course "{course}". Ready for the next lesson?',
                    'color': 'info',
                    'priority': 'low',
                },
                {
                    'title': 'Learning Session Complete',
                    'message': 'Great job completing the video "{video}". Your learning streak continues!',
                    'color': 'primary',
                    'priority': 'low',
                },
            ],
            'achievement': [
                {
                    'title': 'Achievement Unlocked! 🏆',
                    'message': 'You earned the "{achievement}" achievement for your outstanding performance!',
                    'color': 'warning',
                    'priority': 'high',
                },
                {
                    'title': 'Learning Streak Achievement',
                    'message': 'Amazing! You\'ve maintained a {days}-day learning streak. Keep the momentum going!',
                    'color': 'warning',
                    'priority': 'medium',
                },
                {
                    'title': 'Quiz Master Badge',
                    'message': 'You scored 100% on {count} quizzes this month. You\'ve earned the Quiz Master badge!',
                    'color': 'warning',
                    'priority': 'medium',
                },
            ],
            'announcement': [
                {
                    'title': 'New Course Available',
                    'message': 'A new course "{course}" has been added to your program. Check it out now!',
                    'color': 'primary',
                    'priority': 'medium',
                },
                {
                    'title': 'System Maintenance Notice',
                    'message': 'Scheduled maintenance will occur on {date} from 2:00 AM to 4:00 AM UTC. Please plan accordingly.',
                    'color': 'warning',
                    'priority': 'high',
                },
                {
                    'title': 'Platform Update Released',
                    'message': 'We\'ve released new features including improved video player and enhanced quiz experience!',
                    'color': 'info',
                    'priority': 'medium',
                },
            ],
            'reminder': [
                {
                    'title': 'Quiz Deadline Approaching',
                    'message': 'Don\'t forget! The quiz "{quiz}" is due in 2 days. Complete it before the deadline.',
                    'color': 'warning',
                    'priority': 'high',
                },
                {
                    'title': 'Course Assignment Due',
                    'message': 'Reminder: Your assignment for "{course}" is due tomorrow. Submit it on time to avoid late penalties.',
                    'color': 'danger',
                    'priority': 'urgent',
                },
                {
                    'title': 'Resume Your Learning',
                    'message': 'You haven\'t accessed "{course}" in 3 days. Continue where you left off!',
                    'color': 'info',
                    'priority': 'low',
                },
            ],
            'milestone': [
                {
                    'title': 'Learning Milestone: {milestone}',
                    'message': 'Congratulations! You\'ve reached an important milestone in your learning journey.',
                    'color': 'success',
                    'priority': 'medium',
                },
                {
                    'title': '50% Course Progress',
                    'message': 'You\'re halfway through "{course}"! Keep pushing forward to reach the finish line.',
                    'color': 'primary',
                    'priority': 'medium',
                },
            ],
            'welcome': [
                {
                    'title': 'Welcome to the Learning Platform! 👋',
                    'message': 'Welcome {name}! We\'re excited to have you join our learning community. Start your journey today!',
                    'color': 'primary',
                    'priority': 'medium',
                },
                {
                    'title': 'Getting Started Guide',
                    'message': 'New to the platform? Check out our getting started guide to make the most of your learning experience.',
                    'color': 'info',
                    'priority': 'low',
                },
            ],
        }

        # Create notifications
        created_count = 0
        for i in range(notifications_count):
            user = random.choice(users)
            notification_type = random.choice(list(notification_templates.keys()))
            template = random.choice(notification_templates[notification_type])
            
            # Generate dynamic content based on type
            course = random.choice(courses) if courses else None
            video = random.choice(videos) if videos else None
            quiz = random.choice(quizzes) if quizzes else None
            
            # Format message with dynamic content
            message = template['message']
            title = template['title']
            
            # Replace placeholders
            if '{course}' in message and course:
                message = message.replace('{course}', course.title)
                title = title.replace('{course}', course.title)
            
            if '{video}' in message and video:
                message = message.replace('{video}', video.title)
            
            if '{quiz}' in message and quiz:
                message = message.replace('{quiz}', quiz.title)
            
            if '{name}' in message:
                try:
                    full_name = user.get_full_name() if hasattr(user, 'get_full_name') else user.username
                except:
                    full_name = str(user.first_name + ' ' + user.last_name) if hasattr(user, 'first_name') else user.username
                message = message.replace('{name}', full_name)
            
            # Generate random values for placeholders
            message = message.replace('{progress}', str(random.randint(20, 95)))
            message = message.replace('{count}', str(random.randint(5, 25)))
            message = message.replace('{hours}', str(random.randint(2, 12)))
            message = message.replace('{courses}', str(random.randint(2, 8)))
            message = message.replace('{days}', str(random.randint(7, 30)))
            message = message.replace('{achievement}', random.choice([
                'Course Completion Expert', 'Video Enthusiast', 'Quiz Champion', 'Learning Streaker'
            ]))
            message = message.replace('{milestone}', random.choice([
                '100 Videos Watched', '10 Courses Completed', '1000 Points Earned', 'First Month Complete'
            ]))
            message = message.replace('{date}', (timezone.now() + timedelta(days=7)).strftime('%B %d, %Y'))
            
            # Generate creation time (last 30 days)
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            created_at = timezone.now() - timedelta(
                days=days_ago, 
                hours=hours_ago, 
                minutes=minutes_ago
            )
            
            # Random read status (70% chance of being read for older notifications)
            is_read = random.random() < 0.7 if days_ago > 3 else random.random() < 0.3
            
            # Create the notification
            notification = Notification.objects.create(
                recipient=user,
                notification_type=notification_type,
                title=title,
                message=message,
                priority=template['priority'],
                is_read=is_read,
                related_course=course if notification_type in ['progress_update', 'course_completion'] else None,
                related_video=video if notification_type == 'video_completion' else None,
            )
            
            # Update created_at manually
            notification.created_at = created_at
            notification.save(update_fields=['created_at'])
            
            # Set read_at for read notifications
            if is_read:
                notification.read_at = created_at + timedelta(
                    hours=random.randint(1, 48)
                )
                notification.save(update_fields=['read_at'])
            
            created_count += 1
            
            # Progress indicator
            if created_count % 10 == 0:
                self.stdout.write(f'Created {created_count}/{notifications_count} notifications...')

        # Ensure all users have notification preferences
        for user in users:
            NotificationPreference.objects.get_or_create(
                user=user,
                defaults={
                    'digest_frequency': 'immediate',
                    'email_progress_updates': random.choice([True, False]),
                    'email_course_completion': True,
                    'email_achievements': True,
                    'email_announcements': random.choice([True, False]),
                    'email_reminders': True,
                    'app_progress_updates': True,
                    'app_course_completion': True,
                    'app_achievements': True,
                    'app_announcements': True,
                    'app_reminders': True,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} demo notifications for {len(users)} users!'
            )
        )
        
        # Display statistics
        total_notifications = Notification.objects.count()
        unread_notifications = Notification.objects.filter(is_read=False).count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('NOTIFICATION STATISTICS:')
        self.stdout.write('='*50)
        self.stdout.write(f'Total notifications: {total_notifications}')
        self.stdout.write(f'Unread notifications: {unread_notifications}')
        self.stdout.write(f'Read notifications: {total_notifications - unread_notifications}')
        
        # Per-type breakdown
        self.stdout.write('\nNotifications by type:')
        for notification_type in notification_templates.keys():
            count = Notification.objects.filter(notification_type=notification_type).count()
            self.stdout.write(f'  {notification_type}: {count}')
        
        # Per-user breakdown
        self.stdout.write('\nTop 5 users by notification count:')
        from django.db.models import Count
        top_users = User.objects.annotate(
            notification_count=Count('notifications')
        ).order_by('-notification_count')[:5]
        
        for user in top_users:
            self.stdout.write(f'  {user.username}: {user.notification_count} notifications')
        
        self.stdout.write('\n' + self.style.SUCCESS('Demo notification creation completed! 🎉'))
        self.stdout.write('You can now test the notification system in the UI.')