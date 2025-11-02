from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time, random, string

BASE = 'https://savvyindians-lms-portal-2.onrender.com'

suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL = f'smoke2_{suffix}@test.com'
PASS = 'SmokeTest@2024#Pass'
PHONE = f'98765{random.randint(10000,99999)}'

D = webdriver.Chrome()
D.maximize_window()
W = WebDriverWait(D, 20)

try:
    # Register
    D.get(f'{BASE}/accounts/student/register/')
    W.until(EC.presence_of_element_located((By.ID, 'modern-register-form')))
    W.until(EC.presence_of_element_located((By.ID, 'id_first_name'))).send_keys('Smoke2')
    D.find_element(By.ID, 'id_last_name').send_keys('User')
    D.find_element(By.ID, 'id_email').send_keys(EMAIL)
    D.find_element(By.ID, 'id_phone').send_keys(PHONE)
    D.find_element(By.ID, 'id_city').send_keys('Test City')
    Select(D.find_element(By.ID, 'id_level')).select_by_value('Beginner')
    time.sleep(1)
    Select(D.find_element(By.ID, 'id_program')).select_by_index(0)
    D.find_element(By.ID, 'id_password1').send_keys(PASS)
    D.find_element(By.ID, 'id_password2').send_keys(PASS)
    D.execute_script('arguments[0].click();', D.find_element(By.ID, 'id_terms_accepted'))
    D.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(4)
    print('After register URL:', D.current_url)

    # Go to login directly
    D.get(f'{BASE}/accounts/student/login/')
    W.until(EC.presence_of_element_located((By.ID, 'student-login-modern')))
    W.until(EC.presence_of_element_located((By.ID, 'id_username'))).send_keys(EMAIL)
    D.find_element(By.ID, 'id_password').send_keys(PASS)
    D.find_element(By.ID, 'signin-btn').click()
    time.sleep(4)
    print('After manual login URL:', D.current_url)
    print('Title:', D.title)

    if 'login' in D.current_url:
        print('RESULT: FAIL (still on login)')
        try:
            err = D.find_element(By.CSS_SELECTOR, '.alert-danger, .invalid-feedback')
            print('Error:', err.text)
        except Exception:
            print('No visible error element found')
    else:
        print('RESULT: PASS (redirected)')

finally:
    D.quit()
    print('Done')
