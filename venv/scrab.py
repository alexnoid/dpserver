from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome()
def site_login():
    driver.get ("https://vk.com/")
    driver.find_element_by_id("index_email").send_keys("+375447022103")
    driver.find_element_by_id ("index_pass").send_keys("6626816")
    driver.find_element_by_id(index_login_button).click()
    url = 'https://vk.com/feed'
    driver = webdriver.Chrome()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.title_contains("home"))

site_login()
soup = BeautifulSoup(driver.page_source)

