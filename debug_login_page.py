from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

D = webdriver.Chrome()
D.maximize_window()

try:
    D.get('https://savvyindians-lms-portal-2.onrender.com/accounts/student/login/')
    time.sleep(5)
    
    print('Current URL:', D.current_url)
    print('Page Title:', D.title)
    print('\n--- Page Source (first 3000 chars) ---')
    print(D.page_source[:3000])
    print('\n--- Looking for input fields ---')
    
    inputs = D.find_elements(By.TAG_NAME, 'input')
    print(f'Found {len(inputs)} input elements:')
    for inp in inputs[:10]:
        print(f'  - type={inp.get_attribute("type")}, name={inp.get_attribute("name")}, id={inp.get_attribute("id")}')
    
    D.save_screenshot('login_page_debug.png')
    print('\nScreenshot saved: login_page_debug.png')
    
    time.sleep(3)
finally:
    D.quit()
