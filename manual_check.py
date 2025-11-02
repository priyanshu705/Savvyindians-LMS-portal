import time
print(' Manual Browser Check - Register a user and keep browser open')
print('Then we will check if user exists in database')
print('')
print('Steps:')
print('1. Browser will open registration page')
print('2. Fill form manually or wait for auto-fill')
print('3. After successful registration, keep window open')
print('4. We will check database')
print('')
input('Press ENTER to start...')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import random
import string

suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f'manualcheck_{suffix}@test.com'
test_password = 'ManualCheck@2024'
test_phone = f'98765{random.randint(10000, 99999)}'

print(f'\n Test Credentials:')
print(f'Email: {test_email}')
print(f'Password: {test_password}')
print(f'Phone: {test_phone}')

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/register/')
    time.sleep(3)
    
    # Auto-fill
    driver.find_element(By.ID, 'id_first_name').send_keys('Manual')
    driver.find_element(By.ID, 'id_last_name').send_keys('Check')
    driver.find_element(By.ID, 'id_email').send_keys(test_email)
    driver.find_element(By.ID, 'id_phone').send_keys(test_phone)
    driver.find_element(By.ID, 'id_city').send_keys('Test City')
    
    Select(driver.find_element(By.ID, 'id_level')).select_by_value('Beginner')
    time.sleep(2)
    
    program_select = Select(driver.find_element(By.ID, 'id_program'))
    if len(program_select.options) > 0:
        program_select.select_by_index(0)
    
    driver.find_element(By.ID, 'id_password1').send_keys(test_password)
    driver.find_element(By.ID, 'id_password2').send_keys(test_password)
    
    checkbox = driver.find_element(By.ID, 'id_terms_accepted')
    driver.execute_script('arguments[0].click();', checkbox)
    
    print('\n Form filled! Now submit manually or press ENTER to auto-submit...')
    input()
    
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print(' Submitted! Waiting 10 seconds...')
    time.sleep(10)
    
    print(f'\n Current URL: {driver.current_url}')
    
    print('\n Keeping browser open for 30 seconds...')
    print('Check the page and see if registration succeeded.')
    time.sleep(30)

finally:
    driver.quit()

print(f'\n Test email was: {test_email}')
print(' Browser closed')
