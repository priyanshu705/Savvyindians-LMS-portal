from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'recipient_username', 
        'notification_type', 
        'priority_badge', 
        'is_read', 
        'is_sent', 
        'created_at',
        'action_buttons'
    ]
    list_filter = [
        'notification_type', 
        'priority', 
        'is_read', 
        'is_sent', 
        'created_at'
    ]
    search_fields = [
        'title', 
        'message', 
        'recipient__username', 
        'recipient__first_name', 
        'recipient__last_name'
    ]
    readonly_fields = [
        'created_at', 
        'read_at', 
        'sent_at', 
        'time_since_created'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'title', 'message')
        }),
        ('Classification', {
            'fields': ('notification_type', 'priority', 'icon', 'color')
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent')
        }),
        ('Related Objects', {
            'fields': ('related_course', 'related_video', 'action_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at', 'sent_at', 'time_since_created'),
            'classes': ('collapse',)
        })
    )
    
    def recipient_username(self, obj):
        return obj.recipient.username
    recipient_username.short_description = 'Recipient'
    recipient_username.admin_order_field = 'recipient__username'
    
    def priority_badge(self, obj):
        colors = {
            'low': '#6c757d',
            'medium': '#007bff', 
            'high': '#ffc107',
            'urgent': '#dc3545'
        }
        color = colors.get(obj.priority, '#007bff')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    priority_badge.admin_order_field = 'priority'
    
    def action_buttons(self, obj):
        buttons = []
        
        if not obj.is_read:
            mark_read_url = reverse('admin:notifications_notification_changelist')
            buttons.append(
                f'<a href="{mark_read_url}?mark_read={obj.id}" '
                f'style="background: #28a745; color: white; padding: 2px 6px; '
                f'text-decoration: none; border-radius: 3px; font-size: 11px;">Mark Read</a>'
            )
        
        if obj.action_url:
            buttons.append(
                f'<a href="{obj.action_url}" target="_blank" '
                f'style="background: #17a2b8; color: white; padding: 2px 6px; '
                f'text-decoration: none; border-radius: 3px; font-size: 11px;">View Action</a>'
            )
            
        return mark_safe(' '.join(buttons)) if buttons else '-'
    action_buttons.short_description = 'Actions'
    
    actions = ['mark_as_read', 'mark_as_unread', 'delete_selected']
    
    def mark_as_read(self, request, queryset):
        updated = 0
        for notification in queryset:
            if not notification.is_read:
                notification.mark_as_read()
                updated += 1
        
        self.message_user(
            request,
            f'{updated} notification(s) marked as read.'
        )
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.filter(is_read=True).update(
            is_read=False,
            read_at=None
        )
        self.message_user(
            request,
            f'{updated} notification(s) marked as unread.'
        )
    mark_as_unread.short_description = "Mark selected notifications as unread"


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user_info',
        'email_notifications_summary',
        'app_notifications_summary', 
        'digest_frequency',
        'updated_at'
    ]
    list_filter = [
        'digest_frequency',
        'email_progress_updates',
        'email_course_completion',
        'app_progress_updates',
        'app_course_completion'
    ]
    search_fields = [
        'user__username',
        'user__first_name', 
        'user__last_name',
        'user__email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': (
                'email_progress_updates',
                'email_course_completion', 
                'email_achievements',
                'email_announcements',
                'email_reminders'
            )
        }),
        ('In-App Notifications', {
            'fields': (
                'app_progress_updates',
                'app_course_completion',
                'app_achievements', 
                'app_announcements',
                'app_reminders'
            )
        }),
        ('Notification Settings', {
            'fields': (
                'digest_frequency',
                'quiet_hours_start',
                'quiet_hours_end'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def user_info(self, obj):
        return f"{obj.user.get_full_name} ({obj.user.username})"
    user_info.short_description = 'User'
    user_info.admin_order_field = 'user__username'
    
    def email_notifications_summary(self, obj):
        enabled = sum([
            obj.email_progress_updates,
            obj.email_course_completion,
            obj.email_achievements,
            obj.email_announcements,
            obj.email_reminders
        ])
        total = 5
        color = '#28a745' if enabled > 3 else '#ffc107' if enabled > 1 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{} enabled</span>',
            color, enabled, total
        )
    email_notifications_summary.short_description = 'Email Notifications'
    
    def app_notifications_summary(self, obj):
        enabled = sum([
            obj.app_progress_updates,
            obj.app_course_completion,
            obj.app_achievements,
            obj.app_announcements,
            obj.app_reminders
        ])
        total = 5
        color = '#28a745' if enabled > 3 else '#ffc107' if enabled > 1 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{} enabled</span>',
            color, enabled, total
        )
    app_notifications_summary.short_description = 'App Notifications'
