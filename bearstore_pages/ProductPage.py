from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_header_element(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.pd-name')