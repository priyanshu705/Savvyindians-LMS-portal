"""
SavvyIndians LMS - Minimal Django Settings for Perfect Serverless Operation
=========================================================================
Simplified configuration for zero-error deployment on Vercel
"""

import os
import sys
import dj_database_url

# CRITICAL: Setup Render environment variables FIRST (before anything else)
# This must run before any database configuration
try:
    from config.render_env import setup_render_database
    setup_render_database()
except Exception as e:
    print(f"Warning: Could not load render_env: {e}", file=sys.stderr)

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
# CRITICAL: SECRET_KEY must be set in environment variables
# No fallback for production security
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if os.environ.get('RENDER'):
        # On Render, SECRET_KEY is required
        raise EnvironmentError(
            "SECRET_KEY environment variable is required for production. "
            "Please set it in the Render dashboard (use 'generateValue: true' in render.yaml)"
        )
    else:
        # Local development only - generate a random key
        import secrets
        SECRET_KEY = secrets.token_urlsafe(50)
        print("⚠ WARNING: Using auto-generated SECRET_KEY for development", file=sys.stderr)

# DEBUG should default to False for security (only enable explicitly)
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# Allowed hosts - specific domains only for security
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "testserver",
    ".vercel.app",
    ".savvyindians.com",
    ".onrender.com",  # Render domain
    "savvyindians-lms-portal-2.onrender.com",  # Specific Render URL
]

# Only allow wildcard in local development
if DEBUG and not os.environ.get('RENDER'):
    ALLOWED_HOSTS.append("*")

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
DATABASE_URL = os.environ.get("DATABASE_URL")

# Debug logging for database configuration
import sys
if DATABASE_URL:
    print(f"✓ DATABASE_URL found: {DATABASE_URL[:50]}...", file=sys.stderr)
    
    # Parse DATABASE_URL - supports PostgreSQL, MySQL, and SQLite
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    
    # Add database-specific options
    engine = DATABASES["default"]["ENGINE"]
    if "postgresql" in engine or "psycopg2" in engine:
        # PostgreSQL configuration - use prefer for Render compatibility
        DATABASES["default"]["OPTIONS"] = {
            "sslmode": "prefer",
            "connect_timeout": 10,
        }
        print(f"✓ Using PostgreSQL database: {DATABASES['default']['NAME']}", file=sys.stderr)
    elif "mysql" in engine:
        # MySQL configuration
        DATABASES["default"]["OPTIONS"] = {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
        print(f"✓ Using MySQL database: {DATABASES['default']['NAME']}", file=sys.stderr)
    else:
        print(f"✓ Using {engine} database: {DATABASES['default']['NAME']}", file=sys.stderr)
else:
    print("✗ DATABASE_URL NOT FOUND in environment!", file=sys.stderr)
    # Fallback to SQLite for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
    print("✓ Using SQLite database for local development", file=sys.stderr)
    # Print warning if running in production without DATABASE_URL
    if not DEBUG:
        print("✗✗✗ CRITICAL: Running in production mode without DATABASE_URL!", file=sys.stderr)

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

# WhiteNoise configuration for Render
# Use basic storage without compression or manifest to avoid database queries
if os.environ.get('RENDER'):
    # On Render, use WhiteNoise but disable manifest/compression to avoid DB issues
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
else:
    # Local development
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

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

# Production Security Settings (always enabled, not just when DEBUG=False)
# These settings protect against common web attacks
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS enforcement - only on production (Render)
if os.environ.get('RENDER'):
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
