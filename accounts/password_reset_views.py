"""
Custom password reset views to fix domain issue
Overrides Django's default to use request domain instead of Sites framework
"""
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom form that overrides email context to use request domain
    """
    
    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None, from_email=None,
             request=None, html_email_template_name=None, extra_email_context=None):
        """
        Override save to inject correct domain, protocol, and FROM email from request
        """
        # Get domain and protocol from request instead of Sites framework
        if request:
            domain_override = request.get_host()
            use_https = request.is_secure()
        
        # Use the configured DEFAULT_FROM_EMAIL (which is gy068644@gmail.com in production)
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        
        # Add custom email context
        if extra_email_context is None:
            extra_email_context = {}
        
        extra_email_context.update({
            'site_name': 'SavvyIndians LMS',
        })
        
        return super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context
        )


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view that uses the actual request domain
    instead of the Sites framework domain
    """
    form_class = CustomPasswordResetForm
