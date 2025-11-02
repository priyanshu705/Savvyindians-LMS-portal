"""Quick test to see login error message"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://savvyindians-lms-portal-2.onrender.com/admin/login/')
time.sleep(3)

# Enter credentials
driver.find_element(By.ID, 'id_username').send_keys('SavvyIndians')
driver.find_element(By.ID, 'id_password').send_keys('Savvy@2024#Admin')

# Click login
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
time.sleep(5)

# Check for error message
try:
    error_list = driver.find_element(By.CLASS_NAME, 'errorlist')
    print(f"❌ LOGIN ERROR: {error_list.text}")
except:
    print("✅ No error message found (might have logged in successfully)")

print(f"🔗 Current URL: {driver.current_url}")
print(f"📄 Page Title: {driver.title}")

# Check if we're on admin dashboard
if "/admin/" in driver.current_url and "/login/" not in driver.current_url:
    print("✅ Successfully logged in!")
else:
    print("❌ Still on login page - login failed")

driver.save_screenshot("quick_login_test.png")
print("📸 Screenshot saved: quick_login_test.png")

time.sleep(3)
driver.quit()
