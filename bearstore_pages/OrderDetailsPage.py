from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class OrderDetailsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_order_details_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,"small[class='text-muted'] > small")