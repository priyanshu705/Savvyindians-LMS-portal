"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

# Setup DATABASE_URL first (before Django loads)
from config.render_env import setup_render_database
setup_render_database()

from django.core.wsgi import get_wsgi_application

# Ensure minimal settings are used if imported indirectly
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_minimal")

application = get_wsgi_application()

# Run migrations AFTER Django is fully initialized (only on Render)
if os.environ.get('RENDER'):
    try:
        from django.core.management import call_command
        print("🔄 Running migrations on Render startup...", file=sys.stderr, flush=True)
        call_command('migrate', '--noinput', verbosity=1)
        print("✓ Migrations completed successfully!", file=sys.stderr, flush=True)
        
        print("🔄 Collecting static files...", file=sys.stderr, flush=True)
        call_command('collectstatic', '--noinput', '--clear', verbosity=1)
        print("✓ Static files collected!", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"⚠ Warning: Could not run migrations: {e}", file=sys.stderr, flush=True)
