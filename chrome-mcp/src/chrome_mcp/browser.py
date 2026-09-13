import base64
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ChromeBrowser:
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None

    def start(self):
        if self.driver is not None:
            return

        chrome_options = Options()
        # Keep window open
        chrome_options.add_experimental_option("detach", True)
        
        # Start browser
        # In Selenium 4.6+, webdriver-manager is no longer needed; Selenium Manager handles it automatically.
        self.driver = webdriver.Chrome(options=chrome_options)
        # Position the browser as a small popup on the right side
        self.driver.set_window_rect(x=1400, y=50, width=500, height=900)

    def stop(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _get_driver(self) -> webdriver.Chrome:
        if not self.driver:
            self.start()
        return self.driver

    def navigate(self, url: str) -> str:
        driver = self._get_driver()
        driver.get(url)
        # basic wait for page load
        time.sleep(2)
        return f"Navigated to {url}"

    def get_title(self) -> str:
        driver = self._get_driver()
        return driver.title

    def get_page_source(self) -> str:
        driver = self._get_driver()
        # Return innerText instead of full raw HTML to prevent Gemini Live websocket from crashing
        # due to massive payload sizes (some pages have MBs of HTML).
        script = "return document.body ? document.body.innerText : '';"
        text_content = driver.execute_script(script)
        
        # Limit to 30,000 characters to be absolutely safe with the WebSocket chunk limit
        if text_content and len(text_content) > 30000:
            text_content = text_content[:30000] + "\n...[Content Truncated]..."
            
        return text_content

    def click(self, selector: str, by_type: str = "css selector") -> str:
        driver = self._get_driver()
        by = self._get_by(by_type)
        
        try:
            from selenium.common.exceptions import TimeoutException
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            return f"Clicked element matching {by_type} '{selector}'"
        except TimeoutException:
            return f"Error: Could not find clickable element with {by_type}='{selector}' within 10 seconds."

    def type_text(self, selector: str, text: str, by_type: str = "css selector") -> str:
        driver = self._get_driver()
        by = self._get_by(by_type)
        
        try:
            from selenium.common.exceptions import TimeoutException
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((by, selector))
            )
            element.clear()
            element.send_keys(text)
            return f"Typed text into element matching {by_type} '{selector}'"
        except TimeoutException:
            return f"Error: Could not find visible element with {by_type}='{selector}' within 10 seconds."

    def execute_script(self, script: str) -> str:
        driver = self._get_driver()
        result = driver.execute_script(script)
        return str(result)

    def take_screenshot(self) -> str:
        try:
            driver = self._get_driver()
            # Return base64 encoded image
            return driver.get_screenshot_as_base64()
        except Exception as e:
            return f"Error: Failed to take screenshot - {str(e)}"

    def _get_by(self, by_type: str) -> str:
        by_map = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "link text": By.LINK_TEXT,
            "partial link text": By.PARTIAL_LINK_TEXT,
            "tag name": By.TAG_NAME,
            "class name": By.CLASS_NAME,
            "css selector": By.CSS_SELECTOR,
        }
        return by_map.get(by_type.lower(), By.CSS_SELECTOR)
