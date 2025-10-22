from django.contrib import admin
from .models import TakenCourse, Result


class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "course",
        "assignment",
        "mid_exam",
        "quiz",
        "attendance",
        "final_exam",
        "total",
        "grade",
        "comment",
    ]
    list_filter = ['grade', 'course']
    search_fields = ['student__student__username', 'student__student__email', 'course__title']
    
    fieldsets = (
        ('Participant & Course', {
            'fields': ('student', 'course')
        }),
        ('Assessment Scores', {
            'fields': ('assignment', 'mid_exam', 'quiz', 'attendance', 'final_exam')
        }),
        ('Final Results', {
            'fields': ('total', 'grade', 'comment')
        }),
    )


admin.site.register(TakenCourse, ScoreAdmin)
admin.site.register(Result)
