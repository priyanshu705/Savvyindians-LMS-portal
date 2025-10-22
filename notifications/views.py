from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json

from .models import Notification, NotificationPreference
from .models import create_notification, bulk_create_announcement


@login_required
@require_GET
def notification_list_api(request):
    """API endpoint to get user's notifications"""
    
    # Get query parameters
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
    notification_type = request.GET.get('type', None)
    
    # Build queryset
    notifications = Notification.objects.for_user(request.user)
    
    if unread_only:
        notifications = notifications.unread()
    
    if notification_type:
        notifications = notifications.by_type(notification_type)
    
    # Paginate
    paginator = Paginator(notifications, per_page)
    page_obj = paginator.get_page(page)
    
    # Serialize notifications
    notifications_data = []
    for notification in page_obj:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'priority': notification.priority,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat(),
            'time_since': notification.time_since_created,
            'icon': notification.type_icon,
            'color': notification.type_color,
            'action_url': notification.action_url,
            'related_course': {
                'id': notification.related_course.id,
                'title': notification.related_course.title
            } if notification.related_course else None,
            'related_video': {
                'id': notification.related_video.id,
                'title': notification.related_video.title
            } if notification.related_video else None,
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        },
        'unread_count': Notification.objects.for_user(request.user).unread().count()
    })


@login_required
@require_POST 
@csrf_exempt
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    notification.mark_as_read()
    
    return JsonResponse({
        'success': True,
        'message': 'Notification marked as read',
        'notification_id': notification_id
    })


@login_required
@require_POST
@csrf_exempt 
def mark_all_notifications_read(request):
    """Mark all user's notifications as read"""
    
    updated_count = 0
    unread_notifications = Notification.objects.for_user(request.user).unread()
    
    for notification in unread_notifications:
        notification.mark_as_read()
        updated_count += 1
    
    return JsonResponse({
        'success': True,
        'message': f'{updated_count} notifications marked as read',
        'updated_count': updated_count
    })


@login_required
@require_GET
def notification_count_api(request):
    """Get unread notification count for user"""
    
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    return JsonResponse({
        'unread_count': unread_count
    })


@login_required
@require_POST
@csrf_exempt
def delete_notification(request, notification_id):
    """Delete a specific notification"""
    
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    
    notification.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Notification deleted successfully'
    })


@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    """HTML view for notifications page"""
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.for_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add notification statistics
        user_notifications = Notification.objects.for_user(self.request.user)
        context.update({
            'unread_count': user_notifications.unread().count(),
            'total_count': user_notifications.count(),
            'notification_types': [
                {
                    'type': nt[0],
                    'label': nt[1],
                    'count': user_notifications.by_type(nt[0]).count()
                }
                for nt in Notification.NOTIFICATION_TYPES
                if user_notifications.by_type(nt[0]).exists()
            ]
        })
        
        return context


@login_required
def notification_preferences_view(request):
    """View and update notification preferences"""
    
    preferences, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        # Update preferences
        preferences.email_progress_updates = request.POST.get('email_progress_updates') == 'on'
        preferences.email_course_completion = request.POST.get('email_course_completion') == 'on'
        preferences.email_achievements = request.POST.get('email_achievements') == 'on'
        preferences.email_announcements = request.POST.get('email_announcements') == 'on'
        preferences.email_reminders = request.POST.get('email_reminders') == 'on'
        
        preferences.app_progress_updates = request.POST.get('app_progress_updates') == 'on'
        preferences.app_course_completion = request.POST.get('app_course_completion') == 'on'
        preferences.app_achievements = request.POST.get('app_achievements') == 'on'
        preferences.app_announcements = request.POST.get('app_announcements') == 'on'
        preferences.app_reminders = request.POST.get('app_reminders') == 'on'
        
        preferences.digest_frequency = request.POST.get('digest_frequency', 'immediate')
        
        # Handle quiet hours
        quiet_start = request.POST.get('quiet_hours_start')
        quiet_end = request.POST.get('quiet_hours_end')
        
        if quiet_start:
            preferences.quiet_hours_start = timezone.datetime.strptime(quiet_start, '%H:%M').time()
        if quiet_end:
            preferences.quiet_hours_end = timezone.datetime.strptime(quiet_end, '%H:%M').time()
        
        preferences.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification preferences updated successfully'
        })
    
    context = {
        'preferences': preferences
    }
    
    return render(request, 'notifications/preferences.html', context)


# Admin functions
@login_required
@require_POST
@csrf_exempt
def create_announcement_api(request):
    """Create announcement for all students (admin only)"""
    
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        title = data.get('title')
        message = data.get('message')
        priority = data.get('priority', 'medium')
        
        if not title or not message:
            return JsonResponse({
                'success': False,
                'error': 'Title and message are required'
            }, status=400)
        
        # Create announcement for all students
        from accounts.models import User
        students = User.objects.filter(is_student=True)
        
        count = bulk_create_announcement(
            title=title,
            message=message,
            users=students,
            priority=priority
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Announcement sent to {count} students',
            'count': count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def notification_test_view(request):
    """Test notification creation (for demo purposes)"""
    
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    
    # Create test notifications
    from .models import (
        create_welcome_notification,
        create_progress_notification,
        create_completion_notification,
        PROGRESS_UPDATE, HIGH
    )
    
    test_notifications = []
    
    # Create welcome notification
    welcome_notif = create_welcome_notification(request.user)
    test_notifications.append(welcome_notif)
    
    # Create progress notification
    progress_notif = create_notification(
        recipient=request.user,
        title="🚀 Great Progress!",
        message="You're making excellent progress in your learning journey. Keep it up!",
        notification_type=PROGRESS_UPDATE,
        priority=HIGH,
        icon='chart-line',
        color='info'
    )
    test_notifications.append(progress_notif)
    
    # Create achievement notification
    achievement_notif = create_notification(
        recipient=request.user,
        title="🏆 Achievement Unlocked!",
        message="You've completed 5 videos this week. Amazing dedication!",
        notification_type='achievement',
        priority=HIGH,
        icon='trophy',
        color='warning'
    )
    test_notifications.append(achievement_notif)
    
    return JsonResponse({
        'success': True,
        'message': f'Created {len(test_notifications)} test notifications',
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'type': n.notification_type
            } for n in test_notifications
        ]
    })
