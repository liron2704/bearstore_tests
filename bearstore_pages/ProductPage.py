from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_header_element(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.pd-name')

    def change_quantity(self,quantity):
        quantity_element = self.driver.find_element(By.CSS_SELECTOR,'.form-control-lg')
        quantity_element.clear()
        quantity_element.send_keys(quantity)

    def add_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()