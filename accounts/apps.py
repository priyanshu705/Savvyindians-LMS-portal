from django.apps import AppConfig
import os


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self) -> None:
        # In serverless boot, skip importing heavy signal handlers to reduce init side effects
        if os.environ.get("DJANGO_SERVERLESS") == "True" or os.environ.get("DISABLE_SIGNALS") == "1":
            return super().ready()

        # Import all signal handlers - they are automatically connected via @receiver decorator
        from . import signals  # noqa: F401

        return super().ready()
