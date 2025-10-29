"""
Quick Static Files Checker - Verify static file loading
"""

import requests

BASE_URL = "https://savvyindians-lms-portal-2.onrender.com"

CRITICAL_STATIC_FILES = [
    "/static/vendor/fontawesome-6.5.1/css/all.min.css",
    "/static/vendor/bootstrap-5.3.2/css/bootstrap.min.css",
    "/static/css/style.min.css",
    "/static/css/savvyindians-theme.css",
    "/static/js/main.js",
    "/static/img/savvyindians-logo.png",
]

print("\n" + "="*80)
print("🔍 STATIC FILES LOADING CHECK")
print("="*80 + "\n")

for file_path in CRITICAL_STATIC_FILES:
    url = BASE_URL + file_path
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'unknown')
            print(f"✅ {file_path}")
            print(f"   Status: {response.status_code} | Type: {content_type}")
        elif response.status_code == 404:
            print(f"❌ {file_path}")
            print(f"   Status: 404 NOT FOUND")
        elif response.status_code == 500:
            print(f"⚠️  {file_path}")
            print(f"   Status: 500 INTERNAL SERVER ERROR")
        else:
            print(f"⚠️  {file_path}")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ {file_path}")
        print(f"   Error: {str(e)}")
    print()

print("="*80)
