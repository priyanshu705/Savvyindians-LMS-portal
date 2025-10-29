"""
Management command to create superuser automatically
Usage: python manage.py ensure_superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        # Get credentials from environment or use defaults
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@savvyindians.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin@SavvyIndians2025!')
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            existing_admin = User.objects.filter(is_superuser=True).first()
            self.stdout.write(
                self.style.WARNING(
                    f'✅ Superuser already exists: {existing_admin.username}'
                )
            )
            return
        
        # Check if user with this username exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Upgraded existing user "{username}" to superuser'
                )
            )
        else:
            # Create new superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser created successfully: {username}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'   Email: {email}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '   ⚠️  Remember to change the default password!'
                )
            )
