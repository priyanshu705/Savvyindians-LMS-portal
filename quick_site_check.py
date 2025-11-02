"""
Quick test to check if site is up and running
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BASE_URL = "https://savvyindians-lms-portal-2.onrender.com"

print("🔍 Checking if site is up...")

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

try:
    # Check homepage first
    print(f"\n1️⃣ Checking homepage: {BASE_URL}")
    driver.get(BASE_URL)
    time.sleep(5)  # Wait for Render to wake up if needed
    
    print(f"   📄 Title: {driver.title}")
    print(f"   📍 URL: {driver.current_url}")
    driver.save_screenshot('site_check_homepage.png')
    
    # Check registration page
    print(f"\n2️⃣ Checking registration page...")
    driver.get(f"{BASE_URL}/accounts/student/register/")
    time.sleep(5)
    
    print(f"   📄 Title: {driver.title}")
    print(f"   📍 URL: {driver.current_url}")
    driver.save_screenshot('site_check_registration.png')
    
    # Check login page
    print(f"\n3️⃣ Checking login page...")
    driver.get(f"{BASE_URL}/accounts/student/login/")
    time.sleep(5)
    
    print(f"   📄 Title: {driver.title}")
    print(f"   📍 URL: {driver.current_url}")
    driver.save_screenshot('site_check_login.png')
    
    if "loading" in driver.title.lower() or "render" in driver.title.lower():
        print("\n⚠️ Site is loading or in sleep mode. Waiting 30 seconds...")
        time.sleep(30)
        driver.refresh()
        time.sleep(5)
        print(f"   📄 Title after refresh: {driver.title}")
    
    print("\n✅ Site check complete!")
    time.sleep(5)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    driver.save_screenshot('site_check_error.png')
    
finally:
    driver.quit()
    print("\n✓ Browser closed")
