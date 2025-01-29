from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.forbes.com/')
sleep(2)

# close cookie button
cookie_button = driver.find_element(By.XPATH, value='//*[@id="ketch-consent-banner"]/div[2]/div[2]/button[2]')
cookie_button.click()
sleep(2)


sleep(2)


# driver.quit()
