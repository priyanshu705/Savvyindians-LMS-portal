"""
Context processors to provide site-wide template variables
"""
from django.conf import settings


def site_info(request):
    """
    Add site domain and name to all templates
    This fixes password reset emails showing wrong domain
    """
    # Get domain from request (works in both dev and production)
    domain = request.get_host()
    
    # Use HTTPS in production
    protocol = 'https' if not settings.DEBUG else 'http'
    
    return {
        'site_name': 'SavvyIndians LMS',
        'site_domain': domain,
        'site_protocol': protocol,
    }
