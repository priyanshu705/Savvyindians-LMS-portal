import logging

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import BEGINNER, Student, User
from .utils import (
    generate_lecturer_credentials,
    generate_student_credentials,
    send_new_account_email,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def post_save_account_receiver(sender, instance=None, created=False, *args, **kwargs):
    """
    Send email notification for manually created accounts (NOT for form-based registrations)
    """
    # Skip if this is an OAuth user or if the user registered via form (has password already set)
    if (
        created
        and not hasattr(instance, "_oauth_created")
        and not hasattr(instance, "_form_registration")
    ):
        if instance.is_student:
            username, password = generate_student_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            # Send email with the generated credentials
            send_new_account_email(instance, password)

        if instance.is_lecturer:
            username, password = generate_lecturer_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            # Send email with the generated credentials
            send_new_account_email(instance, password)


@receiver(user_signed_up)
def oauth_user_signed_up(sender, request, user, **kwargs):
    """
    Handle OAuth user signup - automatically create student profile
    """
    logger.info(f"OAuth user signed up: {user.email}")

    # Mark user as OAuth created to avoid duplicate processing
    user._oauth_created = True

    # Set user as student by default for OAuth signups
    user.is_student = True
    user.is_active = True

    # Generate student ID if not already set
    if not user.username or user.username.startswith("oauth_"):
        username, _ = generate_student_credentials()
        user.username = username

    user.save()

    # Create student profile if it doesn't exist
    if not hasattr(user, "student"):
        try:
            student = Student.objects.create(
                student=user,
                level=BEGINNER,  # Default level for new bootcamp participants
            )
            logger.info(f"Created student profile for OAuth user: {user.email}")
        except Exception as e:
            logger.error(f"Failed to create student profile for {user.email}: {str(e)}")


@receiver(social_account_added)
def social_account_added_handler(sender, request, sociallogin, **kwargs):
    """
    Handle when a social account is added to an existing user
    """
    user = sociallogin.user
    provider = sociallogin.account.provider

    logger.info(f"Social account added: {provider} for user {user.email}")

    # Ensure user has student profile if they don't already
    if not hasattr(user, "student") and not user.is_lecturer and not user.is_superuser:
        user.is_student = True
        user.save()

        try:
            student = Student.objects.create(
                student=user,
                level=BEGINNER,
            )
            logger.info(f"Created student profile for existing user: {user.email}")
        except Exception as e:
            logger.error(
                f"Failed to create student profile for existing user {user.email}: {str(e)}"
            )


@receiver(user_logged_in)
def oauth_user_logged_in(sender, request, user, **kwargs):
    """
    Handle OAuth user login - ensure proper student profile exists
    """
    # Check if this is an OAuth login
    if hasattr(request, "session") and request.session.get("socialaccount_state"):
        logger.info(f"OAuth user logged in: {user.email}")

        # Ensure user has proper student access
        if user.is_student and not hasattr(user, "student"):
            try:
                Student.objects.create(
                    student=user,
                    level=BEGINNER,
                )
                logger.info(
                    f"Created missing student profile for OAuth user: {user.email}"
                )

                # Add success message
                messages.success(
                    request,
                    _("Welcome! Your student profile has been set up successfully."),
                )
            except Exception as e:
                logger.error(
                    f"Failed to create student profile during login for {user.email}: {str(e)}"
                )
                messages.warning(
                    request,
                    _(
                        "Welcome! Please complete your profile setup in your account settings."
                    ),
                )
