from django.contrib import admin

from .models import NewsAndEvents, Semester, Session


# Temporarily using standard ModelAdmin instead of TranslationAdmin
class NewsAndEventsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(NewsAndEvents, NewsAndEventsAdmin)
