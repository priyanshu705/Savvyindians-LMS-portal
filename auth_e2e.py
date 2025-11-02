from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, random, string

BASE = 'https://savvyindians-lms-portal-2.onrender.com'

suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL = f'e2e_{suffix}@test.com'
PASS = 'E2eTest@2024#Pass'
PHONE = f'98765{random.randint(10000,99999)}'

print('='*60)
print('AUTH E2E: register  auto-login  logout (confirm)  manual login')
print('='*60)
print('Email:', EMAIL)
print('Phone:', PHONE)

D = webdriver.Chrome()
D.maximize_window()
W = WebDriverWait(D, 20)

try:
    # Register
    D.get(f'{BASE}/accounts/student/register/')
    W.until(EC.presence_of_element_located((By.ID, 'modern-register-form')))
    W.until(EC.presence_of_element_located((By.ID, 'id_first_name'))).send_keys('E2E')
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
    D.save_screenshot('e2e_before_submit.png')
    D.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(3)
    print('After register URL:', D.current_url)

    # Logout: visit confirm page then submit POST
    D.get(f'{BASE}/accounts/student/logout/')
    W.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'form.logout-form')))
    # Click the submit button
    btn = W.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.logout-confirm-btn')))
    D.execute_script('arguments[0].click();', btn)
    time.sleep(3)
    print('After logout URL:', D.current_url)

    # Go to login page
    D.get(f'{BASE}/accounts/student/login/')
    W.until(EC.presence_of_element_located((By.ID, 'student-login-modern')))
    W.until(EC.presence_of_element_located((By.ID, 'id_username'))).send_keys(EMAIL)
    D.find_element(By.ID, 'id_password').send_keys(PASS)
    D.save_screenshot('e2e_before_login.png')
    D.find_element(By.ID, 'signin-btn').click()
    time.sleep(4)
    print('After manual login URL:', D.current_url)

    if 'login' in D.current_url:
        print('RESULT: FAIL - still on login page')
        try:
            err = D.find_element(By.CSS_SELECTOR, '.alert-danger, .invalid-feedback')
            print('Error:', err.text)
        except NoSuchElementException:
            pass
        D.save_screenshot('e2e_failed.png')
    else:
        print('RESULT: PASS - redirected to', D.current_url)
        D.save_screenshot('e2e_success.png')

except TimeoutException as e:
    print('TIMEOUT:', e)
    D.save_screenshot('e2e_timeout.png')
except Exception as e:
    print('ERROR:', e)
    D.save_screenshot('e2e_error.png')
finally:
    time.sleep(3)
    D.quit()
    print('Done.')
