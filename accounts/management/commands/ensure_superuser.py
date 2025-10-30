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
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'SavvyIndians')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'gy068644@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Savvy@2024#Admin')
        
        self.stdout.write(self.style.SUCCESS(f'🔍 Checking for superuser: {username}'))
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            existing_admin = User.objects.filter(is_superuser=True).first()
            self.stdout.write(
                self.style.WARNING(
                    f'✅ Superuser already exists: {existing_admin.username}'
                )
            )
            
            # Update password if it's the admin user we're trying to create
            if existing_admin.username == username:
                existing_admin.set_password(password)
                existing_admin.email = email
                existing_admin.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'🔄 Updated password for existing superuser: {username}'
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
