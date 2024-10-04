import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

username = os.getenv('NAUKRI_USERNAME')
password = os.getenv('NAUKRI_PASSWORD')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.naukri.com/nlogin/login")
driver.find_element(By.ID, 'usernameField').send_keys(username)
driver.find_element(By.ID, 'passwordField').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
time.sleep(5)
driver.get("https://www.naukri.com/mnjuser/profile?id=")
time.sleep(5)

edit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//em[@class='icon edit ' and @data-ga-track='spa-event|EditProfile|Basic Details|EditOpen']"))
)
edit_button.click()
time.sleep(3)
save_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'saveBasicDetailsBtn'))
)
save_button.click()
time.sleep(3)
driver.quit()
