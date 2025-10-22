from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # API endpoints
    path('api/list/', views.notification_list_api, name='notification_list_api'),
    path('api/count/', views.notification_count_api, name='notification_count_api'),
    path('api/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('api/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    
    # HTML views
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('preferences/', views.notification_preferences_view, name='notification_preferences'),
    
    # Admin functions
    path('api/create-announcement/', views.create_announcement_api, name='create_announcement_api'),
    path('api/test/', views.notification_test_view, name='notification_test'),
]