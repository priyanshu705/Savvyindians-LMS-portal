"""
SavvyIndians LMS - Minimal Django Settings for Perfect Serverless Operation
=========================================================================
Simplified configuration for zero-error deployment on Vercel
"""

import os
import dj_database_url

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "bFp3Us&2LTCD+x9M_dC68sSnD41&SRl$7!)om!!1Zr_tV_hs2e"
)
DEBUG = os.environ.get("DEBUG", "True").lower() in ("1", "true", "yes")

# Allowed hosts for Vercel
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "testserver",
    ".vercel.app",
    ".savvyindians.com",
    ".onrender.com",  # Add Render domain
    "*",  # For serverless flexibility
]

# CSRF Trusted Origins for production
CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    "https://*.savvyindians.com",
    "https://*.onrender.com",  # Add Render domain
]

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Minimal application definition for serverless
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # required by allauth and useful for admin
    # Third-party - allauth required for URLs
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Essential project apps only
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "course.apps.CourseConfig",
    "result.apps.ResultConfig",
    "notifications.apps.NotificationsConfig",
    "quiz.apps.QuizConfig",
    # "payments.apps.PaymentsConfig",  # Temporarily disabled - missing gopay dependency
    "search.apps.SearchConfig",
    # Crispy forms for nicer form rendering in templates
    "crispy_forms",
    "crispy_bootstrap5",
]

# Minimal middleware stack
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Required by allauth
]

ROOT_URLCONF = "config.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Avoid implicit imports of config.wsgi during serverless initialization
# Use a single WSGI entrypoint for Django
WSGI_APPLICATION = "config.wsgi.application"

# Database configuration
# Use DATABASE_URL from environment (Render will provide this)
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=0)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# Serverless database optimization (PostgreSQL-safe)
DATABASES["default"]["CONN_MAX_AGE"] = 0  # No persistent connections in serverless

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Use StaticFilesStorage (no manifest) to avoid manifest lookup errors
# WhiteNoise will still serve files efficiently
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Login/Logout redirects
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Default ID prefixes used by account utilities (tests rely on these)
STUDENT_ID_PREFIX = os.environ.get("STUDENT_ID_PREFIX", "STD")
LECTURER_ID_PREFIX = os.environ.get("LECTURER_ID_PREFIX", "LECT")

# Email defaults used in tests to avoid background thread errors
EMAIL_FROM_ADDRESS = os.environ.get("EMAIL_FROM_ADDRESS", "no-reply@example.com")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.locmem.EmailBackend")

# Sites framework (required by allauth)
SITE_ID = 1

# Authentication backends for allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Allauth configuration
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_EMAIL_REQUIRED = True

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_ADAPTER = "accounts.adapters.CustomSocialAccountAdapter"
SOCIALACCOUNT_LOGIN_ON_GET = True

# Google OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
        "FETCH_USERINFO": True,
        "APP": {
            "client_id": os.environ.get("GOOGLE_OAUTH2_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET", ""),
            "key": "",
        },
    }
}

# Simplified logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Essential settings only
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# django-crispy-forms configuration
# Use Bootstrap 5 templates if available
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Production Security Settings (applied when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
