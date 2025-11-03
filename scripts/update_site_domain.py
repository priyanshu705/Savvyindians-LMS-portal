#!/usr/bin/env python
"""
Update Django Site domain for password reset emails
Run this in Render Shell after deployment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.sites.models import Site

# Get or create the default site
site = Site.objects.get_or_create(pk=1)[0]

# Update with production domain
site.domain = 'savvyindians-lms-portal-2.onrender.com'
site.name = 'SavvyIndians LMS'
site.save()

print(f"✅ Site updated: {site.domain} ({site.name})")
