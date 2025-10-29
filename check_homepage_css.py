"""
Homepage CSS Overlap & Responsiveness Check
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def check_homepage_css():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Test multiple screen sizes
    screen_sizes = [
        ("Desktop", 1920, 1080),
        ("Laptop", 1366, 768),
        ("Tablet", 768, 1024),
        ("Mobile", 375, 667)
    ]
    
    for device, width, height in screen_sizes:
        print(f"\n{'=' * 80}")
        print(f"🔍 Testing {device} ({width}x{height})")
        print('=' * 80)
        
        chrome_options.add_argument(f'--window-size={width},{height}')
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            url = "https://savvyindians-lms-portal-2.onrender.com/"
            driver.get(url)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            
            # Check key elements
            elements = [
                ("Navbar", "nav, .navbar"),
                ("Logo", "img[alt*='logo'], .navbar-brand img"),
                ("Hero Section", ".hero, section:first-of-type"),
                ("Main Content", "main, .container"),
                ("Footer", "footer"),
            ]
            
            print("\n📋 Element Visibility:")
            visible_count = 0
            
            for name, selector in elements:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if elem.is_displayed():
                        rect = elem.rect
                        print(f"✅ {name:20} | Position: ({rect['x']:.0f}, {rect['y']:.0f}), "
                              f"Size: {rect['width']:.0f}x{rect['height']:.0f}")
                        visible_count += 1
                    else:
                        print(f"⚠️  {name:20} | Not visible")
                except:
                    print(f"❌ {name:20} | Not found")
            
            print(f"\n📊 Result: {visible_count}/{len(elements)} elements visible")
            
            # Check for horizontal scrollbar (indicates overflow)
            body_width = driver.execute_script("return document.body.scrollWidth")
            window_width = driver.execute_script("return window.innerWidth")
            
            if body_width > window_width:
                print(f"⚠️  Horizontal overflow detected: Body {body_width}px > Window {window_width}px")
            else:
                print(f"✅ No horizontal overflow")
            
            # Save screenshot
            filename = f"homepage_{device.lower()}_{width}x{height}.png"
            driver.save_screenshot(filename)
            print(f"📸 Screenshot: {filename}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            driver.quit()
    
    print(f"\n{'=' * 80}")
    print("✅ HOMEPAGE CSS CHECK COMPLETE!")
    print('=' * 80)

if __name__ == "__main__":
    check_homepage_css()
