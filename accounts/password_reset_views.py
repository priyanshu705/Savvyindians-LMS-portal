"""
Custom password reset views to fix domain issue
Overrides Django's default to use request domain instead of Sites framework
"""
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view that uses the actual request domain
    instead of the Sites framework domain
    """
    
    def get_email_context(self, **kwargs):
        """
        Override to provide correct domain and protocol from request
        """
        context = super().get_email_context(**kwargs)
        
        # Get the actual domain from the request
        request = self.request
        domain = request.get_host()
        
        # Determine protocol (https in production, http in debug)
        protocol = 'https' if request.is_secure() else 'http'
        
        # Override the default context
        context.update({
            'domain': domain,
            'protocol': protocol,
            'site_name': 'SavvyIndians LMS',
        })
        
        return context
