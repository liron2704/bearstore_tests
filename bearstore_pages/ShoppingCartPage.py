from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShoppingCartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_header_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.h3')

    def get_total_amount_price(self):
        price_strip = self.driver.find_element(By.CSS_SELECTOR, '.cart-summary-total >.cart-summary-value > span').text.strip()
        price_str = ''.join(char for char in price_strip if char.isdigit() or char == '.')
        price = float(price_str)
        return price
