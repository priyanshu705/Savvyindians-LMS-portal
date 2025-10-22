import datetime
import os
import random
import string
import re
from urllib.parse import urlparse, parse_qs

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def extract_youtube_video_id(url):
    """
    Extract YouTube video ID from various YouTube URL formats
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID  
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    """
    if not url:
        return None
    
    # YouTube URL patterns
    youtube_patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in youtube_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def get_youtube_embed_url(video_id, autoplay=False, controls=True, modestbranding=True):
    """
    Generate YouTube embed URL with security and customization options
    
    Parameters:
    - video_id: YouTube video ID
    - autoplay: Whether to autoplay video (default: False)
    - controls: Show video controls (default: True) 
    - modestbranding: Use modest YouTube branding (default: True)
    """
    if not video_id:
        return None
    
    params = []
    
    # Security and customization parameters
    if not autoplay:
        params.append("autoplay=0")
    
    if not controls:
        params.append("controls=0")
    
    if modestbranding:
        params.append("modestbranding=1")
    
    # Additional security parameters
    params.extend([
        "rel=0",          # Don't show related videos
        "showinfo=0",     # Don't show video title and uploader
        "fs=0",           # Disable fullscreen button
        "disablekb=1",    # Disable keyboard controls
        "iv_load_policy=3" # Hide video annotations
    ])
    
    params_string = "&".join(params)
    embed_url = f"https://www.youtube.com/embed/{video_id}?{params_string}"
    
    return embed_url


def validate_youtube_url(url):
    """
    Validate if the provided URL is a valid YouTube URL
    Returns: (is_valid: bool, video_id: str or None, error_message: str or None)
    """
    if not url:
        return False, None, "URL is required"
    
    video_id = extract_youtube_video_id(url)
    
    if not video_id:
        return False, None, "Invalid YouTube URL format"
    
    # Basic video ID validation (11 characters, alphanumeric + _ -)
    if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
        return False, None, "Invalid YouTube video ID format"
    
    return True, video_id, None


def get_youtube_thumbnail_url(video_id, quality='hqdefault'):
    """
    Get YouTube thumbnail URL for a video
    Quality options: default, hqdefault, mqdefault, sddefault, maxresdefault
    """
    if not video_id:
        return None
    
    return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
