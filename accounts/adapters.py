from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Student
from .utils import generate_student_credentials
import logging

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for handling OAuth social account creation and linking
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        user = sociallogin.user
        
        # If user exists but doesn't have a social account, link them
        if user.pk:
            return
            
        # Check if a user with the same email already exists
        if user.email:
            try:
                existing_user = user.__class__.objects.get(email=user.email)
                # Connect the social account to the existing user
                sociallogin.user = existing_user
                sociallogin.connect(request, existing_user)
                logger.info(f"Connected social account to existing user: {existing_user.email}")
            except user.__class__.DoesNotExist:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user.
        """
        user = sociallogin.user
        user.set_unusable_password()
        
        # Set basic user information from social account
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            
            # Set user fields from Google data
            user_field(user, 'email', extra_data.get('email', ''))
            user_field(user, 'first_name', extra_data.get('given_name', ''))
            user_field(user, 'last_name', extra_data.get('family_name', ''))
            
            # Set picture URL if available
            if extra_data.get('picture'):
                # You might want to download and save the image locally
                # For now, we'll just store the URL
                pass
        
        # Mark as student by default
        user.is_student = True
        user.is_active = True
        
        # Generate student credentials
        if not user.username:
            username, _ = generate_student_credentials()
            user.username = username
            
        # Save the user
        user.save()
        
        # Create student profile
        self._create_student_profile(user)
        
        # Add welcome message
        messages.success(
            request,
            _("Welcome to our Learning Management System! Your student account has been created successfully.")
        )
        
        return user
    
    def _create_student_profile(self, user):
        """
        Create a student profile for OAuth users
        """
        try:
            if not hasattr(user, 'student'):
                student = Student.objects.create(
                    student=user,
                    id_number=user.username,
                    level="100",  # Default level for new students
                )
                logger.info(f"Created student profile for OAuth user: {user.email}")
        except Exception as e:
            logger.error(f"Failed to create student profile for {user.email}: {str(e)}")
    
    def populate_user(self, request, sociallogin, data):
        """
        Populates user information from social provider data
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Additional processing for Google OAuth
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            
            # Set additional fields if available
            if extra_data.get('locale'):
                # Set user language preference if supported
                pass
                
            if extra_data.get('verified_email'):
                # Mark email as verified
                user.email_verified = True
        
        return user
    
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Handle authentication errors gracefully
        """
        logger.error(f"OAuth authentication error for provider {provider_id}: {error}")
        
        # Add user-friendly error message
        messages.error(
            request,
            _("There was an error connecting to your Google account. Please try again or contact support if the problem persists.")
        )
        
        return super().authentication_error(request, provider_id, error, exception, extra_context)