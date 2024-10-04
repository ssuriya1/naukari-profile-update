import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")

username = os.getenv('NAUKRI_USERNAME')
password = os.getenv('NAUKRI_PASSWORD')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=chrome_options))
driver.get("https://www.naukri.com/nlogin/login")
timeout = 20

try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, 'usernameField'))
    )
    driver.save_screenshot('naukri_login_screenshot.png')

    driver.find_element(By.ID, 'usernameField').send_keys(username)
    driver.find_element(By.ID, 'passwordField').send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    WebDriverWait(driver, timeout).until(EC.url_contains("naukri.com/mnjuser/profile"))
    driver.get("https://www.naukri.com/mnjuser/profile?id=")
    time.sleep(5)
    edit_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//em[@class='icon edit ' and @data-ga-track='spa-event|EditProfile|Basic Details|EditOpen']"))
    )
    edit_button.click()
    time.sleep(3)
    driver.save_screenshot('naukri_login_screenshot.png')

    save_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, 'saveBasicDetailsBtn'))
    )
    save_button.click()
    driver.save_screenshot('naukri_login_screenshot.png')
    time.sleep(3)
    print("Updated Successfully")

except Exception as e:
    print("Error encountered:", e)
    print(driver.page_source)

finally:
    driver.quit()
