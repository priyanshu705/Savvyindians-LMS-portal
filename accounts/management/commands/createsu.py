"""
Django management command to create a superuser if none exists.
This is used during AWS deployment to automatically create an admin account.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return
        
        try:
            User.objects.create_superuser(
                username='admin',
                email='admin@savvyindians.com',
                password='Admin@123Change',  # Change this after first login!
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            self.stdout.write(self.style.WARNING('⚠️  Default password: Admin@123Change'))
            self.stdout.write(self.style.WARNING('⚠️  CHANGE THIS PASSWORD IMMEDIATELY!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
