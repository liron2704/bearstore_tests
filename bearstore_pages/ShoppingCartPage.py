from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
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
    
    def get_quantity_elements_list(self):
        return self.driver.find_elements(By.XPATH,"//div[@class='qty-input']//input")

    def change_quantities(self, quantity_list: list):
        for i in range(len(quantity_list)):
            quantity_elements_list = self.get_quantity_elements_list()
            # Get the current price before changing the quantity
            initial_price = self.get_total_products_price_list()[i]

            quantity_elements_list[i].clear()
            quantity_elements_list[i].send_keys(quantity_list[i])
            quantity_elements_list[i].send_keys(Keys.TAB)

            # Wait for the total price to change from its initial value
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.get_total_products_price_list()[i] != initial_price)

    def get_total_products_price_list(self):
        price_elements_list = self.driver.find_elements(By.CSS_SELECTOR, '.cart-col-subtotal > span')
        price_list = []
        for price_element in price_elements_list:
            price_strip = price_element.text.strip()
            price = ''.join(char for char in price_strip if char.isdigit() or char == '.')
            price_list.append(float(price))
        return price_list

    def get_sub_total_price(self):
        price_strip = self.driver.find_element(By.CSS_SELECTOR, 'tr[class="cart-summary-total"]>td[class="cart-summary-value"] >span').text.strip()
        price_str = ''.join(char for char in price_strip if char.isdigit() or char == '.')
        price = float(price_str)
        return price

    def get_unit_price_list(self):
        """Fetch the list of unit prices for all products in the cart."""
        price_elements_list = self.driver.find_elements(By.CSS_SELECTOR, "div[data-caption='Price']>span.price")
        price_list = []
        for price_element in price_elements_list:
            price_strip = price_element.text.strip()
            price = ''.join(char for char in price_strip if char.isdigit() or char == '.')
            price_list.append(float(price))
        return price_list





