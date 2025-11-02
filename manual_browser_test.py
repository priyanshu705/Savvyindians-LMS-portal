"""
Simple Manual Browser Test - Opens browser and waits
This lets you see what's actually happening on the page
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print("🌐 Opening browser to admin login page...")
print("URL: https://savvyindians-lms-portal-2.onrender.com/admin/login/")
print("\n⏸️  Browser will stay open for 30 seconds - CHECK WHAT YOU SEE!")
print("=" * 80)

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Navigate to admin login
    driver.get("https://savvyindians-lms-portal-2.onrender.com/admin/login/")
    time.sleep(5)
    
    # Print debug info
    print(f"\n✅ Page loaded!")
    print(f"📄 Page Title: {driver.title}")
    print(f"🔗 Current URL: {driver.current_url}")
    print(f"📏 Page Length: {len(driver.page_source)} characters")
    
    # Check if it's an error page
    page_text = driver.page_source.lower()
    if "error" in page_text[:500]:
        print(f"\n⚠️  'Error' found in page!")
    if "500" in driver.title or "error" in driver.title.lower():
        print(f"\n🔴 Error page detected in title!")
    
    # Try to find common elements
    print("\n🔍 Looking for page elements...")
    try:
        h1 = driver.find_element(By.TAG_NAME, "h1")
        print(f"   H1 found: {h1.text[:100]}")
    except:
        print("   ❌ No H1 found")
    
    try:
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"   Forms found: {len(forms)}")
    except:
        print("   ❌ No forms found")
    
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"   Input fields found: {len(inputs)}")
        for inp in inputs[:5]:
            print(f"      - Type: {inp.get_attribute('type')}, Name: {inp.get_attribute('name')}, ID: {inp.get_attribute('id')}")
    except:
        print("   ❌ No inputs found")
    
    # Save screenshot
    screenshot_name = f"manual_test_{time.strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(screenshot_name)
    print(f"\n📸 Screenshot saved: {screenshot_name}")
    
    print("\n" + "=" * 80)
    print("⏳ Keeping browser open for 30 seconds...")
    print("   👀 LOOK AT THE BROWSER - What do you see?")
    print("   - Is it the admin login page?")
    print("   - Is it an error page?")
    print("   - Is it the homepage?")
    print("=" * 80)
    
    time.sleep(30)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
finally:
    print("\n🔄 Closing browser...")
    driver.quit()
    print("✅ Done!")
