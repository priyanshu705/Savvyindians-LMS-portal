"""
Quick CSS Overlap Detection for Registration Form
Tests for any overlapping elements or visibility issues
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def check_css_overlaps():
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("\n" + "=" * 80)
        print("🔍 CSS OVERLAP & VISIBILITY CHECK - Registration Form")
        print("=" * 80)
        
        # Navigate to registration page
        url = "https://savvyindians-lms-portal-2.onrender.com/accounts/student/register/"
        print(f"\n📍 Testing: {url}")
        driver.get(url)
        
        # Wait for page load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        time.sleep(2)
        
        print("\n✅ Page loaded successfully\n")
        
        # Check all form elements
        elements_to_check = [
            ("Form Heading", "h2.register-title"),
            ("First Name Label", "label[for='id_first_name'], .col-md-6:nth-of-type(1) .form-label"),
            ("First Name Input", "input[name='first_name']"),
            ("Last Name Label", "label[for='id_last_name'], .col-md-6:nth-of-type(2) .form-label"),
            ("Last Name Input", "input[name='last_name']"),
            ("Email Label", "label[for='id_email']"),
            ("Email Input", "input[name='email']"),
            ("Phone Label", "label[for='id_phone']"),
            ("Phone Input", "input[name='phone']"),
            ("City Label", "label[for='id_city']"),
            ("City Input", "input[name='city']"),
            ("Level Label", "label[for='id_level']"),
            ("Level Select", "select[name='level']"),
            ("Submit Button", "button[type='submit']"),
        ]
        
        all_elements = []
        print("📋 Element Visibility Check:")
        print("-" * 80)
        
        for name, selector in elements_to_check:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                is_displayed = element.is_displayed()
                
                # Get element position and size
                location = element.location
                size = element.size
                rect = {
                    'x': location['x'],
                    'y': location['y'],
                    'width': size['width'],
                    'height': size['height'],
                    'right': location['x'] + size['width'],
                    'bottom': location['y'] + size['height']
                }
                
                # Get styling
                color = element.value_of_css_property('color')
                bg_color = element.value_of_css_property('background-color')
                opacity = element.value_of_css_property('opacity')
                z_index = element.value_of_css_property('z-index')
                position = element.value_of_css_property('position')
                
                status = "✅" if is_displayed else "❌"
                print(f"{status} {name:25} | Visible: {is_displayed}")
                
                if is_displayed:
                    print(f"   └─ Position: ({rect['x']:.0f}, {rect['y']:.0f}), "
                          f"Size: {rect['width']:.0f}x{rect['height']:.0f}")
                    print(f"   └─ Color: {color}, Opacity: {opacity}, Z-index: {z_index}")
                
                all_elements.append({
                    'name': name,
                    'rect': rect,
                    'displayed': is_displayed,
                    'element': element
                })
                
            except Exception as e:
                print(f"❌ {name:25} | Not found")
        
        print("\n" + "-" * 80)
        
        # Check for overlaps
        print("\n🔍 Checking for CSS Overlaps:")
        print("-" * 80)
        
        overlaps_found = []
        for i, elem1 in enumerate(all_elements):
            if not elem1['displayed']:
                continue
                
            for elem2 in all_elements[i+1:]:
                if not elem2['displayed']:
                    continue
                
                # Check if rectangles overlap
                r1 = elem1['rect']
                r2 = elem2['rect']
                
                # Rectangles overlap if:
                # - One rectangle's left edge is to the left of the other's right edge, AND
                # - One rectangle's right edge is to the right of the other's left edge, AND
                # - One rectangle's top edge is above the other's bottom edge, AND
                # - One rectangle's bottom edge is below the other's top edge
                
                horizontal_overlap = r1['x'] < r2['right'] and r1['right'] > r2['x']
                vertical_overlap = r1['y'] < r2['bottom'] and r1['bottom'] > r2['y']
                
                if horizontal_overlap and vertical_overlap:
                    overlap_area = (
                        min(r1['right'], r2['right']) - max(r1['x'], r2['x'])
                    ) * (
                        min(r1['bottom'], r2['bottom']) - max(r1['y'], r2['y'])
                    )
                    
                    if overlap_area > 10:  # Ignore tiny overlaps (< 10px²)
                        overlaps_found.append({
                            'elem1': elem1['name'],
                            'elem2': elem2['name'],
                            'area': overlap_area
                        })
                        print(f"⚠️  OVERLAP DETECTED:")
                        print(f"   '{elem1['name']}' overlaps with '{elem2['name']}'")
                        print(f"   Overlap area: {overlap_area:.0f} px²")
        
        if not overlaps_found:
            print("✅ No CSS overlaps detected!")
        
        print("\n" + "=" * 80)
        
        # Final Summary
        print("\n📊 FINAL SUMMARY:")
        print("-" * 80)
        
        visible_count = sum(1 for e in all_elements if e['displayed'])
        total_count = len(all_elements)
        
        print(f"✅ Visible Elements: {visible_count}/{total_count}")
        print(f"{'✅' if not overlaps_found else '⚠️ '} CSS Overlaps: {len(overlaps_found)}")
        
        if visible_count == total_count and not overlaps_found:
            print("\n🎉 PERFECT! No visibility or overlap issues found!")
        elif overlaps_found:
            print("\n⚠️  WARNING: Some elements are overlapping")
        else:
            print(f"\n⚠️  WARNING: {total_count - visible_count} elements are not visible")
        
        print("=" * 80)
        
        # Take screenshot
        driver.save_screenshot("registration_css_check.png")
        print(f"\n📸 Screenshot saved: registration_css_check.png")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    check_css_overlaps()
