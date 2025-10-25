"""
Admin Dashboard Configuration for SavvyIndians Bootcamp Platform
This file customizes what appears in the admin dashboard
"""

from django.contrib import admin

# Unregister unnecessary models to keep admin clean
# admin.site.unregister(Group)  # Uncomment if you don't need Groups


def customize_admin():
    """
    Customize the admin site for bootcamp-specific needs
    Remove clutter and focus on core bootcamp management
    """

    # Set custom admin site properties
    admin.site.site_header = "SavvyIndians Bootcamp Admin"
    admin.site.site_title = "SavvyIndians Admin Portal"
    admin.site.index_title = "Welcome to SavvyIndians Bootcamp Administration"

    # Optional: Customize admin index page order
    # You can control which apps/models appear first

    print("✅ Admin dashboard customized for bootcamp platform")
