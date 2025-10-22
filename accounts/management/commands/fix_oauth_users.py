from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from accounts.models import Student, BACHELOR_DEGREE
from accounts.utils import generate_student_credentials
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = 'Fix OAuth users without proper student profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fix users even if they already have some profile',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS('Starting OAuth user profile fix...')
        )
        
        # Find OAuth users
        oauth_users = User.objects.filter(
            socialaccount__isnull=False
        ).distinct()
        
        self.stdout.write(f'Found {oauth_users.count()} OAuth users')
        
        fixed_count = 0
        skipped_count = 0
        error_count = 0
        
        for user in oauth_users:
            try:
                # Check if user needs fixing
                needs_fixing = False
                issues = []
                
                # Check if user is marked as student
                if not user.is_student and not user.is_lecturer and not user.is_superuser:
                    needs_fixing = True
                    issues.append('not marked as student')
                
                # Check if user has student profile
                if user.is_student and not hasattr(user, 'student'):
                    needs_fixing = True
                    issues.append('missing student profile')
                
                # Check if username is properly set
                if not user.username or user.username.startswith('oauth_'):
                    needs_fixing = True
                    issues.append('improper username')
                
                if not needs_fixing and not force:
                    skipped_count += 1
                    continue
                
                self.stdout.write(
                    f'Fixing user {user.email} - Issues: {", ".join(issues)}'
                )
                
                if not dry_run:
                    # Fix user flags
                    if not user.is_student and not user.is_lecturer and not user.is_superuser:
                        user.is_student = True
                        user.is_active = True
                    
                    # Fix username
                    if not user.username or user.username.startswith('oauth_'):
                        username, _ = generate_student_credentials()
                        user.username = username
                    
                    user.save()
                    
                    # Create student profile if needed
                    if user.is_student and not hasattr(user, 'student'):
                        Student.objects.create(
                            student=user,
                            level=BACHELOR_DEGREE,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'Created student profile for {user.email}')
                        )
                
                fixed_count += 1
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'Error fixing user {user.email}: {str(e)}')
                )
                logger.error(f'Error fixing OAuth user {user.email}: {str(e)}')
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== SUMMARY ==='))
        self.stdout.write(f'Total OAuth users found: {oauth_users.count()}')
        self.stdout.write(f'Users fixed: {fixed_count}')
        self.stdout.write(f'Users skipped: {skipped_count}')
        self.stdout.write(f'Errors encountered: {error_count}')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No changes were made. Run without --dry-run to apply fixes.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('OAuth user profile fix completed!')
            )