# Video DRM Protection System

## Overview
The SavvyIndians LMS now includes a comprehensive Digital Rights Management (DRM) protection system to prevent unauthorized video sharing, screen recording, and content piracy.

## 🔒 Protection Features

### 1. **Screen Recording Detection & Blocking**
- Detects screen capture API usage attempts
- Monitors for recording software activity
- Pauses video when recording is detected
- Displays warning message to users
- Logs all recording attempts with user details

### 2. **Right-Click Protection**
- Context menu completely disabled on video player
- Prevents "Save video as..." options
- Blocks "Inspect Element" from right-click
- Shows alert message on violation attempts

### 3. **Keyboard Shortcuts Blocked**
The following keyboard shortcuts are disabled:
- **PrintScreen** - Screenshot capture blocked
- **F12** - DevTools access blocked
- **Ctrl+Shift+I** - Inspect Element blocked
- **Ctrl+Shift+J** - Console access blocked
- **Ctrl+Shift+C** - Element selector blocked
- **Ctrl+U** - View source blocked
- **Ctrl+S** - Save page blocked
- **Ctrl+Shift+K** - Firefox console blocked
- **Meta+Option+I** - Mac DevTools blocked

### 4. **Developer Tools Detection**
- Real-time detection of open DevTools
- Video automatically pauses when DevTools opens
- Blur effect applied to video container
- Warning banner displayed
- All attempts logged

### 5. **User Watermark Overlay**
- Visible watermark showing user email and ID
- Position randomly changes every 30 seconds (6 positions)
- Watermark cannot be removed or hidden
- Transparent background (60% opacity)
- Always on top (z-index: 9999)

**Watermark Format:**
```
user@email.com • ID: 123
```

### 6. **Video Download Protection**
- `controlsList="nodownload"` attribute on HTML5 video
- Drag-and-drop disabled
- Copy operation blocked
- Video source tampering monitored
- Opening video in new tab prevented

### 7. **Picture-in-Picture Disabled**
- `disablePictureInPicture` attribute set
- Prevents floating video windows
- Users cannot watch video while switching tabs

### 8. **Text Selection Disabled**
- User cannot select text/elements in video container
- Prevents copying video URL or metadata
- CSS `user-select: none` applied

### 9. **Violation Logging System**
All protection violations are logged with:
- Timestamp
- User information (username, email, ID)
- Video details
- Violation type
- IP address
- User agent (browser/OS)
- Screen resolution
- Platform details
- Page URL

## 📊 Admin Dashboard

### Viewing DRM Logs
Administrators can view all protection events in Django Admin:

**Path:** `/admin/course/videodrmlog/`

**Log Types:**
- ✅ **Access** - Normal video access (green)
- ⚠️ **Violation** - Protection breach attempt (red)

**Violation Types:**
- Screen Recording Detected
- Developer Tools Opened
- Right-Click Attempt
- Keyboard Shortcut Blocked
- Video Source Tampering
- Download Attempt
- Inspect Element Attempt
- Other Violation

### Admin Features
- Filter logs by type, violation type, and date
- Search by user, video, IP address
- Read-only logs (cannot be edited/deleted)
- Color-coded log type display
- Automatic activity log creation for violations

## 🎬 Video Player Features

### For HTML5 Videos (Uploaded Files)
```html
<video 
    controls 
    controlsList="nodownload"
    disablePictureInPicture
    preload="metadata"
    id="protectedVideo">
</video>
```

### For YouTube Videos
- Watermark overlay still applied
- DevTools detection active
- Keyboard shortcuts blocked
- Note: YouTube's native controls cannot be fully restricted

## 🔧 Technical Implementation

### JavaScript Class: `DRMProtectionSystem`
Located in: `templates/upload/video_single.html`

**Methods:**
1. `disableRightClick()` - Blocks context menu
2. `disableKeyboardShortcuts()` - Intercepts key events
3. `detectDevTools()` - Monitors window size changes
4. `detectScreenRecording()` - Checks screen capture API
5. `protectVideo()` - Adds video element protection
6. `disableTextSelection()` - Prevents selection
7. `preventInspect()` - Blocks inspect attempts
8. `randomizeWatermark()` - Changes watermark position
9. `logAccess()` / `logViolation()` - Sends logs to server

### Django Model: `VideoDRMLog`
Located in: `course/models.py`

**Fields:**
- `video` - ForeignKey to UploadVideo
- `user` - ForeignKey to User (nullable for anonymous)
- `log_type` - Choice: 'access' or 'violation'
- `violation_type` - Type of violation (if applicable)
- `ip_address` - Client IP address
- `user_agent` - Browser/OS information
- `screen_resolution` - Screen dimensions
- `platform` - Operating system platform
- `url` - Page URL where event occurred
- `timestamp` - When event occurred

### API Endpoint
**URL:** `/course/api/video/drm-log/`
**Method:** POST
**Authentication:** Not required (captures anonymous attempts)

**Request Format:**
```javascript
{
    log_type: "violation",
    data: JSON.stringify({
        video_id: 123,
        user_id: "456",
        violation_type: "DevTools opened",
        timestamp: "2024-01-15T10:30:00.000Z",
        user_agent: "Mozilla/5.0...",
        screen_resolution: "1920x1080",
        platform: "Win32",
        url: "https://example.com/video"
    })
}
```

## 🚀 Deployment Notes

### Database Migration
Run the following command after deploying:
```bash
python manage.py migrate course
```

This will create the `course_videodrmlog` table.

### Render Deployment
The migration will run automatically via `render.yaml` build command:
```yaml
buildCommand: pip install -r requirements.txt && python manage.py migrate
```

### Environment Variables
No additional environment variables required for DRM system.

## 📱 Browser Compatibility

### Fully Supported:
- ✅ Chrome/Edge (Chromium) - All features
- ✅ Firefox - All features
- ✅ Safari - Most features

### Limitations:
- Safari has limited DevTools detection
- Mobile browsers may allow native screen recording via OS
- iOS does not support `controlsList="nodownload"`

## ⚠️ Important Notes

### What DRM Protection Can Do:
- ✅ Prevent casual users from downloading videos
- ✅ Deter screen recording attempts
- ✅ Block DevTools and inspect element
- ✅ Log all violation attempts
- ✅ Display user watermark on video
- ✅ Prevent right-click download options

### What DRM Protection Cannot Do:
- ❌ Cannot stop determined hackers with advanced tools
- ❌ Cannot prevent external camera recording
- ❌ Cannot stop OS-level screen recorders (may detect but not block)
- ❌ Cannot prevent video playback on rooted/jailbroken devices

### Best Practices:
1. **Use HTTPS** - Always serve videos over secure connections
2. **Token-based URLs** - Consider adding expiring tokens to video URLs
3. **HLS Encryption** - For premium content, use HLS with encryption keys
4. **Legal Notice** - Display terms of service warning against piracy
5. **Monitor Logs** - Regularly review DRM violation logs
6. **Take Action** - Suspend accounts with repeated violations

## 🔐 Additional Security Recommendations

### 1. Video URL Obfuscation
Add signed URLs that expire:
```python
# In models.py
def get_signed_video_url(self, expires_in=3600):
    """Generate time-limited signed URL for video"""
    import time
    import hashlib
    
    timestamp = int(time.time()) + expires_in
    token = hashlib.sha256(
        f"{self.id}{timestamp}{settings.SECRET_KEY}".encode()
    ).hexdigest()
    
    return f"{self.video.url}?token={token}&expires={timestamp}"
```

### 2. Rate Limiting
Implement rate limiting on video endpoints:
```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60)  # Cache for 1 minute
def handle_video_single(request, course_slug, video_slug):
    # Your existing code
    pass
```

### 3. IP-Based Access Control
Track simultaneous streams per user:
```python
# Maximum concurrent streams per user
MAX_CONCURRENT_STREAMS = 2

def check_concurrent_streams(user, video):
    cache_key = f"video_stream_{user.id}"
    active_streams = cache.get(cache_key, [])
    
    if len(active_streams) >= MAX_CONCURRENT_STREAMS:
        return False  # Deny access
    
    active_streams.append({
        'video_id': video.id,
        'started_at': timezone.now()
    })
    cache.set(cache_key, active_streams, timeout=7200)  # 2 hours
    return True
```

### 4. Geofencing (Optional)
Restrict video access by country:
```python
import geoip2.database

def check_country_access(ip_address, allowed_countries=['IN', 'US']):
    reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
    response = reader.country(ip_address)
    return response.country.iso_code in allowed_countries
```

## 📈 Monitoring & Analytics

### Key Metrics to Track:
1. **Total Access Logs** - Normal video views
2. **Violation Rate** - Percentage of attempts vs. views
3. **Top Violators** - Users with most violations
4. **Violation Types** - Most common breach attempts
5. **Geographic Distribution** - Where violations occur
6. **Time Patterns** - When violations peak

### Sample Admin Query:
```python
from course.models import VideoDRMLog
from django.db.models import Count

# Get violation statistics
stats = VideoDRMLog.objects.filter(
    log_type='violation'
).values('violation_type').annotate(
    count=Count('id')
).order_by('-count')

# Top violators
top_violators = VideoDRMLog.objects.filter(
    log_type='violation'
).values('user__username').annotate(
    violation_count=Count('id')
).order_by('-violation_count')[:10]
```

## 🎯 User Experience

### For Students:
- Videos play normally with standard controls
- No noticeable performance impact
- Watermark is subtle but visible
- Warning messages only on violation attempts

### For Lecturers:
- Upload videos as usual (YouTube URL or file)
- DRM protection applied automatically
- No additional configuration required
- Can view violation logs in admin

### For Administrators:
- Full visibility into access patterns
- Real-time violation tracking
- Easy-to-use admin interface
- Export logs for reporting

## 📝 Changelog

### Version 1.0 (Initial Release)
**Date:** January 2024

**Added:**
- Screen recording detection system
- Right-click and keyboard shortcut blocking
- DevTools detection with video pause
- User watermark overlay with random positioning
- Video download protection
- Picture-in-Picture disable
- Text selection disable
- VideoDRMLog model and admin interface
- DRM logging API endpoint
- Activity log integration

**Database Changes:**
- Created `course_videodrmlog` table with indexes
- Added foreign keys to User and UploadVideo

**Files Modified:**
- `templates/upload/video_single.html` - Added DRM JavaScript
- `course/models.py` - Added VideoDRMLog model
- `course/views.py` - Added log_drm_event view
- `course/urls.py` - Added API endpoint
- `course/admin.py` - Added VideoDRMLog admin
- `course/migrations/0009_videodrmlog.py` - Database migration

## 🆘 Troubleshooting

### Issue: Videos not loading
**Solution:** Check if JavaScript is enabled in browser

### Issue: Watermark not appearing
**Solution:** Ensure user is authenticated and JavaScript is running

### Issue: DRM logs not being created
**Solution:** 
1. Check database connection
2. Verify API endpoint is accessible: `/course/api/video/drm-log/`
3. Check browser console for errors
4. Ensure migrations are applied: `python manage.py migrate`

### Issue: DevTools detection not working
**Solution:** Detection works best in Chrome/Firefox. Some browsers may not trigger all detection methods.

### Issue: False positive violations
**Solution:** Some browser extensions may trigger DevTools detection. Consider adding a grace period or confirmation dialog.

## 📞 Support

For issues or questions regarding the DRM protection system:
- Check logs in Django Admin
- Review browser console for JavaScript errors
- Contact: gy068644@gmail.com

---

**Last Updated:** January 2024  
**Author:** SavvyIndians LMS Development Team  
**License:** Proprietary - All Rights Reserved
