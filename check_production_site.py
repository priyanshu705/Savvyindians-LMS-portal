"""
Check Production Site Status and Data via HTTP requests
"""
import requests
import json
from bs4 import BeautifulSoup

BASE_URL = "https://savvyindians-lms-portal-2.onrender.com"

print("\n" + "="*70)
print("🌐 PRODUCTION SITE CHECK (Render)")
print("="*70)

# 1. Check homepage
print("\n1️⃣ HOMEPAGE:")
try:
    resp = requests.get(f"{BASE_URL}/", timeout=30)
    print(f"   Status: {resp.status_code} ✅" if resp.status_code == 200 else f"   Status: {resp.status_code} ❌")
    print(f"   Size: {len(resp.text):,} bytes")
    print(f"   Title: {resp.text[resp.text.find('<title>')+7:resp.text.find('</title>')][:50]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Check student login
print("\n2️⃣ STUDENT LOGIN PAGE:")
try:
    resp = requests.get(f"{BASE_URL}/accounts/student/login/", timeout=30)
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(f"   Status: {resp.status_code} ✅" if resp.status_code == 200 else f"   Status: {resp.status_code} ❌")
    
    # Check form fields
    form = soup.find('form')
    if form:
        print(f"   ✅ Login form found")
        inputs = form.find_all(['input', 'button'])
        print(f"   📋 Form fields: {len(inputs)}")
        field_names = [inp.get('name') for inp in inputs if inp.get('name')]
        print(f"   🔑 Field names: {', '.join(field_names[:5])}")
    
    # Check modern theme
    if 'form-modern' in resp.text:
        print(f"   ✅ Modern theme CSS loaded")
    if 'savvyindians-logo.png' in resp.text:
        print(f"   ✅ Logo reference found")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Check student registration
print("\n3️⃣ STUDENT REGISTRATION PAGE:")
try:
    resp = requests.get(f"{BASE_URL}/accounts/student/register/", timeout=30)
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(f"   Status: {resp.status_code} ✅" if resp.status_code == 200 else f"   Status: {resp.status_code} ❌")
    
    # Check form fields
    form = soup.find('form')
    if form:
        print(f"   ✅ Registration form found")
        
        # Check specific fields
        fields_to_check = ['first_name', 'last_name', 'email', 'phone', 'city', 'level', 'program', 'password1', 'password2', 'terms_accepted']
        found_fields = []
        for field in fields_to_check:
            if soup.find(['input', 'select', 'textarea'], {'name': field}):
                found_fields.append(field)
        
        print(f"   📋 Required fields found: {len(found_fields)}/{len(fields_to_check)}")
        print(f"   ✅ Fields: {', '.join(found_fields)}")
        
        # Check program dropdown
        program_select = soup.find('select', {'name': 'program'})
        if program_select:
            options = program_select.find_all('option')
            print(f"   🎓 Program options: {len(options)}")
            if len(options) > 1:
                print(f"   📚 Programs available:")
                for opt in options[1:6]:  # Skip first (blank) and show max 5
                    print(f"      • {opt.text.strip()}")
            else:
                print(f"   ⚠️  No programs in dropdown!")
        
        # Check level dropdown
        level_select = soup.find('select', {'name': 'level'})
        if level_select:
            options = level_select.find_all('option')
            print(f"   📊 Level options: {len(options)}")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Check admin panel
print("\n4️⃣ ADMIN PANEL:")
try:
    resp = requests.get(f"{BASE_URL}/admin/", timeout=30)
    print(f"   Status: {resp.status_code} ✅" if resp.status_code == 200 else f"   Status: {resp.status_code} ❌")
    
    if 'id_username' in resp.text and 'id_password' in resp.text:
        print(f"   ✅ Admin login page accessible")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Check static files
print("\n5️⃣ STATIC FILES:")
try:
    # Check modern theme CSS
    resp = requests.get(f"{BASE_URL}/static/css/modern-theme.css", timeout=30)
    if resp.status_code == 200:
        print(f"   ✅ modern-theme.css: {len(resp.text):,} bytes")
    else:
        print(f"   ❌ modern-theme.css: {resp.status_code}")
    
    # Check logo
    resp2 = requests.get(f"{BASE_URL}/static/img/savvyindians-logo.png", timeout=30)
    if resp2.status_code == 200:
        print(f"   ✅ Logo: {len(resp2.content):,} bytes")
    else:
        print(f"   ⚠️  Logo: {resp2.status_code}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ Production site check complete!")
print("\n💡 TO CHECK DATABASE DATA:")
print("   1. Go to: https://savvyindians-lms-portal-2.onrender.com/admin/")
print("   2. Login with admin credentials")
print("   3. Check: course/programs, accounts/users")
print("="*70 + "\n")
