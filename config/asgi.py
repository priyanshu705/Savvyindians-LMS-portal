import os
from django.core.asgi import get_asgi_application

# Use minimal settings and let Django initialize lazily
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_minimal")

application = get_asgi_application()
