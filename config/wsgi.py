"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Ensure minimal settings are used if imported indirectly
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_minimal")

application = get_wsgi_application()
