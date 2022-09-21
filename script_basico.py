import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.youtube.com")

time.sleep(10)

driver.close()