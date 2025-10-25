from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

admin.site.site_header = "SavvyIndians Bootcamp Admin"
admin.site.site_title = "SavvyIndians Admin Portal"
admin.site.index_title = "Welcome to SavvyIndians Bootcamp Administration"

# Simplified URL patterns - English only
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("programs/", include("course.urls")),
    path("notifications/", include("notifications.urls")),
    path("search/", include("search.urls")),
    path("quiz/", include("quiz.urls")),
    path("result/", include("result.urls")),
    # path("payments/", include("payments.urls")),  # Temporarily disabled - needs gopay package
    # Django Allauth URLs
    path("auth/", include("allauth.urls")),
    # Logo Test Page (for debugging)
    path(
        "test-logo/",
        TemplateView.as_view(template_name="test_logo.html"),
        name="test_logo",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
