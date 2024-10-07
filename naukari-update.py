import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

username = os.getenv('NAUKRI_USERNAME')
password = os.getenv('NAUKRI_PASSWORD')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
    driver.get("https://www.naukri.com/mnjuser/profile")
    print("Navigating to the profile page...")
    driver.save_screenshot('naukari-login/naukri_login_screenshot.png')
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
    print("Error encountered")

finally:
    driver.quit()
