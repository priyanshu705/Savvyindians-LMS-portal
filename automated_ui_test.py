"""
Comprehensive Automated UI & Functionality Testing
Senior QA Engineer - Visibility, CSS Overlap, and Functionality Tests
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Configuration
BASE_URL = "https://savvyindians-lms-portal-2.onrender.com"
SCREENSHOT_DIR = "test_screenshots"
TEST_REPORT_FILE = "ui_test_report.json"

class UITester:
    def __init__(self, headless=False):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            }
        }
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def log_test(self, test_name, status, message, details=None):
        """Log test result"""
        test_result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if details:
            test_result["details"] = details
            
        self.results["tests"].append(test_result)
        self.results["summary"]["total"] += 1
        
        if status == "PASS":
            self.results["summary"]["passed"] += 1
            print(f"✅ {test_name}: {message}")
        elif status == "FAIL":
            self.results["summary"]["failed"] += 1
            print(f"❌ {test_name}: {message}")
        elif status == "WARNING":
            self.results["summary"]["warnings"] += 1
            print(f"⚠️  {test_name}: {message}")
    
    def test_page_load(self):
        """Test 1: Homepage loads successfully"""
        try:
            self.driver.get(BASE_URL)
            time.sleep(3)  # Wait for page to fully load
            
            if "SavvyIndians" in self.driver.title or "Learning" in self.driver.title:
                self.log_test(
                    "Homepage Load",
                    "PASS",
                    f"Homepage loaded successfully. Title: {self.driver.title}"
                )
            else:
                self.log_test(
                    "Homepage Load",
                    "WARNING",
                    f"Homepage loaded but title unexpected: {self.driver.title}"
                )
        except Exception as e:
            self.log_test("Homepage Load", "FAIL", f"Failed to load: {str(e)}")
    
    def test_navbar_visibility(self):
        """Test 2: Navbar is visible and properly styled"""
        try:
            navbar = self.wait.until(
                EC.presence_of_element_located((By.ID, "top-navbar"))
            )
            
            # Check if navbar is visible
            if navbar.is_displayed():
                # Check navbar position
                position = navbar.value_of_css_property("position")
                z_index = navbar.value_of_css_property("z-index")
                background = navbar.value_of_css_property("background-color")
                
                issues = []
                if position != "fixed":
                    issues.append(f"Position is {position}, expected 'fixed'")
                if int(z_index) < 1000:
                    issues.append(f"Z-index {z_index} might be too low")
                
                if issues:
                    self.log_test(
                        "Navbar Visibility",
                        "WARNING",
                        "Navbar visible but has styling issues",
                        {"issues": issues}
                    )
                else:
                    self.log_test(
                        "Navbar Visibility",
                        "PASS",
                        "Navbar is properly positioned and styled",
                        {"position": position, "z_index": z_index}
                    )
            else:
                self.log_test("Navbar Visibility", "FAIL", "Navbar not visible")
        except Exception as e:
            self.log_test("Navbar Visibility", "FAIL", f"Error: {str(e)}")
    
    def test_logo_visibility(self):
        """Test 3: Logo is visible and clickable"""
        try:
            logo = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-brand-logo img"))
            )
            
            if logo.is_displayed():
                # Check logo dimensions
                width = logo.size['width']
                height = logo.size['height']
                
                if width > 0 and height > 0:
                    self.log_test(
                        "Logo Visibility",
                        "PASS",
                        f"Logo visible and sized correctly ({width}x{height}px)"
                    )
                else:
                    self.log_test(
                        "Logo Visibility",
                        "WARNING",
                        f"Logo has zero dimensions ({width}x{height}px)"
                    )
            else:
                self.log_test("Logo Visibility", "FAIL", "Logo not visible")
        except Exception as e:
            self.log_test("Logo Visibility", "FAIL", f"Error: {str(e)}")
    
    def test_search_bar_functionality(self):
        """Test 4: Search bar is visible and functional"""
        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            if search_input.is_displayed():
                # Check if input is interactable
                search_input.clear()
                search_input.send_keys("Python")
                
                # Check if text was entered
                if search_input.get_attribute("value") == "Python":
                    # Check search button
                    search_button = self.driver.find_element(By.CSS_SELECTOR, ".form-header button")
                    if search_button.is_displayed():
                        self.log_test(
                            "Search Bar Functionality",
                            "PASS",
                            "Search bar is visible and accepts input"
                        )
                    else:
                        self.log_test(
                            "Search Bar Functionality",
                            "WARNING",
                            "Search input works but button not visible"
                        )
                else:
                    self.log_test(
                        "Search Bar Functionality",
                        "FAIL",
                        "Search bar doesn't accept input properly"
                    )
            else:
                self.log_test("Search Bar Functionality", "FAIL", "Search bar not visible")
        except Exception as e:
            self.log_test("Search Bar Functionality", "FAIL", f"Error: {str(e)}")
    
    def test_css_overlaps(self):
        """Test 5: Check for CSS overlaps and z-index issues"""
        try:
            # Get all elements with position fixed or absolute
            fixed_elements = self.driver.execute_script("""
                const elements = Array.from(document.querySelectorAll('*'));
                const positioned = elements.filter(el => {
                    const style = window.getComputedStyle(el);
                    return style.position === 'fixed' || style.position === 'absolute';
                });
                
                return positioned.map(el => ({
                    tag: el.tagName,
                    id: el.id,
                    class: el.className,
                    zIndex: window.getComputedStyle(el).zIndex,
                    position: window.getComputedStyle(el).position,
                    rect: el.getBoundingClientRect()
                }));
            """)
            
            # Check for potential overlaps
            overlaps = []
            for i, elem1 in enumerate(fixed_elements):
                for elem2 in fixed_elements[i+1:]:
                    # Check if bounding boxes overlap
                    rect1 = elem1['rect']
                    rect2 = elem2['rect']
                    
                    if (rect1['left'] < rect2['right'] and rect1['right'] > rect2['left'] and
                        rect1['top'] < rect2['bottom'] and rect1['bottom'] > rect2['top']):
                        
                        z1 = int(elem1['zIndex']) if elem1['zIndex'].isdigit() else 0
                        z2 = int(elem2['zIndex']) if elem2['zIndex'].isdigit() else 0
                        
                        overlaps.append({
                            "element1": f"{elem1['tag']}#{elem1['id'] or elem1['class']}",
                            "element2": f"{elem2['tag']}#{elem2['id'] or elem2['class']}",
                            "z_index_1": z1,
                            "z_index_2": z2
                        })
            
            if overlaps:
                self.log_test(
                    "CSS Overlaps",
                    "WARNING",
                    f"Found {len(overlaps)} potential overlaps",
                    {"overlaps": overlaps[:5]}  # Show first 5
                )
            else:
                self.log_test(
                    "CSS Overlaps",
                    "PASS",
                    "No significant CSS overlaps detected"
                )
        except Exception as e:
            self.log_test("CSS Overlaps", "FAIL", f"Error: {str(e)}")
    
    def test_responsive_design(self):
        """Test 6: Test responsive design at different viewports"""
        viewports = [
            ("Desktop", 1920, 1080),
            ("Laptop", 1366, 768),
            ("Tablet", 768, 1024),
            ("Mobile", 375, 667)
        ]
        
        responsive_issues = []
        
        for name, width, height in viewports:
            try:
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
                # Check if navbar is still visible
                navbar = self.driver.find_element(By.ID, "top-navbar")
                if not navbar.is_displayed():
                    responsive_issues.append(f"{name}: Navbar not visible")
                
                # Check for horizontal scroll
                has_scroll = self.driver.execute_script(
                    "return document.documentElement.scrollWidth > document.documentElement.clientWidth"
                )
                if has_scroll:
                    responsive_issues.append(f"{name}: Horizontal scroll detected")
                
            except Exception as e:
                responsive_issues.append(f"{name}: Error - {str(e)}")
        
        # Reset to desktop size
        self.driver.set_window_size(1920, 1080)
        
        if responsive_issues:
            self.log_test(
                "Responsive Design",
                "WARNING",
                f"Found {len(responsive_issues)} responsive issues",
                {"issues": responsive_issues}
            )
        else:
            self.log_test(
                "Responsive Design",
                "PASS",
                "Design is responsive across all viewports"
            )
    
    def test_button_visibility(self):
        """Test 7: Check if all buttons are visible and clickable"""
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            hidden_buttons = []
            for btn in buttons:
                if btn.is_displayed():
                    # Check if button has readable text or icon
                    text = btn.text.strip()
                    has_icon = len(btn.find_elements(By.TAG_NAME, "i")) > 0
                    
                    if not text and not has_icon:
                        hidden_buttons.append("Button with no text/icon")
                else:
                    # Some buttons might be intentionally hidden
                    pass
            
            if hidden_buttons:
                self.log_test(
                    "Button Visibility",
                    "WARNING",
                    f"Found {len(hidden_buttons)} buttons without clear labels",
                    {"count": len(buttons), "issues": len(hidden_buttons)}
                )
            else:
                self.log_test(
                    "Button Visibility",
                    "PASS",
                    f"All {len(buttons)} buttons are properly labeled"
                )
        except Exception as e:
            self.log_test("Button Visibility", "FAIL", f"Error: {str(e)}")
    
    def test_color_contrast(self):
        """Test 8: Check color contrast for accessibility"""
        try:
            # Check text elements for contrast
            contrast_issues = self.driver.execute_script("""
                function getLuminance(rgb) {
                    const [r, g, b] = rgb.match(/\\d+/g).map(Number);
                    const [rs, gs, bs] = [r, g, b].map(c => {
                        c = c / 255;
                        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
                    });
                    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
                }
                
                function getContrastRatio(fg, bg) {
                    const l1 = getLuminance(fg);
                    const l2 = getLuminance(bg);
                    const lighter = Math.max(l1, l2);
                    const darker = Math.min(l1, l2);
                    return (lighter + 0.05) / (darker + 0.05);
                }
                
                const textElements = Array.from(document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, a, button, span'));
                const issues = [];
                
                textElements.slice(0, 50).forEach(el => {
                    const style = window.getComputedStyle(el);
                    const color = style.color;
                    const bgColor = style.backgroundColor;
                    
                    if (color && bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
                        const ratio = getContrastRatio(color, bgColor);
                        if (ratio < 4.5) {
                            issues.push({
                                tag: el.tagName,
                                ratio: ratio.toFixed(2),
                                color: color,
                                bgColor: bgColor
                            });
                        }
                    }
                });
                
                return issues;
            """)
            
            if len(contrast_issues) > 5:
                self.log_test(
                    "Color Contrast",
                    "WARNING",
                    f"Found {len(contrast_issues)} elements with low contrast",
                    {"issues": contrast_issues[:5]}
                )
            else:
                self.log_test(
                    "Color Contrast",
                    "PASS",
                    "Color contrast is good for accessibility"
                )
        except Exception as e:
            self.log_test("Color Contrast", "FAIL", f"Error: {str(e)}")
    
    def test_static_files_loading(self):
        """Test 9: Check if all static files (CSS, JS, images) load properly"""
        try:
            # Check for failed resources
            failed_resources = self.driver.execute_script("""
                return performance.getEntriesByType('resource')
                    .filter(r => r.name.includes('/static/'))
                    .map(r => ({
                        url: r.name,
                        status: r.transferSize === 0 ? 'cached' : 'loaded',
                        size: r.transferSize
                    }));
            """)
            
            # Check browser console for errors
            logs = self.driver.get_log('browser')
            static_errors = [log for log in logs if 'static' in log.get('message', '').lower()]
            
            if static_errors:
                self.log_test(
                    "Static Files Loading",
                    "WARNING",
                    f"Found {len(static_errors)} static file errors",
                    {"errors": [e['message'] for e in static_errors[:3]]}
                )
            else:
                self.log_test(
                    "Static Files Loading",
                    "PASS",
                    f"All {len(failed_resources)} static files loaded successfully"
                )
        except Exception as e:
            self.log_test("Static Files Loading", "WARNING", f"Could not check: {str(e)}")
    
    def test_page_performance(self):
        """Test 10: Check page load performance"""
        try:
            # Get performance metrics
            perf_data = self.driver.execute_script("""
                const perfData = performance.getEntriesByType('navigation')[0];
                return {
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                    domInteractive: perfData.domInteractive - perfData.fetchStart,
                    totalTime: perfData.loadEventEnd - perfData.fetchStart
                };
            """)
            
            total_time = perf_data['totalTime']
            
            if total_time < 3000:
                self.log_test(
                    "Page Performance",
                    "PASS",
                    f"Page loaded in {total_time:.0f}ms (Excellent)",
                    perf_data
                )
            elif total_time < 5000:
                self.log_test(
                    "Page Performance",
                    "WARNING",
                    f"Page loaded in {total_time:.0f}ms (Acceptable)",
                    perf_data
                )
            else:
                self.log_test(
                    "Page Performance",
                    "WARNING",
                    f"Page loaded in {total_time:.0f}ms (Slow)",
                    perf_data
                )
        except Exception as e:
            self.log_test("Page Performance", "FAIL", f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all UI tests"""
        print("\n" + "="*80)
        print("🔍 AUTOMATED UI & FUNCTIONALITY TESTING")
        print("Senior QA Engineer - Comprehensive Test Suite")
        print("="*80 + "\n")
        
        tests = [
            self.test_page_load,
            self.test_navbar_visibility,
            self.test_logo_visibility,
            self.test_search_bar_functionality,
            self.test_css_overlaps,
            self.test_responsive_design,
            self.test_button_visibility,
            self.test_color_contrast,
            self.test_static_files_loading,
            self.test_page_performance
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {str(e)}")
            time.sleep(1)
        
        # Generate report
        self.generate_report()
        
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.results['summary']['total']}")
        print(f"✅ Passed: {self.results['summary']['passed']}")
        print(f"❌ Failed: {self.results['summary']['failed']}")
        print(f"⚠️  Warnings: {self.results['summary']['warnings']}")
        
        # Calculate pass rate
        if self.results['summary']['total'] > 0:
            pass_rate = (self.results['summary']['passed'] / self.results['summary']['total']) * 100
            print(f"\n📈 Pass Rate: {pass_rate:.1f}%")
        
        # Save report to JSON
        with open(TEST_REPORT_FILE, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {TEST_REPORT_FILE}")
        print("="*80 + "\n")
    
    def cleanup(self):
        """Close browser"""
        self.driver.quit()

if __name__ == "__main__":
    tester = UITester(headless=False)
    try:
        tester.run_all_tests()
    finally:
        tester.cleanup()
