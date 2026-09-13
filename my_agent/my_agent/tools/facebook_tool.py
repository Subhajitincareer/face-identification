from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def open_facebook() -> str:
    """
    Opens Facebook in a new Google Chrome browser window.
    Call this tool when the user asks to open Facebook.
    """
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) # Keep browser open after script finishes
        
        # Selenium Manager will automatically download the correct ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.facebook.com")
        
        return "Facebook has been opened successfully in a new browser window."
    except Exception as e:
        return f"Failed to open Facebook: {str(e)}"
