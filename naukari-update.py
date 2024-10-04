import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")

username = os.getenv('NAUKRI_USERNAME')
password = os.getenv('NAUKRI_PASSWORD')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://www.naukri.com/nlogin/login")

    time.sleep(random.uniform(2, 5))
    print("Waiting for username field to be visible...")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'usernameField')))
    print("Username field is visible.")
    
    print("Entering username...")
    driver.find_element(By.ID, 'usernameField').send_keys(username)
    
    print("Entering password...")
    driver.find_element(By.ID, 'passwordField').send_keys(password)
    
    print("Clicking the login button...")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    driver.get("https://www.naukri.com/mnjuser/profile?id=&altresid")
    
    print("Waiting for edit button to be clickable...")
    edit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//em[@class='icon edit ' and @data-ga-track='spa-event|EditProfile|Basic Details|EditOpen']"))
    )
    edit_button.click()
    print("Edit button clicked. Updating profile...")

    save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'saveBasicDetailsBtn'))
    )
    save_button.click()
    print("Profile updated successfully.")

except Exception as e:
    print("Error encountered:", e)
    print(driver.page_source)

finally:
    driver.quit()
