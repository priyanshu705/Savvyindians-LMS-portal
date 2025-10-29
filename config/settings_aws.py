"""
AWS-specific Django settings for production deployment on Elastic Beanstalk.
This configuration is optimized for AWS services and Free Tier usage.
"""
import os
from .settings import *

# AWS Elastic Beanstalk detection
IS_AWS_EB = 'RDS_HOSTNAME' in os.environ

# Security settings for AWS
DEBUG = False
ALLOWED_HOSTS = [
    os.environ.get('EB_DOMAIN', ''),
    '.elasticbeanstalk.com',
    '.amazonaws.com',
]

# AWS RDS PostgreSQL Database
if IS_AWS_EB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('RDS_DB_NAME', 'lmsdb'),
            'USER': os.environ.get('RDS_USERNAME', 'postgres'),
            'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
            'HOST': os.environ.get('RDS_HOSTNAME', 'localhost'),
            'PORT': os.environ.get('RDS_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
        }
    }

# AWS S3 Storage Configuration
if IS_AWS_EB and os.environ.get('AWS_STORAGE_BUCKET_NAME'):
    # Install: pip install django-storages boto3
    INSTALLED_APPS += ['storages']
    
    # S3 Settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # S3 Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # S3 Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    
    # S3 Security
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_QUERYSTRING_AUTH = False

# Security Headers
SECURE_SSL_REDIRECT = IS_AWS_EB
SESSION_COOKIE_SECURE = IS_AWS_EB
CSRF_COOKIE_SECURE = IS_AWS_EB
SECURE_HSTS_SECONDS = 31536000 if IS_AWS_EB else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_AWS_EB
SECURE_HSTS_PRELOAD = IS_AWS_EB
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging for AWS CloudWatch
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email Configuration for AWS SES (optional)
if os.environ.get('AWS_SES_REGION_NAME'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = f'email-smtp.{os.environ.get("AWS_SES_REGION_NAME")}.amazonaws.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('AWS_SES_USERNAME', '')
    EMAIL_HOST_PASSWORD = os.environ.get('AWS_SES_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@savvyindians.com')

print("🚀 AWS Elastic Beanstalk settings loaded!")
if IS_AWS_EB:
    print("✅ Running on AWS with RDS PostgreSQL")
else:
    print("⚠️  Not on AWS - using local database")
