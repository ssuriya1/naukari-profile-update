import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time

username = os.getenv('NAUKRI_USERNAME')
password = os.getenv('NAUKRI_PASSWORD')

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.get("https://www.naukri.com/nlogin/login")
timeout = 20

try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, 'usernameField'))
    )
    driver.find_element(By.ID, 'usernameField').send_keys(username)
    driver.find_element(By.ID, 'passwordField').send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    time.sleep(2)
    current_url = driver.current_url
    print("Current URL:", current_url)

    try:
        error_message = driver.find_element(By.CSS_SELECTOR, '.login-error')
        if error_message:
            print("Login error:", error_message.text)
    except Exception as e:
        print("No specific error message found.")
    driver.get("https://www.naukri.com/mnjuser/profile?id=&altresid")
    print("Navigating to the profile page...")
    time.sleep(5)

    edit_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//em[@class='icon edit ' and @data-ga-track='spa-event|EditProfile|Basic Details|EditOpen']"))
    )
    edit_button.click()
    time.sleep(3)

    save_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, 'saveBasicDetailsBtn'))
    )
    save_button.click()
    print("Profile updated successfully.")
    time.sleep(3)

except Exception as e:
    print("Error encountered:")

finally:
    driver.quit()
