"""
Simple manual test to check student login page and see error messages
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Use an account that was already created
TEST_EMAIL = "teststudent_ljjvpn@test.com"  # From previous test
TEST_PASSWORD = "TestPass@2024#Student"

print("🔍 Testing student login with existing account...")
print(f"Email: {TEST_EMAIL}")

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

try:
    # Go to login page
    driver.get("https://savvyindians-lms-portal-2.onrender.com/accounts/student/login/")
    time.sleep(3)
    
    print(f"\n📄 Page title: {driver.title}")
    
    # Fill login form
    login_field = driver.find_element(By.NAME, "login")
    login_field.send_keys(TEST_EMAIL)
    print(f"✓ Entered email: {TEST_EMAIL}")
    
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(TEST_PASSWORD)
    print("✓ Entered password")
    
    # Take screenshot before clicking
    driver.save_screenshot('manual_test_before_login.png')
    print("📸 Screenshot saved: manual_test_before_login.png")
    
    # Click login button
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    submit_button.click()
    print("✓ Clicked login button")
    
    # Wait and check result
    time.sleep(4)
    
    current_url = driver.current_url
    print(f"\n📍 Current URL: {current_url}")
    print(f"📄 Page title: {driver.title}")
    
    # Check for error messages
    try:
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".alert, .error, .errorlist, .messages li")
        if error_elements:
            print("\n⚠️ Messages/Errors found:")
            for elem in error_elements:
                if elem.is_displayed():
                    print(f"   - {elem.text}")
        else:
            print("\n✓ No error messages found")
    except Exception as e:
        print(f"\n⚠️ Could not check for errors: {e}")
    
    # Take screenshot after login attempt
    driver.save_screenshot('manual_test_after_login.png')
    print("\n📸 Screenshot saved: manual_test_after_login.png")
    
    # Check if logged in
    if "/login" in current_url:
        print("\n❌ Still on login page - Login FAILED")
        
        # Try to get form errors
        try:
            form_errors = driver.find_elements(By.CSS_SELECTOR, ".errorlist li, .help-block, .invalid-feedback")
            if form_errors:
                print("\n🔴 Form errors:")
                for error in form_errors:
                    if error.is_displayed():
                        print(f"   - {error.text}")
        except:
            pass
    else:
        print(f"\n✅ LOGIN SUCCESSFUL! Redirected to: {current_url}")
    
    print("\n⏳ Keeping browser open for 10 seconds to inspect...")
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    driver.save_screenshot('manual_test_error.png')

finally:
    driver.quit()
    print("\n✓ Browser closed")
