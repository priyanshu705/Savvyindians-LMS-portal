from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string

# Generate unique test data
suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f'livetest_{suffix}@test.com'
test_password = 'LiveTest@2024#Pass'
test_phone = f'98765{random.randint(10000, 99999)}'

print('='*60)
print(' FRESH REGISTRATION + LOGIN TEST')
print('='*60)
print(f' Email: {test_email}')
print(f' Phone: {test_phone}')
print('='*60)

driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Step 1: Register
    reg_url = 'https://savvyindians-lms-portal-2.onrender.com/accounts/student/register/'
    print(f'\n REGISTRATION')
    driver.get(reg_url)
    time.sleep(3)
    
    # Fill form
    driver.find_element(By.ID, 'id_first_name').send_keys('Live')
    driver.find_element(By.ID, 'id_last_name').send_keys('Test')
    driver.find_element(By.ID, 'id_email').send_keys(test_email)
    driver.find_element(By.ID, 'id_phone').send_keys(test_phone)
    driver.find_element(By.ID, 'id_city').send_keys('Test City')
    
    from selenium.webdriver.support.ui import Select
    Select(driver.find_element(By.ID, 'id_level')).select_by_value('Beginner')
    time.sleep(2)
    
    program_select = Select(driver.find_element(By.ID, 'id_program'))
    if len(program_select.options) > 0:
        program_select.select_by_index(0)
    
    driver.find_element(By.ID, 'id_password1').send_keys(test_password)
    driver.find_element(By.ID, 'id_password2').send_keys(test_password)
    
    # Use JavaScript to click checkbox
    checkbox = driver.find_element(By.ID, 'id_terms_accepted')
    driver.execute_script('arguments[0].click();', checkbox)
    time.sleep(1)
    
    # Submit
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(5)
    
    current_url = driver.current_url
    print(f' After registration: {current_url}')
    
    if 'login' not in current_url.lower():
        print(' Auto-logged in after registration')
    
    # Logout
    print(f'\n LOGOUT')
    driver.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/logout/')
    time.sleep(3)
    
    # Login
    print(f'\n MANUAL LOGIN')
    driver.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/login/')
    time.sleep(2)
    
    driver.find_element(By.ID, 'id_username').send_keys(test_email)
    driver.find_element(By.ID, 'id_password').send_keys(test_password)
    time.sleep(1)
    
    driver.find_element(By.ID, 'signin-btn').click()
    time.sleep(5)
    
    login_result_url = driver.current_url
    print(f' After login: {login_result_url}')
    
    if 'login' not in login_result_url.lower():
        print('\n SUCCESS! Login worked!')
        driver.save_screenshot('success.png')
    else:
        print('\n FAILED! Still on login page')
        try:
            error = driver.find_element(By.CSS_SELECTOR, '.alert-danger, .invalid-feedback')
            print(f'Error: {error.text}')
        except:
            pass
        driver.save_screenshot('failed.png')
    
    time.sleep(5)

except Exception as e:
    print(f'\n Error: {str(e)}')
finally:
    driver.quit()

print(f'\n Test User: {test_email} / {test_password}')
