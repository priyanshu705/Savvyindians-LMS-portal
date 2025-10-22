from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Notification Types
PROGRESS_UPDATE = 'progress_update'
COURSE_COMPLETION = 'course_completion'
VIDEO_COMPLETION = 'video_completion'
ACHIEVEMENT = 'achievement'
ANNOUNCEMENT = 'announcement'
REMINDER = 'reminder'
MILESTONE = 'milestone'
WELCOME = 'welcome'

NOTIFICATION_TYPES = (
    (PROGRESS_UPDATE, _('Progress Update')),
    (COURSE_COMPLETION, _('Course Completion')),
    (VIDEO_COMPLETION, _('Video Completion')),
    (ACHIEVEMENT, _('Achievement')),
    (ANNOUNCEMENT, _('Announcement')),
    (REMINDER, _('Reminder')),
    (MILESTONE, _('Milestone')),
    (WELCOME, _('Welcome')),
)

# Priority Levels
LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'
URGENT = 'urgent'

PRIORITY_LEVELS = (
    (LOW, _('Low')),
    (MEDIUM, _('Medium')),
    (HIGH, _('High')),
    (URGENT, _('Urgent')),
)


class NotificationManager(models.Manager):
    def unread(self):
        """Get unread notifications"""
        return self.filter(is_read=False)
    
    def read(self):
        """Get read notifications"""
        return self.filter(is_read=True)
    
    def for_user(self, user):
        """Get notifications for a specific user"""
        return self.filter(recipient=user)
    
    def recent(self, limit=10):
        """Get recent notifications"""
        return self.order_by('-created_at')[:limit]
    
    def by_type(self, notification_type):
        """Get notifications by type"""
        return self.filter(notification_type=notification_type)


class Notification(models.Model):
    """
    Notification model to handle all types of notifications for students
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_("User who will receive this notification")
    )
    
    # Notification Content
    title = models.CharField(
        max_length=200,
        help_text=_("Short notification title")
    )
    message = models.TextField(
        help_text=_("Detailed notification message")
    )
    
    # Notification Metadata
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default=ANNOUNCEMENT,
        help_text=_("Type of notification")
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default=MEDIUM,
        help_text=_("Notification priority level")
    )
    
    # Status Fields
    is_read = models.BooleanField(
        default=False,
        help_text=_("Whether the notification has been read")
    )
    is_sent = models.BooleanField(
        default=False,
        help_text=_("Whether the notification has been sent/delivered")
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the notification was created")
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the notification was read")
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the notification was sent")
    )
    
    # Optional Related Objects
    related_course = models.ForeignKey(
        'course.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Related course if applicable")
    )
    related_video = models.ForeignKey(
        'course.UploadVideo',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Related video if applicable")
    )
    
    # Action URL (optional)
    action_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL to redirect when notification is clicked")
    )
    
    # Icon and styling
    icon = models.CharField(
        max_length=50,
        default='bell',
        help_text=_("Font Awesome icon name")
    )
    color = models.CharField(
        max_length=20,
        default='primary',
        help_text=_("Bootstrap color class")
    )
    
    objects = NotificationManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        if not self.is_sent:
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save(update_fields=['is_sent', 'sent_at'])
    
    @property
    def time_since_created(self):
        """Human readable time since creation"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    @property
    def priority_badge_class(self):
        """Get CSS class for priority badge"""
        priority_classes = {
            LOW: 'badge-secondary',
            MEDIUM: 'badge-primary',
            HIGH: 'badge-warning',
            URGENT: 'badge-danger',
        }
        return priority_classes.get(self.priority, 'badge-primary')
    
    @property
    def type_icon(self):
        """Get icon based on notification type"""
        type_icons = {
            PROGRESS_UPDATE: 'chart-line',
            COURSE_COMPLETION: 'graduation-cap',
            VIDEO_COMPLETION: 'play-circle',
            ACHIEVEMENT: 'trophy',
            ANNOUNCEMENT: 'bullhorn',
            REMINDER: 'clock',
            MILESTONE: 'flag',
            WELCOME: 'hand-wave',
        }
        return type_icons.get(self.notification_type, self.icon)
    
    @property
    def type_color(self):
        """Get color based on notification type"""
        type_colors = {
            PROGRESS_UPDATE: 'info',
            COURSE_COMPLETION: 'success',
            VIDEO_COMPLETION: 'primary',
            ACHIEVEMENT: 'warning',
            ANNOUNCEMENT: 'secondary',
            REMINDER: 'warning',
            MILESTONE: 'success',
            WELCOME: 'primary',
        }
        return type_colors.get(self.notification_type, self.color)


class NotificationPreference(models.Model):
    """
    User preferences for different types of notifications
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Email Notifications
    email_progress_updates = models.BooleanField(
        default=True,
        help_text=_("Receive email for progress updates")
    )
    email_course_completion = models.BooleanField(
        default=True,
        help_text=_("Receive email for course completions")
    )
    email_achievements = models.BooleanField(
        default=True,
        help_text=_("Receive email for achievements")
    )
    email_announcements = models.BooleanField(
        default=True,
        help_text=_("Receive email for announcements")
    )
    email_reminders = models.BooleanField(
        default=True,
        help_text=_("Receive email for reminders")
    )
    
    # In-App Notifications
    app_progress_updates = models.BooleanField(
        default=True,
        help_text=_("Show in-app progress notifications")
    )
    app_course_completion = models.BooleanField(
        default=True,
        help_text=_("Show in-app completion notifications")
    )
    app_achievements = models.BooleanField(
        default=True,
        help_text=_("Show in-app achievement notifications")
    )
    app_announcements = models.BooleanField(
        default=True,
        help_text=_("Show in-app announcements")
    )
    app_reminders = models.BooleanField(
        default=True,
        help_text=_("Show in-app reminders")
    )
    
    # Notification Frequency
    digest_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', _('Immediate')),
            ('daily', _('Daily Digest')),
            ('weekly', _('Weekly Digest')),
            ('never', _('Never')),
        ],
        default='immediate',
        help_text=_("How often to receive notification digests")
    )
    
    # Quiet Hours
    quiet_hours_start = models.TimeField(
        null=True,
        blank=True,
        help_text=_("Start of quiet hours (no notifications)")
    )
    quiet_hours_end = models.TimeField(
        null=True,
        blank=True,
        help_text=_("End of quiet hours")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
    
    def should_send_notification(self, notification_type, delivery_method='app'):
        """Check if notification should be sent based on preferences"""
        if delivery_method == 'email':
            email_prefs = {
                PROGRESS_UPDATE: self.email_progress_updates,
                COURSE_COMPLETION: self.email_course_completion,
                ACHIEVEMENT: self.email_achievements,
                ANNOUNCEMENT: self.email_announcements,
                REMINDER: self.email_reminders,
            }
            return email_prefs.get(notification_type, True)
        else:  # app notifications
            app_prefs = {
                PROGRESS_UPDATE: self.app_progress_updates,
                COURSE_COMPLETION: self.app_course_completion,
                ACHIEVEMENT: self.app_achievements,
                ANNOUNCEMENT: self.app_announcements,
                REMINDER: self.app_reminders,
            }
            return app_prefs.get(notification_type, True)


# Signal to create notification preferences for new users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_notification_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationPreference.objects.get_or_create(user=instance)


# Utility Functions for Creating Notifications
def create_notification(
    recipient,
    title,
    message,
    notification_type=ANNOUNCEMENT,
    priority=MEDIUM,
    related_course=None,
    related_video=None,
    action_url=None,
    icon=None,
    color=None
):
    """
    Utility function to create notifications
    """
    notification = Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        priority=priority,
        related_course=related_course,
        related_video=related_video,
        action_url=action_url,
        icon=icon or 'bell',
        color=color or 'primary'
    )
    
    # Mark as sent immediately for in-app notifications
    notification.mark_as_sent()
    
    return notification


def create_progress_notification(student, video, progress_percentage):
    """Create a progress update notification"""
    if progress_percentage >= 50 and progress_percentage < 90:
        title = f"Great progress on {video.title}!"
        message = f"You're {progress_percentage:.0f}% through '{video.title}'. Keep going!"
        notification_type = PROGRESS_UPDATE
    elif progress_percentage >= 90:
        title = f"Almost finished with {video.title}!"
        message = f"You're {progress_percentage:.0f}% done with '{video.title}'. Just a little more!"
        notification_type = MILESTONE
    else:
        return None  # Don't create notification for low progress
    
    return create_notification(
        recipient=student,
        title=title,
        message=message,
        notification_type=notification_type,
        related_course=video.course,
        related_video=video,
        action_url=video.get_absolute_url()
    )


def create_completion_notification(student, video):
    """Create a video completion notification"""
    title = f"🎉 Congratulations! Video completed!"
    message = f"You've successfully completed '{video.title}' in {video.course.title}. Great job!"
    
    return create_notification(
        recipient=student,
        title=title,
        message=message,
        notification_type=VIDEO_COMPLETION,
        priority=HIGH,
        related_course=video.course,
        related_video=video,
        action_url=video.course.get_absolute_url(),
        icon='check-circle',
        color='success'
    )


def create_course_completion_notification(student, course):
    """Create a course completion notification"""
    title = f"🏆 Course Completed!"
    message = f"Congratulations! You've completed the entire '{course.title}' course. Amazing achievement!"
    
    return create_notification(
        recipient=student,
        title=title,
        message=message,
        notification_type=COURSE_COMPLETION,
        priority=HIGH,
        related_course=course,
        action_url=course.get_absolute_url(),
        icon='graduation-cap',
        color='success'
    )


def create_welcome_notification(student):
    """Create a welcome notification for new students"""
    title = "🎓 Welcome to Django LMS!"
    message = "Welcome to your learning journey! Explore our courses and start building your skills today."
    
    return create_notification(
        recipient=student,
        title=title,
        message=message,
        notification_type=WELCOME,
        priority=HIGH,
        icon='hand-wave',
        color='primary'
    )


def bulk_create_announcement(title, message, users=None, priority=MEDIUM):
    """Create announcement for multiple users"""
    if users is None:
        from accounts.models import User
        users = User.objects.filter(is_student=True)
    
    notifications = []
    for user in users:
        notifications.append(
            Notification(
                recipient=user,
                title=title,
                message=message,
                notification_type=ANNOUNCEMENT,
                priority=priority,
                icon='bullhorn',
                color='info'
            )
        )
    
    # Bulk create for efficiency
    Notification.objects.bulk_create(notifications)
    
    return len(notifications)
