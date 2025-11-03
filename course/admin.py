from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Course,
    CourseAllocation,
    Program,
    Upload,
    UploadVideo,
    VideoProgress,
    VideoDRMLog,
)


class ProgramAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "skill_level",
        "total_duration_weeks",
        "is_featured",
        "course_count",
        "video_count",
    ]
    list_filter = ["skill_level", "is_featured"]
    search_fields = ["title", "summary"]
    list_editable = ["is_featured"]

    fieldsets = (
        ("Bootcamp Information", {"fields": ("title", "summary")}),
        (
            "Bootcamp Settings",
            {"fields": ("skill_level", "total_duration_weeks", "is_featured")},
        ),
    )

    def course_count(self, obj):
        return obj.get_course_count()

    course_count.short_description = "Courses"

    def video_count(self, obj):
        return obj.get_video_count()

    video_count.short_description = "Videos"


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "code",
        "program",
        "level",
        "module",
        "duration_weeks",
        "is_premium",
    ]
    list_filter = ["program", "level", "module", "is_premium"]
    search_fields = ["title", "code", "summary"]
    list_editable = ["is_premium"]

    fieldsets = (
        ("Course Information", {"fields": ("title", "code", "summary")}),
        (
            "Bootcamp Settings",
            {"fields": ("program", "level", "module", "duration_weeks")},
        ),
        ("Access Control", {"fields": ("is_premium",), "classes": ("collapse",)}),
    )


class UploadAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "upload_time"]
    list_filter = ["course", "upload_time"]
    search_fields = ["title", "course__title"]


class UploadVideoAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "is_youtube_video", "video_preview", "timestamp"]
    list_filter = ["course", "is_youtube_video", "timestamp"]
    search_fields = ["title", "course__title", "summary"]
    readonly_fields = ["slug", "is_youtube_video", "video_thumbnail_preview"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "course", "summary")}),
        (
            "Video Source",
            {
                "fields": ("youtube_url", "video"),
                "description": "Provide either a YouTube URL (recommended for storage optimization) or upload a video file.",
            },
        ),
        (
            "Auto-Generated Fields",
            {
                "fields": ("slug", "is_youtube_video", "video_duration"),
                "classes": ("collapse",),
            },
        ),
        ("Preview", {"fields": ("video_thumbnail_preview",), "classes": ("collapse",)}),
    )

    def video_preview(self, obj):
        """Display video type and preview link"""
        if obj.is_youtube_video and obj.youtube_url:
            video_id = obj.get_youtube_video_id()
            if video_id:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/default.jpg"
                return format_html(
                    '<img src="{}" width="60" height="45" style="border-radius: 4px;"> <br><small>📺 YouTube</small>',
                    thumbnail_url,
                )
            return "📺 YouTube"
        elif obj.video:
            return "🎬 File Upload"
        return "❌ No Video"

    video_preview.short_description = "Video Preview"

    def video_thumbnail_preview(self, obj):
        """Show larger thumbnail preview in admin"""
        if obj.is_youtube_video and obj.youtube_url:
            video_id = obj.get_youtube_video_id()
            if video_id:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                youtube_link = obj.youtube_url
                return format_html(
                    '<div style="text-align: center;">'
                    '<img src="{}" style="max-width: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"><br>'
                    '<small><a href="{}" target="_blank">🔗 View on YouTube</a></small>'
                    "</div>",
                    thumbnail_url,
                    youtube_link,
                )
        return "No preview available"

    video_thumbnail_preview.short_description = "Thumbnail Preview"


class VideoProgressAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "video",
        "completion_percentage",
        "is_completed",
        "last_watched",
    ]
    list_filter = ["is_completed", "last_watched"]
    search_fields = ["student__username", "video__title"]
    readonly_fields = [
        "completion_percentage",
        "first_watched",
        "last_watched",
        "completed_at",
    ]

    fieldsets = (
        ("Student & Video", {"fields": ("student", "video")}),
        (
            "Progress Details",
            {
                "fields": (
                    "watch_time",
                    "total_duration",
                    "last_position",
                    "completion_percentage",
                    "is_completed",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("first_watched", "last_watched", "completed_at")},
        ),
    )


class VideoDRMLogAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
        "log_type",
        "user",
        "video",
        "violation_type",
        "ip_address",
        "colored_log_type",
    ]
    list_filter = ["log_type", "violation_type", "timestamp"]
    search_fields = ["user__username", "video__title", "ip_address", "user_agent"]
    readonly_fields = [
        "timestamp",
        "log_type",
        "violation_type",
        "user",
        "video",
        "ip_address",
        "user_agent",
        "screen_resolution",
        "platform",
        "url",
    ]

    fieldsets = (
        ("Log Information", {"fields": ("log_type", "violation_type", "timestamp")}),
        ("User & Video", {"fields": ("user", "video")}),
        (
            "Technical Details",
            {
                "fields": (
                    "ip_address",
                    "user_agent",
                    "screen_resolution",
                    "platform",
                    "url",
                )
            },
        ),
    )

    def colored_log_type(self, obj):
        """Display log type with color coding"""
        if obj.log_type == "violation":
            color = "#dc3545"  # Red
            icon = "⚠️"
        else:
            color = "#28a745"  # Green
            icon = "✓"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_log_type_display(),
        )

    colored_log_type.short_description = "Log Type"

    def has_add_permission(self, request):
        """Prevent manual addition of logs through admin"""
        return False

    def has_change_permission(self, request, obj=None):
        """Make logs read-only"""
        return False


# Register bootcamp-related models only
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation)
admin.site.register(Upload, UploadAdmin)
admin.site.register(UploadVideo, UploadVideoAdmin)
admin.site.register(VideoProgress, VideoProgressAdmin)
admin.site.register(VideoDRMLog, VideoDRMLogAdmin)

# Unregister translation models if modeltranslation was previously used
try:
    from modeltranslation.models import TranslationModel

    # Translation models already removed from INSTALLED_APPS
except ImportError:
    pass  # modeltranslation not installed
